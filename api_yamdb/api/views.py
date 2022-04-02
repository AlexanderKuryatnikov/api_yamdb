from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .permissions import AuthorOrReadOnly
from .serializers import (
    AccessTokenObtainSerializer,
    CategorySerializer,
    ConfirmationCodeObtainSerializer,
    ReviewSerializer,
    CommentsSerializer
)
from reviews.models import Category, Title, Review, User


class ConfirmationCodeObtainView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ConfirmationCodeObtainSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        username = request.data.get('username')
        if User.objects.filter(email=email, username=username):
            confirmation_code = self.generate_key_and_send_email(email)
            user = get_object_or_404(User, email=email)
            user.confirmation_code = confirmation_code
            user.save()
            serializer = self.get_serializer(data=request.data)
            headers = self.get_success_headers(serializer.initial_data)
            return Response(serializer.initial_data,
                            status=status.HTTP_200_OK,
                            headers=headers)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_200_OK,
                        headers=headers)

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        confirmation_code = self.generate_key_and_send_email(email)
        serializer.save(confirmation_code=confirmation_code)

    def generate_key_and_send_email(self, email):
        confirmation_code = get_random_secret_key()
        send_mail(
            'Cofirmation Code',
            f'{confirmation_code}',
            'yamdb@example.com',
            [f'{email}'],
            fail_silently=False,
        )
        return confirmation_code


class AccessTokenObtainView(TokenViewBase):
    serializer_class = AccessTokenObtainSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('name', )


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
