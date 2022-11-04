from django.db import models
from django.conf import settings

class Project(models.Model):

    BACK_END = 'back-end'
    FRONT_END = 'front-end'
    IOS = 'iOS'
    ANDROID = 'Android'
    TYPE = [
        (BACK_END, ('back-end')),
        (FRONT_END, ('front-end')),
        (IOS, ('iOS')),
        (ANDROID, ('android')),
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE, default=BACK_END)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title

class Issue(models.Model):

    BUG = 'BUG'
    IMPROVEMENT = 'AMELIORATION'
    TASK = 'TACHE'
    TAG = [
        (BUG, ('BUG')),
        (IMPROVEMENT, ('AMELIORATION')),
        (TASK, ('TACHE')),
    ]

    LOW = 'FAIBLE'
    MEDIUM = 'MOYENNE'
    HIGH = 'ELEVEE'
    PRIORITY = [
        (LOW, ('FAIBLE')),
        (MEDIUM, ('MOYENNE')),
        (HIGH, ('ELEVEE')),
    ]

    TO_DO = 'A faire'
    IN_PROGRESS = 'En cours'
    DONE = 'Terminé'
    STATUS = [
        (TO_DO, ('A faire')),
        (IN_PROGRESS, ('En cours')),
        (DONE, ('Terminé')),
    ]

    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    tag = models.CharField(max_length=12, choices=TAG, default=BUG)
    priority = models.CharField(max_length=7, choices=PRIORITY, default=MEDIUM)
    status = models.CharField(max_length=8, choices=STATUS, default=TO_DO)
    created_time = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey('tracking.Project', on_delete=models.CASCADE, related_name='issues')
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="author_issues")
    assignee_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_issues", default=author_user)

    def __str__(self):
        return self.title

class Comment(models.Model):

    description = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    issue = models.ForeignKey('tracking.Issue', on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.title

class Contributor(models.Model):

    AUTHOR = 'auteur'
    CONTRIBUTOR = 'collaborateur'
    ROLE = [
        (AUTHOR, ('auteur')),
        (CONTRIBUTOR, ('collaborateur')),
    ]

    role = models.CharField(max_length=255, choices=ROLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_contributor")
    project = models.ForeignKey('tracking.Project', on_delete=models.CASCADE, related_name="contributors")

    def __str__(self):
        return self.user.first_name
