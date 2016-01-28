from django.contrib import admin

from home_page.models import Comment

# Register your models here.


class CommentsAdmin(admin.ModelAdmin):
    fields = ['id_image', 'user', 'text', 'history', 'edits', 'updated_at']
    list_display = ['id_image', 'user']
    list_editable = ['id_image', 'user']
    list_filter = ['id_image', 'user']
    search_fields = ['id_image', 'user']

admin.site.register( Comment, CommentsAdmin)
