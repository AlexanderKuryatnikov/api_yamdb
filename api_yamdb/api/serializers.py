from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # todo подумаю и допишу
    # author = serializers.SlugRelatedField(
        #read_only=True, slug_field='username'
    #)
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('pub_date',)
