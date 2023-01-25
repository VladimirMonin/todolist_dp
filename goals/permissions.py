from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.IsAuthenticated):
    """Доступ к доске (разрешено только создателю)"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.IsAuthenticated):
    """Доступ к доске (разрешено создателю и редактору)"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class GoalPermissions(permissions.IsAuthenticated):
    """Доступ к цели (разрешено создателю и редактору)"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.category.board
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj.category.board,
            role__in=(BoardParticipant.Role.owner, BoardParticipant.Role.writer)
        ).exists()


class CommentPermissions(permissions.IsAuthenticated):
    """Доступ к комментариям"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.goal.category.board
            ).exists()
        return request.user == obj.user
