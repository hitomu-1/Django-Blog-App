from django.db.models import Count, Q

from blog.models import Category, Tag


def common(request):
    # このcontext内ですべてのページで共通で使いたいカテゴリーやタグを登録していく
    context = {
        # Category.objestsでCategoryのクエリーセットを取得
        # annotateでCategoryの各オブジェクトに注釈（カウントなどの集計値）を付与している
        "categories": Category.objects.annotate(
            count=Count("post", Q(post__is_published=True))
        ),
        "tags": Tag.objects.all(),
    }
    return context
