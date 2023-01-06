from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from my_app.documents import InterestDocument,AccountDocument,ProductDocument,Interest_Junction_cDocument
from elasticsearch_dsl import Q
from django.http import JsonResponse


# Create your views here.
def test(request):
    return render(request,'my_app/test.html')



###--------------------------save and get account api---------------------------------###

class AccountList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Account.objects.all()
    serializer_class=AccountSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        serializer=AccountSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            q=serializer.data.get('Accountid')
            if Account.objects.filter(Accountid=q).exists():
                return Response({'error':'Accountid already exist !'})
            else:    
                return self.create(request,*args,**kwargs) 

###----------------------------save and get contact api------------------------------------###

class ContactList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Contact.objects.all()
    serializer_class=ContactSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        serializers=ContactSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            q=serializers.data.get('Contactid')
            if Contact.objects.filter(Contactid=q).exists():
                return Response({'error':'Contactid already exist !'})
            else:    
                return self.create(request,*args,**kwargs)         

###--------------------------save and get interest api------------------------------------###

class InterestList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest.objects.all()
    serializer_class=InterestSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        serializers=InterestSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            q=serializers.data.get('InterestID')
            if Interest.objects.filter(InterestID=q).exists():
                return Response({'error':'InterestID already exist !'})
            else:    
                return self.create(request,*args,**kwargs) 

###-----------------------------save and get interest junction api-------------------------------###

class InterestJunctionList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest_Junction_c.objects.all()
    serializer_class=InterestJunctionSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

###------------------------------save and get product api---------------------------------------###

class ProductList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        serializers=ProductSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            q=serializers.data.get('Productid')
            if Product.objects.filter(Productid=q).exists():
                return Response({'error':'Productid already exist !'})
            else:    
                return self.create(request,*args,**kwargs) 



class SearchInterest(APIView):
    def post(self,request,format=None):
        serializer=InterestSerializers(data=request.data)
        serializer2=AccountSerializers(data=request.data)
        if serializer2.is_valid(raise_exception=True):
            accountid=serializer2.data.get('Accountid')
            accountname=serializer2.data.get('AccountName')
            print(accountname,accountid)
            search=InterestDocument.search().filter('fuzzy',InterestID=accountid)
            for x in search:
                print(x.InterestID,x.InterestType,x.InterestName,x.ApprovalStatus)
                interestid=x.InterestID
                interesttype=x.InterestType
                interestname=x.InterestName
                approvalstatus=x.ApprovalStatus
                



        
        return Response([{'messages':'success',
                        'Accountid':accountid,
                        'AccountName':accountname,
                        'Contactid':'Null',
                        'ContactName':'Null',
                        'InterestID':interestid,
                        'InterestName':interestname,
                        'InterestType':interesttype,
                        'ApprovalStatus':approvalstatus
                        }])

####----------------------------------search_interest api---------------------------------------###
from rest_framework.pagination import LimitOffsetPagination

class SearchListInterest(APIView,LimitOffsetPagination):
    def get(self,request,format=None):
        interest=Interest.objects.all()
        serializer=InterestSerializers(interest,many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer=InterestSearchSerialiizers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            datas=serializer.data.get('searchinterest')
            query=datas
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'InterestName',
                    'InterestID',
                    'InterestType'
                ],
                fuzziness='auto')
            # search=InterestDocument.search().filter(Q('fuzzy',InterestID=datas)|Q('fuzzy',InterestType=datas)|Q('fuzzy',InterestName=datas)|Q('term',InterestID=datas)|Q('term',InterestName=datas))
            search=InterestDocument().search().query(q)
            print([data for data in search])
            serial=InterestSerializers(search,many=True)
        return  Response(serial.data)


###---------------------------------search_account api-----------------------------------------###

class SearchListAccount(APIView):
    def get(self,request,format=None):
        account=Account.objects.all()
        serializers=AccountSerializers(account,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        serializers=AccountSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchaccount')
            query=datas
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'AccountName',
                    'Accountid'
                ],
                fuzziness='auto')
            search=AccountDocument().search().query(q)
    
            # search=AccountDocument.search().filter(Q('fuzzy',Accountid=datas)|Q('fuzzy',AccountName=datas))
            print([result for result in search])
            serial=AccountSerializers(search,many=True)
        return Response(serial.data)


###-----------------------------search_product api-----------------------------------------###

class SearchListProduct(APIView):
    def get(self,request,format=None):
        product=Product.objects.all()
        serializers=ProductSerializers(product,many=True)        
        return Response(serializers.data)

    def post(self,request,format=None):
        serializers=ProductSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchproduct')
            query=datas
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'ProductName',
                    'Productid'
                ],
                fuzziness='auto')
            search=ProductDocument().search().query(q)
            # search=ProductDocument.search().filter(Q('fuzzy',Productid=datas)|Q('fuzzy',ProductName=datas))
            print([result for result in search])
            serial=ProductSerializers(search,many=True)
        return Response(serial.data)

###----------------------------------client search interest----------------------------------------###
class SearchClientInterest(APIView):
    def get(self,request,format=None):
        data=Interest_Junction_c.objects.all()
        serializers=InterestJunctionSerializers(data,many=True)
        return Response(serializers.data)
    def post(self,request,format=None):
        serializers= ClientInterestSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('findclient')
            exact=serializers.data.get('ExactMatch')
            query=datas
            if exact=='No' or exact == 'no':
                q = Q(
                'multi_match',
                query=query,
                fields=[
                   'InterestJunctionID',
                        'Category_of_Interest_c',
                        'Maker_Artist_Interest_c',
                        'Period_of_Interest_c',
                        'Material_Theme_c',
                       'Interest.InterestName',
                       'Interest.InterestID',
                       'Interest.InterestType',
                        'Account.AccountName',
                        'Account.Accountid',
                        'Product.ProductName',
                        'Product.Productid',
                        'Contact.ContactName',
                        'Contact.Contactid'
                ],
                fuzziness='auto')
                search=Interest_Junction_cDocument.search().query(q)
                serial=InterestJunctionSerializers(search,many=True)
                return Response(serial.data)
            elif exact == 'Yes' or exact == 'yes':
                p = Q(
                    'multi_match',
                    
                    query=query,
                    fields=[
                        'InterestJunctionID',
                        'Category_of_Interest_c',
                        'Maker_Artist_Interest_c',
                        'Period_of_Interest_c',
                        'Material_Theme_c',
                       'Interest.InterestName',
                       'Interest.InterestID',
                       'Interest.InterestType',
                        'Account.AccountName',
                        'Account.Accountid',
                        'Product.ProductName',
                        'Product.Productid',
                        'Contact.ContactName',
                        'Contact.Contactid'
                    ],
                    )
                search=Interest_Junction_cDocument.search().query(p)
                serial=InterestJunctionSerializers(search,many=True)
                return Response(serial.data)
            else:
                return Response({'Error':'Please choose Yes or No only !'})
                






###----------------------------------client search account-----------------------------------------###