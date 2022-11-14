from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

from tracking.permissions import IsAuthor
from authentication.models import User
from tracking.models import Project, Issue, Comment, Contributor
from tracking.serializers import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentSerializer,
    ContributorSerializer,
    UserSerializer,
)


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class GetProjectMixin:
    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs["project_pk"])


class CheckContributorMixin:
    def check_contributor(self):
        return Contributor.objects.filter(
            user=self.request.user, project=self.kwargs["project_pk"]
        ).exists()


class SignUpViewset(APIView):
    def post(self, request, format=None):
        data = request.data.copy()
        data['password'] = make_password(request.data["password"])
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data=serializer.data)


class ProjectViewset(CheckContributorMixin, MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsAuthenticated, IsAuthor]

    def create(self, request, *args, **kargs):
        user = request.user.id
        data = request.data.copy()
        data["author_user"] = user
        serializer = ProjectListSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            contributor = Contributor(user=request.user, project=project, role="auteur")
            contributor.save()

        return Response(data=serializer.data)

    def get_queryset(self):
        return (
            Project.objects.filter(author_user=self.request.user)
            | Project.objects.filter(contributors__user=self.request.user)
        ).distinct()


class IssueViewset(
    CheckContributorMixin, GetProjectMixin, MultipleSerializerMixin, ModelViewSet
):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated, IsAuthor]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        project = self.get_project()

        if self.check_contributor():
            data = request.data.copy()
            data["project"] = kwargs["project_pk"]
            data["author_user"] = user
            try:
                if request.data["assignee_user"]:
                    assignee_user = User.objects.get(id=request.data["assignee_user"])
                    get_object_or_404(Contributor, user=assignee_user, project=project)
                    data["assignee_user"] = request.data["assignee_user"]
            except KeyError:
                data["assignee_user"] = user
            serializer = IssueListSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response(data=serializer.data)

    def get_queryset(self):
        self.get_project()
        if self.check_contributor():
            return Issue.objects.filter(project=self.kwargs["project_pk"])
        raise PermissionDenied(
            detail="You must be contributor on this project to do this action"
        )


class CommentViewset(
    CheckContributorMixin, GetProjectMixin, MultipleSerializerMixin, ModelViewSet
):
    serializer_class = CommentSerializer

    permission_classes = [IsAuthenticated, IsAuthor]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        project = self.get_project()
        get_object_or_404(Issue, pk=kwargs["issue_pk"], project=project)

        if self.check_contributor():
            data = request.data.copy()
            data["issue"] = kwargs["issue_pk"]
            data["author_user"] = user
            serializer = CommentSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return Response(data=serializer.data)

    def get_queryset(self):
        project = self.get_project()
        get_object_or_404(pk=self.kwargs["issue_pk"], project=project)
        if self.check_contributor():
            return Comment.objects.filter(issue=self.kwargs["issue_pk"])
        raise PermissionDenied(
            detail="You must be contributor on this project to do this action"
        )


class ContributorViewset(
    CheckContributorMixin, GetProjectMixin, MultipleSerializerMixin, ModelViewSet
):
    serializer_class = ContributorSerializer

    permission_classes = [IsAuthenticated, IsAuthor]

    def create(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_object_permissions(request, project)
        data = request.data.copy()
        data["project"] = kwargs["project_pk"]
        serializer = ContributorSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(data=serializer.data)

    def get_queryset(self):
        self.get_project()
        if self.check_contributor():
            return Contributor.objects.filter(project=self.kwargs["project_pk"])
        raise PermissionDenied(
            detail="You must be contributor on this project to do this action"
        )
