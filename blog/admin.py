from django.contrib import admin

from blog.models import Post, Category, Tag, Comment, Reply


# 管理画面の表示方法を変更
class PostAdmin(admin.ModelAdmin):
    # 記事の表示方法を変更したい
    list_display = ("title", "category", "created_at", "updated_at", "is_published")
    # 管理画面で検索できるようにする
    search_fields = ("title", "content")
    # カテゴリーで絞り込めるようにする
    list_filter = ("category",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Reply)
