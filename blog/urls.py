from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="post_list"),
    path("post/new/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<slug:slug>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<slug:slug>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
    path(
        "category/<slug:slug>/",
        views.CategoryPostListView.as_view(),
        name="category_posts",
    ),
    path("tag/<slug:slug>/", views.TagPostListView.as_view(), name="tag_posts"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("post/<slug:slug>/comment/", views.add_comment, name="add_comment"),
]
