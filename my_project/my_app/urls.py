from django.urls import path,include
from .views import *

from rest_framework import routers
router=routers.DefaultRouter()
router.register(r'api/account_allmethod',AccountView)
router.register(r'api/product_allmethod',ProductView)
router.register(r'api/interest_allmethod',InterestView)
router.register(r'api/interest_junction_allmethod',Interest_Junction_cView)
router.register(r'api/opportunity_allmethod',OpportunityView)

urlpatterns=[
    path('',include(router.urls)),
    # path('api-auth',include('rest_framework.urls')),
    path('',test,name='test'),
    path('api/save-accounts/',AccountList.as_view()),
    path('api/save-opportunity/',OpportunityList.as_view()),
    path('api/save-interests/',InterestList.as_view()),
    path('api/save-interestjunctions/',InterestJunctionList.as_view()),
    path('api/save-products/',ProductList.as_view()),
    # path('api/search-search/',SearchInterest.as_view()),
    # path('api/search_interest/',SearchListInterest.as_view()),
    # path('api/search_account/',SearchListAccount.as_view()),
    # path('api/search_product/',SearchListProduct.as_view()),
    # path('api/find_client/',SearchClientInterest.as_view()),
    # path('api/search_all/',SearchAllApi.as_view()),
    path('api/save-get-update-bulk-product/',ProductApiVIew.as_view()),
    path('api/save-get-update-bulk-account/',AccountApiVIew.as_view()),
    path('api/save-get-update-bulk-interest/',InterestApiVIew.as_view()),
    path('api/save-get-update-bulk-opportunity/',OpportunityApiVIew.as_view()),
    path('api/save-get-update-bulk-interestjunction/',InterstJunctionApiVIew.as_view())
]


