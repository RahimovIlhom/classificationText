from django.contrib import admin
from .models import Field, Post, Comment


# Register your models here.

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInLine]


admin.site.register(Field)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
