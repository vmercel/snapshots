from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

##new
## class Category(models.Model):
##     name = models.CharField(max_length=50, blank=True, null=True)
##
##     class Meta:
##         verbose_name_plural= "Categories"
##
##     def __str__(self):
##         return self.name


class Data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_data')
    country = models.CharField(max_length=100, null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)
    statusn = models.BooleanField(null=True)

    def __str__(self):
        return self.country


class Covid(models.Model):
    image = models.ImageField(upload_to='images/')
    data = models.ForeignKey(Data, on_delete=models.CASCADE, related_name='covid_data')
    status = models.BooleanField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Covid ' + str(self.created)