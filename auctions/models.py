from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    Category_name = models.CharField(max_length=60)

    def __str__(self):
        return self.Category_name
    

class AddBidd(models.Model):
    person = models.ForeignKey(User,on_delete=models.CASCADE , blank=True, null=True, related_name='userbid')
    newbid = models.FloatField()
    bidlist = models.IntegerField()


class CreateList(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=600)
    imageurl = models.CharField(max_length=1000)
    price = models.FloatField()
    IsActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE , blank=True, null=True, related_name='user')
    category = models.ForeignKey(Category,on_delete=models.CASCADE , blank=True, null=True, related_name='category')
    date = models.CharField(max_length=40)
    waatchlist = models.ManyToManyField(User , blank=True, null=True, related_name='userlist')

    
class Comments(models.Model):
    Writer = models.ForeignKey(User,on_delete=models.CASCADE , blank=True, null=True, related_name='usercomment')
    comment = models.CharField(max_length=150)
    comlist = models.ForeignKey(CreateList,on_delete=models.CASCADE , blank=True, null=True, related_name='commentlist')
    