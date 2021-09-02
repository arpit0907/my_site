from django.shortcuts import render,redirect
from .models import Products, Category, Customer
from django.views import View
from django.contrib.auth.hashers import make_password,check_password
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView,View
from .forms import CreateCategoryForm,UpdateCategoryForm,CreateProductForm,UpdateProductForm
from django.contrib import messages
from django.views.generic.edit import DeleteView


# Create your views here.
class Index(View):
    def get(self, request):
        """Get Products From Data on the Basis of id and all Products"""
        category_ID         = request.GET.get('category')
        categories          = Category.get_all_categories()
        if category_ID:
            products        = Products.get_product_by_id(category_ID)
        else:
            products     = Products.objects.all()
        data                = {}
        data['products']    = products
        data['categories']  = categories
        return render(request, 'index.html', data)

def search(request):
    """Search for products on the basis of input given by the user"""
    try:
        query = request.GET.get('search')
    except:
        query=None
    if query:
        products = Products.objects.filter(name__icontains=query)
        return render(request, 'search.html',{'products':products})
    else:
        return render(request, 'search.html')

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        mobile = postData.get('mobile')
        email = postData.get('email')
        password = postData.get('password')

        value = {'first_name': first_name,
                 'last_name': last_name,
                 'mobile': mobile,
                 'email': email}

        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            mobile=mobile,
                            email=email, password=password)

        error_message = self.validateCustomer(customer)
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('/')
        else:
            data = {'error': error_message, 'values': value}
            return render(request, 'signup.html', data)
    
    def validateCustomer(self, customer):
        """Check all inputs and sign up if all fields are vailid"""
        error_message = None
        if not customer.first_name:
            error_message = 'First Name Required !'
        elif len(customer.first_name) < 4:
            error_message = 'First Name Must be four Char Long or more !'
        elif not customer.last_name:
            error_message = 'Last Name Required !'
        elif len(customer.first_name) < 4:
            error_message = 'Last Name Must be four Char Long or more !'
        elif not customer.mobile:
            error_message = 'mobile number required !'
        elif len(customer.mobile) < 10:
            error_message = 'mobile number must be 10 digit !'
        elif len(customer.password) < 6:
            error_message = 'password must be 6 char long !'
        elif customer.isExists():
            error_message = 'Email already Registerd !'

        return error_message

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.getcustomer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer_id'] = customer.id
                request.session['email'] = customer.email                
                return redirect('homepage')
            else:
                error_message = 'Email or Password Invailid!!!'
        else:
            error_message = 'Email or Password Invailid!!!'

        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('/')


def get_details(request):
    """Get Details About the Products"""
    prodcut_detail = request.GET.get('product_id')
    products = Products.objects.filter(id=prodcut_detail)
    return render(request,'details.html',{'products':products})

class CategoryCreateView(CreateView):
    model = Category
    form_class = CreateCategoryForm
    success_url = '/category/list/'

    def form_valid(self, form, **kwargs):
        name = self.request.POST.get('name')
        category = form.save(commit=False)
        category.name = name
        category.created_by = self.request.user
        category.save()
        return redirect(self.success_url)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = UpdateCategoryForm
    template_name = 'product/category_update.html'
    success_url = '/category/list/'
   
    def form_valid(self, form, **kwargs):
        category = form.save(commit=False)
        category.created_by = self.request.user
        category.save()
        messages.success(self.request, 'Practice area updated successfully!')
        return redirect(self.success_url)

class CategoryListView(ListView):
    model = Category
    ordering = ['name']
    form_class = CreateCategoryForm
    template_name = 'products/category_list.html'
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['createcategoryform'] = CreateCategoryForm
        return context

class CategoryDeleteView(DeleteView):
    model = Category
    success_url ="/category/list/"
    
class ProductCreateView(CreateView):
    model = Products
    form_class = CreateProductForm
    success_url = '/product/list/'

    def form_valid(self, form, **kwargs):
        name = self.request.POST.get('name')
        product = form.save(commit=False)
        product.created_by = self.request.user
        product.save()
        return redirect(self.success_url)

class ProductListView(ListView):
    model = Products
    ordering = ['name']
    form_class = CreateProductForm
    template_name = 'products/products_list.html'
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['createproductform'] = CreateProductForm
        return context

class ProductUpdateView(UpdateView):
    model = Products
    form_class = UpdateProductForm
    template_name = 'product/products_update.html'
    success_url = '/product/list/'
   
    def form_valid(self, form, **kwargs):
        product_obj = form.save(commit=False)
        product_obj.created_by = self.request.user
        product_obj.save()
        messages.success(self.request, 'Practice area updated successfully!')
        return redirect(self.success_url)


class ProductDeleteView(DeleteView):
    model = Products
    success_url ="/product/list/"        