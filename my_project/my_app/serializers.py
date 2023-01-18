from rest_framework import serializers
from .models import Account,Opportunity,Interest,Product,Interest_Junction_c




class AccountSerializers(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields="__all__"


class InterestSerializers(serializers.ModelSerializer):
    class Meta:
        model=Interest
        fields='__all__'

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=[
            'id',
            'Productid',
            'ProductName',
        ]    

class OpportunitySerializers(serializers.ModelSerializer):
    class Meta:
        model=Opportunity
        fields='__all__'
        
class OpportunitySerializersPost(serializers.ModelSerializer):
    account=AccountSerializers(many=False,write_only=True)
    class Meta:
        model=Opportunity
        fields=[
            'OpportunityId',
            'OpportunityName',
            'StageName',
            'Billing_City',
            'AverageitemSold',
            'account',
        ]
                

class InterestJunctionSerializers(serializers.ModelSerializer):
    Product=ProductSerializers(many=False,read_only=True)
    Interest=InterestSerializers(many=False,read_only=True)
    Account=AccountSerializers(many=False,read_only=True)
    # Contact=ContactSerializers(many=False,read_only=True)
    class Meta:
        model=Interest_Junction_c
        fields=[
            "id",
            "InterestNameJunction",
            "InterestName",
            "InterestJunctionID",
            "link_With",
            "Product",
            "Interest",
            "Account",
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


class SearchallSerializers(serializers.Serializer):
    search=serializers.CharField(max_length=100)



class JunctionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Interest_Junction_c
        fields='__all__'


class BulkProductserializers(serializers.ListSerializer):
    def create(self, validated_data):
        foo=[Product(**item) for item in validated_data]
        return Product.objects.bulk_create(foo)

    class Meta:
        model=Product
        fields=[
            'Productid',
            'ProductName',
        ]    


