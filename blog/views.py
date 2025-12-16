from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .forms import PostForm, CommentForm
from .models import Post, Category, Tag


class OwnerOrStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool:
        obj = self.get_object()
        return self.request.user.is_staff or obj.author == self.request.user


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(
            status="published",
            publish_date__lte=timezone.now(),
        )
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(category__name__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
        return (
            queryset.select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-publish_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["query"] = self.request.GET.get("q", "")
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_queryset(self):
        # Allow checking draft posts if use is staff OR the author
        queryset = Post.objects.all() 
        return queryset.select_related("author", "category").prefetch_related(
            "tags", "comments__author"
        )
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.status == 'published' and obj.publish_date <= timezone.now():
            return obj
        if self.request.user.is_authenticated and (self.request.user.is_staff or obj.author == self.request.user):
            return obj
        # Trigger 404 for others
        from django.http import Http404
        raise Http404("Post not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(active=True)
        context["related_posts"] = (
            Post.objects.filter(
                status="published",
                publish_date__lte=timezone.now(),
                category=self.object.category,
            )
            .exclude(pk=self.object.pk)
            .order_by("-publish_date")[:3]
        )
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "blog/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
             context["posts"] = Post.objects.select_related("author", "category").all()
        else:
             context["posts"] = Post.objects.select_related("author", "category").filter(author=self.request.user)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(OwnerOrStaffRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PostDeleteView(OwnerOrStaffRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("blog:post_list")


class CategoryPostListView(PostListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        queryset = Post.objects.filter(
            status="published",
            publish_date__lte=timezone.now(),
            category=self.category,
        )
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(category__name__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
        return queryset.select_related("author", "category").prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_category"] = self.category
        return context


class TagPostListView(PostListView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        queryset = Post.objects.filter(
            status="published",
            publish_date__lte=timezone.now(),
            tags=self.tag,
        )
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(category__name__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
        return queryset.select_related("author", "category").prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current_tag"] = self.tag
        return context


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect(post.get_absolute_url())
