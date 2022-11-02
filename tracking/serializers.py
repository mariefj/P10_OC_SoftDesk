from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError
 
from tracking.models import Project, Issue, Comment, Contributor


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user',
        ]

    def validate_type(self, value):
        if value not in ['back-end', 'front-end', 'iOS', 'Android']:
            raise ValidationError('Invalid type')
        return value

class ProjectDetailSerializer(ModelSerializer):

    issues = SerializerMethodField()

    def get_issues(self, instance):
        queryset = instance.issues
        serializer = IssueDetailSerializer(queryset, many=True)
        return serializer.data

    def get_contributors(self, instance):
        queryset = instance.contributors
        serializer = ContributorSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'type',
            'author_user',
            'issues',
            'contributors',
        ]

class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'desc',
            'tag',
            'priority',
            'status',
            'project',
            'author_user',
            'assignee_user',
            'created_time',
        ]

class IssueDetailSerializer(ModelSerializer):

    def get_comments(self, instance):
        queryset = instance.comments
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'desc',
            'tag',
            'priority',
            'status',
            'project',
            'author_user',
            'assignee_user',
            'created_time',
            'comments',
        ]

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'description',
            'issue',
            'author_user',
            'created_time',
        ]

class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'project',
            'permission',
            'role',
        ]
