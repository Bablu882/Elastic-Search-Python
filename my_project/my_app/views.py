from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response
# from my_app.documents import InterestDocument,AccountDocument,ProductDocument,Interest_Junction_cDocument
from my_app.documents import AccountDocument,ProductDocument,InterestDocument,Interest_Junction_cDocument,OpportunityDocument
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


# ###---------------------------------search_account api-----------------------------------------###

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


# ###-----------------------------search_product api-----------------------------------------###

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
###---------------------opportunity search---------------------------------------------###
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


# ###-----------------------------find client search interest junction--------------------###
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


class InterstJunctionApiVIew(APIView):
    def get(self,request,format=None):
        opp=Interest_Junction_c.objects.all()
        serializers=InterestJunctionSerializers(opp,many=True)
        return Response(serializers.data)

    def post(self,request,format=None):
        data=request.data.get('data')
        print(data)  
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
                if not account and not product and not interest:
                    gets=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                    gets.link_With=linkwith
                    gets.InterestNameJunction=interestnamejunction
                    gets.InterestName=interestname
                    gets.Account=None
                    gets.Product=None
                    gets.Interest=None
                    gets.save()
                else:
                    if not Account.objects.filter(Accountid=account).exists():
                        return Response({"error":"Accountid does not exists in Account table ",'Accountid':account,'InterestJunctionID':interest})
                    
                    if not Product.objects.filter(Productid=product).exists():     
                        return Response({"error":"Product does not exists in InterstJunction table ",'Productid':product,'InterestJunctionid':interestjunctionid})    
                    
                    if not Interest.objects.filter(InterestID=interest).exists():     
                        return Response({"error":"Interst does not exists in InterestJunction table ",'Interestid':interest,'InterestJunctionID':interestjunctionid})   
                    prod=Product.objects.get(Productid=product)    
                    acc=Account.objects.get(Accountid=account)
                    intr=Interest.objects.get(InterestID=interest)

                    gets1=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                    gets1.link_With=linkwith
                    gets1.InterestNameJunction=interestnamejunction
                    gets1.InterestName=interestname
                    gets1.Account=acc
                    gets1.Product=prod
                    gets1.Interest=intr  
                    gets1.save() 
            else:
                if not account and not product and not interest:
                    produc=Interest_Junction_c.objects.create(
                        InterestJunctionID=interestjunctionid,
                        link_With=linkwith,
                        InterestNameJunction=interestnamejunction,
                        InterestName=interestname
                    )   
                else:
                    if not Account.objects.filter(Accountid=account).exists():
                        return Response({"error":"Accountid does not exists in Account table ",'Accountid':account,'InterestJunctionID':interest})
                    
                    if not Product.objects.filter(Productid=product).exists():     
                        return Response({"error":"Product does not exists in InterstJunction table ",'Productid':product,'InterestJunctionid':interestjunctionid})    
                    
                    if not Interest.objects.filter(InterestID=interest).exists():     
                        return Response({"error":"Interst does not exists in InterestJunction table ",'Interestid':interest,'InterestJunctionID':interestjunctionid})    
                        
                    prod1=Product.objects.get(Productid=product)    
                    acc1=Account.objects.get(Accountid=account)
                    intr1=Interest.objects.get(InterestID=interest)    
                    produce=Interest_Junction_c.objects.create(
                    InterestJunctionID=interestjunctionid,
                    link_With=linkwith,
                    InterestNameJunction=interestnamejunction,
                    InterestName=interestname,
                    Account=acc1,
                    Product=prod1,
                    Interest=intr1
                    ) 
        return Response({'msg':'InterestJunction created or updated success !'}) 



        


# class InterestJunctionApiVIew(APIView):
#     def get(self,request,format=None):
#         interest=Interest_Junction_c.objects.all()
#         serializers=InterestJunctionSerializers(interest,many=True)
#         return Response(serializers.data)

#     def post(self,request,format=None):
#         data=request.data.get('data')
#         print(data)  
#         for dicts in data:
#             print(dicts)
            # interestjunctionid=dicts['InterestJunctionID']
            # print(interestjunctionid)
            # linkwith=dicts['link_With']
            # account=dicts['Account']
            # interest=dicts['Interest']
            # product=dicts['Product']
            # interestnamejunction=dicts['InterestNameJunction']
            # interestname=dicts['InterestName']
#             if Interest_Junction_c.objects.filter(InterestJunctionID=interestjunctionid).exists():
#                 if not product:
#                     if not Account.objects.filter(Accountid=account).exists():
#                         return Response({"error":"accpunt not exists"})
#                     if not Interest.objects.filter(InterestID=interest).exists():
#                         return Response({'error':'interst not exists'})    
#                     acc=Account.objects.get(Accountid=account)
#                     print(acc)    
#                     intrst=Interest.objects.get(InterestID=interest)
#                     gets=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
                    # gets.link_With=linkwith
                    # gets.InterestNameJunction=interestnamejunction
                    # gets.InterestName=interestname
                    # gets.Account=acc
                    # gets.Product=None
                    # gets.Interest=intrst
                    # gets.save()
#                 if not account:
#                     if not Product.objects.filter(Productid=product).exists():
#                         return Response({"error":"product not exists"})
#                     if not Interest.objects.filter(InterestID=interest).exists():
#                         return Response({'error':'interst not exists'})
#                     interest1=Interest.objects.get(InterestID=interest)
#                     product1=Product.objects.get(Productid=product)
#                     gets1=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets1.link_With=linkwith
#                     gets1.InterestNameJunction=interestnamejunction
#                     gets1.InterestName=interestname
#                     gets1.Account=None
#                     gets1.Product=product1
#                     gets1.Interest=interest1
#                     gets1.save()  
#                 if not interest:
#                     if not Product.objects.filter(Productid=product).exists():
#                         return Response({"error":"product not exists"})
#                     if not Account.objects.filter(Accountid=account).exists():
#                         return Response({'error':'account not exists'})
#                     account2=Account.objects.get(Accountid=account)
#                     product2=Product.objects.get(Productid=product)
#                     gets2=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets2.link_With=linkwith
#                     gets2.InterestNameJunction=interestnamejunction
#                     gets2.InterestName=interestname
#                     gets2.Account=account2
#                     gets2.Product=product2
#                     gets2.Interest=None
#                     gets2.save()  
#                 if not account and not product:  
#                     if not Interest.objects.filter(InterestID=interest).exists():
#                         return Response({'error':'interest not exists'})
#                     interest3=Interest.objects.get(InterestID=interest)
#                     gets3=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets3.link_With=linkwith
#                     gets3.InterestNameJunction=interestnamejunction
#                     gets3.InterestName=interestname
#                     gets3.Account=None
#                     gets3.Product=None
#                     gets3.Interest=interest3
#                     gets3.save() 
#                 if not account and not interest:
#                     if not Product.objects.filter(Productid=product).exists():
#                         return Response({'error':'product not exists'})
#                     product4=Product.objects.get(Productid=product)
#                     gets4=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets4.link_With=linkwith
#                     gets4.InterestNameJunction=interestnamejunction
#                     gets4.InterestName=interestname
#                     gets4.Account=None
#                     gets4.Product=product4
#                     gets4.Interest=None
#                     gets4.save() 

#                 if not interest and not product:
#                     if not Account.objects.filter(Accountid=account).exists():
#                         return Response({'error':'account not exists'})
#                     account5=Account.objects.get(Accountid=account)
#                     gets5=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets5.link_With=linkwith
#                     gets5.InterestNameJunction=interestnamejunction
#                     gets5.InterestName=interestname
#                     gets5.Account=account5
#                     gets5.Product=None
#                     gets5.Interest=None
#                     gets5.save() 
#                 if not account and not product and not interest:
#                     gets6=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets6.link_With=linkwith
#                     gets6.InterestNameJunction=interestnamejunction
#                     gets6.InterestName=interestname
#                     gets6.Account=None
#                     gets6.Product=None
#                     gets6.Interest=None
#                     gets6.save() 
#                 if account and product and interest is not None:
#                     if not Product.objects.filter(Productid=product).exists():
#                         return Response({"error":"product not exists"})
#                     if not Account.objects.filter(Accountid=account).exists():
#                         return Response({'error':'account not exists'})
#                     if not Interest.objects.filter(InterestID=interest):
#                         return Response({"error":"account not exist"})    
#                     interest6=Interest.objects.get(InterestID=interest)    
#                     account6=Account.objects.get(Accountid=account)
#                     product6=Product.objects.get(Productid=product)
#                     gets7=Interest_Junction_c.objects.get(InterestJunctionID=interestjunctionid)
#                     gets7.link_With=linkwith
#                     gets7.InterestNameJunction=interestnamejunction
#                     gets7.InterestName=interestname
#                     gets7.Account=account6
#                     gets7.Product=product6
#                     gets7.Interest=interest6
#                     gets7.save()  


#             else:
#                 pass
#                 # if not accountid:
#                 #     prod=Opportunity.objects.create(
#                 #         OpportunityId=opportunityid,
#                 #         OpportunityName=opportunityname,
#                 #         StageName=stagename,
#                 #         Billing_City=billingcity,
#                 #         AverageitemSold=avarageitemsold,
#                 #     )   
#                 # else:
#                 #     if not Account.objects.filter(Accountid=accountid).exists():     
#                 #         return Response({"error":"Accountid does not exists in Account table ",'Accountid':accountid,'Opportunityid':opportunityid})
#                 #     else:
#                 #         accou=Account.objects.get(Accountid=accountid)
#                 #         prod=Opportunity.objects.create(
#                 #         OpportunityId=opportunityid,
#                 #         OpportunityName=opportunityname,
#                 #         StageName=stagename,
#                 #         Billing_City=billingcity,
#                 #         AverageitemSold=avarageitemsold,
#                 #         AccountId=accou
#                 #     )     
#         return Response({'msg':'interest created or updated success !'})        



class AccountDelete(APIView):
    def get(self,request,format=None):
        get=Account.objects.all()
        serial=AccountSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('Accountid')
        if not Account.objects.filter(Accountid=data).exists():
            return Response({'error':'Account not exist with this id ','id':data})
        account=Account.objects.get(Accountid=data)
        account.delete()
        return Response({'message':'Account deleted successfully'})
        
class InterestDelete(APIView):
    def get(self,request,format=None):
        get=Interest.objects.all()
        serial=InterestSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('InterestID')
        if not Interest.objects.filter(InterestID=data).exists():
            return Response({'error':'Product not exists with this id','id':data})
        interest=Interest.objects.get(InterestID=data)
        interest.delete()
        return Response({'message':'Interest deleted successfully'})
                
class ProductDelete(APIView):
    def get(self,request,format=None):
        get=Product.objects.all()
        serial=ProductSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('Productid')
        if not Product.objects.filter(Productid=data).exists():
            return Response({'error':'Product not exists with this id','id':data})
        product=Product.objects.get(Productid=data)
        product.delete()
        return Response({'message':'Product  deleted successfully'})


class OpportunityDelete(APIView):
    def get(self,request,format=None):
        get=Opportunity.objects.all()
        serial=OpportunitySerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('OpportunityId')
        if not Opportunity.objects.filter(OpportunityId=data).exists():
            return Response({'error':'Opportunity not exists with this id','id':data})
        oppor=Opportunity.objects.get(OpportunityId=data)
        oppor.delete()
        return Response({'message':'Opportunity  deleted successfully'})


class InterestJunctionDelete(APIView):
    def get(self,request,format=None):
        get=Interest_Junction_c.objects.all()
        serial=InterestJunctionSerializers(get,many=True)
        return Response(serial.data)

    def post(self,request,format=None):
        data=request.data.get('InterestJunctionID')
        if not Interest_Junction_c.objects.filter(InterestJunctionID=data).exists():
            return Response({'error':'InterstJunction not exists with this id','id':data})
        junc=Interest_Junction_c.objects.get(InterestJunctionID=data)    
        junc.delete()
        return Response({'message':'InterstJunction deleted successfully'})
       


