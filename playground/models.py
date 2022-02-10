from sre_constants import CATEGORY
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User


    
    
class Customer(models.Model):
	cf_handle = models.CharField(max_length=200, null=False, blank=True)
	username = models.ForeignKey(User,on_delete=models.CASCADE)
	password = models.CharField(max_length=200, null=False, blank=True)
	email = models.CharField(max_length=200, null=False, blank=True)
	phone = models.CharField(max_length=200, null=False, blank=False)
	category1 = models.BooleanField(name='CP1')
	category2 = models.BooleanField(name='CP2')
	category3 = models.BooleanField(name='DSA1')  
	category4 = models.BooleanField(name='DSA2')
	category5 = models.BooleanField(name='CP3')
	score1=models.IntegerField(default=0)
	score2=models.IntegerField(default=0)
	def __str__(self):
		return self.username.username
        
        
class Resources(models.Model):
    def __str__(self):
        return self.description
    CATEGORY = (
        ('DSA1', 'DSA1'),
        ('DSA2', 'DSA2'),
        ('CP1', 'CP1'),
        ('CP2', 'CP2'),
        ('CP3','CP3'),
    )
    description = models.CharField(max_length=200, null=False, blank=True)
    link = models.CharField(max_length=200, null=False, blank=True)
    slides = models.CharField(max_length=200, null=False, blank=True)
    category = models.CharField(max_length=200, null=False, blank=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    
class DailyTask(models.Model):
    def __str__(self):
        return self.description
    CATEGORY = (
        ('DSA1', 'DSA1'),
        ('DSA2', 'DSA2'),
        ('CP1', 'CP1'),
        ('CP2', 'CP2'),
        ('CP3','CP3'),
    )
    description = models.CharField(max_length=200, null=False, blank=True)
    link = models.CharField(max_length=200, null=False, blank=True)
    category = models.CharField(max_length=200, null=False, blank=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)