from django.db import models
from django.utils.timezone import now


class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(null=False, max_length=200)
    
    def __str__(self):
        return "Name: " + self.name + ", " \
            "Description: " + self.description

class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=80)
    dealer_id = models.IntegerField(null=False)
    year = models.DateField(null=False, default=now)

    TYPE_OPTIONS = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('wagon', 'WAGON')
    ]

    car_type = models.CharField(null=False, max_length=20, choices=TYPE_OPTIONS)

    def __str__(self):
        return "Name: " + self.name + " Make: " \
            + self.car_make.name + " Type: " \
            + self.car_type + " Year: " \
            + str(self.year) + " Dealer ID: " + str(self.dealer_id)

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
