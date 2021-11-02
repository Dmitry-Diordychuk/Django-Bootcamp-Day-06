from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	# username = models.CharField(max_length=32, null=False, unique=True)
	# password = models.CharField(max_length=256, null=False)

	def __str__(self):
		return str(self.username)
