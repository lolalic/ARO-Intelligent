# Create your models here.
from django.db import models


class Corpus_Data(models.Model):

    objects = None
    content = models.CharField(max_length=2000)
    language = models.CharField(max_length=100)
    corpus_date = models.CharField(max_length=100)
    corpus_id = models.CharField(max_length=100)
    certification = models.CharField(max_length=100)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'corpus_data'
