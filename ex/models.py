from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	# username = models.CharField(max_length=32, null=False, unique=True)
	# password = models.CharField(max_length=256, null=False)

	def __str__(self):
		return str(self.username)

class Tip(models.Model):
	content = models.TextField(null=False)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	date = models.DateField(auto_now_add=True, null=False)
	upvotes = models.ManyToManyField(User, related_name='upvotes')
	downvotes = models.ManyToManyField(User, related_name='downvotes')

	@property
	def define_total_upvotes(self):
		return self.upvotes.count()

	@property
	def define_total_downvotes(self):
		return self.downvotes.count()
