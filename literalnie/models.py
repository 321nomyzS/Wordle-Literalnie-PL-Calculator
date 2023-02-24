from django.db import models


class FiveLetterWords(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=5)
