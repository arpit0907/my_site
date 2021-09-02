from django.urls import path
from . views import Index,Signup,Login,CategoryCreateView,CategoryUpdateView,CategoryDeleteView,ProductCreateView,ProductUpdateView,ProductDeleteView,ProductListView,CategoryListView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('index/', Index.as_view(),name='homepage'),
    path('s/',views.search),

    path('signup/',Signup.as_view(), name = 'signup'),
    path('',Login.as_view(), name = 'login'),
    path('logout/',views.logout),
    path('details/',views.get_details),
   
    #for manage categories
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='category-update'),
    path('category/list/', CategoryListView.as_view(), name='category-list'),
    path('<pk>/category/delete/', CategoryDeleteView.as_view(), name='category-delete'),

    #for manage categories
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='product-update'),
    path('product/list/', ProductListView.as_view(), name='product-list'),
    path('<pk>/product/delete/', ProductDeleteView.as_view(),name='product-delete'),

]
