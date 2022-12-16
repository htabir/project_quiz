from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404

from quiz.api.v1.permissions import MethodWisePermission
from quiz.api.v1.serializers import QuestionSerializer, QuizSerializer
from core.api.pagination import StandardResultsSetPagination
from quiz.models import Question, Quiz


class QuestionListCreateAPIView(ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    permission_classes = [MethodWisePermission]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.all()


class QuizListCreateAPIView(ListCreateAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()


class QuizRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = QuizSerializer

    def get_object(self):
        quiz_id = self.request.query_params.get('id')
        return get_object_or_404(Quiz, id=quiz_id)
