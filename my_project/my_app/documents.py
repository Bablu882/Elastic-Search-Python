from django_elasticsearch_dsl import Document,fields
from django_elasticsearch_dsl.registries import registry
from my_app.models import Interest,Account,Product,Interest_Junction_c

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
             'id',
             'InterestID',
             'InterestName',
             'InterestType',
             'ApprovalStatus',
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
             'id',
             'Accountid',
             'AccountName',
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
             'id',
             'Productid',
             'ProductName',
         ]


@registry.register_document
class Interest_Junction_cDocument(Document):
    Account=fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'Accountid':fields.TextField(),
        'AccountName':fields.TextField(),
    })
    Contact=fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'Contactid':fields.TextField(),
        'ContactName':fields.TextField(),
    })
    Product=fields.ObjectField(properties={
        'id':fields.IntegerField(),
        # 'Productid':fields.TextField(),
        "ProductName":fields.TextField(),
        "Productid":fields.TextField()
    })
    Interest=fields.ObjectField(properties={
        'id':fields.IntegerField(),
        'InterestID':fields.TextField(),
        'InterestName':fields.TextField(),
        'InterestType':fields.TextField(),
        'ApprovalStatus':fields.TextField(),
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
             'id',
             'InterestJunctionID',
             'Category_of_Interest_c',
             'Maker_Artist_Interest_c',
             'Period_of_Interest_c',
             'Material_Theme_c',


         ]         