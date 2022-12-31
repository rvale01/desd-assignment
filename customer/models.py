from django.db import models
    
class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    age_rating = models.CharField(max_length=100)
    film_id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.title

class Showing(models.Model):
    showing_id = models.AutoField(primary_key=True)
    time = models.TimeField()
    date = models.DateField()
    available_seats = models.IntegerField()
    film_id = models.ForeignKey(Film, to_field='film_id', on_delete=models.CASCADE)

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    customer = models.CharField(max_length=200)
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    total = models.IntegerField()
    quantity = models.IntegerField()
