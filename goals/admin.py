from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment, Board


class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created", "updated")
    search_fields = ("title", "user")


class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "category",
        "title",
        "description",
        "status",
        "priority",
        "due_date",
        "created",
        "updated"
    )
    search_fields = ("title", "user", "description")


class GoalCommentAdmin(admin.ModelAdmin):
    list_display = (
        "goal",
        "user",
        "text",
        "created",
        "updated"
    )
    search_fields = ("goal", "text", "user")


class BoardAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created",
        "updated"
    )
    search_fields = ("title",)


admin.site.register(GoalCategory, GoalCategoryAdmin)
admin.site.register(Goal, GoalAdmin)
admin.site.register(GoalComment, GoalCommentAdmin)
admin.site.register(Board, BoardAdmin)
