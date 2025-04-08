from django import template

register = template.Library()

@register.filter
def add_card_spaces(value):
    return ' '.join(value[i:i+4] for i in range(0, len(value), 4)) #фильтр для вставки пробела после каждой 4 цифры на карте,чисто для красоты
