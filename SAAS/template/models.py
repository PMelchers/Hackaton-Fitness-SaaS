from django.db import models

class TestModel():
    test_text = models.CharField(max_length=255)
    