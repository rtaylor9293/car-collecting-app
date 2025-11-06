from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Choices for event type
DATES = (
    ('d', 'I Got the car'),
    ('p', 'I Lost the car'),

)

class Car(models.Model):
    type = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    mileage = models.IntegerField()
    year = models.IntegerField()
    cartrips = models.ManyToManyField('CarTrip', related_name='cars', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.type} {self.model}"

    def get_absolute_url(self):
        return reverse('cars_detail', kwargs={'car_id': self.id})


class CarDate(models.Model):
    date = models.DateField('Date you got car')
    present = models.CharField(
        max_length=1,
        choices=DATES,
        default=DATES[0][0]
    )
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    class Meta: 
     ordering = ['-date']  # This line makes the newest feedings appear first
    def __str__(self):
        return f"{self.get_present_display()} on {self.date}"

    def get_absolute_url(self):
        return reverse('cars_detail', kwargs={'car_id': self.car.id})


# Add the Toy model
class CarTrip(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=100)
    date = models.DateField('Trip date')
    location = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # ✅ add this field
    
    def __str__(self):
        return f"{self.event_name} on {self.date}"

    def get_absolute_url(self):
        return reverse('cartrip-create')