from django.urls import path
from .views import PartsListView,PartsDetailView,PartsCreateView ,PartsUpdateView, PartsPurchaseDetailView, PartsPurchaseCreateView  ,PartsListAddView
from .views import PartsReleaseDetailView, PartsReleaseCreateView,LocationCreateView, MoveLocation,PartsSearch,LoadDropdown,MoveLocationTo,PartAddFileCreateView,PartAddFileDeleteView


urlpatterns = [

    path('', PartsListView.as_view(), name='parts-list-page'),
    path('add/', PartsListAddView.as_view(), name='parts-list-add-page'),
    
    path('<int:pk>/', PartsDetailView.as_view(), name='parts-detail-page'), 
    path('new/', PartsCreateView.as_view(), name='parts-new-page'),
    path('update/<int:pk>/', PartsUpdateView.as_view(), name='parts-update-page'),
    
    path('addfile/<int:partid>/', PartAddFileCreateView.as_view(), name='parts-file-add-page'),
    path('deletfile/<int:pk>/', PartAddFileDeleteView.as_view(), name='parts-file-delete-page'),
    

    path('partssearch/', PartsSearch),
    path('loaddropdown/',LoadDropdown),
    path('movelocationto/',MoveLocationTo),
    path('purchase/detail/<int:pk>/', PartsPurchaseDetailView.as_view(), name='parts-purchase-detail-page'),
    path('purchase/<int:partid>/', PartsPurchaseCreateView.as_view(), name='parts-purchase-page'),
    path('location/<int:purchaseid>/', LocationCreateView.as_view(), name='parts-location-page'),
    path('movelocation/<int:pk>/', MoveLocation.as_view(), name='parts-move-location-page'),


    path('release/detail/<int:pk>/', PartsReleaseDetailView.as_view(), name='parts-release-detail-page'),
    path('release/<int:partid>/', PartsReleaseCreateView.as_view(), name='parts-release-page'),

]


