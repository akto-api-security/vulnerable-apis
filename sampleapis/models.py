from django.contrib.auth.models import User
from django.db import models
from djongo import models as djongo_models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    roll_number = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    departement = models.CharField(max_length=55, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            self.email = self.user.email
            self.username = self.user.username
            self.name = f"{self.user.first_name} {self.user.last_name}"
        super().save(*args, **kwargs)

class CardDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16,unique=True)
    card_holder_name = models.CharField(max_length=255)
    card_expiry_date = models.DateField()
    card_type = models.CharField(max_length=100)
    payment_network = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
    
class student(djongo_models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=20, primary_key=True)
    departement = models.CharField(max_length=50)
    batch = models.CharField(max_length=4)

    class Meta:
        db_table = 'STUDENTS_TABLE'

    @classmethod
    def objects(cls):
        return super().objects.using('mongo')

    def save(self, *args, **kwargs):
        using = kwargs.pop('using', 'default')
        super().save(using=using, *args, **kwargs)

class Result(djongo_models.Model):
    user = models.OneToOneField('student', on_delete=models.CASCADE, primary_key=True)
    subject1 = models.IntegerField()
    subject2 = models.IntegerField()
    subject3 = models.IntegerField()
    subject4 = models.IntegerField()
    subject5 = models.IntegerField()
    subject6 = models.IntegerField()

    class Meta:
        db_table = 'RESULT_TABLE'

