from django.contrib import admin

from .models import Post, Tags, Category,Review, HitCount
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time']

class HitCountAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'posts', 'body']

admin.site.register(Post, PostAdmin)
admin.site.register(Tags)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)
admin.site.register(HitCount, HitCountAdmin)
