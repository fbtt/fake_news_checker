from django.db import models

# Create your models here.


class News(models.Model):
    news = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return f'{self.created_at}'