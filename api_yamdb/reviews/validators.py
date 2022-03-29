from django.core.exceptions import ValidationError

def validate_nums(value):
    '''Проверка диапазона оценки от 1 до 10.'''
    if value <= 0 or value >= 11:
        raise ValidationError(f'оценка {value} должна быть от 1 до 10')
