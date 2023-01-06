from django.urls import path
from .views import *

urlpatterns=[
    path('',test,name='test'),
    path('api/save-accounts/',AccountList.as_view()),
    path('api/save-contacts/',ContactList.as_view()),
    path('api/save-interests/',InterestList.as_view()),
    path('api/save-interestjunctions/',InterestJunctionList.as_view()),
    path('api/save-products/',ProductList.as_view()),
    path('api/search-search/',SearchInterest.as_view()),
    path('api/search_interest/',SearchListInterest.as_view()),
    path('api/search_account/',SearchListAccount.as_view()),
    path('api/search_product/',SearchListProduct.as_view()),
    path('api/find_client/',SearchClientInterest.as_view())
]