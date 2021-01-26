from django.db import models
from django.contrib.auth.models import User

QUESTION_TYPES = [
    ('T', 'Text'),
    ('O', 'One answer'),
    ('S', 'Several answers')
]


class Poll(models.Model):
    title = models.CharField(max_length=256)
    start_date = models.DateField(null=False)
    finish_date = models.DateField(null=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField(max_length=1024)
    ttype = models.CharField(max_length=1, choices=QUESTION_TYPES)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=1024)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.CharField(max_length=1024)
    text = models.CharField(max_length=1024, null=True, default=None)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        if self.text is None:
            return self.answer.text
        else:
            return self.text
