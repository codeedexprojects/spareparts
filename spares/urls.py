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


 # Profile CRUD operations
    path('profile/<int:id>/', views.UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('user-reg/', views.UserProfileCreateView.as_view(), name='user-register'),
   

#Top categories CRUD

    path('Top_categories/', views.TopCategoryListCreateView.as_view(), name='Top_categories_list_create'),
    path('Top_categories/<int:pk>/',views.TopCategoryDetailview.as_view(), name='Top_categories_detail'),


#offer products filter

    path('offer_products/<int:is_offer>/',views.PartsFilterbyIsofferView.as_view(), name='offer_products_List'),


#review LIST CRETAE DELETE
    path('reviews/', views.ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

#cart

    path('add-to-cart/<int:user_id>/<int:parts_id>', views.AddToCartView.as_view(), name='cart-add-product'),
    path('view-cart/<int:user_id>/', views.UserCartView.as_view(), name='user_cart'),
    path('update-cart/<int:user_id>/<int:cart_item_id>/', views.UpdateCartView.as_view(), name='update_cart'),
    path('delete-cart-item/<int:user_id>/<int:cart_item_id>/', views.DeleteCartItemView.as_view(), name='delete_cart_item'),
   
    
#Filter by car/ike

    path('parts_categories/filter/<int:is_car>/', views.PartsCategoryFilterByVehicleType.as_view(), name='parts_category_filter_by_vehicle_type'),

#Filter by Top-Categories

    path('Top_categories/filter/<int:parts_Cat>/', views.PartsCategoryFilterByTopCategories.as_view(), name='parts_category_filter_by_TOP_Cat'),

#checkout 
    path('checkout/<int:user_id>/<int:cart_id>/', views.CheckoutView.as_view(), name='checkout'),
]