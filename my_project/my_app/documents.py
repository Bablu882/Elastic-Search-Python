from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry
from my_app.models import Interest,Account,Product,Interest_Junction_c,Opportunity

@registry.register_document
class InterestDocument(Document):
    class Index:
        name = 'interests'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Interest
         fields = [
             'InterestID',
             'InterestName',
             'ApprovalStatus'
         ]


@registry.register_document
class AccountDocument(Document):
    class Index:
        name = 'accounts'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Account
         fields = [
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
             'BouncedEmail',
             'OwnerId'
         ]         


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Product
         fields = [
             'Productid',
             'ProductName',
         ]


@registry.register_document
class Interest_Junction_cDocument(Document):
    Account=fields.ObjectField(properties={
        'Accountid':fields.TextField(),
        'AccountName':fields.TextField(),
        'State':fields.TextField(),
        'LastPurchasedDate':fields.DateField(format='yyyy-MM-dd',ignore_malformed=True),
        'TotalPurchase':fields.TextField(),
        'PersonHasOptedOutOfEmail':fields.TextField(),
        'CategoryOfInterest':fields.TextField(),
        'PeriodOfInterest':fields.TextField(),
        'TypeOfInterest':fields.TextField(),
        'YoungerAudience':fields.TextField(),
        'Star5':fields.TextField(),
        'AccountLastPurchaseDate':fields.DateField(format='yyyy-MM-dd',ignore_malformed=True),
        'HolidayCelebrated':fields.TextField(),
        'Email':fields.TextField(),
        'ShippingCity':fields.TextField(),
        'BouncedEmail':fields.TextField(),
        'OwnerId':fields.TextField()

    })
    Product=fields.ObjectField(properties={
        # 'Productid':fields.TextField(),
        "ProductName":fields.TextField(),
        "Productid":fields.TextField()
    })
    Interest=fields.ObjectField(properties={
        'InterestID':fields.TextField(),
        'InterestName':fields.TextField(),
        'ApprovalStatus':fields.TextField(),
        # 'InterestType':fields.TextField()
    })
    # type = fields.TextField(attr='type_to_string')

    class Index:
        name = 'interest_junction_cs'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Interest_Junction_c
         fields = [
            'InterestNameJunction',
            'InterestName',
            'InterestJunctionID',
            'link_With',
            'InterestType'

         ]         



@registry.register_document
class OpportunityDocument(Document):
    AccountId=fields.ObjectField(properties={
        'Accountid':fields.TextField(),
        'AccountName':fields.TextField(),
        'State':fields.TextField(),
        'LastPurchasedDate':fields.TextField(),
        'TotalPurchase':fields.TextField(),
        'PersonHasOptedOutOfEmail':fields.TextField(),
        'CategoryOfInterest':fields.TextField(),
        'PeriodOfInterest':fields.TextField(),
        'TypeOfInterest':fields.TextField(),
        'YoungerAudience':fields.TextField(),
        'Star5':fields.TextField(),
        'AccountLastPurchaseDate':fields.TextField(),
        'HolidayCelebrated':fields.TextField(),
        'Email':fields.TextField(),
        'ShippingCity':fields.TextField(),
        'BouncedEmail':fields.TextField(),
        'OwnerId':fields.TextField()

    })

    class Index:
        name = 'opportunitys'
    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Opportunity
         fields = [
             'OpportunityId',
             'OpportunityName',
             'StageName',
             'Billing_City',
             'AverageitemSold'
         ]         