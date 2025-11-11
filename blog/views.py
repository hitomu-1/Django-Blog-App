from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post, Category, Tag, Comment, Reply
from blog.forms import CommentForm, ReplyForm


posts_per_page = 5


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    # 1ページごとに表示するブログの数
    paginate_by = posts_per_page

    def get_queryset(self):
        posts = super().get_queryset()
        return posts.order_by("-updated_at")


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_object(self, queryset=None):
        # 公開済み or ログイン
        post = super().get_object(queryset)
        if post.is_published or self.request.user.is_authenticated:
            return post
        else:
            raise Http404


# カテゴリーで絞り込んだ後にPostを一覧表示
class CategoryPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    paginate_by = posts_per_page

    def get_queryset(self):
        # トップページでアクセスのあったカテゴリーのURLを変数slugに代入
        slug = self.kwargs["slug"]
        self.category = get_object_or_404(Category, slug=slug)
        return super().get_queryset().filter(category=self.category)

    # modelで指定したPostモデルとは別の任意のデータを渡すためのメソッド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        print(context)
        return context


# タグで絞り込んだ後にPostを一覧表示
class TagPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = posts_per_page

    def get_queryset(self):
        # トップページでアクセスのあったタグのURLを変数slugに代入
        slug = self.kwargs["slug"]
        self.tag = get_object_or_404(Tag, slug=slug)
        return super().get_queryset().filter(tag=self.tag)

    # modelで指定したPostモデルとは別の任意のデータを渡すためのメソッド
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class SearchPostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = posts_per_page

    def get_queryset(self):
        # getメソッドで送られてきたクエリパラメータの値を取得する
        self.query = self.request.GET.get("query") or ""
        queryset = super().get_queryset()

        if self.query:
            queryset = queryset.filter(
                # タイトルの中に検索キーワードが含まれるか、iがあると大文字小文字を区別しない
                # または
                # 本文の中に検索キーワードが含まれるか、iがあると大文字小文字を区別しない
                Q(title__icontains=self.query)
                | Q(content__icontains=self.query)
            )

        if not self.request.user.is_authenticated:
            # 公開済みの記事だけに絞り込む
            queryset = queryset.filter(is_published=True)

        self.post_count = len(queryset)

        return queryset

    # どんなキーワードで検索したかをテンプレートで表示できるようにする
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.query
        context["post_count"] = self.post_count
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    # フォームでは名前とコメントのみの入力、どのpostに対するコメントかはアプリ側が自動で決める
    # 引数で受け取ったformに何らかの編集を加えて、最終的にDBへ登録する
    def form_valid(self, form):
        # commit=Falseとすることでformの内容をDBに保存する前にメソッド内で扱えるようにする
        comment = form.save(commit=False)

        post_pk = self.kwargs["post_pk"]
        # 対象のpostがあるなら、postに代入
        post = get_object_or_404(Post, pk=post_pk)

        comment.post = post
        comment.save()

        return redirect("post-detail", pk=post_pk)

    # Postの情報もテンプレートに渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pk = self.kwargs["post_pk"]
        context["post"] = get_object_or_404(Post, pk=post_pk)

        return context


class ReplyCreateView(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name = "blog/comment_form.html"

    # フォームでは名前と返信のみの入力、どのcommentに対する返信かはアプリ側が自動で決める
    # 引数で受け取ったformに何らかの編集を加えて、最終的にDBへ登録する
    def form_valid(self, form):
        # commit=Falseとすることでformの内容をDBに保存する前にメソッド内で扱えるようにする
        reply = form.save(commit=False)

        comment_pk = self.kwargs["comment_pk"]
        # 対象のpostがあるなら、postに代入
        comment = get_object_or_404(Comment, pk=comment_pk)

        reply.comment = comment
        reply.save()

        return redirect("post-detail", pk=comment.post.pk)

    # Commentの情報もテンプレートに渡す
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment_pk = self.kwargs["comment_pk"]
        context["comment"] = get_object_or_404(Comment, pk=comment_pk)

        return context


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_delete.html"
    # success_url = reverse_lazy("post-detail")

    # reverse_lazyでは"どの"詳細ページなのかまでは指定できないため、メソッドを定義する必要がある
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})


class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = "blog/comment_delete.html"
    # success_url = reverse_lazy("post-detail")

    # reverse_lazyでは"どの"詳細ページなのかまでは指定できないため、メソッドを定義する必要がある
    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.comment.post.pk})
