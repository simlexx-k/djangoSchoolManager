from rest_framework import permissions

class IsParentOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['student', 'parent']

class IsAdminOrTeacherOrParentOrStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type in ['admin', 'teacher', 'parent', 'student']

class IsOwnerOrParent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'student':
            return obj.learner_id == request.user.id
        elif request.user.user_type == 'parent':
            return obj.learner_id in request.user.children.all().values_list('id', flat=True)
        return False

class IsStudentOrParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['student', 'parent']
