from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Employees Departments
class Department(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, default='')

	def __str__(self):
		return '{} - {}' \
			.format(self.id, self.name)


GENDER_CHOICES = (
	('', 'Select a title'),
	('male', 'male'),
	('female', 'female'),
)

TITLE_CHOICES = (
	('', 'Select a title'),
	('entry', 'entry'),
	('junior', 'junior'),
	('mid', 'mid'),
	('senior', 'senior'),
	('manager', 'manager'),
)


# Additional Employee Details
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	birth_date = models.DateField(null=True, blank=True,)
	phone = models.CharField(max_length=20, blank=True, null=True)
	mobile = models.CharField(max_length=20, blank=True, null=True)
	address = models.CharField(max_length=150, blank=True, null=True)
	postcode = models.CharField(max_length=5, blank=True, null=True)
	title = models.CharField(choices=sorted(TITLE_CHOICES), default='', max_length=7)
	father_name = models.CharField(max_length=50, default='')
	department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
	gender = models.CharField(choices=sorted(GENDER_CHOICES), default='', max_length=6)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Employee Detail'

	def __str__(self):
		return "{} {}".format(self.user.first_name, self.user.last_name)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()


PRIORITY_CHOICES = (
	('high', 'high'),
	('low', 'low'),
)

REPORT_TITLES_CHOICES = (
	('', 'Select a title'),
	('CON', 'Consumables'),
	('PRO', 'Promotion'),
	('EXP', 'Expenses'),
	('SUP', 'Support')
)


# Employees Reports
class Report(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(choices=sorted(REPORT_TITLES_CHOICES), default='', max_length=3)
	description = models.CharField(max_length=300, blank=True)
	priority = models.CharField(choices=sorted(PRIORITY_CHOICES), default='low', max_length=4)
	solved = models.BooleanField(default=False)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Employee Report'

	def __str__(self):
		return '{} - {}' \
			.format(self.user.username, self.title)



