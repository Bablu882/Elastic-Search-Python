from rest_framework import serializers
from .models import Account,Contact,Interest,Product,InterestJunction




class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=['id','Accountid','AccountName']

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model=Contact
        fields=['id','Contactid','ContactName']

class InterestSerializers(serializers.ModelSerializer):
    class Meta:
        model=Interest
        fields=['id','InterestID','InterestName','InterestType','ApprovalStatus']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','Productid','ProductName','EmailStatus']        

class InterestJunctionSerializers(serializers.ModelSerializer):
    class Meta:
        model=InterestJunction
        fields='__all__'


class InterestSearchSerialiizers(serializers.Serializer):
    searchinterest=serializers.CharField(max_length=100)

class AccountSearchSerializer(serializers.Serializer):
    searchaccount=serializers.CharField(max_length=100)    

class ProductSearchSerializer(serializers.Serializer):
    searchproduct=serializers.CharField(max_length=100)    