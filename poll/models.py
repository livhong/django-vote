import datetime

from django.db import models
from django.utils import timezone
from DjangoUeditor.models import UEditorField
from vote.managers import VotableManager

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

    unionid = models.CharField(max_length=400)
    headimgurl = models.CharField(max_length=1000)
    openid = models.CharField(max_length=400)
    nickname = models.CharField(max_length=200)
    sex = models.CharField(max_length=10) #1 for male, 2 for female, 0 for known
    city = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

class ActivityDetail(models.Model):
    #投稿方式可以编写在这里
    content = UEditorField(default="", toolbars="full", imagePath="ueditor/images/%(year)s/%(month)s/",
                           filePath="ueditor/file/%(year)s/%(month)s/")

class Building(models.Model):
    title = models.CharField(max_length=1000)
    avator = models.ImageField(upload_to='building/%Y/%m/')
    description = models.CharField(max_length=1000)
    abstract = models.TextField()
    content = UEditorField(default="", toolbars="full", imagePath="ueditor/images/%(year)s/%(month)s/",
                           filePath="ueditor/file/%(year)s/%(month)s/")
    banner_img = models.ImageField(upload_to='', default="")
    is_online = models.BooleanField(default=False)
    is_after_ddl = models.BooleanField(default=False)
    option_count = models.IntegerField(default=0)
# class Questionnaire(models.Model):
#     title = models.CharField(max_length=1000)
#
#     content = UEditorField(default="", toolbars="full", imagePath="ueditor/images/%(year)s/%(month)s/",
#                            filePath="ueditor/file/%(year)s/%(month)s/")
#     building = models.OneToOneField(Building)


class Option(models.Model):
    avator = models.ImageField(upload_to='option/%Y/%m/')
    abstract = models.TextField()
    description = models.CharField(max_length=1000)
    pub_time = models.DateField()
    content = UEditorField(default="", toolbars="full", imagePath="ueditor/images/%(year)s/%(month)s/",
                           filePath="ueditor/file/%(year)s/%(month)s/")
    votes = VotableManager()
    building = models.ForeignKey(Building)


