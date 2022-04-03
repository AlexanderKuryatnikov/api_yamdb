from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.db.models import Avg
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from .permissions import AuthorOrReadOnly
from .serializers import (
    CategorySerializer, 
    ReviewSerializer, 
    CommentsSerializer,
    TitleSerializerRead,
    TitleSerializerWrite,
)
from reviews.models import Category, Title, Comments, Review


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleSerializerRead
        else:
            return TitleSerializerWrite


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()
    
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        reveiw_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=reveiw_id)
        return review.comments.all()
