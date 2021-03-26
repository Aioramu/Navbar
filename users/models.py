from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Tokens(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=200,primary_key=True)
