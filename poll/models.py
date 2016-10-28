import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
# model for question
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# model for choice, related to question
class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class User(models.Model):
    union_id = models.CharField(max_length=400)
    headimgurl = models.CharField(max_length=1000)
    openid = models.CharField(max_length=400)
    nickname = models.CharField(max_length=200)
    sex = models.CharField(max_length=10) #1 for male, 2 for female, 0 for known
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=50)







