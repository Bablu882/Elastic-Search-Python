from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from my_app.models import Interest,Account,Product

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