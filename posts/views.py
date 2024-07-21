from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from .forms import PostCreationForm, TagForm, PostEditForm, CommentForm
from .models import Post, Tags, HitCount, Review


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        created_form_post = PostCreationForm()
        tag_form = TagForm()
        context = {
            'post_form': created_form_post,
            "tag_form": tag_form
        }
        return render(request, 'posts/post_create.html', context)

    def post(self, request):
        create_form_post = PostCreationForm(request.POST, request.FILES)
        form_tag = TagForm(request.POST)
        if create_form_post.is_valid():
            post = create_form_post.save(commit=False)
            post.author = request.user
            post.save()

            if form_tag.is_valid():
                tags_form = form_tag.cleaned_data['name']
                tags_list = list(tags_form.split(','))
                for tag in tags_list:
                    if Tags.objects.filter(name=tag).exists():
                        t = Tags.objects.get(name=tag)
                    else:
                        t = Tags(name=tag)
                        t.save()
                    post.tags.add(t)
            create_form_post.save_m2m()
            return redirect('posts:post_list')
        context = {
            'post_form': create_form_post,
            'tag_form': form_tag
        }
        return render(request,'posts/post_create.html', context)


@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, Q(status="PB") & Q(id=id))
    user = request.user
    if not HitCount.objects.filter(post=post, user=user).exists():
        HitCount.objects.create(post=post, user=user)
    comment_form = CommentForm()
    context = {
        'post': post,
        'hits': post.get_hit_count,
        'comment_form': comment_form
    }
    return render(request, 'posts/post_detail.html', context)


class TagPostListView(ListView):
    model = Post
    template_name = 'posts/tag_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return Post.objects.filter(tags__name=tag_name, status="PB")


class AddCommentView(View):
    def post(self, request, id):
        post = Post.objects.get(id=id, status="PB")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            Review.objects.create(
                posts=post,
                author=request.user,
                body=comment_form.cleaned_data['body']
            )
            return redirect(reverse("posts:post_detail", kwargs={"id": post.id}))
        context = {
            "post": post,
            "comment_form": comment_form
        }
        return render(request, "posts/post_detail.html", context)


class EditCommentView(View):
    def get(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id, status="PB")
        comment = post.reviews.get(id=comment_id)
        comment_form = CommentForm(instance=comment)

        context = {
            "post": post,
            "comment": comment,
            "comment_form": comment_form
        }
        return render(request, "posts/edit_comment.html", context)

    def post(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id, status="PB")
        comment = post.reviews.get(id=comment_id)
        comment_form = CommentForm(instance=comment, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()

            return redirect(reverse("posts:post_detail", kwargs={"id": post.id}))

        context = {
            "post": post,
            "comment": comment,
            "comment_form": comment_form
        }
        return render(request, "posts/edit_comment.html", context)


class ConfirmDeleteCommentView(View):
    def get(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id, status="PB")
        comment = post.reviews.get(id=comment_id)
        context = {
            'post': post,
            'comment': comment
        }
        return render(request, "posts/confirm_delete_comment.html", context)


class DeleteCommentView(View):
    def get(self, request, post_id, comment_id):
        post = Post.objects.get(id=post_id, status="PB")
        comment = post.reviews.get(id=comment_id)
        comment.delete()
        messages.success(request, "Siz commentingiz  muvaffaqiyatli o'chirdingiz")
        return redirect(reverse("posts:post_detail", kwargs={"id": post_id}))


class PostListView(View):
    def get(self, request, tag=None):
        posts = Post.objects.all().filter(status='PB').annotate(hit_count=Count('hitcount'))
        search_query = request.GET.get('q', '')
        if search_query:
            posts = posts.filter(tags__name__icontains=search_query)
        context = {
            "posts": posts,
            "search_query": search_query
        }
        return render(request, "posts/post_list.html", context)


class PostEditView(LoginRequiredMixin ,View):
    def get(self, request, id):
        post = Post.objects.get(id=id, status="PB")
        post_edit_form = PostEditForm(instance=post)
        context = {
            "post": post,
            "post_edit_form": post_edit_form
        }
        return render(request, "posts/post_edit.html", context)

    def post(self, request, id):
        post = Post.objects.get(id=id, status="PB")
        post_edit_form = PostEditForm(instance=post, data=request.POST, files=request.FILES)
        if post_edit_form.is_valid():
            post_edit_form.save()
            return redirect(reverse("posts:post_detail", kwargs={"id": post.id}))

        context = {
            "post": post,
            "post_edit_form": post_edit_form
        }
        return render(request, "posts/post_edit.html", context)


class ConfirmDeletePostView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id, status="PB")

        context = {
            "post": post
        }
        return render(request, "posts/confirm_delete_post.html", context)


class DeletePostView(View):
    def get(self, request, id):
        post = Post.objects.get(id=id, status="PB")
        post.delete()
        messages.success(request, "Siz postingizni muvaffaqiyatli o'chirdingiz")
        return redirect(reverse("posts:post_list"))


class LandingPageView(View):
    def get(self, request):
        post_objects = Post.objects.all().filter(status="PB")
        new_posts = post_objects.annotate(hit_count=Count('hitcount')).order_by("-publish_time")[:4]
        popular_posts = post_objects.annotate(hit_count=Count('hitcount')).order_by('-hit_count')[:4]

        time_week_ago = timezone.now() - timedelta(days=7)
        week_posts = post_objects.filter(publish_time__gte=time_week_ago).annotate(hit_count=Count('hitcount')).order_by('-hit_count')[:4]

        time_month_ago = timezone.now() - timedelta(days=30)
        month_posts = post_objects.filter(publish_time__gte=time_month_ago).annotate(hit_count=Count('hitcount')).order_by('-hit_count')[:4]

        recommended_posts = post_objects.filter(recommended=True).annotate(hit_count=Count('hitcount'))
        context = {
            "new_posts": new_posts,
            "popular_posts": popular_posts,
            "week_posts": week_posts,
            "month_posts": month_posts,
            "recommended_posts": recommended_posts
        }
        return render(request, "landing.html", context)


class LatestPostView(View):

    def get(self, request):
        latest_posts = Post.objects.filter(status="PB").annotate(hit_count=Count('hitcount')).order_by("-publish_time")
        context = {
            "latest_posts": latest_posts
        }
        return render(request, 'posts/latest_post.html', context)


class WeekPostAgoView(View):

    def get(self, request):
        time_week_ago = timezone.now() - timedelta(days=7)
        week_posts = Post.objects.filter(publish_time__gte=time_week_ago).annotate(hit_count=Count('hitcount')).order_by('-hit_count')

        context = {
            "week_posts": week_posts
        }
        return render(request, "posts/week_posts.html", context)


class MonthPostAgoView(View):

    def get(self, request):
        time_month_ago = timezone.now() - timedelta(days=30)
        month_posts = Post.objects.filter(publish_time__gte=time_month_ago).annotate(hit_count=Count('hitcount')).order_by('-hit_count')

        context = {
            "month_posts": month_posts
        }
        return render(request, "posts/month_posts.html", context)


class RecommendedPostView(View):
    def get(self, request):
        recommended_posts = Post.objects.filter(Q(recommended=True) & Q(status="PB")).annotate(hit_count=Count('hitcount')).order_by("-publish_time")
        context = {
            "recommended_posts": recommended_posts
        }
        return render(request, "posts/recommended_posts.html", context)


class PythonPostView(View):

    def get(self, request):
        post_python = Post.objects.all().filter(Q(category__name='Python') & Q(status="PB"))
        search_query = request.GET.get('q', '')
        if search_query:
            post_python = post_python.filter(Q(title__icontains=search_query) & Q(body__icontains=search_query))
        context = {
            'post_python': post_python,
            'search_query': search_query
        }
        return render(request, 'posts/categorys/python_post_list.html', context)


class CsharpPostView(View):

    def get(self, request):
        post_csharp = Post.objects.all().filter(Q(category__name='C#') & Q(status="PB"))
        search_query = request.GET.get('q', '')
        if search_query:
            post_csharp = post_csharp.filter(Q(title__icontains=search_query) & Q(body__icontains=search_query))

        context = {
            'post_csharp': post_csharp,
            'search_query':search_query
        }
        return render(request, 'posts/categorys/csharp_post_list.html', context)


class RustPostView(View):

    def get(self, request):
        post_rust = Post.objects.all().filter(Q(category__name='Rust') & Q(status="PB"))
        search_query = request.GET.get('q', '')
        if search_query:
            post_rust = post_rust.filter(Q(title__icontains=search_query) & Q(body__icontains=search_query))
        context = {
            'post_rust': post_rust,
            'search_query': search_query
        }
        return render(request, 'posts/categorys/rust_post_list.html', context)


class JavascriptPostView(View):

    def get(self, request):
        post_javascript = Post.objects.filter(Q(category__name='JavaScripts') & Q(status="PB"))
        search_query = request.GET.get('q', '')
        if search_query:
            post_javascript = post_javascript.filter(Q(title__icontains=search_query) & Q(body__icontains=search_query))
        context = {
            'post_javascript': post_javascript,
            'search_query': search_query
        }
        return render(request, 'posts/categorys/javascript_post_list.html', context)


class CplusplusPostView(View):

    def get(self, request):
        post_cplusplus = Post.objects.filter(Q(status="PB") & Q(category__name='C++'))
        search_query = request.GET.get('q', '')
        if search_query:
            post_cplusplus = post_cplusplus.filter(Q(title__icontains=search_query) & Q(body__icontains=search_query))
        context = {
            'post_cplusplus': post_cplusplus,
            'search_query': search_query
        }
        return render(request, 'posts/categorys/cplusplus_post_list.html', context)
