from django.urls import path
from .views import *                            


app_name = "ecomapp"

urlpatterns = [
    path("", HomeView.as_view(), name="home"), # first page after website opens
    path("register/",CustomerRegistrationView.as_view(), name="customerregistration"), # customer register
    path("logout/", CustomerLogoutView.as_view(), name="customerlogout"), #logout
    path("login/", CustomerLoginView.as_view(), name="customerlogin"), # customer login

    path("profile/", CustomerProfileView.as_view(), name="customerprofile"), # custoemr profile show
    path("editprofile/<int:id>", CustomerProfileEditView.as_view(), name="editprofile"), # customer profile edit

    path("profile/order-<int:pk>/", CustomerOrderDetailView.as_view(),name="customerorderdetail"), # order detail of customer

    path("search/", SearchView.as_view(), name="search"), # home search

    path("adminlogin/", AdminLoginView.as_view(), name="adminlogin"), # admin login
    path("adminregister/", AdminRegisterView.as_view(), name="adminregister"),
    path("adminhome/", AdminHomeView.as_view(), name="adminhome"),
    path("adminorder/<int:pk>/", AdminOrderDetailView.as_view(),name="adminorderdetail"),
    path("adminallorders/", AdminOrderListView.as_view(), name="adminorderlist"),
    path("adminorder-<int:pk>-change/",AdminOrderStatuChangeView.as_view(), name="adminorderstatuschange"),
    path("admincategory/add/", AdminCategoryCreateView.as_view(), name="admincategorycreate"),
    path("admincategory/list/", AdminCategoryList.as_view(), name="admincategorylist"),
    path('admincategorydelete/<int:pk>/', AdminDeleteCategory.as_view(), name="admincategorydelete"),
    path('admincategoryupdate/<int:id>/', AdminUpdateCategory.as_view(), name="admincategoryupdate"),  
    path("adminproduct/list/", AdminProductListView.as_view(), name="adminproductlist"),
    path("adminproduct/add/", AdminProductCreateView.as_view(), name="adminproductcreate"),
    path('adminproductdelete/<int:pk>/', AdminDeleteProduct.as_view(), name="adminproductdelete"),
    path('adminproductupdate/<int:id>/', AdminUpdateProduct.as_view(), name="adminproductupdate"),
    path("adminusers/list/", AdminListView.as_view(), name="adminuserslist"),
    path('adminuserupdate/<int:id>/', AdminUserUpdateView.as_view(), name="adminuserupdate"),
    
    path("paymentsucess/", PaymentSucess.as_view(), name="payment-sucess"),
    path("allproducts/", AllProductsView.as_view(), name="allproducts"),
    path("product/<slug:productslug>/", ProductDetailView.as_view(), name="productdetail"),         
    
    path("addtocart-<int:pro_id>/", AddToCartView.as_view(), name="addtocart"),
    path("mycart/", MyCartView.as_view(), name="mycart"),
    path("managecart/<int:cp_id>/", ManageCartView.as_view(), name="managecart"),
    path("emptycart/", EmptyCartView.as_view(), name="emptycart"),

    path("checkout/", CheckoutView.as_view(), name="checkout"),
    

]
