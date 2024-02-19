from django.test import TestCase
from decouple import config


SECRET_KEY = config('password',default='')

print(SECRET_KEY)