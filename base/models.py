from django.db import models
from django.utils.timezone import localtime
import pytz
import uuid
# Create your models here.

REPEAT_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),

]


class TodoModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    repeat = models.CharField(max_length=20, choices=REPEAT_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.date:
            # Convert UTC datetime to IST
            ist_tz = pytz.timezone('Asia/Kolkata')
            self.date = self.date.astimezone(ist_tz)
        super().save(*args, **kwargs)
