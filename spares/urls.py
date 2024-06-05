from django.urls import path
from spares import views


urlpatterns = [
    
#login register logout

    path('register/', views.register, name='user-register'),
    path('verify-otp/', views.verify, name='verify'),
    path('login/',views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),

#create vehicle cate,brands,parts

    path('vehicle_categories/', views.VehicleCategoriesList.as_view(), name='vehicle_categories_list'),
    path('brands/', views.BrandsList.as_view(), name='brands_list'),
    path('parts_categories/', views.PartsCategoryList.as_view(), name='parts_categories_list'),


#update delete

    path('vehicle_categories/<int:pk>/', views.VehicleCategoryDetail.as_view(), name='vehicle_category_detail'),
    path('brands/<int:pk>/', views.BrandDetail.as_view(), name='brand_detail'),
    path('parts_categories/<int:pk>/', views.PartsCategoryDetail.as_view(), name='parts_category_detail'),

#filter is car/bike

    path('brands/filter/is_car/<int:is_car>/', views.BrandFilterByIsCarView.as_view(), name='brand_filter_by_is_car'),



#filter parts

    path('parts_categories/filter/vehicle/<int:vehicle_id>/', views.PartsCategoryFilterByVehicle.as_view(), name='parts_category_filter_by_vehicle'),
    path('parts_categories/filter/brand/<int:brand_id>/', views.PartsCategoryFilterByBrand.as_view(), name='parts_category_filter_by_brand'),


 # Address CRUD operations
    path('addresses/', views.AddressListCreateView.as_view(), name='address_list_create'),
    path('addresses/<int:pk>/', views.AddressDetailView.as_view(), name='address_detail'),

#Top categories CRUD

    path('Top_categories/', views.TopCategoryListCreateView.as_view(), name='Top_categories_list_create'),
    path('Top_categories/<int:pk>/',views.TopCategoryDetailview.as_view(), name='Top_categories_detail'),

]