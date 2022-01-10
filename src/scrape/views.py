import json

import nltk
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from nltk import word_tokenize

from .models import ScrapeHistory

nltk.download('punkt')


class WordCountView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            params = json.loads(request.body)
            word = params.get("word", None)
            url = params.get("url", None)

            if not word or not url:
                return JsonResponse({"status": "error", "msg": "Invalid Params"}, status=400)

            word = word.strip()
            url = url.strip()

            # Check old history
            prev_rec = ScrapeHistory.objects.filter(url=url, word=word).last()

            if prev_rec:
                return JsonResponse({"status": "ok", "count": prev_rec.word_count}, status=200)

            # pass params to seperate function to word count
            word_count = self.scrap_url_and_word_count(word, url)

            # save to db
            _ = ScrapeHistory.objects.create(
                url=url, word=word, word_count=word_count)

            return JsonResponse({"status": "ok", "count": word_count}, status=200)

        except Exception as err:
            return JsonResponse({"status": "error", "msg": str(err)}, status=500)


    def scrap_url_and_word_count(self, word, url):

        # headers: Although it is optional but safe for skiping most of the non-blocking issue
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        # send request to get data from url and pass to BeautifulSoup library to parse html records.
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')

        """
        soup object may parse get_text() but it may skip few text which is under tag. So prettify() was used to get dom structure.
        Then tokenizee using NLTK library
        Count the word and return
        """
        source = soup.prettify()
        tokens = word_tokenize(source)

        return tokens.count(word)
