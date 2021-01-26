from rest_framework import serializers
from polling.models import *

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'start_date', 'finish_date']
        read_only_fields = ['start_date']

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError('start date can\'t be after end date')


class PollCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'title', 'start_date', 'finish_date']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'ttype', 'poll']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['text', 'question']

    def validate(self, data):
        if data['question'].ttype == 'T':
            return serializers.ValidationError('Answer for text questions are created automatically')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'

    def validate(self, data):
        if Result.objects.filter(user=data['user'], answer=data['answer']):
            raise serializers.ValidationError("This answer was already recorded")

        if 'text' in data and data['text'] is not None and data['answer'].question.ttype != 'T':
            raise serializers.ValidationError("Text required only for text answer questions")
        if data['answer'].question.ttype == 'O' and Result.objects.filter(user=data['user'], answer__question=data['answer'].question).count() > 0:
            raise serializers.ValidationError("Only one answer allowed for this question")
        return data