from django.db import models

# Create your models here.

class Account(models.Model):
    Accountid=models.CharField(max_length=100,null=False,blank=False,unique=True)
    AccountName=models.CharField(max_length=100,null=False,blank=False)
    State=models.CharField(max_length=100,null=False,blank=False)
    LastPurchasedDtae=models.CharField(max_length=50,null=False,blank=False)
    TotalPurchase=models.CharField(max_length=100,null=False,blank=False)
    choices_opt=(
        ('OptIn','OptIn'),
        ('OptOut','OptOut')
    )
    PersonHasOptedOutOfEmail=models.CharField(max_length=20,choices=choices_opt)
    CategoryOfInterest=models.CharField(max_length=100,null=False,blank=False)
    PeriodOfInterest=models.CharField(max_length=100,null=False,blank=False)
    TypeOfInterest=models.CharField(max_length=100,null=False,blank=False)
    YoungerAudience=models.CharField(max_length=100,null=False,blank=False)
    Star5=models.IntegerField()
    AccountLastPurchaseDate=models.CharField(max_length=50,null=False,blank=False)
    HolidayCelebrated=models.CharField(max_length=100,null=False,blank=False)
    Email=models.EmailField()
    ShippingCity=models.CharField(max_length=100,null=False,blank=False)
    FindClients_visible=models.CharField(max_length=100,null=False,blank=False)



class Contact(models.Model):
    Contactid=models.CharField(max_length=100,null=True,blank=True)
    ContactName=models.CharField(max_length=100,null=True,blank=True)


class Interest(models.Model):
    InterestID=models.CharField(max_length=100,null=False,blank=False,unique=True)    
    InterestName=models.CharField(max_length=100,null=False,blank=False)

    Approvel_choices=(
        ('True','True'),
        ('False','False')

    )
    ApprovalStatus=models.CharField(max_length=20,choices=Approvel_choices)




class Product(models.Model):
    Productid=models.CharField(max_length=100,null=False,blank=False,unique=True)
    ProductName=models.CharField(max_length=100,null=False,blank=False)
    

# class InterestJunction(models.Model):
#     InterestJunctionID=models.CharField(max_length=100)    


# class AllFieldData(models.Model):
#     Account=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
#     Contact=models.ForeignKey(Contact,on_delete=models.SET_NULL,null=True)
#     Interest=models.ForeignKey(Interest,on_delete=models.SET_NULL,null=True)
#     Product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
#     InterestJunction=models.ForeignKey(InterestJunction,on_delete=models.SET_NULL,null=True)



class Interest_Junction_c(models.Model):
    InterestNameJunction=models.CharField(max_length=100,null=False,blank=False)
    InterestName=models.CharField(max_length=100,null=False,blank=False)
    InterestJunctionID=models.CharField(primary_key=True,max_length=100)
    choices_with=(
        ('Account','Account'),
        ('Product','Product')
    )
    link_With=models.CharField(max_length=50,choices=choices_with)
    Account=models.ForeignKey(Account,to_field='Accountid',on_delete=models.SET_NULL,null=True)
    Interest=models.ForeignKey(Interest,to_field='InterestID',on_delete=models.SET_NULL,null=True)
    Product=models.ForeignKey(Product,to_field='Productid',on_delete=models.SET_NULL,null=True)



class Opportunity(models.Model):
    OpportunityId=models.CharField(max_length=100,null=False,blank=False,unique=True)
    OpportunityName=models.CharField(max_length=100,null=False,blank=False)
    AccountId=models.ForeignKey(Account,to_field='Accountid',on_delete=models.SET_NULL,null=True)
    StageName=models.CharField(max_length=100,null=False,blank=False)
    Billing_City=models.CharField(max_length=100,null=False,blank=False)
    AverageitemSold=models.CharField(max_length=100,null=False,blank=False)



    