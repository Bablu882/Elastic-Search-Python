from django.db import models

# Create your models here.

class Account(models.Model):
    Accountid=models.CharField(max_length=100,null=False,blank=False)
    AccountName=models.CharField(max_length=100,null=False,blank=False)


class Contact(models.Model):
    Contactid=models.CharField(max_length=100,null=True,blank=True)
    ContactName=models.CharField(max_length=100,null=True,blank=True)


class Interest(models.Model):
    InterestID=models.CharField(max_length=100,null=False,blank=False)    
    InterestName=models.CharField(max_length=100,null=False,blank=False)
    InterestType=models.CharField(max_length=100,null=False,blank=False)

    Approvel_choices=(
        ('Approved','Approved'),
        ('Unapproved','Unapproved'),
        ('Unknown','Unknown')

    )
    ApprovalStatus=models.CharField(max_length=20,choices=Approvel_choices,default='Unknown')




class Product(models.Model):
    Productid=models.CharField(max_length=100,null=False,blank=False)
    ProductName=models.CharField(max_length=100,null=False,blank=False)
    EmailStatus=models.CharField(max_length=100,default='OptIn/OptOut')


# class InterestJunction(models.Model):
#     InterestJunctionID=models.CharField(max_length=100)    


# class AllFieldData(models.Model):
#     Account=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
#     Contact=models.ForeignKey(Contact,on_delete=models.SET_NULL,null=True)
#     Interest=models.ForeignKey(Interest,on_delete=models.SET_NULL,null=True)
#     Product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
#     InterestJunction=models.ForeignKey(InterestJunction,on_delete=models.SET_NULL,null=True)



class Interest_Junction_c(models.Model):
    InterestJunctionID=models.CharField(max_length=100)
    Category_of_Interest_c=models.CharField(max_length=100,null=False,blank=False)
    Maker_Artist_Interest_c=models.CharField(max_length=100,null=True,blank=True)
    Period_of_Interest_c=models.CharField(max_length=100,null=True,blank=True)
    Material_Theme_c=models.CharField(max_length=100,null=True,blank=True)
    Account=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    Interest=models.ForeignKey(Interest,on_delete=models.SET_NULL,null=True)
    Contact=models.ForeignKey(Contact,on_delete=models.SET_NULL,null=True)
    Product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)