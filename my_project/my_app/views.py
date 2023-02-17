from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from my_app.documents import AccountDocument,ProductDocument,InterestDocument,Interest_Junction_cDocument,OpportunityDocument
from elasticsearch_dsl import Q
from django.http import JsonResponse
from rest_framework import status
import json
from functools import reduce
from operator import and_ ,or_      
from elasticsearch import Elasticsearch

# Testing
def test(request):
    return render(request,'my_app/test.html')



###--------------------------SAVE AND GET ACCOUNT API---------------------------------###

class AccountList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Account.objects.all()
    serializer_class=AccountSerializers

    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)

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

# ###--------------------------SAVE AND GET INTEREST------------------------------------###

class InterestList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest.objects.all()
    serializer_class=InterestSerializers

    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###-----------------------------SAVE AND GET INTEREST JUNCTION API-------------------------------###

class InterestJunctionList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest_Junction_c.objects.all()
    serializer_class=JunctionSerializers

    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###------------------------------SAVE AND GET PRODUCT API---------------------------------------###

class ProductList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 



# ####----------------------------------SEARCH INTEREST API---------------------------------------###
from rest_framework.pagination import LimitOffsetPagination

class SearchListInterest(APIView,LimitOffsetPagination):
    # def get(self,request,format=None):
    #     interest=Interest.objects.all()
    #     serializer=InterestSerializers(interest,many=True)
    #     return Response(serializer.data)

    def post(self,request,format=None):
        serializer=InterestSearchSerialiizers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            datas=serializer.data.get('searchinterest')
            query=datas
            #making query for fuzzy search in elasticsearch 
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'InterestName',
                    'InterestID',
                ],
                fuzziness='auto')
            #search the fields in InterestDocument in elasticsearch 
            search=InterestDocument().search().query(q)
            print([data for data in search])
            serial=InterestSerializers(search,many=True)
        return  Response(serial.data)


# ###---------------------------------SEARCH ACCOUNT API-----------------------------------------###

class SearchListAccount(APIView):
    # def get(self,request,format=None):
    #     account=Account.objects.all()
    #     serializers=AccountSerializers(account,many=True)
    #     return Response(serializers.data)

    def post(self,request,format=None):
        serializers=AccountSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchaccount')
            query=datas
            #making query for account search in account document for fuzzy match
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'Accountid',
                    'AccountName',
                    'State',
                    'LastPurchasedDate',
                    'TotalPurchase',
                    'PersonHasOptedOutOfEmail',
                    'CategoryOfInterest',
                    'PeriodOfInterest',
                    'TypeOfInterest',
                    'YoungerAudience',
                    'Star5',
                    'AccountLastPurchaseDate',
                    'HolidayCelebrated',
                    'Email',
                    'ShippingCity',
                    'FindClients_visible'
                ],
                fuzziness='auto')
            #search above fields in account documents in elasticsearch
            search=AccountDocument().search().query(q)
            print([result for result in search])
            serial=AccountSerializers(search,many=True)
        return Response(serial.data)


# ###-----------------------------SEARCH PRODUCT API-----------------------------------------###

class SearchListProduct(APIView):
    # def get(self,request,format=None):
    #     product=Product.objects.all()
    #     serializers=ProductSerializers(product,many=True)        
    #     return Response(serializers.data)

    def post(self,request,format=None):
        serializers=ProductSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchproduct')
            query=datas
            #making query for fuzzy match
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'ProductName',
                    'Productid'
                ],
                fuzziness='auto')
            #searching above query in product document in elsticsearch
            search=ProductDocument().search().query(q)
            print([result for result in search])
            serial=ProductSerializers(search,many=True)
        return Response(serial.data)

###---------------------------OPPORTUNITY SEARCH API---------------------------------------###

class SearchListOpportunity(APIView):
    # def get(self,request,format=None):
    #     opportunity=Opportunity.objects.all()
    #     serializers=OpportunitySerializers(opportunity,many=True)        
    #     return Response(serializers.data)

    def post(self,request,format=None):
        serializers=OpportunitySearchSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchopportunity')
            query=datas
            #making quries for opportunity fields and account fields ,opportunity has foreign key relation of account
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'OpportunityId',
                    'OpportunityName',
                    'StageName',
                    'Billing_City',
                    'AverageitemSold',
                    'AccountId.Accountid',
                    'AccountId.AccountName',
                    'AccountId.State',
                    'AccountId.LastPurchasedDate',
                    'AccountId.TotalPurchase',
                    'AccountId.PersonHasOptedOutOfEmail',
                    'AccountId.CategoryOfInterest',
                    'AccountId.PeriodOfInterest',
                    'AccountId.TypeOfInterest',
                    'AccountId.YoungerAudience',
                    'AccountId.Star5',
                    'AccountId.AccountLastPurchaseDate',
                    'AccountId.HolidayCelebrated',
                    'AccountId.Email',
                    'AccountId.ShippingCity',
                    'AccountId.FindClients_visible'
                ],
                fuzziness='auto')
            #search above query in Opportunity documents in elasticsearch    
            search=OpportunityDocument().search().query(q)
            serial=OpportunitySerializersPost(search,many=True)
        return Response(serial.data) 


# ###-----------------------------SEARCH INTEREST JUNCTION API ---------------------------------###
class SearchInterestJunction(APIView):
    # def get(self,request,format=None):
    #     data=Interest_Junction_c.objects.all()
    #     serializers=InterestJunctionSerializers(data,many=True)
    #     return Response(serializers.data)
    def post(self,request,format=None):
        serializers= ClientInterestSearchSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('JunctionField')
            exact=serializers.data.get('ExactMatch')
            query=datas
            if exact=='No' or exact == 'no':
                q = Q(
                'multi_match',
                query=query,
                #making query for fuzzy match to all fields in interestjunctuion,account,interest,product
                fields=[
                   'InterestJunctionID',
                        'InterestNameJunction',
                        'InterestName',
                        'link_With',
                        'InterestType',
                       'Interest.InterestName',
                       'Interest.InterestID',
                        'Account.AccountName',
                        'Account.Accountid',
                        'Account.State',
                        'Account.LastPurchasedDate',
                        'Account.TotalPurchase',
                        'Account.PersonHasOptedOutOfEmail',
                        'Account.CategoryOfInterest',
                        'Account.PeriodOfInterest',
                        'Account.TypeOfInterest',
                        'Account.YoungerAudience',
                        'Account.Star5',
                        'Account.AccountLastPurchaseDate',
                        'Account.HolidayCelebrated',
                        'Account.Email',
                        'Account.ShippingCity',
                        'Account.FindClients_visible',
                        'Product.ProductName',
                        'Product.Productid',
                        
                ],fuzziness='auto')
                #search above query in elasticsearch in Interest junction documents
                search=Interest_Junction_cDocument.search().query(q)
                serial=InterestJunctionFindClientSerializers(search,many=True)
                return Response(serial.data)
            elif exact == 'Yes' or exact == 'yes':
                p = Q(
                    'multi_match',
                    
                    query=query,
                    fields=[
                       'InterestNameJunction',
                        'InterestName',
                        'InterestJunctionID',
                        'link_With',
                        'InterestType',
                       'Interest.InterestName',
                       'Interest.InterestID',
                       'Interest.InterestType',
                        'Account.AccountName',
                        'Account.Accountid',
                        'Account.State',
                        'Account.LastPurchasedDate',
                        'Account.TotalPurchase',
                        'Account.PersonHasOptedOutOfEmail',
                        'Account.CategoryOfInterest',
                        'Account.PeriodOfInterest',
                        'Account.TypeOfInterest',
                        'Account.YoungerAudience',
                        'Account.Star5',
                        'Account.AccountLastPurchaseDate',
                        'Account.HolidayCelebrated',
                        'Account.Email',
                        'Account.ShippingCity',
                        'Account.FindClients_visible',
                        'Product.ProductName',
                        'Product.Productid',
                        
                    ],
                    )
                #making query for fuzzy match to all fields in interestjunctuion,account,interest,product
                search=Interest_Junction_cDocument.search().query(p)
                serial=InterestJunctionFindClientSerializers(search,many=True)
                return Response(serial.data)
            else:
                return Response({'Error':'Please choose Yes or No only !'})
                


###------------------------SAVE AND GET OPPORTUNITY API------------------------------------###

class OpportunityList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Opportunity.objects.all()
    serializer_class=OpportunitySerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):

        return self.create(request,*args,**kwargs) 



###-------------------------------------CREATE SINGLE API -------------------------------------------####
## Currently these section of apis is not working 
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

###---------------------------------PRODUCT BULK SAVE API-----------------------------------###
from django.core.paginator import Paginator

class ProductApiVIew(APIView):
    PAGE_SIZE=1000
    def get(self,request,format=None):
        page_num=request.query_params.get('page',1)
        product=Product.objects.all()
        paginator=Paginator(product,self.PAGE_SIZE)
        page=paginator.get_page(page_num)
        serializers=ProductSerializers(page,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            productid=dicts['Productid']
            productname=dicts['ProductName']
            #check if Product is exists in database then update
            if Product.objects.filter(Productid=productid).exists():
                gets=Product.objects.get(Productid=productid)
                gets.ProductName=productname
                gets.save()
                update.append(str(gets))
            else:
                prod=Product.objects.create(Productid=productid,ProductName=productname)
                create.append(str(prod))
                #if product is not exist in database then created new

        return Response({'Product updated !':'success','Product created !':'success'})        

###----------------------------------------ACCOUNT BULK SAVE API-------------------------------###

class AccountApiVIew(APIView):
    def get(self,request,format=None):
        product=Account.objects.all()
        serializers=AccountSerializers(product,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            accountid=dicts['Accountid']
            accountname=dicts['AccountName']
            state=dicts['State']
            lastpuchasedate=dicts['LastPurchasedDate']
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
            #check if account is exists in database then update it 
            if Account.objects.filter(Accountid=accountid).exists():
                gets=Account.objects.get(Accountid=accountid)
                gets.AccountName=accountname
                gets.State=state
                gets.LastPurchasedDate=lastpuchasedate
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
                update.append(str(gets))
            else:
                prod=Account.objects.create(
                    Accountid=accountid,
                    AccountName=accountname,
                    State=state,
                    LastPurchasedDate=lastpuchasedate,
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
                create.append(str(prod))
                #if account is not exists in database then created new   
        return Response({'Account updated !':'success','Account created !':'success'})        

###-------------------------------------INTEREST BULK SAVE API--------------------------------###

class InterestApiVIew(APIView):
    def get(self,request,format=None):
        interest=Interest.objects.all()
        serializers=InterestSerializers(interest,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            Interestid=dicts['InterestID']
            interestname=dicts['InterestName']
            approvalstatus=dicts['ApprovalStatus']
            #check if interest is exists in database then update it
            if Interest.objects.filter(InterestID=Interestid).exists():
                gets=Interest.objects.get(InterestID=Interestid)
                gets.InterestName=interestname
                gets.ApprovalStatus=approvalstatus
                gets.save()
                update.append(str(gets))
            else:
                prod=Interest.objects.create(InterestID=Interestid,
                InterestName=interestname,
                ApprovalStatus=approvalstatus,
                )
                create.append(str(prod)) 
                #if interest is not exists in the database then create new    
        return Response({'Interest updated !':'success','Interest created !':'success'})        

###--------------------------------------OPPORTUNITY BULK SAVE API-------------------------------###

class OpportunityApiVIew(APIView):
    def get(self,request,format=None):
        opp=Opportunity.objects.all()
        serializers=OpportunitySerializers(opp,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            opportunityid=dicts['OpportunityId']
            opportunityname=dicts['OpportunityName']
            stagename=dicts['StageName']
            billingcity=dicts['Billing_City']
            avarageitemsold=dicts['AverageitemSold']
            accountid=dicts['AccountId']
            #check if opportunity is exists in the database then update and manage account id given or not 
            if Opportunity.objects.filter(OpportunityId=opportunityid).exists():
                if not accountid:
                    gets=Opportunity.objects.get(OpportunityId=opportunityid)
                    gets.OpportunityName=opportunityname
                    gets.StageName=stagename
                    gets.Billing_City=billingcity
                    gets.AverageitemSold=avarageitemsold
                    gets.AccountId=None
                    gets.save()
                    update.append(str(gets))
                else:
                    #check account id in database that is exists or not
                    if not Account.objects.filter(Accountid=accountid).exists():
                        fail=({"Failed to update !":"Accountid does not exists in Account table ",'Accountid':accountid,'Opportunityid':opportunityid})
                        failed.append(fail)
                    else:    
                        insta=Account.objects.get(Accountid=accountid)
                        gets=Opportunity.objects.get(OpportunityId=opportunityid)
                        gets.OpportunityName=opportunityname
                        gets.StageName=stagename
                        gets.Billing_City=billingcity
                        gets.AverageitemSold=avarageitemsold
                        gets.AccountId=insta
                        gets.save() 
                        update.append(str(gets))  
            else:
                if not accountid:
                    prod=Opportunity.objects.create(
                        OpportunityId=opportunityid,
                        OpportunityName=opportunityname,
                        StageName=stagename,
                        Billing_City=billingcity,
                        AverageitemSold=avarageitemsold,
                    )  
                    create.append(str(prod)) 
                else:
                    if not Account.objects.filter(Accountid=accountid).exists():     
                        fail=({"Failed to create !":"Accountid does not exists in Account table ",'Accountid':accountid,'Opportunityid':opportunityid})
                        failed.append(fail)
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
                        create.append(str(prod))
                        #if not exists in the database then cteated new 
        return Response({'Opportunity updated !':'success','Opportunity created !':'success','Opportunity failed':failed}) 

###------------------------------INTEREST JUNCTION BULK SAVE API--------------------------------###

class InterstJunctionApiVIew(APIView):
    def get(self,request,format=None):
        opp=Interest_Junction_c.objects.all()
        serializers=InterestJunctionSerializers(opp,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            interestjunctionid=dicts['InterestJunctionID']
            linkwith=dicts['link_With']
            account=dicts['Account']
            interest=dicts['Interest']
            product=dicts['Product']
            interestnamejunction=dicts['InterestNameJunction']
            interestname=dicts['InterestName']
            interesttype=dicts['InterestType']
            #check interest junction is exists in the database then update 
            if Interest_Junction_c.objects.filter(InterestJunctionID=interestjunctionid).exists():
                #check link with account or product and also check that is exist in database or not 
                if linkwith == 'Account' and not interest:
                    if not Account.objects.filter(Accountid=account).exists():
                        fail0=({'Failed to update !':'Account object does not exist in account','Accountid':account,'InterestJunctionID':interestjunctionid})
                        failed.append(fail0)
                    else:
                        accou=Account.objects.get(Accountid=account)    
                        gets=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                        gets.link_With=linkwith
                        gets.InterestNameJunction=interestnamejunction
                        gets.InterestName=interestname
                        gets.InterestType=interesttype
                        gets.Account=accou
                        gets.Product=None
                        gets.Interest=None
                        gets.save()
                        update.append(str(gets))
                elif linkwith == 'Account' and interest:
                    if not Account.objects.filter(Accountid=account).exists():
                        fail1=({'Failed to update !':'Account object does not exist in account','Accountid':account,'InterestJunctionID':interestjunctionid})
                        failed.append(fail1)
                    elif not Interest.objects.filter(InterestID=interest).exists():
                        fail2=({'Failed to update !':'Interest object does not exists in interest','InterestID':interest,'InterestJunctionID':interestjunctionid})    
                        failed.append(fail2)
                    else:
                        accou=Account.objects.get(Accountid=account) 
                        intre=Interest.objects.get(InterestID=interest)   
                        gets1=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                        gets1.link_With=linkwith
                        gets1.InterestNameJunction=interestnamejunction
                        gets1.InterestName=interestname
                        gets1.InterestType=interesttype
                        gets1.Account=accou
                        gets1.Product=None
                        gets1.Interest=intre
                        gets1.save()
                        update.append(str(gets1))        
                elif linkwith == 'Product' and not interest:
                    if not Product.objects.filter(Productid=product).exists():
                        fail3=({'Failed to update !':'Product object does not exist in product','Productid':product,'InterestJunctionID':interestjunctionid})
                        failed.append(fail3)
                    else:
                        prod1=Product.objects.get(Productid=product)    
                        gets2=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                        gets2.link_With=linkwith
                        gets2.InterestNameJunction=interestnamejunction
                        gets2.InterestName=interestname
                        gets2.InterestType=interesttype
                        gets2.Account=None
                        gets2.Product=prod1
                        gets2.Interest=None
                        gets2.save()
                        update.append(str(gets2))        
                else:
                    if not Product.objects.filter(Productid=product).exists():
                        fail4=({"Failed to update !":"Product object does not exists in product",'Productid':product,'InterestJunctionID':interest})
                        failed.append(fail4)                    
                    elif not Interest.objects.filter(InterestID=interest).exists():     
                        fail5=({"Failed to update !":"Interst objects does not exists in interest",'Interestid':interest,'InterestJunctionID':interestjunctionid})   
                        failed.append(fail5)
                    else:
                        prod3=Product.objects.get(Productid=product)    
                        intr3=Interest.objects.get(InterestID=interest)
                        gets3=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                        gets3.link_With=linkwith
                        gets3.InterestNameJunction=interestnamejunction
                        gets3.InterestName=interestname
                        gets3.InterestType=interesttype
                        gets3.Account=None
                        gets3.Product=prod3
                        gets3.Interest=intr3  
                        gets3.save()
                        update.append(str(gets3)) 
            else:
                #if interst junction is not exists in database then create new with check account and interest and product
                if linkwith == 'Account' and  not interest:
                    if not Account.objects.filter(Accountid=account).exists():
                        fail6=({'Failed to Create !':'Account object does not exists in account','Accountid':account,'InterestJunctionID':interestjunctionid})
                        failed.append(fail6)
                    else:
                        getaccou=Account.objects.get(Accountid=account)
                        produc=Interest_Junction_c.objects.create(
                            InterestJunctionID=interestjunctionid,
                            link_With=linkwith,
                            InterestNameJunction=interestnamejunction,
                            InterestName=interestname,
                            InterestType=interesttype,
                            Account=getaccou
                            )
                        create.append(str(produc))
                elif linkwith == 'Account' and interest:
                    if not Account.objects.filter(Accountid=account).exists():
                        fail7=({'Failed to create !':'Account object does not exists in account','Accountid':account,'InterestJunctionID':interestjunctionid})
                        failed.append(fail7)
                    elif not Interest.objects.filter(InterestID=interest).exists():
                        fail8=({'Failed to create !':'Interest object does not exists in interest','InterestID':interest,'InterestJunctionID':interestjunctionid})    
                        failed.append(fail8)
                    else:
                        getaccou1=Account.objects.get(Accountid=account)
                        getintere1=Interest.objects.get(InterestID=interest)
                        produc1=Interest_Junction_c.objects.create(
                            InterestJunctionID=interestjunctionid,
                            link_With=linkwith,
                            InterestNameJunction=interestnamejunction,
                            InterestName=interestname,
                            InterestType=interesttype,
                            Interest=getintere1,
                            Account=getaccou1
                            )
                        create.append(str(produc1)) 
                elif linkwith == 'Product' and  not interest:
                    if not Product.objects.filter(Productid=product).exists():
                        fail9=({'Failed to create !':'Product object does not exists in product','Productid':product,'InterestJunctionID':interestjunctionid})
                        failed.append(fail9)
                    else:
                        getprod11=Product.objects.get(Productid=product)
                        produc11=Interest_Junction_c.objects.create(
                            InterestJunctionID=interestjunctionid,
                            link_With=linkwith,
                            InterestNameJunction=interestnamejunction,
                            InterestName=interestname,
                            InterestType=interesttype,
                            Product=getprod11
                            )
                        create.append(str(produc11))                        
                else:
                    if not Product.objects.filter(Productid=product).exists():
                        fail10=({'Failed to create !':'Product object does not exists in product','Productid':product,'InterestJunctionID':interestjunctionid})
                        failed.append(fail10)
                    elif not Interest.objects.filter(InterestID=interest).exists():
                        fail11=({'Failed to create !':'Interest object does not exists in interest','InterestID':interest,'InterestJunctionID':interestjunctionid})    
                        failed.append(fail11)
                    else:
                        getprod22=Product.objects.get(Productid=product)
                        getintere22=Interest.objects.get(InterestID=interest)
                        produc22=Interest_Junction_c.objects.create(
                            InterestJunctionID=interestjunctionid,
                            link_With=linkwith,
                            InterestNameJunction=interestnamejunction,
                            InterestName=interestname,
                            InterestType=interesttype,
                            Interest=getintere22,
                            Product=getprod22
                            )
                        create.append(str(produc22)) 
        return Response({'InterestJunction updated !':'success','InterestJunction created':'success','InterestJunction failed':failed}) 



###--------------------------------------ACCOUNT BULK DELETE API---------------------------------###

class AccountDelete(APIView):
    def get(self,request,format=None):
        get=Account.objects.all()
        serial=AccountSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            accountid=dicts['Accountid']
            print(accountid)
            #check if account is exists in database then delete it else show error msg
            if not Account.objects.filter(Accountid=accountid).exists():
                fail=({'Error':'Account does not exist with this id ','Accountid':accountid})
                failed.append(fail)
            else:
                account=Account.objects.get(Accountid=accountid)
                account.delete()
        return Response({'Account deleted !':'success','Failed to delete':failed})

###-------------------------------------INTEREST BULK DELETE API----------------------------------###

class InterestDelete(APIView):
    def get(self,request,format=None):
        get=Interest.objects.all()
        serial=InterestSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            interestid=dicts['InterestID']
            print(interestid)
            #check if interest is exists in the database then delete else show error msg
            if not Interest.objects.filter(InterestID=interestid).exists():
                fail=({'Error':'Interest does not exists with this id','InterestID':interestid})
                failed.append(fail)
            else:
                interest=Interest.objects.get(InterestID=interestid)
                interest.delete()
        return Response({'Interest deleted !':'success','Failed to delete':failed})

###------------------------------------PRODUCT BULK DELETE API-----------------------------------###

class ProductDelete(APIView):
    def get(self,request,format=None):
        get=Product.objects.all()
        serial=ProductSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            productid=dicts['Productid']
            print(productid)
            #check if product is exists in the database then delete it else show error msg
            if not Product.objects.filter(Productid=productid).exists():
                fail=({'Error':'Product not exists with this id','Productid':productid})
                failed.append(fail)
            else:    
                product=Product.objects.get(Productid=productid)
                product.delete()
        return Response({'Product deleted !':'success','Failed to delete':failed})

###----------------------------------OPPORTUNITY BULK DELETE API---------------------------------###

class OpportunityDelete(APIView):
    def get(self,request,format=None):
        get=Opportunity.objects.all()
        serial=OpportunitySerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            opportunityid=dicts['OpportunityId']
            print(opportunityid)
            #check if opportunity is exists in the database then delete else show error msg
            if not Opportunity.objects.filter(OpportunityId=opportunityid).exists():
                fail=({'Error':'Opportunity not exists with this id','Opportunityid':opportunityid})
                failed.append(fail)
            else:    
                oppor=Opportunity.objects.get(OpportunityId=opportunityid)
                oppor.delete()
        return Response({'Opportunity deleted !':'success','Failed to delete':failed})

###--------------------------------INTEREST JUNCTION BULK DELETE API----------------------------------###

class InterestJunctionDelete(APIView):
    def get(self,request,format=None):
        get=Interest_Junction_c.objects.all()
        serial=InterestJunctionSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        failed=[]
        data=request.data.get('data')
        for dicts in data:
            junctionid=dicts['InterestJunctionID']
            print(junctionid)
            #check if interest jucntion is exists in the database then delete it else show error msg
            if not Interest_Junction_c.objects.filter(InterestJunctionID=junctionid).exists():
                fail=({'error':'InterstJunction not exists with this id','InterestJunctionid':junctionid})
                failed.append(fail)
            else:    
                junc=Interest_Junction_c.objects.get(InterestJunctionID=junctionid)    
                junc.delete()
        return Response({'InterestJunction deleted !':'success','Failed to delete':failed})
       


###-------------------------------------ACCOUNT BULK DELETE API--------------------------------###
##currently this api is not working instead of it AccountDelete above is working 
class AccountBulkDelete(APIView):
    def get(self,request,format=None):
        get=Account.objects.all()
        serial=AccountSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        for obj in data:
            accountid=obj['Accountid']
            print(accountid)
            if not Account.objects.filter(Accountid=accountid).exists():
                return Response({'error':'Account not exist with this id ','id':accountid})
            account=Account.objects.get(Accountid=accountid)
            account.delete()
        return Response({'message':'Account deleted successfully'})


###---------------------------------------FIND CLIENT API------------------------------------------###
##this api is used for find client first version 
class ClientFind(APIView):
    def get(self,request,format=None):
        data=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(data,many=True)
        return Response(serializers.data)
    def post(self,request,format=None):
        getaccountid=[]
        #difining globle variable for not getting error of local variable refrence
        global qz1
        global qz2
        global qz3
        global qz5
        global qz7
        global qz9
        global qz10
        global qz11
        global qz23
        global qz6
        global qz4
        global qz8
        global qz12
        global qz13
        global qz14
        global qz15
        global qz16
        global qz17
        global qz18
        global qz19
        global qz20
        global qz21
        global qz22
        global qz23
        global qz24
        global qz25
        global qz26
        global qz27
        global qz28
        global qz29
        global qz30
        global qz31
        global qz32
        global qz33
        global qz34
        global qz35
        global qz36
        global qz37
        global qz38
        global qz39
        global qz40
        global qz41
        global qz42
        global qz43
        global qz44
        global qz45
        global qz46
        global qz47
        global qz48
        global qz49
        global qz50
        global qz51
        global qz52
        global qz53
        global qz54
        global qz55
        global qz56
        global qz57
        global qz58
        global qz59
        global qz60
        global qz61
        global qz62
        global qz63
        global qz64
        global qz65
        global qz66
        #defining null values for global variables 
        qz1=Q({"multi_match": {"query": "", "fields": [""]}})
        qz23=Q({"multi_match": {"query": "", "fields": [""]}})
        qz6=Q({"multi_match": {"query": "", "fields": [""]}})
        qz4=Q({"multi_match": {"query": "", "fields": [""]}})
        qz8=Q({"multi_match": {"query": "", "fields": [""]}})
        qz2=Q({"multi_match": {"query": "", "fields": [""]}})
        qz3=Q({"multi_match": {"query": "", "fields": [""]}})
        qz5=Q({"multi_match": {"query": "", "fields": [""]}})
        qz7=Q({"multi_match": {"query": "", "fields": [""]}})
        qz9=Q({"multi_match": {"query": "", "fields": [""]}})
        qz10=Q({"multi_match": {"query": "", "fields": [""]}})
        qz11=Q({"multi_match": {"query": "", "fields": [""]}})
        qz12=Q({"multi_match": {"query": "", "fields": [""]}})
        qz13=Q({"multi_match": {"query": "", "fields": [""]}})
        qz14=Q({"multi_match": {"query": "", "fields": [""]}})
        qz15=Q({"multi_match": {"query": "", "fields": [""]}})
        qz16=Q({"multi_match": {"query": "", "fields": [""]}})
        qz17=Q({"multi_match": {"query": "", "fields": [""]}})
        qz18=Q({"multi_match": {"query": "", "fields": [""]}})
        qz19=Q({"multi_match": {"query": "", "fields": [""]}})
        qz20=Q({"multi_match": {"query": "", "fields": [""]}})
        qz21=Q({"multi_match": {"query": "", "fields": [""]}})
        qz22=Q({"multi_match": {"query": "", "fields": [""]}})
        qz23=Q({"multi_match": {"query": "", "fields": [""]}})
        qz24=Q({"multi_match": {"query": "", "fields": [""]}})
        qz25=Q({"multi_match": {"query": "", "fields": [""]}})
        qz26=Q({"multi_match": {"query": "", "fields": [""]}})
        qz27=Q({"multi_match": {"query": "", "fields": [""]}})
        qz28=Q({"multi_match": {"query": "", "fields": [""]}})
        qz29=Q({"multi_match": {"query": "", "fields": [""]}})
        qz30=Q({"multi_match": {"query": "", "fields": [""]}})
        qz31=Q({"multi_match": {"query": "", "fields": [""]}})
        qz32=Q({"multi_match": {"query": "", "fields": [""]}})
        qz33=Q({"multi_match": {"query": "", "fields": [""]}})
        qz34=Q({"multi_match": {"query": "", "fields": [""]}})
        qz35=Q({"multi_match": {"query": "", "fields": [""]}})
        qz36=Q({"multi_match": {"query": "", "fields": [""]}})
        qz37=Q({"multi_match": {"query": "", "fields": [""]}})
        qz38=Q({"multi_match": {"query": "", "fields": [""]}})
        qz39=Q({"multi_match": {"query": "", "fields": [""]}})
        qz40=Q({"multi_match": {"query": "", "fields": [""]}})
        qz41=Q({"multi_match": {"query": "", "fields": [""]}})
        qz42=Q({"multi_match": {"query": "", "fields": [""]}})
        qz43=Q({"multi_match": {"query": "", "fields": [""]}})
        qz44=Q({"multi_match": {"query": "", "fields": [""]}})
        qz45=Q({"multi_match": {"query": "", "fields": [""]}})
        qz46=Q({"multi_match": {"query": "", "fields": [""]}})
        qz47=Q('term',**{"StageName":"NULL"})
        qz48=Q('term',**{"StageName":"NULL"})
        qz49=Q('term',**{"StageName":"NULL"})
        qz50=Q('term',**{"StageName":"NULL"})
        qz51=Q('term',**{"StageName":"NULL"})
        qz52=Q('term',**{"StageName":"NULL"})
        qz53=Q('term',**{"StageName":"NULL"})
        qz54=Q('term',**{"StageName":"NULL"})
        qz55=Q('term',**{"StageName":"NULL"})
        qz56=Q('term',**{"StageName":"NULL"})
        qz57=Q('term',**{"StageName":"NULL"})
        qz58=Q('term',**{"StageName":"NULL"})
        qz59=Q('term',**{"StageName":"NULL"})
        qz60=Q('term',**{"StageName":"NULL"})
        qz61=Q('term',**{"StageName":"NULL"})
        qz62=Q('term',**{"StageName":"NULL"})
        qz63=Q('term',**{"StageName":"NULL"})
        qz64=Q('term',**{"StageName":"NULL"})
        qz65=Q('term',**{"StageName":"NULL"})
        qz66=Q('term',**{"StageName":"NULL"})
        #getting json body by indexing
        data=request.data.get('data')
        interestcondition=data[0]
        interestname=data[1]
        accountfiltercondition=data[2]
        accountfilters=data[3]
        acc=accountfilters['AccountFilters']
        categoryofinterestfilter=acc[0]
        youngeraudiencefilter=acc[1]
        lastpurchasedatefilter=acc[2]
        holidayscelebratedfilter=acc[3]
        emailcondition=acc[4]
        email=acc[5]
        shippingcity=acc[6]
        accountfiltername=accountfilters['AccountFilters']
        interestfiltercondition=data[4]
        interestfilter=data[5]
        interestfiltername=interestfilter['InterestFilter']
        accountinteresttype=interestfiltername[0]
        accountinterestname=interestfiltername[1]
        opportunityfiltercondition=data[6]
        opportunityfilter=data[7]
        opportunitycolumn=opportunityfilter['OpportunityFilter']
        opportunitystagename=opportunitycolumn[0]
        opportunitybillingcity=opportunitycolumn[1]
        opportunityavarageitemsold=opportunitycolumn[2]
        interestitem=interestname['InterestName']
        #making queries for all fields to check logic and field name and field value
        #and also check condition AND and OR if and condition then make for AND query else OR query 
        qz=Q('terms',**interestname)
        if accountfiltercondition['AccountFiltersCondition'] == 'AND':
            if categoryofinterestfilter['FilterLogic'] =='Includes':
                qz1=Q('terms', **{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})
            elif categoryofinterestfilter['FilterLogic'] == 'Exclude':
                qz2=Q('bool', must_not=[Q('terms',**{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})])
            else:
                qz3=Q('bool', must=[Q('terms',**{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})])
            if youngeraudiencefilter['FilterLogic'] == 'Equal': 
                qz4=Q(
                    'multi_match',
                    query=youngeraudiencefilter['FieldValue'],
                    fields=[
                        'Account.YoungerAudience',
                    ]
                    )
            else:
                qz5=Q('bool', must_not=[Q('term',**{'Account.YoungerAudience':youngeraudiencefilter['FieldName']})])
                
            if holidayscelebratedfilter['FilterLogic'] == 'Equal':
                qz6=Q(
                    'multi_match',
                    query=holidayscelebratedfilter['FieldValue'],
                    fields=[
                        'Account.HolidayCelebrated',
                    ]
                    )
            else:
                qz7=Q('bool', must_not=[Q('term',**{'Account.HolidayCelebrated':holidayscelebratedfilter['FieldValue']})])
            if lastpurchasedatefilter['FilterLogic'] == 'Equal':
                qz8=Q(
                    'multi_match',
                    query=lastpurchasedatefilter['FieldValue'],
                    fields=[
                        'Account.LastPurchasedDate',
                    ]
                    )
            elif lastpurchasedatefilter['FilterLogic'] == 'Not Equal':
                qz9=Q('bool', must_not=[Q('term',**{'Account.LastPurchasedDate':lastpurchasedatefilter['FieldValue']})])

            elif lastpurchasedatefilter['FilterLogic'] == 'Greater than':
                qz10=Q('bool', filter=[Q('range',**{'Account.LastPurchasedDate': {'gte':lastpurchasedatefilter['FieldValue'],'format':'dd-mm-yy'}})])

            else:
                qz11=Q('bool', filter=[Q('range',**{'Account.LastPurchasedDate': {'lte':lastpurchasedatefilter['FieldValue'],'format':'dd-mm-yy'}})])
        else:
            if categoryofinterestfilter['FilterLogic'] =='Includes':
                qz12=Q('terms', **{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})
            elif categoryofinterestfilter['FilterLogic'] == 'Exclude':
                qz13=Q('bool', must_not=[Q('terms',**{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})])
            else:
                qz14=Q('bool', must=[Q('terms',**{'Account.CategoryOfInterest':categoryofinterestfilter['FieldValue']})])
            if youngeraudiencefilter['FilterLogic'] == 'Equal': 
                qz15=Q(
                    'multi_match',
                    query=youngeraudiencefilter['FieldValue'],
                    fields=[
                        'Account.YoungerAudience',
                    ]
                    )
            else:
                qz16=Q('bool', must_not=[Q('term',**{'Account.YoungerAudience':youngeraudiencefilter['FieldName']})])
            if holidayscelebratedfilter['FilterLogic'] == 'Equal':
                qz17=Q(
                    'multi_match',
                    query=holidayscelebratedfilter['FieldValue'],
                    fields=[
                        'Account.HolidayCelebrated',
                    ]
                    )
            else:
                qz18=Q('bool', must_not=[Q('term',**{'Account.HolidayCelebrated':holidayscelebratedfilter['FieldValue']})])
            if lastpurchasedatefilter['FilterLogic'] == 'Equal':
                qz19=Q(
                    'multi_match',
                    query=lastpurchasedatefilter['FieldValue'],
                    fields=[
                        'Account.LastPurchasedDate',
                    ]
                    )
            elif lastpurchasedatefilter['FilterLogic'] == 'NotEqual':
                qz20=Q('bool', must_not=[Q('match',**{'Account.LastPurchasedDate':lastpurchasedatefilter['FieldValue']})])

            elif lastpurchasedatefilter['FilterLogic'] == 'Greater than':
                # qz10=Q('bool', must=[Q('range',**{'Account.LastPurchaseDtae':{"gte":{lastpurchasedatefilter['FieldValue']}}})])
                qz21=Q('range', **{'Account.LastPurchasedDate': {"gte":lastpurchasedatefilter['FieldValue']}})

            else:
                qz22=Q('range', **{'Account.LastPurchasedDate': {"lte":lastpurchasedatefilter['FieldValue']}})
        if emailcondition['EmailCondition'] =='AND':
            if email['FilterLogic'] =='Equal':
                qz23=Q(
                    'multi_match',
                    query=email['FieldValue'],
                    fields=[
                        'Account.Email',
                    ]
                    )
            else:
                qz24=Q('bool', must_not=[Q('match',**{'Account.Email':email['FieldValue']})])

            if shippingcity['FilterLogic'] =='Includes':
                qz25=Q(
                    'multi_match',
                    query=shippingcity['FieldValue'],
                    fields=[
                        'Account.ShippingCity',
                    ],fuzziness='auto'
                    )
            elif shippingcity['FilterLogic'] == 'Excludes':
                qz26=Q('bool', must_not=[Q('match',**{'Account.ShippingCity':shippingcity['FieldValue']})])
            elif shippingcity['FilterLogic'] == 'Equal':
                qz27=Q(
                    'multi_match',
                    query=shippingcity['FieldValue'],
                    fields=[
                        'Account.ShippingCity',
                    ]
                    )
            else:
                qz28=Q('bool', must_not=[Q('match',**{'Account.ShippingCity':shippingcity['FieldValue']})])

        else:
            if email['FilterLogic'] =='Equal':
                qz29=Q(
                    'multi_match',
                    query=email['FieldValue'],
                    fields=[
                        'Account.Email',
                    ]
                    )
            else:
                qz30=Q('bool', must_not=[Q('match',**{'Account.Email':email['FieldValue']})])

            if shippingcity['FilterLogic'] =='Includes':
                qz31=Q(
                    'multi_match',
                    query=shippingcity['FieldValue'],
                    fields=[
                        'Account.ShippingCity',
                    ],fuzziness='auto'
                    )
            elif shippingcity['FilterLogic'] == 'Excludes':
                qz32=Q('bool', must_not=[Q('match',**{'Account.ShippingCity':shippingcity['FieldValue']})])
            elif shippingcity['FilterLogic'] == 'Equal':
                qz33=Q(
                    'multi_match',
                    query=shippingcity['FieldValue'],
                    fields=[
                        'Account.ShippingCity',
                    ]
                    )
            else:
                qz34=Q('bool', must_not=[Q('match',**{'Account.ShippingCity':shippingcity['FieldValue']})])
        if interestfiltercondition['InterestFilterCondition'] == 'AND':
            if accountinterestname['FilterLogic'] == 'Includes':
                qz35=Q(
                    'multi_match',
                    query=accountinterestname['FieldValue'],
                    fields=[
                        'Interest.InterestName',
                    ],fuzziness='auto'
                    )
            elif accountinterestname['FilterLogic'] == 'Exclude':
                qz36=Q('bool', must_not=[Q('match',**{'Interest.InterestName':accountinterestname['FieldValue']})])


            elif accountinterestname['FilterLogic'] == 'Equal':
                qz37=Q(
                    'multi_match',
                    query=accountinterestname['FieldValue'],
                    fields=[
                        'Interest.InterestName',
                    ]
                    )
            else:
                qz38=Q('bool', must_not=[Q('match',**{'Interest.InterestName':accountinterestname['FieldValue']})])
       
            if accountinteresttype['FilterLogic'] == 'Equal':
                qz39=Q(
                    'multi_match',
                    query=accountinteresttype['FieldValue'],
                    fields=[
                        'Interest.InterestType',
                    ]
                    )

            else:
                qz40=Q('bool', must_not=[Q('match',**{'Interest.InterestType':accountinteresttype['FieldValue']})])
        else:
            if accountinterestname['FilterLogic'] == 'Includes':
                qz41=Q(
                    'multi_match',
                    query=accountinterestname['FieldValue'],
                    fields=[
                        'Interest.InterestName',
                    ],fuzziness='auto'
                    )
            elif accountinterestname['FilterLogic'] == 'Exclude':
                qz42=Q('bool', must_not=[Q('match',**{'Interest.InterestName':accountinterestname['FieldValue']})])


            elif accountinterestname['FilterLogic'] == 'Equal':
                qz43=Q(
                    'multi_match',
                    query=accountinterestname['FieldValue'],
                    fields=[
                        'Interest.InterestName',
                    ]
                    )
            else:
                qz44=Q('bool', must_not=[Q('match',**{'Interest.InterestName':accountinterestname['FieldValue']})])
       
            if accountinteresttype['FilterLogic'] == 'Equal':
                qz45=Q(
                    'multi_match',
                    query=accountinteresttype['FieldValue'],
                    fields=[
                        'Interest.InterestType',
                    ]
                    )

            else:
                qz46=Q('bool', must_not=[Q('match',**{'Interest.InterestType':accountinteresttype['FieldValue']})])
        if opportunityfiltercondition['OpportunityFilterCondition'] == 'AND':
            query_list=[]
            if opportunitystagename['FilterLogic'] =='Equal':
                qz47=Q('bool', must=[Q('match',**{opportunitystagename['FieldName']:opportunitystagename['FieldValue']})])
                query_list.append(qz47)
            else:
                qz48=Q('bool', must_not=[Q('match',**{opportunitystagename['FieldName']:opportunitystagename['FieldValue']})])
                query_list.append(qz48)
            if opportunitybillingcity['FilterLogic'] == 'Includes':
                qz49=Q(
                    'multi_match',
                    query=opportunitybillingcity['FieldValue'],
                    fields=[
                        opportunitybillingcity['FieldName']
                    ],fuzziness='auto')
                query_list.append(qz49)

            elif opportunitybillingcity['FilterLogic'] == 'Exclude':
                qz50=Q('bool', must_not=[Q('match',**{opportunitybillingcity['FieldName']:opportunitybillingcity['FieldValue']})])
                query_list.append(qz50)
            elif opportunitybillingcity['FilterLogic'] == 'Equal':
                qz51=Q('bool', must=[Q('match',**{opportunitybillingcity['FieldName']:opportunitybillingcity['FieldValue']})])
                query_list.append(qz1)
            else:
                qz52=Q('bool', must_not=[Q('match',**{opportunitybillingcity['FieldName']:opportunitybillingcity['FieldValue']})])
                query_list.append(qz52)
            if opportunityavarageitemsold['FilterLogic'] == 'Equal':
                qz53=Q('bool', must=[Q('match',**{opportunityavarageitemsold['FieldName']:opportunityavarageitemsold['FieldValue']})])
                query_list.append(qz53)
            elif opportunityavarageitemsold['FilterLogic'] == 'Greater than':
                # qz54=Q('range', **{opportunityavarageitemsold['FieldName']: {"gte":opportunityavarageitemsold['FieldValue']}})
                qz54=Q('bool', filter=[Q('range',**{opportunityavarageitemsold['FieldName']: {'gte':opportunityavarageitemsold['FieldValue']}})])
                query_list.append(qz54)

            elif opportunityavarageitemsold['FilterLogic'] == 'Lesser than':
                qz55=Q('bool', filter=[Q('range',**{opportunityavarageitemsold['FieldName']: {'lte':opportunityavarageitemsold['FieldValue']}})])
                query_list.append(qz55)

            else:
                qz56=Q('bool', must_not=[Q('match',**{opportunityavarageitemsold['FieldName']:opportunityavarageitemsold['FieldValue']})])
                query_list.append(qz56)
            final_query=Q('bool',should=query_list)  
    
        else:
            query_list=[]
            if opportunitystagename['FilterLogic'] =='Equal':
                qz57=Q(
                    'multi_match',
                    query=opportunitystagename['FieldValue'],
                    fields=[
                        opportunitystagename['FieldName']
                    ]
                    )
                query_list.append(qz57)    
            else:
                qz58=Q('bool', must_not=[Q('match',**{opportunitystagename['FieldName']:opportunitystagename['FieldValue']})])
                query_list.append(qz58)
            if opportunitybillingcity['FilterLogic'] == 'Includes':
                qz59=Q(
                    'multi_match',
                    query=opportunitybillingcity['FieldValue'],
                    fields=[
                        opportunitybillingcity['FieldName']
                    ],fuzziness='auto')
                query_list.append(qz59) 
            elif opportunitybillingcity['FilterLogic'] == 'Exclude':
                qz60=Q('bool', must_not=[Q('match',**{opportunitybillingcity['FieldName']:opportunitybillingcity['FieldValue']})])
                query_list.append(qz60)
            elif opportunitybillingcity['FilterLogic'] == 'Equal':
                qz61=Q(
                    'multi_match',
                    query=opportunitybillingcity['FieldValue'],
                    fields=[
                        opportunitybillingcity['FieldName']
                    ])
                query_list.append(qz61)    
            else:
                qz62=Q('bool', must_not=[Q('match',**{opportunitybillingcity['FieldName']:opportunitybillingcity['FieldValue']})])
                query_list.append(qz62)
            if opportunityavarageitemsold['FilterLogic'] == 'Equal':
                qz63=Q(
                    'multi_match',
                    query=opportunityavarageitemsold['FieldValue'],
                    fields=[
                        opportunityavarageitemsold['FieldName']
                    ])
                query_list.append(qz63)    
            elif opportunityavarageitemsold['FilterLogic'] == 'Greater than':
                qz64=Q('range', **{opportunityavarageitemsold['FieldName']: {"gte":opportunityavarageitemsold['FieldValue']}})
                query_list.append(qz64)
            elif opportunityavarageitemsold['FilterLogic'] == 'Lesser than':
                qz65=Q('range', **{opportunityavarageitemsold['FieldName']: {"lte":opportunityavarageitemsold['FieldValue']}})
                query_list.append(qz65)
            else:
                qz66=Q('bool', must_not=[Q('match',**{opportunityavarageitemsold['FieldName']:opportunityavarageitemsold['FieldValue']})])
                query_list.append(qz66)
            final_query=Q('bool',should=query_list) 
        #concatinate query for search opportunity in opportunity table and extract account id,store in array      
        qqq=final_query|qz57|qz58|qz59|qz60|qz61|qz62|qz63|qz64|qz65|qz66                    
        opportunity=OpportunityDocument.search().query(qqq)
        serializer=OpportunitySerializersPost(opportunity,many=True)
        for x in serializer.data:
           zz=x
           print(zz)
           od2 = json.loads(json.dumps(zz))
           dictaccount=(od2['AccountId'])
           getaccount=(dictaccount['Accountid'])
           getaccountid.append(str(getaccount))
        qz80=Q('terms',**{'Account.Accountid':getaccountid}) 
        #Concatinating all fields query and search in interestjunction documents in elasticsearch 
        xy=qz1&qz6&qz4&qz8&qz2&qz3&qz5&qz7&qz9&qz10&qz11|qz12|qz13|qz14|qz15|qz16|qz17|qz18|qz19|qz20|qz21|qz22&qz23&qz24&qz25&qz26&qz27&qz28|qz29|qz30|qz31|qz32|qz33|qz34&qz35&qz36&qz37&qz38&qz39&qz40|qz41|qz42|qz43|qz44|qz45|qz46|qz|qz80
        search=Interest_Junction_cDocument.search().query(xy)
        serial1=InterestJunctionFindClientSerializers(search,many=True)        
        return Response(serial1.data) 

        

 ###-----------------------------------FIND CLIENT VERSION 2-------------------------------------------###       
 ##making this function for handle to make query it will make autometically query according to condition           
 ##only provide field name,logic,value in the parameter ,this func is not for array search
def handle_filter(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        # return Q("terms", field=field_name, value=field_value)
        return Q('bool', filter=[Q('terms', **{field_name: field_value})])
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('terms',**{field_name: field_value})])
    elif filter_logic == 'Equal':
        return Q('multi_match', query=field_value, fields=[field_name])
    elif filter_logic == 'Not Equal':
        return Q('bool', must_not=[Q('term',**{field_name: field_value})])
    elif filter_logic == 'Greater than':
        return Q('bool', filter=[Q('range',**{field_name: {'gte': field_value, 'format':'dd-mm-yy'}})])
    elif filter_logic == 'Lesser than':
        return Q('bool', filter=[Q('range',**{field_name: {'lte': field_value, 'format':'dd-mm-yy'}})])
    else:
        return Q()
    
##making this function for handle to make query it will make autometically query according to condition           
##only provide field name,logic,value in the parameter ,this func is for array search
def handle_filter_array(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        # return Q("terms", field=field_name, value=field_value)
        return Q('bool', filter=[Q('terms', **{field_name: field_value})])
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('terms',**{field_name: field_value})])
    elif filter_logic == 'Equal':
        return Q('terms',**{field_name:field_value})
    elif filter_logic == 'Not Equal':
        return Q('bool', must_not=[Q('terms',**{field_name: field_value})])
    elif filter_logic == 'Greater than':
        return Q('bool', filter=[Q('range',**{field_name: {'gte': field_value, 'format':'dd-mm-yy'}})])
    elif filter_logic == 'Lesser than':
        return Q('bool', filter=[Q('range',**{field_name: {'lte': field_value, 'format':'dd-mm-yy'}})])
    else:
        return Q()    

def handle_filter_term(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        # return Q("terms", field=field_name, value=field_value)
        return Q(
            'multi_match',
            query=field_value,
            fields=[
                field_name
            ],fuzziness='auto')
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('match_phrase',**{field_name: field_value})])
    elif filter_logic == 'Equal':
        match_phrase_queries = [Q('match_phrase', **{field_name:field_value})]
        return Q('bool', should=match_phrase_queries)
    #    return Q('term', query=field_value, fields=[field_name])
        # return Q('match', query=field_value, fields=[field_name])
    elif filter_logic == 'Not Equal':
        return Q('bool', must_not=[Q('match_phrase', **{field_name:field_value})])
    elif filter_logic == 'Greater than':
        queries=[Q('range', **{field_name: {'gt': field_value}})]
        return Q('bool',should=queries)
    elif filter_logic == 'Lesser than':
        queries=[Q('range', **{field_name: {'gt': field_value}})]
        return Q('bool',should=queries)
    else:
        return Q()           
        
class FindClientNewVersionApi(APIView):
    def get (self,request):
        interestjunction=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
        return Response(serializers.data)
        
    def post(self,request):
        getaccountid=[]
        interestcondition=request.data.get('InterestCondition',None)
        interestname=request.data.get('InterestName',None)
        accountfilters=request.data.get('AccountFilters',None)
        interestfilters=request.data.get('InterestFilters',None)
        opportunityfilters=request.data.get('OpportunityFilters',None)
        ##to making query call the above function that is auto create query for all 
        queries = [
        handle_filter(accountfilters['CategoryOfInterestFieldName'], accountfilters['CategoryOfInterestFilterLogic'], accountfilters['CategoryOfInterestFieldValue']),
        handle_filter(accountfilters['YoungerAudienceFieldName'], accountfilters['YoungerAudienceFilterLogic'], accountfilters['YoungerAudienceFieldValue']),
        handle_filter(accountfilters['HolidayCelebratedFieldName'], accountfilters['HolidayCelebratedFilterLogic'], accountfilters['HolidayCelebratedFieldValue']),
        handle_filter(accountfilters['LastPurchasedDateFieldName'], accountfilters['LastPurchasedDateFilterLogic'], accountfilters['LastPurchasedDateFieldValue'])
        ]
        queries2= [
        handle_filter_term(accountfilters['EmailFieldName'], accountfilters['EmailFilterLogic'], accountfilters['EmailFieldValue']),
        handle_filter_term(accountfilters['ShippingCityFieldName'], accountfilters['ShippingCityFilterLogic'], accountfilters['ShippingCityFieldValue']),
        ]
        queries3=[
        handle_filter_term(interestfilters['InterestTypeFieldName'], interestfilters['InterestTypeFilterLogic'], interestfilters['InterestTypeFieldValue']),
        handle_filter_term(interestfilters['InterestNameFieldName'], interestfilters['InterestNameFilterLogic'], interestfilters['InterestNameFieldValue']),
        ]
        queries4=[
        handle_filter_term(opportunityfilters['StageNameFieldName'], opportunityfilters['StageNameFilterLogic'], opportunityfilters['StageNameFieldValue']),
        handle_filter_term(opportunityfilters['BillingCityFieldName'], opportunityfilters['BillingCityFilterLogic'], opportunityfilters['BillingCityFieldValue']),
        handle_filter_term(opportunityfilters['AverageItemSoldFieldName'], opportunityfilters['AverageItemSoldFilterLogic'], opportunityfilters['AverageItemSoldFieldValue']),

        ]
        #checking condition for the fields if AND then concatinate all queries with same and 
        #if OR condition then concatinate all queries with same or
        #and make final query for searching in interestjunction
        if interestcondition == 'AND':
            final_query0=Q('terms', **{'InterestName': interestname})
        elif interestcondition == 'OR':
            final_query0=Q('terms', **{'InterestName': interestname})    
        else:
            final_query0=Q()    
        if accountfilters['AccountFiltersCondition'] == 'AND':
            final_query = reduce(and_, queries)
        elif accountfilters['AccountFiltersCondition'] =='OR':
            final_query=reduce(or_,queries)    
        else:
            final_query=Q()    
        if accountfilters['EmailCondition'] == 'AND':
            final_query2=reduce(and_,queries2)
        elif accountfilters['EmailCondition'] == 'OR':
            final_query2=reduce(or_,queries2)
        else:
            final_query2=Q()    
        if interestfilters['InterestFilterCondition'] == 'AND':
            final_query3=reduce(and_,queries3)
        elif interestfilters['InterestFilterCondition'] =='OR':    
            final_query3=reduce(or_,queries3)
        else:
            final_query3=Q()    
        if opportunityfilters['OpportunityFilterCondition'] == 'AND':
            final_query4=reduce(and_,queries4)        
        elif opportunityfilters['OpportunityFilterCondition'] =='OR':
            final_query4=reduce(or_,queries4)   
        else:
            final_query4=Q() 
        ##first search opportunity on opportunity documents and extract account id 
        ##with opportunity query and store it in array to make another query for array and search
        ##that array query in interest junction         
        opportunity_search=OpportunityDocument.search().query(final_query4)
        serial=OpportunitySerializersPost(opportunity_search,many=True)
        for x in serial.data:
           od2 = json.loads(json.dumps(x))
           dictaccount=(od2['AccountId'])
           getaccount=(dictaccount['Accountid'])
           getaccountid.append(str(getaccount))        
        opportunity_query=Q('terms' ,**{'Account.Accountid':getaccountid})
        #making final query for all fields and opportunity also 
        result_query=(final_query0&final_query&final_query2&final_query3) |final_query0|final_query|final_query2|final_query3
        search=Interest_Junction_cDocument.search().query(result_query)
        serializer=InterestJunctionFindClientSerializers(search,many=True)
        return Response(serializer.data)



class FindClientNew(APIView):
    def get (self,request):
        interestjunction=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
        return Response(serializers.data)
    
    def post(self,request):
        account_array=[]
        interest_array=[]
        junction_array=[]
        opportunity_array=[]
        get_account_id=[]
        formula=request.data.get('Formula')
        data=request.data.get('Filters')
        for dicts in data:
            fields=(dicts['Field'])
            fieldname=fields['FieldName']
            fieldvalue=fields['Value']
            fieldlogic=fields['Logic']
            if fieldname == 'InterestName':
                query1=Q('terms',**{fieldname:fieldvalue})
                junction_array.append(query1)
                interest_array.append(query1)
            elif fieldname == 'CategoryOfInterest':
                query2=handle_filter_array(fieldname,fieldlogic,fieldvalue)
                account_array.append(query2)
            elif fieldname == 'HolidayCelebrated':
                query3=handle_filter_term(fieldname,fieldlogic,fieldvalue)
                account_array.append(query3)
            elif fieldname == 'YoungerAudience':
                query4=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                account_array.append(query4)
            elif fieldname == 'LastPurchasedDate':
                query5=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                account_array.append(query5)
            elif fieldname == 'Email':
                query6=handle_filter_term(fieldname,fieldlogic,fieldvalue)
                account_array.append(query6)    
            elif fieldname == 'ShippingCity':
                query7=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                account_array.append(query7)
            elif fieldname == 'StageName':
                query8=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                opportunity_array.append(query8)
            elif fieldname == 'Billing_City':
                query9=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                opportunity_array.append(query9)
            elif fieldname == 'AvarageitemSold':
                query10=handle_filter_term(fieldname,fieldlogic,fieldvalue)    
                opportunity_array.append(query10)
            elif fieldname == 'InterestType':
                query11=handle_filter_term(fieldname,fieldlogic,fieldvalue)
                interest_array.append(query11)    
            else:
                query12=Q()
        # acc=(", ".join(account_array))
        # print('hello',acc)       
        account_query_must=Q('bool',must=account_array)
        account_query_should=Q('bool',should=account_array)
        junction_query_should=Q('bool',must=junction_array)
        interest_query_should=Q('bool',should=interest_array)
        interest_query_must=Q('bool',must=interest_array)
        opportunity_query_should=Q('bool',should=opportunity_array)
        opportunity_query_must=Q('bool',must=opportunity_array)
        logic=get_tokens(formula)
        if len(logic) == 3:
            final_qery1=account_query_must
        else:
            if logic[3] == 'OR':
                final_qery1=account_query_should
            elif logic[3] =='AND':
                final_qery1=account_query_must 
            else:
                final_qery1=account_query_must    
            # print('HELLO----',final_qery1)  
        # qz=Q('terms',**{'CategoryOfInterest':['diamond']})    
        search1=AccountDocument.search().query(final_qery1)
        serializers1=AccountSerializers(search1,many=True)
        for x in serializers1.data:
           od2 = json.loads(json.dumps(x))
           getaccount=(od2['Accountid'])
           get_account_id.append(str(getaccount))
        if len(logic) ==3:
            final_qery2=interest_query_must
        else:    
            if logic[3] == 'OR':
                final_qery2=interest_query_should
            elif not logic[3]:
                final_qery2=interest_query_must    
            else:
                final_qery2=interest_query_must

        search2=Interest_Junction_cDocument.search().query(final_qery2)
        serializers2=InterestJunctionFindClientSerializers(search2,many=True)
        for z in serializers2.data:
           od2 = json.loads(json.dumps(z))
           dictaccount=(od2['Account'])
           getaccount=(dictaccount['Accountid'])
        #    get_account_id.append(str(getaccount))
   
        if len(logic)==3:
            final_qery3=opportunity_query_must
        else:    
            if logic[3] == 'AND':
                final_qery3=opportunity_query_must
            if not logic[3]:
                final_qery3=opportunity_query_must    
            else:
                final_qery3=opportunity_query_should 

        search3=OpportunityDocument.search().query(final_qery3)
        serializers3=OpportunitySerializersPost(search3,many=True)
        for y in serializers3.data:
           print(y)
           od2 = json.loads(json.dumps(y))
           dictaccount=(od2['AccountId'])
           getaccount=(dictaccount['Accountid'])
        #    get_account_id.append(str(getaccount))
        # print('get_account------',get_account_id)   
        account_id_query=Q('terms',**{'Account.Accountid':get_account_id})
        # print('query',account_id_query)
        if logic[1] == 'AND':
            result_query=junction_query_should&account_id_query
            # print('result',result_query)
        else:
            result_query=junction_query_should|account_id_query      
        
        q1=Q('terms',**{'Account.CategoryOfInterest':['diamond']})
        # q2=Q('terms',**{"InterestName":['ring']})
        search=Interest_Junction_cDocument.search().query(result_query)
        serializers=InterestJunctionFindClientSerializers(search,many=True)
        return Response(serializers.data)



def get_tokens(expression):
    tokens = []
    current_token = ""
    for char in expression:
        if char in [" ", "AND", "OR", "(", ")"]:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if char in ["AND", "OR", "(", ")"]:
                tokens.append(char)
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens


###------------------------FIND CLIENT V2 API CURRENTLY WORKING-----------------------------###

from django.http import JsonResponse
from elasticsearch_dsl import Q,Search
from elasticsearch_dsl.connections import connections


##This is main class for v2 findclient we get json from here and call the filter data 
##and pass the array and formula
class FindClientApiView(APIView):
    def get (self,request):
        interestjunction=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
        return Response(serializers.data)

    def post(self,request):
        conditions=[]
        filters=request.data.get('filters')
        formula=request.data.get('formula')
        filterdata=filter_data(filters,formula)
        results = [hit.to_dict() for hit in filterdata]
        return JsonResponse(results, safe=False)


##this function makes query and manage all fields concatination according to formula 
##to provide to parameters array of fields and formula
def filter_data(filters, formula):
    search = Search()
    query_list = []
    limit = 20
    page = 1
    for i, filter in enumerate(filters):
        for key in filter:
            # print('key------',key)
            field_name = filter[key]['fieldName']
            logic = filter[key]['logic']
            values = filter[key]['value']
            if not key == 'Opportunity':
                if isinstance(values, list):
                    query = handle_filter_list(field_name, logic, values)  
                else:
                    query = handle_filter_str(field_name, logic, values)
            else:
                query=opportunity_search(field_name,logic,values)
            query_list.append(query)
    client = Elasticsearch()
    s = Search(using=client, index='interest_junction_cs')

    expression = create_query_string(formula,query_list)
    # print("start--> \n")
    print(expression,"\n")
    combined_query = (eval(expression))
    s = s.query(combined_query)
    s = s[(page - 1) * limit:page * limit]  # Implement pagination
    query_dict = s.to_dict()
    print('\combined_query---->',combined_query)
    # print('\nquery_dict---->',query_dict)
    response = s.execute()
    # print(response)
    return response


##this function used for replace &,| on the place of AND,OR
##according to formula 
def create_query_string(formula, query_list):
    formula = formula.replace("AND", "&").replace("OR", "|")
    query_string = ""
    for char in formula:
        if char.isdigit():
            query_string += "Q(query_list[" + char + "])"
        else:
            query_string += char
    return query_string


##making this function for handle to make query it will make autometically query according to condition           
##only provide field name,logic,value in the parameter ,this func is not for array search
def handle_filter_str(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        # return Q("terms", field=field_name, value=field_value)
        return Q(
            'multi_match',
            query=field_value,
            fields=[
                field_name
            ],fuzziness='auto')
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('match_phrase',**{field_name: field_value})])
    elif filter_logic == 'Equal':
        match_phrase_queries = [Q('match_phrase', **{field_name:field_value})]
        return Q('bool', should=match_phrase_queries)
    #    return Q('term', query=field_value, fields=[field_name])
        # return Q('match', query=field_value, fields=[field_name])
    elif filter_logic == 'Not Equal':
        return Q('bool', must_not=[Q('match_phrase', **{field_name:field_value})])
    elif filter_logic == 'Greater than':
        queries=[Q('range', **{field_name: {'gt': field_value}})]
        return Q('bool',should=queries)
    elif filter_logic == 'Lesser than':
        queries=[Q('range', **{field_name: {'gt': field_value}})]
        return Q('bool',should=queries)
    else:
        return Q()

##making this function for handle to make query it will make autometically query according to condition           
##only provide field name,logic,value in the parameter ,this func is for array search
def handle_filter_list(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        return Q('match', **{field_name: {'query': ' '.join(field_value), 'operator': 'or'}})
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('query_string', query=' OR '.join(f'"{value}"' for value in field_value), fields=[field_name])])
    elif filter_logic == 'Contains':
        match_phrase_queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', should=match_phrase_queries)
    elif filter_logic == 'Equal':
        term_queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', should=term_queries)
    elif filter_logic == 'Not Equal':
        queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', must_not=queries)
    elif filter_logic == 'Greater than':
        queries=[Q('range', **{field_name: {'gt': value} for value in field_value})]
        return Q('bool',should=queries)
    elif filter_logic == 'Lesser than':
        queries=[Q('range', **{field_name: {'lt': value} for value in field_value})]
        return Q('bool',should=queries)
    else:
        return Q()
        
def handle_filter_contain(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        return Q('match', **{field_name: {'query': ' '.join(field_value), 'operator': 'or'}})
    elif filter_logic == 'Exclude':
        return Q('bool', must_not=[Q('query_string', query=' OR '.join(f'"{value}"' for value in field_value), fields=[field_name])])
    elif filter_logic == 'Contains':
        match_phrase_queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', should=match_phrase_queries)
    elif filter_logic == 'Equal':
        term_queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', should=term_queries)
    elif filter_logic == 'Not Equal':
        queries = [Q('match_phrase', **{field_name: value}) for value in field_value]
        return Q('bool', must_not=queries)
    elif filter_logic == 'Greater than':
        queries=[Q('range', **{field_name: {'gt': value} for value in field_value})]
        return Q('bool',should=queries)
    elif filter_logic == 'Lesser than':
        queries=[Q('range', **{field_name: {'lt': value} for value in field_value})]
        return Q('bool',should=queries)
    else:
        return Q()
##this function is used for search opportunity and return query 
##only provide 3 parameter fieldname,ligic,values 
def opportunity_search(field_name,logic,values):
    query_list=[] 
    getaccount_id=[]  
    # print('opportunity------',field_name,logic,values) 
    if type(values) == list:
        querys=handle_filter_contain(field_name,logic,values)
    else:
        querys=handle_filter_term(field_name,logic,values)    
    # qzx=Q('bool', should=[Q('term', **{field_name:'Noida'})])
    opportunity_search=OpportunityDocument.search().query(querys)
    serializers=OpportunitySerializersPost(opportunity_search,many=True)
    for y in serializers.data:
        #    print(y)
           od2 = json.loads(json.dumps(y))
           dictaccount=(od2['AccountId'])
           getaccount=(dictaccount['Accountid'])
           getaccount_id.append(getaccount)
    # query1=Q('terms',**{"Account.Accountid":getaccount_id})
    match_phrase_queries = [Q('match_phrase', **{"Account.Accountid": value}) for value in getaccount_id]
    return Q('bool', should=match_phrase_queries)
    # print('query---->',query1)       
    # return query1

           
######-------------------------------BACKUP CODE-----------------------------------------#####
##this code is currently not working but keep as a backup may be used for future
# class FindClientApiView(APIView):
#     def get (self,request):
#         interestjunction=Interest_Junction_c.objects.all()
#         serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
#         return Response(serializers.data)
    
#     def post(self,request):
#         conditions=[]
#         filters=request.data.get('filters')
#         formula=request.data.get('formula')
#         # print(formula)
#         filterdata=filter_data(filters,formula)
        
#         # print(filterdata)
#         # search=Interest_Junction_cDocument.search().query()
#         serializer=InterestJunctionFindClientSerializers(filterdata,many=True)
#         return Response(serializer.data)




# def build_query(query_list, formula):
#     stack = []
#     formula = formula.split()
#     for c in formula:
#         if c == ')':
#             temp = []
#             while stack[-1] != '(':
#                 temp.append(stack.pop())
#             stack.pop()

#             if len(temp) == 1:
#                 stack.append(temp[0])
#             else:
#                 q = Q('bool', should=temp[::-1]) if stack[-1] == 'OR' else Q('bool', must=temp[::-1])
#                 stack.pop()
#                 stack.append(q)
#         elif c == '(':
#             stack.append(c)
#         elif c.isdigit():
#             i = int(c)
#             q = query_list[i][1]
#             stack.append(q)
#         else:
#             stack.append(c)
#     # print(stack)        
#     return stack


# from elasticsearch_dsl import Search, Q

# def filter_data(filters, formula):
#     search = Search()
#     query_list = []
#     for i, filter in enumerate(filters):
#         for key in filter:
#             field_name = filter[key]['fieldName']
#             logic = filter[key]['logic']
#             values = filter[key]['value']

#             if logic == 'Equal':
#                 query = Q('terms', **{field_name: values})
#             elif logic == 'NotEqual':
#                 query = ~Q('terms', **{field_name: values})
#             elif logic == 'Contains':
#                 query = Q('match', **{field_name: values[0]})
#             query_list.append((i, query))

#     final_query = build_query(query_list, formula)
#     print(final_query)
#     # query1=final_query[0]
#     # query2=final_query[2]
#     # query3=final_query[4]
#     # query_result=query1&(query2|query3)
#     # print(query1,query2)
#     convert=convert_query(final_query)
#     search = Interest_Junction_cDocument.search().query(convert)
#     return search

# def convert_stack_to_es_query(stack):
#     query = Q()
#     for item in stack:
#         if isinstance(item, dict):
#             if 'InterestName' in item:
#                 query &= Q('terms', InterestName=item['InterestName'])
#             elif 'CategoryOfInterest' in item:
#                 query |= Q('terms', CategoryOfInterest=item['CategoryOfInterest'])
#             elif 'TypeOfInterest' in item:
#                 query |= Q('terms', TypeOfInterest=item['TypeOfInterest'])
#         elif item == 'AND':
#             query &= Q()
#         elif item == 'OR':
#             query |= Q()
#     return query


from elasticsearch_dsl import Q

def convert_query(query):
    def get_terms_query(field, values):
        return Q('terms', **{field: values})

    def build_query(q1, operator, q2):
        if operator == 'AND':
            return Q('bool', must=[q1, q2])
        elif operator == 'OR':
            return Q('bool', should=[q1, q2])

    queries = []
    operators = []
    for item in query:
        if isinstance(item, tuple) and item[0] == 'Terms':
            queries.append(get_terms_query(item[1][0], item[1][1]))
        else:
            operators.append(item)

    while len(queries) > 1:
        q1 = queries.pop(0)
        operator = operators.pop(0)
        q2 = queries.pop(0)
        queries.insert(0, build_query(q1, operator, q2))
    # print(queries) 
    return queries




# query = [Terms(InterestName=['ring', 'abc']), 'AND', Terms(Account__CategoryOfInterest=['Clock', 'ring']), 'OR', Terms(Account__HolidayCelebrated=['chrismas'])]
# dsl_query = convert_query(query)


# from elasticsearch_dsl import Search, Q

# def convert_query_to_es_dsl(query):
#     # Initialize a search object
#     search = Search()

#     # Iterate through the query elements
#     for element in query:
#         # Check if the element is a Terms object
#         if isinstance(element, dict) and 'Terms' in element:
#             search = search.filter('terms', **element['Terms'])

#         # Check if the element is the 'AND' operator
#         elif element == 'AND':
#             search = search.query('bool', must=[search.to_dict()])

#         # Check if the element is the 'OR' operator
#         elif element == 'OR':
#             search = Interest_Junction_cDocument.search().query('bool', should=[search.to_dict()])

#     return search


# def build_query(query_list, formula):
#     stack = []
#     for c in formula:
#         if c == ')':
#             temp = []
#             while stack[-1] != '(':
#                 temp.append(stack.pop())
#             stack.pop()

#             if len(temp) == 1:
#                 stack.append(temp[0])
#             else:
#                 q = Q('bool', should=temp[::-1]) if 'OR' in temp else Q('bool', must=temp[::-1])
#                 stack.append(q)
#         elif c == '(':
#             stack.append(c)
#         elif c == ' ':
#             continue
#         elif c == 'A':
#             stack.append("AND")
#         elif c == 'O':
#             stack.append("OR")
#         else:
#             pass
#             # i = int(c)
#             # q = query_list[i][1]
#             # stack.append(q)
#     print(stack)    

    # return stack[0]




# class FindClientApiView(APIView):
#     def get (self,request):
#         interestjunction=Interest_Junction_c.objects.all()
#         serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
#         return Response(serializers.data)

#     def post(self,request):
#     # if request.method == 'POST':
#         data = request.data

#         filters = data.get('filters')
#         formula = data.get('formula')

#         client = connections.get_connection()

#         query = Q()
#         filter_queries = []

#         for index, filter in enumerate(filters):
#             for key, value in filter.items():
#                 if key == 'Junction':
#                     field_name = value.get('fieldName')
#                     logic = value.get('logic')
#                     values = value.get('value')
#                     if logic == 'Equal':
#                         filter_queries.append(Q("terms", **{field_name: values}))
#                 if key == 'Account':
#                     field_name = value.get('fieldName')
#                     logic = value.get('logic')
#                     values = value.get('value')
#                     if logic == 'Equal':
#                         filter_queries.append(Q("terms", **{field_name: values}))

#         for filter_query in filter_queries:
#             if 'OR' in formula:
#                 query |= filter_query
#             else:
#                 query &= filter_query
#         print(query)
#         result = client.search(
#             index='interest_junction_cs',
#             body={
#                 'query': query.to_dict()
#             }
#         )
#         return JsonResponse(result, status=200, safe=False)
    




    # return JsonResponse({'error': 'Only POST method allowed'}, status=400)

    # def post(self,request):
    #     conditions=[]
    #     filters=request.data.get('filters')
    #     formula=request.data.get('formula')
    #     # print(formula)
    #     filterdata=apply_filters(filters,formula)
    #     # print(filterdata)
    #     return Response(filterdata)
    

# from elasticsearch_dsl import Q

# def apply_filters(filters, formula):
#     client = Elasticsearch(["http://localhost:9200"])

#     formula = formula.replace("AND", "&").replace("OR", "|").replace("(", "").replace(")", "")
#     formula_list = [int(x) for x in formula.split(" ") if x.isdigit()]

#     queries = []
#     for i, filter_dict in enumerate(filters):
#         for filter_type, filter_obj in filter_dict.items():
#             field_name = filter_obj["fieldName"]
#             logic = filter_obj["logic"]
#             value = filter_obj["value"]
#             if filter_type == "Junction":
#                 query = Q("terms", **{field_name: value})
#             elif filter_type == "Account":
#                 if logic == "Equal":
#                     query = Q("term", **{field_name: value[0]})
#                 elif logic == "NotEqual":
#                     query = ~Q("term", **{field_name: value[0]})
#                 else:
#                     raise ValueError(f"Invalid logic: {logic}")
#             else:
#                 raise ValueError(f"Invalid filter type: {filter_type}")
#             queries.append(query)

#     final_query = Q("bool", must=[queries[formula_list[0]]])
#     for i in range(1, len(formula_list)):
#     if "(" in formula:
#         start = formula.index("(")
#         end = formula.index(")")
#         sub_formula = formula[start + 1:end].strip()
#         sub_formula_list = [int(x) for x in sub_formula.split(" ") if x.isdigit()]
#         sub_final_query = Q("bool", should=[queries[sub_formula_list[0]]])
#         for j in range(1, len(sub_formula_list)):
#             if "&" in sub_formula:
#                 sub_final_query &= queries[sub_formula_list[j]]
#             elif "|" in sub_formula:
#                 sub_final_query |= queries[sub_formula_list[j]]
#             else:
#                 raise ValueError("Invalid formula")
#         final_query &= sub_final_query
#     else:
#         if "&" in formula:
#             final_query &= queries[formula_list[i]]
#         elif "|" in formula:
#             final_query |= queries[formula_list[i]]
#         else:
#             raise ValueError("Invalid formula")
#     print(final_query)
#     results = client.search(index="interest_junction_cs", body={"query": final_query.to_dict()})

#     return results["hits"]["hits"]
# from .models import *
# from django.db.models import Q

# class FindClientV(APIView):
#     def get (self,request):
#         interestjunction=Interest_Junction_c.objects.all()
#         serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
#         return Response(serializers.data)
    
#     def post(self,request):
#         data=request.data.get('filters')
#         data2=request.data
#         for dicts in data:
#             account=(dicts.get('Account'))
#             junction=(dicts.get('Junction'))
#             print(account.get())
    
#         serializers = InterestJunctionFindClientSerializers( many=True)

#         return Response(serializers.data)
    

# # from django.db.models import Q

# # def filter_records(filters, formula):
# #     query = Q()
# #     formula = formula.replace('AND', '&').replace('OR', '|')
# #     for i, filter in enumerate(filters):
# #         filter_query = Q()
# #         for key, value in filter.items():
# #             if key == 'Junction':
# #                 field_name = value['fieldName']
# #                 logic = value.get('logic', 'Equal')
# #                 if logic == 'Equal':
# #                     filter_query &= Q(**{f'junction__{field_name}': value['value']})
# #                 elif logic == 'NotEqual':
# #                     filter_query &= ~Q(**{f'junction__{field_name}': value['value']})
# #             elif key == 'Account':
# #                 field_name = value['fieldName']
# #                 logic = value.get('logic', 'Equal')
# #                 if logic == 'Equal':
# #                     filter_query &= Q(**{f'junction__account__{field_name}': value['value']})
# #                 elif logic == 'NotEqual':
# #                     filter_query &= ~Q(**{f'junction__account__{field_name}': value['value']})
# #         formula = formula.replace(f'{i}', f'filter_query')
# #     query = eval(formula)
# #     return Interest_Junction_c.objects.filter(query)
# from django.db.models import Q
# from my_app.models import  Interest_Junction_c
# def search_by_json(json_query):
#     filters = json_query.get('filters', [])
#     formula = json_query.get('formula', '')
#     query = Q()
#     print(Interest_Junction_c)
#     for index, f in enumerate(filters):
#         for key, value in f.items():
#             field_name = value['fieldName']
#             logic = value['logic']
#             field_value = value['value']
#             kwargs = {
#                 f'{field_name}__{logic.lower()}': field_value
#             }

#             if key == 'Junction':
#                 query &= Q(interest_junction_c__**kwargs)
#             elif key == 'Account':
#                 query &= Q(interest_junction_c__account__**kwargs)

#     result = Interest_Junction_c.objects.filter(query)

#     return result


# # results= Interest_Junction_c.objects.filter(
# #            Q(InterestName="ring", InterestType="abc") &
# #                 (
# #                     Q(Interest__InterestType="Not Interested", Interest__InterestName="ring") |
# #                     (
# #                         Q(account__CategoryOfInterest__contains="Clock") &
# #                         Q(account__YoungerAudience="younger") &
# #                         Q(account__LastPurchasedDate='12-12-2020') &
# #                         Q(account__HolidayCelebrated="chrismas") &
# #                         (
# #                             Q(account__Email__icontains='test@123.com') &
# #                             Q(account__ShippingCity__contains="New York")
# #                         )
# #                     )
# #                 )
# #             ).select_related('Interest', 'Account')



# #         jsonq= search_by_json(data2) 

# def filter_data(filters, formula):
#     search = Search()
#     query_list = []
#     for i, filter in enumerate(filters):
#         for key in filter:
#             field_name = filter[key]['fieldName']
#             logic = filter[key]['logic']
            
#             values = filter[key]['value']

#             if logic == 'Equal':
#                 query = Q('terms', **{field_name: values})
#             elif logic == 'NotEqual':
#                 query = ~Q('terms', **{field_name: values})
#             elif logic == 'Contains':
#                 query = Q('match', **{field_name: values[0]})
#             query_list.append((i, query))

#     final_query = build_query(query_list, formula)
#     search = Interest_Junction_cDocument.search().query(final_query)
#     return search



# # def build_query(query_list, formula):
# #     stack = []
# #     for c in formula:
# #         if c == ')':
# #             temp = []
# #             while stack[-1] != '(':
# #                 temp.append(stack.pop())
# #             stack.pop()

# #             if len(temp) == 1:
# #                 stack.append(temp[0])
# #             else:
# #                 q = Q('bool', should=temp[::-1])
# #                 stack.append(q)
# #         elif c == '(':
# #             stack.append(c)
# #         elif c == ' ':
# #             continue
# #         elif c == 'A':
# #             stack.append("and")
# #         elif c == 'O':
# #             stack.append("or")
# #         else:
# #             i = int(c)
# #             q = query_list[i][1]
# #             stack.append(q)

# #     final_stack = []
# #     for item in stack:
# #         if item == "and":
# #             final_stack[-2:] = [Q("bool", must=[final_stack[-2], final_stack[-1]])]
# #         elif item == "or":
# #             final_stack[-2:] = [Q("bool", should=[final_stack[-2], final_stack[-1]])]
# #         else:
# #             final_stack.append(item)

# #     return final_stack[0]

# def build_query(query_list, formula):
#     stack = []
#     for c in formula:
#         if c == ')':
#             temp = []
#             while stack[-1] != '(':
#                 temp.append(stack.pop())
#             stack.pop()

#             if len(temp) == 1:
#                 stack.append(temp[0])
#             else:
#                 q = Q('bool', should=temp[::-1])
#                 stack.append(q)
#         elif c == '(':
#             stack.append(c)
#         elif c == ' ':
#             continue
#         elif c == 'A':
#             stack.append("and")
#         elif c == 'O':
#             stack.append("or")
#         else:
#             if c.isdigit():
#                 i = int(c)
#                 q = query_list[i][1]
#                 stack.append(q)

#     final_stack = []
#     for item in stack:
#         if item == "and":
#             final_stack[-2:] = [Q("bool", must=[final_stack[-2], final_stack[-1]])]
#         elif item == "or":
#             final_stack[-2:] = [Q("bool", should=[final_stack[-2], final_stack[-1]])]
#         else:
#             final_stack.append(item)

#     return final_stack[0]
#####----------------------------------------------------------------------------------#######