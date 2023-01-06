from rest_framework import serializers
from .models import Account,Contact,Interest,Product,Interest_Junction_c




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
    Product=ProductSerializers(many=False,read_only=True)
    Interest=InterestSerializers(many=False,read_only=True)
    Account=AccountSerializers(many=False,read_only=True)
    Contact=ContactSerializers(many=False,read_only=True)
    class Meta:
        model=Interest_Junction_c
        fields=[
            "id",
            "Category_of_Interest_c",
            'InterestJunctionID',
            'Maker_Artist_Interest_c',
            'Period_of_Interest_c',
            'Material_Theme_c',
            "Product",
            "Interest",
            "Account",
            "Contact",
        ]


class InterestSearchSerialiizers(serializers.Serializer):
    searchinterest=serializers.CharField(max_length=100)

class AccountSearchSerializer(serializers.Serializer):
    searchaccount=serializers.CharField(max_length=100)    

class ProductSearchSerializer(serializers.Serializer):
    searchproduct=serializers.CharField(max_length=100)

class ClientInterestSearchSerializer(serializers.Serializer):
    findclient=serializers.CharField(max_length=100)    
    ExactMatch=serializers.CharField(max_length=10,required=False)

# class ClientInterestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Interest_Junction_c
#         fields='__all__'