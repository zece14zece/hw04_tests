from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group
from django.urls import reverse
import time

User = get_user_model()

SLUG_1 = "test-slug"
SLUG_2 = "group-2"
GROUP_1 = reverse("posts:group_posts", kwargs={"slug": SLUG_1})
GROUP_2 = reverse("posts:group_posts", kwargs={"slug": SLUG_2})
TEMP_PAGE_NAMES = {GROUP_1: "posts/group_posts.html"}


class TaskViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_a = User.objects.create_user(username="user_a")
        cls.author_p = User.objects.create_user(username="author_p")
        cls.group = Group.objects.create(
            slug=SLUG_1,
            title="test-title",
            description="test-desc",
        )
        cls.post = Post.objects.create(
            author=cls.author_p,
            text="TEXT1",
            group=cls.group,
        )
        time.sleep(0.01)
        Post.objects.create(
            author=cls.author_p,
            text="text_2",
        )
        for i in range(13):
            time.sleep(0.01)
            Post.objects.create(author=cls.user_a,
                                text=f"text{i}", group=cls.group)

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username="StasBasov")
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.group = Group.objects.create(
            title="Заголовок",
            slug="test_slug",
        )

        self.author = User.objects.create(
            username="test_name",
        )

        self.post = Post.objects.create(
            author=self.author,
            text="Текст, написанный для проверки",
            group=self.group,
        )

    def test_pages_uses_correct_template(self):

        templates_pages_names = {
            reverse("posts:index"): "posts/index.html",
            reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ): "posts/group_list.html",
            reverse(
                "posts:profile", kwargs={"username": self.author.username}
            ): "posts/profile.html",
            reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ): "posts/post_detail.html",
            reverse("posts:post_create"): "posts/create_post.html",
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_templates_with_paginator(self):

        templates_paginator_names = {
            "posts/post_detail.html": reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ),
            "posts/create_post.html": reverse("posts:post_create"),
        }

        for template, reverse_name in templates_paginator_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_correct_context(self):
        response = self.guest_client.get(reverse("posts:index"))
        self.assertEqual(len(response.context["page_obj"]), 10)

    def test_group_list_correct_context(self):
        response = self.guest_client.get(
            reverse("posts:group_posts", kwargs={"slug": self.group.slug})
        )
        first_object = response.context["page_obj"][0]
        post_group_0 = first_object.group
        self.assertEqual(post_group_0, self.group)

    def test_profile_correct_context(self):
        response = self.guest_client.get(
            reverse("posts:profile", kwargs={"username": self.author.username})
        )
        first_object = response.context["page_obj"][0]
        post_group_0 = first_object.author
        self.assertEqual(post_group_0, self.post.author)

    def test_post_in_2_group(self):
        second_group = Group.objects.create(
            slug=SLUG_2,
            title="test group2",
            description="test desc2",
        )
        Post.objects.create(author=self.user,
                            text="new_text", group=second_group)
        response = self.guest_client.get(GROUP_1)
        self.assertEqual(response.context["page_obj"][0].id, 15)
