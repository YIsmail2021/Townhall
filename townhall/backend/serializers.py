from rest_framework import serializers
from .models import Category, Post, User, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    humanize_created_on = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'ip_address', 'humanize_created_on']

    def get_humanize_created_on(self, obj):
        """Return the created_on field formatted as a human-readable string."""
        return obj.created_on.strftime('%d-%m-%Y %H:%M')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    humanize_created_on = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'author_id', 'category', 'humanize_created_on', 'image']

    def get_humanize_created_on(self, obj):
        """Return the created_on field formatted as a human-readable string."""
        return obj.created_on.strftime('%d-%m-%Y %H:%M')

    def get_author_id(self, obj):
        """Return the ID of the post's author."""
        return obj.author.pk

    def create(self, validated_data):
        """Create a Post instance, generating a random user if needed."""
        self.create_user(validated_data)
        return super().create(validated_data)

    def create_user(self, validated_data):
        """Create a new User instance based on the request IP address."""
        ip_address = self.context['request'].META.get('REMOTE_ADDR', None)
        validated_data['author'] = User.objects.create(ip_address=ip_address)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    humanize_created_on = serializers.SerializerMethodField(read_only=True)
    author_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'post', 'author_id', 'humanize_created_on']

    def get_humanize_created_on(self, obj):
        """Return the created_on field formatted as a human-readable string."""
        return obj.created_on.strftime('%d-%m-%Y %H:%M')

    def get_author_id(self, obj):
        """Return the ID of the comment's author."""
        return obj.author.pk

    def create(self, validated_data):
        """Create a Comment instance, generating a random user if needed."""
        self.create_user(validated_data)
        return super().create(validated_data)

    def create_user(self, validated_data):
        """Create a new User instance based on the request IP address."""
        ip_address = self.context['request'].META.get('REMOTE_ADDR', None)
        validated_data['author'] = User.objects.create(ip_address=ip_address)
