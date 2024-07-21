from django.urls import path
from .views import PostCreateView, PostListView, post_detail, PythonPostView, CsharpPostView, RustPostView, \
    JavascriptPostView, CplusplusPostView, LatestPostView, WeekPostAgoView, MonthPostAgoView, PostEditView, \
    ConfirmDeletePostView, DeletePostView, AddCommentView, EditCommentView, ConfirmDeleteCommentView, DeleteCommentView, \
    RecommendedPostView, TagPostListView

app_name = 'posts'
urlpatterns = [

    path('', PostListView.as_view(), name='post_list'),
    path("<int:id>/", post_detail, name="post_detail"),
    path("create/", PostCreateView.as_view(), name='post_create'),
    path("<int:id>/edit/", PostEditView.as_view(), name="post_edit"),
    path("<int:id>/confirm/delete/", ConfirmDeletePostView.as_view(), name="confirm_delete_post"),
    path("<int:id>/delete/", DeletePostView.as_view(), name="delete_post"),


    path("<int:id>/comments/", AddCommentView.as_view(), name="post_comments"),
    path("<int:post_id>/comment/<int:comment_id>/edit/",  EditCommentView.as_view(), name="edit_comment"),
    path("<int:post_id>/comment/<int:comment_id>/confirm/delete/",  ConfirmDeleteCommentView.as_view(), name="confirm_delete_comment"),
    path("<int:post_id>/comment/<int:comment_id>/delete/",  DeleteCommentView.as_view(), name="delete_comment"),

    path('tag/<str:tag_name>/', TagPostListView.as_view(), name='tag_post_list'),

    path("category/python/", PythonPostView.as_view(), name="python_posts"),
    path("category/csharp/", CsharpPostView.as_view(), name="csharp_posts"),
    path("category/rust/", RustPostView.as_view(), name="rust_posts"),
    path("category/javascript/", JavascriptPostView.as_view(), name="javascript_posts"),
    path("category/cplusplus/", CplusplusPostView.as_view(), name="cplusplus_posts"),


    path("latest/posts/", LatestPostView.as_view(), name='latest_posts'),
    path("week/posts/", WeekPostAgoView.as_view(), name='week_posts'),
    path("month/posts/", MonthPostAgoView.as_view(), name='month_posts'),
    path("recommended/posts/", RecommendedPostView.as_view(), name="recommended_posts")
]