class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer):
        return serializer.context.get(
            'request').parser_context.get('kwargs').get('title_id')
