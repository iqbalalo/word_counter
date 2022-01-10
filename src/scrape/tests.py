from unittest import mock

from django.test import TestCase
from django.urls import resolve, reverse
from nltk import word_tokenize

from .models import ScrapeHistory
from .views import WordCountView


class ScrapeTest(TestCase):

    def _mock_response(
            self,
            status=200,
            content="CONTENT",
            json_data=None,
            raise_for_status=None):

        mock_resp = mock.Mock()

        # mock raise_for_status call w/optional error
        mock_resp.raise_for_status = mock.Mock()

        if raise_for_status:
            mock_resp.raise_for_status.side_effect = raise_for_status
        # set status code and content
        mock_resp.status_code = status
        mock_resp.content = content

        # add json data if provided
        if json_data:
            mock_resp.json = mock.Mock(
                return_value=json_data
            )
        return mock_resp

    def setUp(self):
        self.url = reverse("wordcount")
        self.post_params = {
            "word": "fit",
            "url": "https://www.virtusize.jp/"
        }

    def test_wordcount_url_resolves(self):
        self.assertEqual(resolve(self.url).func.view_class, WordCountView)

    def test_missing_param(self):
        params = {
            "word": "ABC"
        }

        response = self.client.post(
            self.url, params, content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_invalid_link_value(self):
        params = {
            "word": "WORd",
            "url": "https://virtuse"
        }

        response = self.client.post(
            self.url, params, content_type='application/json')

        self.assertEqual(response.status_code, 500)

    @mock.patch("scrape.views.requests.get")
    def test_wordcount_request_to_url(self, m):
        mock_resp = self._mock_response(
            content="<html><body>this is fit</body></html>")

        m.return_value = mock_resp

        response = WordCountView.scrap_url_and_word_count(self,
                                                          "fit", "https://www.virtusize.jp/")

        self.assertEqual(response, 1)

    @mock.patch("scrape.views.WordCountView.scrap_url_and_word_count", return_value=1)
    def test_wordcount_success_result(self, m):
        response = self.client.post(
            self.url, self.post_params, content_type='application/json')

        result = response.json()

        test_content = {
            "status": "ok",
            "count": 1
        }

        self.assertEqual(result, test_content)

    @mock.patch("scrape.views.WordCountView.scrap_url_and_word_count", return_value=1)
    def test_save_to_db(self, m):
        _ = ScrapeHistory.objects.create(
            url="https://www.virtusize.jp/",
            word="fit",
            word_count=1
        )

        _ = self.client.post(
            self.url, self.post_params, content_type='application/json')

        self.assertEqual(ScrapeHistory.objects.last().word_count, 1)

        self.assertNotEqual(ScrapeHistory.objects.last().word_count, 13)

    def test_word_tokenize(self):
        txt = "<html><body>Virtusize works for innovative idea. <'new idea'> idea-ly Although there are lot of new ideas but it focuses e-commerce</body></html>"

        words = word_tokenize(txt)

        self.assertEqual(words.count("idea"), 2)
        self.assertNotEqual(words.count("idea"), 1)
