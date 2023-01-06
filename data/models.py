from django.db import models


# Create your models here.
class Employee(models.Model):
    title = models.CharField(max_length=50, default=None, null=True, blank=True)
    family_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    given_name = models.CharField(max_length=50, default=None)
    work_phone = models.CharField(max_length=50, default=None)
    mobile_phone = models.CharField(max_length=50, default=None, null=True, blank=True)
    direct_line = models.CharField(max_length=50, default=None, null=True, blank=True)
    email = models.CharField(max_length=50, default='example@pangaea.co.zm')
    fax = models.CharField(max_length=50, default=None, null=True, blank=True)
    org = models.CharField(max_length=50, default='PANGAEA SECURITIES LIMITED')
    adr = models.CharField(max_length=50, default='First Floor,Pangaea Office Park,Lusaka Zambia')
    website = models.CharField(max_length=50, default='www.pangaea.co.zm')
