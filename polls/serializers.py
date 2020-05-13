from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueTogetherValidator


class PollSerializer(serializers.ModelSerializer):
    """сериализатор опросов"""
    date_start = serializers.DateField(read_only=True)  # дата старта опроса не подлежит редактированию

    class Meta:
        model = Poll
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    """сериализатор вопросов"""

    class Meta:
        model = Question
        fields = '__all__'


class QuestionInActivePollSerializer(serializers.ModelSerializer):
    """список вопросов в активных опросах"""

    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Question
        exclude = ['poll']


class ActivePollSerializer(serializers.ModelSerializer):
    """активные опросы вместе со списком вопросов"""
    questions = QuestionInActivePollSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    """
    сериализатор ответов
    каждый пользователь может лишь однажды ответить на каждый опрос
    """

    class Meta:
        model = Answer
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(  # запрет на повторное прохождение опросов
                queryset=Answer.objects.all(),
                fields=['user', 'question'],  # проверка уникальности связки полей
                message='Вы уже отвечали на данный вопрос'
            )
        ]


class QuestionAndAnswer(serializers.ModelSerializer):
    """сериализатор вопросов с ответами на них"""
    question_answer = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='answer_text'
     )
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Question
        exclude = ['poll']


class CompletedPollSerializer(serializers.ModelSerializer):
    """пройденные опросы с ответами"""
    questions = QuestionAndAnswer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'

