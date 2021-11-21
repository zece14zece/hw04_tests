from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Создаем экземпляр клиента
        self.guest_client = Client()
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get("/")
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)

    def test_about_author(self):
        self.guest_client = Client()
        response = self.guest_client.get("/about/author/")
        self.assertEqual(response.status_code, 200)

    def test_about_tech(self):
        self.guest_client = Client()
        response = self.guest_client.get("/about/tech/")
        self.assertEqual(response.status_code, 200)


class TaskURLTests(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username="test_name",
        )

        self.group = Group.objects.create(
            title="Заголовок",
            slug="test_slug",
        )

        self.post = Post.objects.create(
            author=self.author,
            text="Текст, написанный для проверки",
            group=self.group,
        )
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username="HasNoName")
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.author)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            "posts/index.html": reverse("posts:index"),
            "posts/group_list.html": reverse(
                "posts:group_posts", kwargs={"slug": self.group.slug}
            ),
            "posts/profile.html": reverse(
                "posts:profile", kwargs={"username": self.author.username}
            ),
            "posts/post_detail.html": reverse(
                "posts:post_detail", kwargs={"post_id": self.post.id}
            ),
            "posts/create_post.html": reverse(
                "posts:post_edit", kwargs={"post_id": self.post.id}
            ),
        }

        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client_author.get(adress)
                self.assertTemplateUsed(response, template)
