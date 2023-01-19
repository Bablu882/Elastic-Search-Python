from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
# from my_app.documents import InterestDocument,AccountDocument,ProductDocument,Interest_Junction_cDocument
from elasticsearch_dsl import Q
from django.http import JsonResponse
from rest_framework import status


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
        return self.create(request,*args,**kwargs) 

###----------------------------save and get contact api------------------------------------###

# class ContactList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset=Contact.objects.all()
#     serializer_class=ContactSerializers

#     def get(self,request,*args,**kwargs):
#         return self.list(request,*args,**kwargs)

#     def post(self,request,*args,**kwargs):
#         serializers=ContactSerializers(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             q=serializers.data.get('Contactid')
#             if Contact.objects.filter(Contactid=q).exists():
#                 return Response({'error':'Contactid already exist !'})
#             else:    
#                 return self.create(request,*args,**kwargs)         

# ###--------------------------save and get interest api------------------------------------###

class InterestList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest.objects.all()
    serializer_class=InterestSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###-----------------------------save and get interest junction api-------------------------------###

class InterestJunctionList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest_Junction_c.objects.all()
    serializer_class=JunctionSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###------------------------------save and get product api---------------------------------------###

class ProductList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        # serializers=ProductSerializers(data=request.data)
        # if serializers.is_valid(raise_exception=True):
        return self.create(request,*args,**kwargs) 



# class SearchInterest(APIView):
#     def post(self,request,format=None):
#         serializer=InterestSerializers(data=request.data)
#         serializer2=AccountSerializers(data=request.data)
#         if serializer2.is_valid(raise_exception=True):
#             accountid=serializer2.data.get('Accountid')
#             accountname=serializer2.data.get('AccountName')
#             print(accountname,accountid)
#             search=InterestDocument.search().filter('fuzzy',InterestID=accountid)
#             for x in search:
#                 print(x.InterestID,x.InterestType,x.InterestName,x.ApprovalStatus)
#                 interestid=x.InterestID
#                 interesttype=x.InterestType
#                 interestname=x.InterestName
#                 approvalstatus=x.ApprovalStatus
                



        
#         return Response([{'messages':'success',
#                         'Accountid':accountid,
#                         'AccountName':accountname,
#                         'Contactid':'Null',
#                         'ContactName':'Null',
#                         'InterestID':interestid,
#                         'InterestName':interestname,
#                         'InterestType':interesttype,
#                         'ApprovalStatus':approvalstatus
#                         }])

# ####----------------------------------search_interest api---------------------------------------###
# from rest_framework.pagination import LimitOffsetPagination

# class SearchListInterest(APIView,LimitOffsetPagination):
#     def get(self,request,format=None):
#         interest=Interest.objects.all()
#         serializer=InterestSerializers(interest,many=True)
#         return Response(serializer.data)

#     def post(self,request,format=None):
#         serializer=InterestSearchSerialiizers(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             datas=serializer.data.get('searchinterest')
#             query=datas
#             q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'InterestName',
#                     'InterestID',
#                     'InterestType'
#                 ],
#                 fuzziness='auto')
#             # search=InterestDocument.search().filter(Q('fuzzy',InterestID=datas)|Q('fuzzy',InterestType=datas)|Q('fuzzy',InterestName=datas)|Q('term',InterestID=datas)|Q('term',InterestName=datas))
#             search=InterestDocument().search().query(q)
#             print([data for data in search])
#             serial=InterestSerializers(search,many=True)
#         return  Response(serial.data)


# ###---------------------------------search_account api-----------------------------------------###

# class SearchListAccount(APIView):
#     def get(self,request,format=None):
#         account=Account.objects.all()
#         serializers=AccountSerializers(account,many=True)
#         return Response(serializers.data)

#     def post(self,request,format=None):
#         serializers=AccountSearchSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             datas=serializers.data.get('searchaccount')
#             query=datas
#             q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'AccountName',
#                     'Accountid'
#                 ],
#                 fuzziness='auto')
#             search=AccountDocument().search().query(q)
    
#             # search=AccountDocument.search().filter(Q('fuzzy',Accountid=datas)|Q('fuzzy',AccountName=datas))
#             print([result for result in search])
#             serial=AccountSerializers(search,many=True)
#         return Response(serial.data)


# ###-----------------------------search_product api-----------------------------------------###

# class SearchListProduct(APIView):
#     def get(self,request,format=None):
#         product=Product.objects.all()
#         serializers=ProductSerializers(product,many=True)        
#         return Response(serializers.data)

#     def post(self,request,format=None):
#         serializers=ProductSearchSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             datas=serializers.data.get('searchproduct')
#             query=datas
#             q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'ProductName',
#                     'Productid'
#                 ],
#                 fuzziness='auto')
#             search=ProductDocument().search().query(q)
#             # search=ProductDocument.search().filter(Q('fuzzy',Productid=datas)|Q('fuzzy',ProductName=datas))
#             print([result for result in search])
#             serial=ProductSerializers(search,many=True)
#         return Response(serial.data)

# ###-----------------------------find client search interest junction--------------------###
# class SearchClientInterest(APIView):
#     def get(self,request,format=None):
#         data=Interest_Junction_c.objects.all()
#         serializers=InterestJunctionSerializers(data,many=True)
#         return Response(serializers.data)
#     def post(self,request,format=None):
#         serializers= ClientInterestSearchSerializer(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#             datas=serializers.data.get('findclient')
#             exact=serializers.data.get('ExactMatch')
#             query=datas
#             if exact=='No' or exact == 'no':
#                 q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                    'InterestJunctionID',
#                         'Category_of_Interest_c',
#                         'Maker_Artist_Interest_c',
#                         'Period_of_Interest_c',
#                         'Material_Theme_c',
#                        'Interest.InterestName',
#                        'Interest.InterestID',
#                        'Interest.InterestType',
#                         'Account.AccountName',
#                         'Account.Accountid',
#                         'Product.ProductName',
#                         'Product.Productid',
#                         'Contact.ContactName',
#                         'Contact.Contactid'
#                 ],
#                 fuzziness='auto')
#                 search=Interest_Junction_cDocument.search().query(q)
#                 serial=InterestJunctionSerializers(search,many=True)
#                 return Response(serial.data)
#             elif exact == 'Yes' or exact == 'yes':
#                 p = Q(
#                     'multi_match',
                    
#                     query=query,
#                     fields=[
#                         'InterestJunctionID',
#                         'Category_of_Interest_c',
#                         'Maker_Artist_Interest_c',
#                         'Period_of_Interest_c',
#                         'Material_Theme_c',
#                        'Interest.InterestName',
#                        'Interest.InterestID',
#                        'Interest.InterestType',
#                         'Account.AccountName',
#                         'Account.Accountid',
#                         'Product.ProductName',
#                         'Product.Productid',
#                         'Contact.ContactName',
#                         'Contact.Contactid'
#                     ],
#                     )
#                 search=Interest_Junction_cDocument.search().query(p)
#                 serial=InterestJunctionSerializers(search,many=True)
#                 return Response(serial.data)
#             else:
#                 return Response({'Error':'Please choose Yes or No only !'})
                






# ###----------------------------client search all in single api------------------------------###

# class SearchAllApi(APIView):
#     def get(self,request,format=None):
#         interest=Interest.objects.all()
#         account=Account.objects.all()
#         product=Product.objects.all()
#         serializers1=InterestSerializers(interest,many=True)
#         serializers2=AccountSerializers(account,many=True)
#         serializers3=ProductSerializers(product,many=True)
#         return Response({"interest":serializers1.data,"account":serializers2.data,"product":serializers3.data})
#     def post(self,request,format=None):
#         serializers=SearchallSerializers(data=request.data)
#         if serializers.is_valid():
#             datas=serializers.data.get('search')
#             query=datas
#             q = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'ProductName',
#                     'Productid'
#                 ],
#                 fuzziness='auto')
#             q1 = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'InterestName',
#                     'Interestid',
#                     'InterestType',
#                     'ApprovalStatus'
#                 ],
#                 fuzziness='auto')
#             q2 = Q(
#                 'multi_match',
#                 query=query,
#                 fields=[
#                     'AccountName',
#                     'Accountid'
#                 ],
#                 fuzziness='auto')
#             interest=InterestDocument.search().query(q1)            
#             product=ProductDocument.search().query(q)
#             account=AccountDocument().search().query(q2)
#             interestserial=InterestSerializers(interest,many=True)
#             productserial=ProductSerializers(product,many=True)
#             accountserial=AccountSerializers(account,many=True)
#             return Response({"interest":interestserial.data,
#             "product":productserial.data,
#             "account":accountserial.data})


class OpportunityList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Opportunity.objects.all()
    serializer_class=OpportunitySerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):

        return self.create(request,*args,**kwargs) 



###--------------------------------------------------------------------------------####

from rest_framework import viewsets

class AccountView(viewsets.ModelViewSet):
    queryset=Account.objects.all()
    serializer_class=AccountSerializers
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = AccountSerializers(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = ProductSerializers(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class InterestView(viewsets.ModelViewSet):
    queryset=Interest.objects.all()    
    serializer_class=InterestSerializers
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = InterestSerializers(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Interest_Junction_cView(viewsets.ModelViewSet):
    queryset=Interest_Junction_c.objects.all()
    serializer_class=JunctionSerializers 
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = JunctionSerializers(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)  

class OpportunityView(viewsets.ModelViewSet):
    queryset=Opportunity.objects.all()     
    serializer_class=OpportunitySerializers
    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = OpportunitySerializersPost(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

###---------------------------------------------------------------------------------###

# class Productapi(APIView):
#     def get(self,request,format=None):
#         product=Product.objects.all()
#         serializers=ProductSerializers(product,many=True)    
#         return Response(serializers.data)

#     def post(self,request,format=None):
#         serializers=ProductSerializers(data=request.data)
#         if serializers.is_valid(raise_exception=True):
#                 serializers.save()   
#                 return Response({'msg':'ok'})

# class CreatListMixin:
#     def get_serializer(self,*args,**kwargs):
#         if isinstance(kwargs.get('data',{}),list):
#             kwargs['many']=True
#         return super().get_serializer(*args,**kwargs)    


# class ApiProduct(viewsets.ModelViewSet):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializers

#     def get_serializer(self, *args, **kwargs):
#         # add many=True if the data is of type list
#         if isinstance(kwargs.get("data", {}), list):
#             kwargs["many"] = True

#         return super(ApiProduct, self).get_serializer(*args, **kwargs)
# from rest_framework import status

# class MyViewSet(viewsets.ModelViewSet):

#     serializer_class = ProductSerializers
#     model = Product
#     queryset = Product.objects.all()

#     def create(self, request, *args, **kwargs):
#         many = True if isinstance(request.data, list) else False
#         serializer = ProductSerializers(data=request.data, many=many)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductApiVIew(APIView):
    def get(self,request,format=None):
        product=Product.objects.all()
        serializers=ProductSerializers(product,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        print(data)  
        for dicts in data:
            print(dicts)
            productid=dicts['Productid']
            print(productid)
            productname=dicts['ProductName']
            print(productname)
            if Product.objects.filter(Productid=productid).exists():
                print('existerror')
                gets=Product.objects.get(Productid=productid)
                gets.ProductName=productname
                gets.save()
            else:
                prod=Product.objects.create(Productid=productid,ProductName=productname)    
        return Response({'msg':'product created or updated success !'})        



class AccountApiVIew(APIView):
    def get(self,request,format=None):
        product=Account.objects.all()
        serializers=AccountSerializers(product,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        print(data)  
        for dicts in data:
            print(dicts)
            accountid=dicts['Accountid']
            accountname=dicts['AccountName']
            state=dicts['State']
            lastpuchasedate=dicts['LastPurchasedDtae']
            totalpurchase=dicts['TotalPurchase']
            personhasoptedemail=dicts['PersonHasOptedOutOfEmail']
            categoryofinterest=dicts['CategoryOfInterest']
            periodofinterest=dicts['PeriodOfInterest']
            typeofinterest=dicts['TypeOfInterest']
            youngeraudience=dicts['YoungerAudience']
            star5=dicts['Star5']
            accountlastpurchasedate=dicts['AccountLastPurchaseDate']
            holidaycelebrated=dicts['HolidayCelebrated']
            email=dicts['Email']
            shippingcity=dicts['ShippingCity']
            findclientvisible=dicts['FindClients_visible']
            if Account.objects.filter(Accountid=accountid).exists():
                print('existerror')
                gets=Account.objects.get(Accountid=accountid)
                gets.AccountName=accountname
                gets.State=state
                gets.LastPurchasedDtae=lastpuchasedate
                gets.TotalPurchase=totalpurchase
                gets.PersonHasOptedOutOfEmail=personhasoptedemail
                gets.CategoryOfInterest=categoryofinterest
                gets.PeriodOfInterest=periodofinterest
                gets.TypeOfInterest=typeofinterest
                gets.YoungerAudience=youngeraudience
                gets.Star5=star5
                gets.AccountLastPurchaseDate=accountlastpurchasedate
                gets.HolidayCelebrated=holidaycelebrated
                gets.Email=email
                gets.ShippingCity=shippingcity
                gets.FindClients_visible=findclientvisible
                gets.save()
            else:
                prod=Account.objects.create(
                    Accountid=accountid,
                    AccountName=accountname,
                    State=state,
                    LastPurchasedDtae=lastpuchasedate,
                    TotalPurchase=totalpurchase,
                    PersonHasOptedOutOfEmail=personhasoptedemail,
                    CategoryOfInterest=categoryofinterest,
                    PeriodOfInterest=periodofinterest,
                    TypeOfInterest=typeofinterest,
                    YoungerAudience=youngeraudience,
                    Star5=star5,
                    AccountLastPurchaseDate=accountlastpurchasedate,
                    HolidayCelebrated=holidaycelebrated,
                    Email=email,
                    ShippingCity=shippingcity,
                    FindClients_visible=findclientvisible
                )    
        return Response({'msg':'account created or updated success !'})        


class InterestApiVIew(APIView):
    def get(self,request,format=None):
        interest=Interest.objects.all()
        serializers=InterestSerializers(interest,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        print(data)  
        for dicts in data:
            print(dicts)

            Interestid=dicts['InterestID']
            interestname=dicts['InterestName']
            approvalstatus=dicts['ApprovalStatus']
            if Interest.objects.filter(InterestID=Interestid).exists():
                print('existerror')
                gets=Interest.objects.get(InterestID=Interestid)
                gets.InterestName=interestname
                gets.ApprovalStatus=approvalstatus
                gets.save()
            else:
                prod=Interest.objects.create(InterestID=Interestid,
                InterestName=interestname,
                ApprovalStatus=approvalstatus)    
        return Response({'msg':'interest created or updated success !'})        


class OpportunityApiVIew(APIView):
    def get(self,request,format=None):
        opp=Opportunity.objects.all()
        serializers=OpportunitySerializers(opp,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        print(data)  
        for dicts in data:
            print(dicts)
            opportunityid=dicts['OpportunityId']
            opportunityname=dicts['OpportunityName']
            stagename=dicts['StageName']
            billingcity=dicts['Billing_City']
            avarageitemsold=dicts['AverageitemSold']
            accountid=dicts['AccountId']

            if Opportunity.objects.filter(OpportunityId=opportunityid).exists():
                if not accountid:
                    gets=Opportunity.objects.get(OpportunityId=opportunityid)
                    gets.OpportunityName=opportunityname
                    gets.StageName=stagename
                    gets.Billing_City=billingcity
                    gets.AverageitemSold=avarageitemsold
                    gets.AccountId=None
                    gets.save()
                else:
                    if not Account.objects.filter(Accountid=accountid).exists():
                        return Response({"error":"Accountid does not exists in Account table ",'Accountid':accountid,'Opportunityid':opportunityid})
                    insta=Account.objects.get(Accountid=accountid)
                    gets=Opportunity.objects.get(OpportunityId=opportunityid)
                    gets.OpportunityName=opportunityname
                    gets.StageName=stagename
                    gets.Billing_City=billingcity
                    gets.AverageitemSold=avarageitemsold
                    gets.AccountId=insta
                    gets.save()   
            else:
                if not accountid:
                    prod=Opportunity.objects.create(
                        OpportunityId=opportunityid,
                        OpportunityName=opportunityname,
                        StageName=stagename,
                        Billing_City=billingcity,
                        AverageitemSold=avarageitemsold,
                    )   
                else:
                    if not Account.objects.filter(Accountid=accountid).exists():     
                        return Response({"error":"Accountid does not exists in Account table ",'Accountid':accountid,'Opportunityid':opportunityid})
                    else:
                        accou=Account.objects.get(Accountid=accountid)
                        prod=Opportunity.objects.create(
                        OpportunityId=opportunityid,
                        OpportunityName=opportunityname,
                        StageName=stagename,
                        Billing_City=billingcity,
                        AverageitemSold=avarageitemsold,
                        AccountId=accou
                    ) 
        return Response({'msg':'product created or updated success !'})        

