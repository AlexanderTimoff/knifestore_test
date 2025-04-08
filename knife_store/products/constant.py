from django.utils import timezone
from datetime import datetime
from decimal import Decimal

AD_TYPE_PRICES = {
    'top': 2000, 
    'highlight': 1000,  
    'special': 5000,  
}
AD_TYPE_CHOICES = [
        ('none', 'Без рекламы'),
        ('highlight', 'Выделение рамкой'),
        ('top', 'Поднятие на первое место'),
        ('special', 'Спецблок'),
    ]
YEAR_CHOICES = [(year, year) for year in range(1900, datetime.now().year + 1)] 
CLAS_CHOICES = [
        ('обычный', 'Обычный'),
        ('особое', 'Особое'),
        ('редкое', 'Редкое'),
        ('мистическое', 'Мистическое'),
        ('легендарное', 'Легендарное'),
    ]

BRAND_CHOICES = [
    ("bowie_knife", "Bowie Knife"),
    ("shadow_daggers", "Shadow Daggers"),
    ("falchion_knife", "Falchion Knife"),
    ("butterfly_knife", "Butterfly Knife"),
    ("huntsman_knife", "Huntsman Knife"),
    ("m9_bayonet", "M9 Bayonet"),
    ("bayonet", "Bayonet"),
    ("flip_knife", "Flip Knife"),
    ("gut_knife", "Gut Knife"),
    ("karambit", "Karambit"),
    ("talon_knife", "Talon Knife"),
    ("stiletto_knife", "Stiletto Knife"),
    ("navaja_knife", "Navaja Knife"),
    ("ursus_knife", "Ursus Knife"),
    ("survival_knife", "Survival Knife"),
    ("skeleton_knife", "Skeleton Knife"),
    ("paracord_knife", "Paracord Knife"),
    ("nomad_knife", "Nomad Knife")
]