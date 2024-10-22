from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Custom User Manager

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100)
    event_date = models.DateField()
    event_time = models.TimeField(null=True, blank=True)
    event_location = models.CharField(max_length=100, default="Unknown Location")
    event_description = models.TextField(default="No description available")
    event_poster = models.ImageField(upload_to='event_posters/', blank=True, null=True)

    def __str__(self):
        return self.event_name

class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=100)
    ticket_quantity = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)

class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=1)