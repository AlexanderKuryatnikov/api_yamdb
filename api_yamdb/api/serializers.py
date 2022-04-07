from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import (Category, Comments, Genre, Review,
                            Title, User)
from .fields import CurrentTitleDefault

class ConfirmationCodeObtainSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.HiddenField(default='')

    class Meta:
        model = User
        fields = ('email', 'username', 'confirmation_code')


class AccessTokenObtainSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = serializers.CharField()
        self.fields['password'].required = False

    def validate(self, data):
        user = User.objects.filter(username=data.get('username')).first()
        if user is None:
            raise NotFound('User not found')
        if user.confirmation_code != data.get('confirmation_code'):
            raise ValidationError('Invalid confirmation code')
        token = self.get_token(user).access_token
        return{'token': str(token)}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserSelfSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=True)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            )
        ]

    def validate_title(self, value):
        return self.context['request'].parser_context['kwargs']['title_id']


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
        read_only_fields = ('pub_date',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id',)
        model = Genre
        lookup_field = 'slug'


class TitleSerializerRead(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerWrite(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title
