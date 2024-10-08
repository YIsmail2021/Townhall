from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import User, Post, Comment, Category
from .serializers import PostSerializer, UserSerializer, CommentSerializer, CategorySerializer


class PostViewSet(ModelViewSet):
    # display latest posts therefore need to reverse order_by
    queryset = Post.objects.all().order_by('-created_on')
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        # Call the superclass destroy method
        super().destroy(request, *args, **kwargs)
        # Return a message and status code 204, prefer this code as it implies successful deletion.
        return Response({"message": "Post has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        ''' work has been done on dynamically filtering based on provided kwargs.
            However this is no need for this feature currently.'''
        
        # # Dynamically filter based on provided kwargs
        # for key, value in self.kwargs.items():
        #     if hasattr(Post, key):
        #         queryset = queryset.filter(**{key: value})

        category = self.request.query_params.get('category', None)
        # If 'category' is provided, filter the queryset by the given category
        if category:
            self.queryset = self.queryset.filter(category__id=category)
        return self.queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Post created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        # Check if filter exists in query string
        # Here in my opinion it is better to just send the necessary data of the latest posts,
        # rather than sending everything and processing it in Vue, everything should be processed here.
        # Get the page_size parameter from the URL query parameters
        page_size = request.query_params.get('page_size', None)
        if page_size:
            page_size = request.query_params.get('page_size')

            try:
                page_size = int(page_size)
            except ValueError:
                page_size = 3  # Fallback to default if conversion fails
            
            posts = self.queryset[:page_size]
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)

# simple viewset, no user operations are needed apart from fetching data.
class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get']

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Comment has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=pk)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Comment created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Category has been successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(queryset, pk=pk)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"message": "Category created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# APIview to link fetch data of comments that are linked to posts.
class PostCommentsAPIView(APIView):
    # APIView is used here for simplicity, focusing solely on the 
    # GET request to retrieve comments for a specific post, which 
    # reduces overhead compared to a ViewSet with unnecessary CRUD 
    # methods. However could've reduced overhead even more.
    def get(self, request, pk, *args, **kwargs):
        comments = Comment.objects.filter(post_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
