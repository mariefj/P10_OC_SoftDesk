from rest_framework.permissions import BasePermission, SAFE_METHODS
 
class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS):
            return True
        return obj.author_user == request.user

class IsContributorAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS):
            return True
        return view.get_project().author_user == request.user
