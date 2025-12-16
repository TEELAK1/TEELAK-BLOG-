from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Category, Tag, Post, Comment


class PostModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="author", password="testpass123")
        self.category = Category.objects.create(name="Tech")
        self.tag = Tag.objects.create(name="Python")

    def test_slug_is_generated_on_save(self):
        post = Post.objects.create(
            title="My First Post",
            author=self.user,
            category=self.category,
            content="Test content",
            status="published",
            publish_date=timezone.now(),
        )
        self.assertTrue(post.slug)

    def test_is_published_property(self):
        post = Post.objects.create(
            title="Draft Post",
            author=self.user,
            category=self.category,
            content="Test content",
            status="draft",
        )
        self.assertFalse(post.is_published)


class CommentModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="author", password="testpass123")
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Commented Post",
            author=self.user,
            category=self.category,
            content="Test content",
            status="published",
            publish_date=timezone.now(),
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            content="Nice post!",
        )
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(comment.content, "Nice post!")


class BlogViewsTests(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user(
            username="author",
            password="testpass123",
            is_staff=True,
        )
        self.reader = User.objects.create_user(username="reader", password="testpass123")
        self.category = Category.objects.create(name="Tech")
        self.post = Post.objects.create(
            title="Published Post",
            author=self.author,
            category=self.category,
            content="Test content",
            status="published",
            publish_date=timezone.now(),
        )

    def test_post_list_view_status_and_template(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_post_detail_view_status_and_template(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_dashboard_requires_staff(self):
        # anonymous redirected
        response = self.client.get(reverse("blog:dashboard"))
        self.assertEqual(response.status_code, 302)

        # non-staff redirected
        self.client.login(username="reader", password="testpass123")
        response = self.client.get(reverse("blog:dashboard"))
        self.assertEqual(response.status_code, 302)

        # staff access
        self.client.login(username="author", password="testpass123")
        response = self.client.get(reverse("blog:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/dashboard.html")

    def test_create_post_requires_staff(self):
        url = reverse("blog:post_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username="reader", password="testpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        self.client.login(username="author", password="testpass123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

    def test_add_comment_flow(self):
        self.client.login(username="reader", password="testpass123")
        url = reverse("blog:add_comment", kwargs={"slug": self.post.slug})
        response = self.client.post(url, {"content": "Great post!"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.comments.count(), 1)
