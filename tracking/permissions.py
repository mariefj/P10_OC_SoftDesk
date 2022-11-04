from rest_framework.permissions import BasePermission, SAFE_METHODS
 
class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS):
            return True
        return obj.author_user == request.user

# class IsProjectContributorOrAuthor(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if (request.method in SAFE_METHODS and ):
#             return True
#         return obj.author_user == request.user

# class IsAssigneeOrAuthor(BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#         return obj.author_user == request.user

    
