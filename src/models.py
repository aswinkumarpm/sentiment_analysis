from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class UserInput(models.Model):
    sentence = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    sentiment_label = models.CharField(max_length=255, null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)
    def __str__(self):
        return f"{self.timestamp} - {self.sentence[:20]}..."

#
