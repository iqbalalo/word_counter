from django.db import models
from django.utils import timezone


class ScrapeHistory(models.Model):
    url = models.TextField()
    word = models.CharField(max_length=60)
    word_count = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "word {} found {} times in {}".format(self.word, self.word_count, self.url)
