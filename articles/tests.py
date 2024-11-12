from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Article, Comment


class ArticleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            age=28,
            password="secret"
        )
        
        cls.article = Article.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user
        )
        
    def login_user(self):
        self.client.login(username="testuser", password="secret")
        
    def test_article_model(self):
        self.assertEqual(self.article.title, "A good title")
        self.assertEqual(self.article.body, "Nice body content")
        self.assertEqual(self.article.author.username, "testuser")
        self.assertEqual(str(self.article), "A good title")
        self.assertEqual(self.article.get_absolute_url(), "/articles/1/")
        
    def test_url_exists_at_correct_location_listview(self):
        self.login_user()
        response = self.client.get("/articles/")
        self.assertEqual(response.status_code, 200)
        
    def test_url_exists_at_correct_location_detailview(self):
        self.login_user()
        response = self.client.get("/articles/1/")
        self.assertEqual(response.status_code, 200)
        
    def test_article_listview(self):
        self.login_user()
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nice body content")
        self.assertTemplateUsed(response, "article_list.html")
        
    def test_article_detailview(self):
        self.login_user()
        response = self.client.get(reverse("article_detail", 
            kwargs={"pk": self.article.pk}))
        no_response = self.client.get("/articles/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "A good title")
        self.assertTemplateUsed(response, "article_detail.html")
        
    def test_comment_creation_detailview(self):
        self.login_user()
        
        response = self.client.post(
            reverse("article_detail", args=[self.article.id]),
            {
                "comment": "This is a comment from the view."
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(
            article=self.article, 
            comment="This is a comment from the view."
            ).exists()
        )
        
    def test_comment_display_detailview(self):
        self.login_user()
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            comment="Display comment."
        )
        response = self.client.get(
            reverse("article_detail", args=[self.article.id]))
        self.assertContains(response, "Display comment.")
        
    def test_article_createview(self):
        self.login_user()
        response = self.client.post(
            reverse("article_new"),
            {
                "title": "New title",
                "body": "New text",
                "author": self.user.id,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.last().title, "New title")
        self.assertEqual(Article.objects.last().body, "New text")
        
    def test_article_updateview(self):
        self.login_user()
        response = self.client.post(
            reverse("article_edit", args="1"),
            {
                "title": "Updated title",
                "body": "Updated text",
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.last().title, "Updated title")
        self.assertEqual(Article.objects.last().body, "Updated text")
       
    def test_article_deleteview(self):
        self.login_user()
        response = self.client.post(reverse("article_delete", args="1"))
        self.assertEqual(response.status_code, 302)

        
class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@email.com",
            age=28,
            password="secret"
        )
        
        cls.article = Article.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user
        )
        
    def test_create_comment(self):
        comment = Comment.objects.create(
            article=self.article,
            author=self.user,
            comment="This is a comment."
        )
        self.assertEqual(comment.article, self.article)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.comment, "This is a comment.")
        self.assertTrue(Comment.objects.filter(article=self.article).exists())
