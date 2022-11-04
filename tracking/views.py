from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

from authentication.models import User
from tracking.models import Project, Issue, Comment, Contributor
from tracking.serializers import (ProjectListSerializer, ProjectDetailSerializer, IssueListSerializer,
IssueDetailSerializer, CommentSerializer, ContributorSerializer, UserSerializer)

class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()

class SignUpViewset(APIView):
    def post(self, request, format=None):
        name = request.data['name']
        email = request.data['email']
        password = make_password(request.data['password'])
        user = User.objects.create(username=name, email=email, password=password)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)

class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.all()

class IssueViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()

class CommentViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

class ContributorViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContributorSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()
