from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Category, Comments, User


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
            raise serializers.ValidationError(
                'User not found'
            )
        if user.confirmation_code != data.get('confirmation_code'):
            raise serializers.ValidationError(
                'Invalid confirmation code'
            )
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
    title_id = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title_id')
        model = Review
        read_only_fields = ('pub_date',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title_id'),
                message=('ты уже оставил отзыв, больше ни-ни')
            )
        ]


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
