from django.db import models


# Create your models here.
class MyUser(models.Model):
    username=models.CharField(max_length=10,unique=True,null=False)
    password=models.CharField(max_length=10)
    create_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='my_user'


class Article(models.Model):
    title=models.CharField(max_length=100)
    keywords=models.CharField(max_length=150)
    content=models.TextField(default=None)
    create_time=models.DateTimeField(auto_now_add=True)

    user=models.ForeignKey(MyUser)

    class Meta:
        db_table='article'