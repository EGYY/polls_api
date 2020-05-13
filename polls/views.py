from datetime import datetime
from .models import *
from rest_framework import viewsets, generics
from .serializers import *
from rest_framework.permissions import IsAdminUser


class PollViewSet(viewsets.ModelViewSet):
    """добавление, редактирование, удаление, вывод списка всех опросов"""
    permission_classes = [IsAdminUser]  # доступно только администратору
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ActivePollViewSet(viewsets.ReadOnlyModelViewSet):
    """все активные опросы вместе со списком вопросов"""
    queryset = Poll.objects.filter(date_end__gte=datetime.now()). \
        exclude(questions__isnull=True)  # только актуальные опросы, содержащие 1 и более вопросов
    serializer_class = ActivePollSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """добавление, редактирование, удаление, вывод списка всех вопросов"""
    permission_classes = [IsAdminUser]  # доступно только администратору
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    """сохранение ответов"""
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class CompletedPollViewSet(viewsets.ReadOnlyModelViewSet):
    """все пройденные опросы вместе со списком вопросов и ответами текущего пользователя"""

    def get_queryset(self):
        return Poll.objects.filter(questions__question_answer__isnull=False,  # вопросы с ответами
                                   questions__question_answer__user=self.request.user)  # текущий пользователь

    serializer_class = CompletedPollSerializer
