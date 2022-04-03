from reviews.models import Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        path = serializer_field.context['request'].path
        for i in path:
            if i.isdigit():
                return Title.objects.get(id=i)
