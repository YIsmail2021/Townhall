from django.test import TestCase
from faker import Faker
from .models import User, Post, Category, Comment

fake = Faker()

class UserModelTest(TestCase):

    def test_user_creation(self):
        # Generate a fake IPv4 address
        ip_address = fake.ipv4()
        user = User.objects.create(ip_address=ip_address)
        # Assert that the IP address matches the one generated by Faker
        self.assertEqual(user.ip_address, ip_address)


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        # Generate a fake category name
        name = fake.word()
        category = Category.objects.create(name=name)
        # Assert that the category name matches
        self.assertEqual(category.name, name)


class PostModelTest(TestCase):

    def test_post_creation(self):
        # Create a fake user and category
        user = User.objects.create(ip_address=fake.ipv4())
        category = Category.objects.create(name=fake.word())
        
        # Ensure the title does not exceed 15 characters
        title = fake.word()[:15]
        
        # Create a fake post
        post = Post.objects.create(
            title=title,
            body=fake.text(max_nb_chars=3000),
            author=user,
            category=category,
            image=None  # Optional, can add a fake image if needed
        )
        
        # Assert the post title and body are as expected
        self.assertEqual(post.title, title)
        self.assertEqual(post.body, post.body)


class CommentModelTest(TestCase):

    def test_comment_creation(self):
        # Create a fake user, category, post, and comment
        user = User.objects.create(ip_address=fake.ipv4())
        category = Category.objects.create(name=fake.word())
        post = Post.objects.create(
            title=fake.word()[:15],
            body=fake.text(max_nb_chars=3000),
            author=user,
            category=category
        )
        comment_body = fake.text(max_nb_chars=300)
        comment = Comment.objects.create(
            body=comment_body,
            post=post,
            author=user
        )
        
        # Assert the comment body and associated post/author are as expected
        self.assertEqual(comment.body, comment_body)
        self.assertEqual(comment.post, post)
        self.assertEqual(comment.author, user)
