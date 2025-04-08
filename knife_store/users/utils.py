from django.conf import settings
from django.contrib.auth.models import User

import jwt
import redis
import datetime


# Настройка редис
redis_client = redis.StrictRedis(
    host='localhost',  
    port=6379,
    db=0,
    decode_responses=True 
)

# Создание токена
def create_jwt_token(user):
    current_time =  datetime.datetime.now(datetime.timezone.utc)
    payload = {
        'id': user.id,
        'exp': int((current_time + datetime.timedelta(days=1)).timestamp()), 
        'iat': int(current_time.timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

# Распаковка токена
def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Помещение токена в черный список в редисе(для оптимизации памяти),на случай перехвата токена когда пользователь уже вышел а время токена еще не истекло
def blacklist_token(token, ttl):
    try:
        redis_client.ping()
        redis_client.setex(f"blacklist:{token}", ttl, "blacklisted")
    except Exception as e:
        print(f"Ошибка при работе с Redis: {e}")

# Индикация присутсвия токена в черном списке
def is_token_blacklisted(token):
    return redis_client.exists(f"blacklist:{token}") > 0
