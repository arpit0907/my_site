from django.urls import path
from . views import Index,Signup,Login,CategoryCreateView,CategoryUpdateView,CategoryDeleteView,ProductCreateView,ProductUpdateView,ProductDeleteView
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', Index.as_view(),name='homepage'),
    path('s/',views.search),

    path('signup',Signup.as_view(), name = 'signup'),
    path('login/',Login.as_view(), name = 'login'),
    path('logout/',views.logout),
    path('details/',views.get_details),
   
    #for manage categories
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/update/<int:pk>', CategoryUpdateView.as_view(), name='category-update'),
    path('<pk>/category/delete/', CategoryDeleteView.as_view()),

    #for manage categories
    path('product/create/', ProductCreateView.as_view(), name='category-create'),
    path('product/update/<int:pk>', ProductUpdateView.as_view(), name='category-update'),
    path('<pk>/product/delete/', ProductDeleteView.as_view()),

]
