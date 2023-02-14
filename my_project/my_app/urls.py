from django.urls import path,include,re_path
from .views import *


# from rest_framework import routers
# router=routers.DefaultRouter()
# router.register(r'api/account_allmethod',AccountView)
# router.register(r'api/product_allmethod',ProductView)
# router.register(r'api/interest_allmethod',InterestView)
# router.register(r'api/interest_junction_allmethod',Interest_Junction_cView)
# router.register(r'api/opportunity_allmethod',OpportunityView)

urlpatterns=[
    re_path('python/', include([

    # path('',include(router.urls)),
    # path('api-auth',include('rest_framework.urls')),
    path('',test,name='test'),
    path('api/save-accounts/',AccountList.as_view()),
    path('api/save-opportunity/',OpportunityList.as_view()),
    path('api/save-interests/',InterestList.as_view()),
    path('api/save-interestjunctions/',InterestJunctionList.as_view()),
    path('api/save-products/',ProductList.as_view()),
    path('api/search_junction/',SearchInterestJunction.as_view()),
    path('api/search_interest/',SearchListInterest.as_view()),
    path('api/search_account/',SearchListAccount.as_view()),
    path('api/search_product/',SearchListProduct.as_view()),
    path('api/search_opportunity/',SearchListOpportunity.as_view()),
    path('api/find_client/',ClientFind.as_view()),
    # path('api/search_all/',SearchAllApi.as_view()),
    path('api/save-get-update-bulk-product/',ProductApiVIew.as_view()),
    path('api/save-get-update-bulk-account/',AccountApiVIew.as_view()),
    path('api/save-get-update-bulk-interest/',InterestApiVIew.as_view()),
    path('api/save-get-update-bulk-opportunity/',OpportunityApiVIew.as_view()),
    path('api/save-get-update-bulk-interestjunction/',InterstJunctionApiVIew.as_view()),
    path('api/get-delete-account/',AccountDelete.as_view()),
    path('api/get-delete-interest/',InterestDelete.as_view()),
    path('api/get-delete-product/',ProductDelete.as_view()),
    path('api/get-delete-opportunity/',OpportunityDelete.as_view()),
    path('api/get-delete-interestjunction/',InterestJunctionDelete.as_view()),
    path('api/get-delete-bulk-account/',AccountBulkDelete.as_view()),
    path('api/find/',ClientFind.as_view()),
    path('api/v-2/find_client/',FindClientNewVersionApi.as_view()),
    path('api/v2/find_client/',FindClientApiView.as_view()),
    path('api/v4/find_client/',FindClientNew.as_view()),
    # path('api/find',FindClientV.as_view()),
])),


]


