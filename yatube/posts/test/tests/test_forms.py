from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class TaskCreateFormTests(TestCase):

    def setUp(self):
        # Создаем авторизованный клиент
        self.test_group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug'
        )
        self.user = User.objects.create(username='test-user')
        self.authorized_client_author = Client()
        self.authorized_client_author.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='тестовый текст',
        )

    def test_create_post(self):

        posts_count = Post.objects.count()

        form_data = {
            'text': 'Тестовый текст',
            'group': self.test_group.id
        }
        # Отправляем POST-запрос
        response = self.authorized_client_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': self.user})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        latest_post = Post.objects.first()
        self.assertEqual(latest_post.text, form_data['text'])
        self.assertEqual(latest_post.author, self.user)
        self.assertEqual(latest_post.group, self.test_group)

    def test_post_edit(self):
        form_data = {
            'text': 'изменённый текст',
        }
        self.authorized_client_author.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True,
        )
        edited_text = Post.objects.first()
        self.assertEqual(edited_text.text, form_data['text'])
