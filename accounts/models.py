from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField

# Create your models here.


class User(AbstractUser):
	staff_status = models.CharField(max_length=20, default='employee')
	leave_pending = models.PositiveSmallIntegerField(default=10)
 
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = ResizedImageField(size=[300, 300], quality=60, default='profile.jpg', upload_to='profile_pics')


	def __str__(self):
		return f'{self.user.username} profile'

class ApplicationForLeave(models.Model):
	employee = models.ForeignKey(User, on_delete=models.CASCADE)
	start_date = models.DateField(blank=False)
	end_date = models.DateField(blank=False)
	description  = models.TextField(blank=False)
	date_posted = models.DateTimeField(auto_now=True)
	application_status = models.CharField(max_length=10, blank=False, default='pending')

	def __str__(self):
		return f'Leave application - {self.employee}'
