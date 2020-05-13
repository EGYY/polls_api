from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):  # опрос
    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание')
    date_start = models.DateField('Дата старта', auto_now_add=True)
    date_end = models.DateField('Дата окончания')


class Question(models.Model):  # вопрос из опроса
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Текст вопроса')
    QUESTION_TYPE = (
        (0, 'Текст'),
        (1, 'Выбор одного варианта'),
        (2, 'Выбор из нескольких вариантов'),
    )
    type = models.IntegerField('Тип вопроса', default=0, choices=QUESTION_TYPE)


class Answer(models.Model):  # ответ пользователя
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_answer')
    # poll = models.ForeignKey(Poll, on_delete=models.PROTECT, related_name='poll_answer')
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='question_answer')
    answer_text = models.CharField('Ответ пользователя', max_length=255)
