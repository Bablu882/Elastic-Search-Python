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


# Testing
def test(request):
    return render(request,'my_app/test.html')



###--------------------------SAVE AND GET ACCOUNT API---------------------------------###

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

# ###--------------------------SAVE AND GET INTEREST------------------------------------###

class InterestList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest.objects.all()
    serializer_class=InterestSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###-----------------------------SAVE AND GET INTEREST JUNCTION API-------------------------------###

class InterestJunctionList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Interest_Junction_c.objects.all()
    serializer_class=JunctionSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 

# ###------------------------------SAVE AND GET PRODUCT API---------------------------------------###

class ProductList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs) 



# ####----------------------------------SEARCH INTEREST API---------------------------------------###
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


# ###---------------------------------SEARCH ACCOUNT API-----------------------------------------###

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
                    'Accountid',
                    'PersonHasOptedOutOfEmail',
                    'CategoryOfInterest'
                ],
                fuzziness='auto')
            search=AccountDocument().search().query(q)
    
            # search=AccountDocument.search().filter(Q('fuzzy',Accountid=datas)|Q('fuzzy',AccountName=datas))
            print([result for result in search])
            serial=AccountSerializers(search,many=True)
        return Response(serial.data)


# ###-----------------------------SEARCH PRODUCT API-----------------------------------------###

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

###---------------------------OPPORTUNITY SEARCH API---------------------------------------###

class SearchListOpportunity(APIView):
    def get(self,request,format=None):
        opportunity=Opportunity.objects.all()
        serializers=OpportunitySerializers(opportunity,many=True)        
        return Response(serializers.data)

    def post(self,request,format=None):
        serializers=OpportunitySearchSerializers(data=request.data)
        if serializers.is_valid(raise_exception=True):
            datas=serializers.data.get('searchopportunity')
            query=datas
            q = Q(
                'multi_match',
                query=query,
                fields=[
                    'OpportunityId',
                    'OpportunityName',
                    'AccouontId.Accountid',
                ],
                fuzziness='auto')
            search=OpportunityDocument().search().query(q)
            serial=OpportunitySerializersPost(search,many=True)
        return Response(serial.data) 


# ###-----------------------------SEARCH INTEREST JUNCTION API ---------------------------------###
class SearchInterestJunction(APIView):
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
                


###------------------------SAVE AND GET OPPORTUNITY API------------------------------------###

class OpportunityList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Opportunity.objects.all()
    serializer_class=OpportunitySerializers

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):

        return self.create(request,*args,**kwargs) 



###-------------------------------------CREATE SINGLE API -------------------------------------------####

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


class ProductApiVIew(APIView):
    def get(self,request,format=None):
        product=Product.objects.all()
        serializers=ProductSerializers(product,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        update=[]
        create=[]
        data=request.data.get('data')
        for dicts in data:
            print(dicts)
            productid=dicts['Productid']
            productname=dicts['ProductName']
            if Product.objects.filter(Productid=productid).exists():
                gets=Product.objects.get(Productid=productid)
                gets.ProductName=productname
                gets.save()
                update.append(str(gets))
            else:
                prod=Product.objects.create(Productid=productid,ProductName=productname)
                create.append(str(prod))

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
                update.append(str(gets))
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
                create.append(str(prod))   
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
            interesttype=dicts['InterestType']
            if Interest.objects.filter(InterestID=Interestid).exists():
                gets=Interest.objects.get(InterestID=Interestid)
                gets.InterestName=interestname
                gets.ApprovalStatus=approvalstatus
                gets.InterestType=interesttype
                gets.save()
                update.append(str(gets))
            else:
                prod=Interest.objects.create(InterestID=Interestid,
                InterestName=interestname,
                ApprovalStatus=approvalstatus,
                InterestType=interesttype)
                create.append(str(prod))    
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

            if Interest_Junction_c.objects.filter(InterestJunctionID=interestjunctionid).exists():
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
                        gets3.Account=None
                        gets3.Product=prod3
                        gets3.Interest=intr3  
                        gets3.save()
                        update.append(str(gets3)) 
            else:
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
            if not Interest_Junction_c.objects.filter(InterestJunctionID=junctionid).exists():
                fail=({'error':'InterstJunction not exists with this id','InterestJunctionid':junctionid})
                failed.append(fail)
            else:    
                junc=Interest_Junction_c.objects.get(InterestJunctionID=junctionid)    
                junc.delete()
        return Response({'InterestJunction deleted !':'success','Failed to delete':failed})
       


###-------------------------------------ACCOUNT BULK DELETE API--------------------------------###

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

class ClientFind(APIView):
    def get(self,request,format=None):
        data=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(data,many=True)
        return Response(serializers.data)
    def post(self,request,format=None):
        getaccountid=[]
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
        # print(opportunityfiltercondition)
        opportunityfilter=data[7]
        opportunitycolumn=opportunityfilter['OpportunityFilter']
        opportunitystagename=opportunitycolumn[0]
        opportunitybillingcity=opportunitycolumn[1]
        opportunityavarageitemsold=opportunitycolumn[2]
        # print(opportunityavarageitemsold)
        # print(opportunitystagename)
        # print(opportunitybillingcity)
        interestitem=interestname['InterestName']
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
                        'Account.LastPurchasedDtae',
                    ]
                    )
            elif lastpurchasedatefilter['FilterLogic'] == 'Not Equal':
                qz9=Q('bool', must_not=[Q('term',**{'Account.LastPurchaseDtae':lastpurchasedatefilter['FieldValue']})])

            elif lastpurchasedatefilter['FilterLogic'] == 'Greater than':
                qz10=Q('bool', filter=[Q('range',**{'Account.LastPurchasedDtae': {'gte':lastpurchasedatefilter['FieldValue'],'format':'dd-mm-yy'}})])

            else:
                qz11=Q('bool', filter=[Q('range',**{'Account.LastPurchasedDtae': {'lte':lastpurchasedatefilter['FieldValue'],'format':'dd-mm-yy'}})])
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
                        'Account.LastPurchasedDtae',
                    ]
                    )
            elif lastpurchasedatefilter['FilterLogic'] == 'NotEqual':
                qz20=Q('bool', must_not=[Q('match',**{'Account.LastPurchaseDtae':lastpurchasedatefilter['FieldValue']})])

            elif lastpurchasedatefilter['FilterLogic'] == 'Greater than':
                # qz10=Q('bool', must=[Q('range',**{'Account.LastPurchaseDtae':{"gte":{lastpurchasedatefilter['FieldValue']}}})])
                qz21=Q('range', **{'Account.LastPurchaseDtae': {"gte":lastpurchasedatefilter['FieldValue']}})

            else:
                qz22=Q('range', **{'Account.LastPurchaseDtae': {"lte":lastpurchasedatefilter['FieldValue']}})
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
        
        xy=qz1&qz6&qz4&qz8&qz2&qz3&qz5&qz7&qz9&qz10&qz11|qz12|qz13|qz14|qz15|qz16|qz17|qz18|qz19|qz20|qz21|qz22&qz23&qz24&qz25&qz26&qz27&qz28|qz29|qz30|qz31|qz32|qz33|qz34&qz35&qz36&qz37&qz38&qz39&qz40|qz41|qz42|qz43|qz44|qz45|qz46|qz|qz80
        # print(xy)
        search=Interest_Junction_cDocument.search().query(xy)
        serial1=InterestJunctionFindClientSerializers(search,many=True)        
        return Response(serial1.data) 

        

 ###-----------------------------------FIND CLIENT VERSION 2-------------------------------------------###       
            
def handle_filter(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        return Q('terms', **{field_name: field_value})
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
        return Q('term',**{field_name:"NULL"})

def handle_filter_term(field_name, filter_logic, field_value):
    if filter_logic == 'Includes':
        return Q(
            'multi_match',
            query=field_value,
            fields=[
                field_name
            ],fuzziness='auto')
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
        return Q('term',**{field_name:"NULL"})            
        
class FindClientNewVersionApi(APIView):
    def get (self,request):
        interestjunction=Interest_Junction_c.objects.all()
        serializers=InterestJunctionFindClientSerializers(interestjunction,many=True)
        return Response(serializers.data)
        
    def post(self,request):
        getaccountid=[]
        interestcondition=request.data.get('InterestCondition')
        interestname=request.data.get('InterestName')
        accountfilters=request.data.get('AccountFilters')
        interestfilters=request.data.get('InterestFilters')
        opportunityfilters=request.data.get('OpportunityFilters')

        queries = [
        handle_filter(accountfilters['CategoryOfInterestFieldName'], accountfilters['CategoryOfInterestFilterLogic'], accountfilters['CategoryOfInterestFieldValue']),
        handle_filter(accountfilters['YoungerAudienceFieldName'], accountfilters['YoungerAudienceFilterLogic'], accountfilters['YoungerAudienceFieldValue']),
        handle_filter(accountfilters['HolidayCelebratedFieldName'], accountfilters['HolidayCelebratedFilterLogic'], accountfilters['HolidayCelebratedFieldValue']),
        handle_filter(accountfilters['LastPurchaseDateFieldName'], accountfilters['LastPurchaseDateFilterLogic'], accountfilters['LastPurchaseDateFieldValue'])
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
        if interestcondition == 'AND':
            final_query0=Q('terms', **{'InterestName': interestname})
        else:
            final_query0=Q('terms', **{'InterestName': interestname})    
        if accountfilters['AccountFiltersCondition'] == 'AND':
            final_query = reduce(and_, queries)
        else:
            final_query=reduce(or_,queries)    
        if accountfilters['EmailCondition'] == 'AND':
            final_query2=reduce(and_,queries2)
        else:
            final_query2=reduce(or_,queries2)
        if interestfilters['InterestFilterCondition'] == 'AND':
            final_query3=reduce(and_,queries3)
        else:
            final_query3=reduce(or_,queries3)
        if opportunityfilters['OpportunityFilterCondition'] == 'AND':
            final_query4=reduce(and_,queries4)        
        else:
            final_query4=reduce(or_,queries4)    
        opportunity_search=OpportunityDocument.search().query(final_query4)
        serial=OpportunitySerializersPost(opportunity_search,many=True)
        for x in serial.data:
           od2 = json.loads(json.dumps(x))
           dictaccount=(od2['AccountId'])
           getaccount=(dictaccount['Accountid'])
           getaccountid.append(str(getaccount))        
        opportunity_query=Q('terms' ,**{'Account.Accountid':getaccountid})
        result_query=(final_query0&final_query&final_query2&final_query3) |(final_query0)|(final_query)|(final_query2)|(final_query3)|(opportunity_query)
        search=Interest_Junction_cDocument.search().query(result_query)
        serializer=InterestJunctionFindClientSerializers(search,many=True)
        return Response(serializer.data)