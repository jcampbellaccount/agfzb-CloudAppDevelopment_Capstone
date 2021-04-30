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

class DealerReview:
    def __init__(self, dealership, id, name, purchase, review="", car_make="", car_model="", car_year=None, purchase_date=None, sentiment=""):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.id = id
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment

    def __str__(self):
        return "Customer name: " + self.name