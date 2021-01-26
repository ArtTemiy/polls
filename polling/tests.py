from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from polling.models import *

import datetime
import json

REQUEST_CONTENT_TYPE = 'application/json'
ADMIN_USERNAME, ADMIN_PASSWORD = 'admin', 'PassWord123'

def create_admin():
    user = User.objects.create(
        username=ADMIN_USERNAME,
        is_staff=True
    )
    user.set_password(ADMIN_PASSWORD)
    user.save()


def add_login_to_url(url):
    if url.find('?') != -1:
        url += '&'
    else:
        url += '?'
    return url + f'username={ADMIN_USERNAME}&password={ADMIN_PASSWORD}'


class PollTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_admin()

    def create_poll(self, i=0, future=True):
        year_difference = 2 * int(future) - 1
        poll = Poll(
            title=f'poll {i}',
            start_date=datetime.date(
                datetime.date.today().year + year_difference,
                1,
                i + 1
            ),
            finish_date=datetime.date(
                datetime.date.today().year + year_difference,
                3,
                i + 1
            )
        )
        poll.save()
        return poll

    def create_polls(self, count, future=True):
        return [self.create_poll(i, future=future) for i in range(count)]

    def test_get_list_of_future(self):
        POLLS_NUMBER = 3
        polls = self.create_polls(POLLS_NUMBER)

        url = reverse('polls')
        response = self.client.get(url)
        objects = json.loads(response.content.decode())
        self.assertEqual(len(objects), len(objects))
        object_ids, object_titles, object_start_dates, object_finish_dates = [list(map(
                lambda x: x[field_name],
                objects
        )) for field_name in ['id', 'title', 'start_date', 'finish_date']]

        for poll in Poll.objects.all():
            self.assertIn(poll.pk, object_ids)
            self.assertIn(poll.title, object_titles)
            self.assertIn(str(poll.start_date), object_start_dates)
            self.assertIn(str(poll.finish_date), object_finish_dates)

    def test_get_list_of_past(self):
        POLLS_NUMBER = 3
        polls = self.create_polls(POLLS_NUMBER, future=False)

        url = reverse('polls')
        response = self.client.get(url)
        objects = json.loads(response.content.decode())
        self.assertEqual(len(objects), 0)

    def test_poll_detail(self):
        POLLS_NUMBER = 3
        polls = self.create_polls(POLLS_NUMBER)
        poll = polls[0]

        url = reverse('poll', args=([poll.pk]))
        response = self.client.get(url)
        object = json.loads(response.content.decode())
        self.assertEqual(object['id'], poll.pk)
        self.assertEqual(object['title'], poll.title)
        self.assertEqual(object['start_date'], str(poll.start_date))
        self.assertEqual(object['finish_date'], str(poll.finish_date))

    def test_today_poll(self):
        poll = Poll.objects.create(
            title='Poll',
            start_date=datetime.date.today(),
            finish_date=datetime.date.today()
        )
        url = reverse('polls')
        response = self.client.get(url)
        objects = json.loads(response.content.decode())
        self.assertEqual(len(objects), 1)

    def test_create(self):
        url = add_login_to_url(reverse('polls'))
        poll_object = {
            'title': 'Poll',
            'start_date': datetime.date(datetime.date.today().year + 1, 1, 1),
            'finish_date': datetime.date(datetime.date.today().year + 1, 2, 1),
        }
        response = self.client.post(
            url,
            data=poll_object,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Poll.objects.all().count(), 1)
        poll = Poll.objects.first()
        self.assertEqual(poll.title, poll_object['title'])
        self.assertEqual(poll.start_date, poll_object['start_date'])
        self.assertEqual(poll.finish_date, poll_object['finish_date'])

    def test_delete(self):
        poll = self.create_poll()

        url = add_login_to_url(reverse('poll', args=([poll.pk])))
        response = self.client.delete(
            url,
            data={
                'id': poll.pk
            }
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Poll.objects.count(), 0)

    def test_update(self):
        poll = Poll(
            title='Poll',
            start_date=datetime.date(datetime.date.today().year + 1, 1, 1),
            finish_date=datetime.date(datetime.date.today().year + 1, 2, 1),
        )
        poll.save()

        new_title = 'Poll new title'
        new_finish_date = datetime.date(datetime.date.today().year + 3, 5, 10)
        poll_object_update = {
            'title': new_title,
            'finish_date': new_finish_date,
        }
        url = add_login_to_url(reverse('poll', args=([poll.pk])))
        response = self.client.put(
            url,
            data=poll_object_update,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 200)

        poll = Poll.objects.get(pk=poll.pk)
        self.assertEqual(poll.title, new_title)
        self.assertEqual(poll.finish_date, new_finish_date)

    def test_start_date_not_changes(self):
        start_date = datetime.date(datetime.date.today().year + 1, 1, 1)
        poll = Poll(
            title='Poll',
            start_date=start_date,
            finish_date=datetime.date(datetime.date.today().year + 1, 2, 1),
        )
        poll.save()

        new_title = 'Poll new title'
        new_start_date = datetime.date(datetime.date.today().year + 2, 2, 1)
        new_finish_date = datetime.date(datetime.date.today().year + 3, 5, 10)
        poll_object_update = {
            'title': new_title,
            'start_date': new_start_date,
            'finish_date': new_finish_date,
        }
        url = add_login_to_url(reverse('poll', args=([poll.pk])))
        response = self.client.put(
            url,
            data=poll_object_update,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 200)

        poll = Poll.objects.get(pk=poll.pk)
        self.assertEqual(poll.title, new_title)
        self.assertEqual(poll.start_date, start_date)
        self.assertEqual(poll.finish_date, new_finish_date)


class QuestionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll1 = Poll.objects.create(
            title='Poll1',
            start_date=datetime.date.today(),
            finish_date=datetime.date.today(),
        )
        cls.poll2 = Poll.objects.create(
            title='Poll2',
            start_date=datetime.date.today(),
            finish_date=datetime.date.today(),
        )
        create_admin()

    def add_question_to_poll(self, count, poll):
        return [Question.objects.create(
            text=f'Text for question ({i})',
            ttype='o',
            poll=poll
        ) for i in range(count)]

    def add_questions_to_all_polls(self, count=3):
        return self.add_question_to_poll(count, poll=self.poll1) + self.add_question_to_poll(count, poll=self.poll2)

    def test_get_all(self):
        questions = self.add_questions_to_all_polls()

        url = add_login_to_url(reverse('questions'))
        response = self.client.get(
            url
        )
        objects = json.loads(response.content.decode())
        self.assertEqual(len(questions), len(objects))

    def test_get_poll_questions(self):
        question_count = 3
        questions = self.add_questions_to_all_polls(question_count)

        url = add_login_to_url(reverse('questions') + f'?poll={self.poll1.pk}')
        response = self.client.get(url)
        objects = json.loads(response.content.decode())
        self.assertEqual(question_count, len(objects))

    def test_create_question(self):
        question_data = {
            'text': 'Text for question',
            'ttype': 'O',
            'poll': self.poll1.pk
        }
        url = add_login_to_url(reverse('questions'))
        response = self.client.post(
            url,
            data=question_data,
            content_type=REQUEST_CONTENT_TYPE
        )
        question_id = json.loads(response.content.decode())['id']
        self.assertEqual(response.status_code, 201)
        question = Question.objects.get(pk=question_id)
        self.assertEqual(question.text, question_data['text'])
        self.assertEqual(question.ttype, question_data['ttype'])
        self.assertEqual(question.poll, self.poll1)

    def test_create_default_answer_for_question(self):
        question_data = {
            'text': 'Text for question',
            'ttype': 'T',
            'poll': self.poll1.pk
        }
        url = add_login_to_url(reverse('questions'))
        response = self.client.post(
            url,
            data=question_data,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(1, Answer.objects.count())

    def test_delete_question(self):
        question_count_for_one_poll = 3
        questions = self.add_questions_to_all_polls(question_count_for_one_poll)
        question_count =  Question.objects.count()
        response = self.client.delete(
            add_login_to_url(reverse('question', args=([Question.objects.first().pk])))
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(question_count - 1, Question.objects.count())


class AnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = Poll.objects.create(
            title='Poll',
            start_date=datetime.date.today(),
            finish_date=datetime.date.today(),
        )
        cls.one_answer_question = Question.objects.create(
            text='One answer Question',
            ttype='O',
            poll=cls.poll
        )
        cls.several_answer_question = Question.objects.create(
            text='Several answer Question',
            ttype='S',
            poll=cls.poll
        )
        cls.text_question = Question.objects.create(
            text='Text Question',
            ttype='T',
            poll=cls.poll
        )
        create_admin()



class ResultTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.poll = Poll.objects.create(
            title='Poll',
            start_date=datetime.date.today(),
            finish_date=datetime.date.today(),
        )

        cls.one_answer_question = Question.objects.create(
            text='One answer Question',
            ttype='O',
            poll=cls.poll
        )
        cls.several_answer_question = Question.objects.create(
            text='Several answer Question',
            ttype='S',
            poll=cls.poll
        )
        cls.text_question = Question.objects.create(
            text='Text Question',
            ttype='T',
            poll=cls.poll
        )

        cls.one_answer_question_answers = [
            Answer.objects.create(
                text=f'Answer text {i}',
                question=cls.one_answer_question
            ) for i in range(3)
        ]

        cls.several_answer_question_answers = [
            Answer.objects.create(
                text=f'Answer text {i}',
                question=cls.several_answer_question
            ) for i in range(3)
        ]

        cls.text_question_answer = Answer.objects.create(
            text='',
            question=cls.text_question
        )

    def add_results(self):
        Result.objects.create(
            user='1',
            answer=self.one_answer_question_answers[0]
        )
        Result.objects.create(
            user='1',
            answer=self.several_answer_question_answers[0]
        )
        Result.objects.create(
            user='1',
            answer=self.several_answer_question_answers[1]
        )
        Result.objects.create(
            user='1',
            text='Custom text answer of user 1',
            answer=self.text_question_answer
        )

        Result.objects.create(
            user='2',
            answer=self.several_answer_question_answers[2]
        )
        Result.objects.create(
            user='2',
            text='Custom text answer of user 2',
            answer=self.text_question_answer
        )

    def test_get_all(self):
        for user_id in ['1', '2']:
            response = self.client.get(
                reverse('result', args=([user_id]))
            )
            self.assertEqual(response.status_code, 200)
            objects = json.loads(response.content.decode())
            self.assertEqual(Result.objects.filter(user=user_id).count(), len(objects))

    def test_create_one_answer_result(self):
        result_data = {
            'user': '1',
            'answer': self.one_answer_question_answers[0].pk
        }
        response = self.client.post(
            reverse('results'),
            data=result_data,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(1, Result.objects.count())

    def test_no_two_similar_answers(self):
        result_data = {
            'user': '1',
            'answer': self.one_answer_question_answers[0].pk
        }
        self.client.post(
            reverse('results'),
            data=result_data,
            content_type=REQUEST_CONTENT_TYPE
        )
        response = self.client.post(
            reverse('results'),
            data=result_data,
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(400, response.status_code)

    def test_no_two_answers_for_one_question(self):
        self.client.post(
            reverse('results'),
            data={
                'user': '1',
                'answer': self.one_answer_question_answers[0].pk
            },
            content_type=REQUEST_CONTENT_TYPE
        )
        response = self.client.post(
            reverse('results'),
            data={
                'user': '1',
                'answer': self.one_answer_question_answers[1].pk
            },
            content_type=REQUEST_CONTENT_TYPE
        )
        self.assertEqual(400, response.status_code)

    def test_several_answers_question(self):
        for i in range(2):
            response = self.client.post(
                reverse('results'),
                data={
                    'user': '1',
                    'answer': self.several_answer_question_answers[i].pk
                },
                content_type=REQUEST_CONTENT_TYPE
            )
            self.assertEqual(201, response.status_code)
