from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import datetime

from polling.serializers import *
from polling.permissions import *


class PollList(APIView):
    def get(self, request, format=None):
        objects = Poll.objects.filter(finish_date__gte=datetime.date.today())
        serializer = PollSerializer(objects, many=True)
        return Response(serializer.data)

    @has_permition
    def post(self, request, format=None):
        serializer = PollCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PollDetail(APIView):

    def get_object(self, pk):
        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = PollSerializer(object)
        return Response(serializer.data)

    @has_permition
    def put(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = PollSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @has_permition
    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class QuestionList(APIView):

    def get(self, request):
        poll_id = request.GET.get('poll', None)
        if poll_id:
            objects = Question.objects.filter(poll_id=poll_id)
            serializer = QuestionSerializer(objects, many=True)
            return Response(serializer.data)
        else:
            objects = Question.objects.filter(poll__finish_date__gt=datetime.date.today())
            serializer = QuestionSerializer(objects, many=True)
            return Response(serializer.data)

    @has_permition
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            Answer.objects.create(
                question=question
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetail(APIView):

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = QuestionSerializer(object)
        return Response(serializer.data)

    @has_permition
    def put(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = QuestionSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @has_permition
    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class AnswerList(APIView):

    def get(self, request):
        question_id = request.GET.get('question', None)
        if question_id:
            objects = Answer.objects.filter(question=get_object_or_404(Question, pk=question_id))
            serializer = AnswerSerializer(objects, many=True)
            return Response(serializer.data)
        else:
            objects = Answer.objects.filter(question__poll__finish_date__gte=datetime.date.today())
            serializer = AnswerSerializer(objects, many=True)
            return Response(serializer.data)

    @has_permition
    def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class AnswerDetail(APIView):

    def get_object(self, pk):
        try:
            return Answer.objects.get(pk=pk)
        except Answer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = AnswerSerializer(object)
        return Response(serializer.data)

    @has_permition
    def put(self, request, pk, format=None):
        object = self.get_object(pk)
        serializer = AnswerSerializer(object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @has_permition
    def delete(self, request, pk, format=None):
        object = self.get_object(pk)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ResultView(APIView):
    def post(self, request, format=None):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class ResultDetail(APIView):
    def get(self, request, id):
        poll_id = request.GET.get('poll', None)
        if poll_id is None:
            polls = list([p for p in Poll.objects.all()])
        else:
            polls = [get_object_or_404(Poll, poll_id)]

        objects = Result.objects.filter(user=id, answer__question__poll__in=polls)
        serializer = ResultSerializer(objects, many=True)
        return Response(serializer.data)
