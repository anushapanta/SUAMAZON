# anusha
from django.views.generic import View, TemplateView, CreateView, FormView, DetailView, ListView, UpdateView, DeleteView         
from django.contrib.auth import authenticate, login, logout             
from django.shortcuts import render, redirect
from .forms import CheckoutForm, CustomerRegistrationForm, CustomerLoginForm, ProductForm, UserForm,AdminEditForm
from django.core.paginator import Paginator    
from django.urls import reverse_lazy
from django.db.models import Q                  
from django.shortcuts import get_object_or_404

from django.db import transaction
from django.db.models import Case, When, Value, BooleanField
from .models import *                           
from .forms import *                            


class Ecommerce_Mixin(object):                                          
    def dispatch(self, request, *args, **kwargs):                      
        card_id = request.session.get("cart_id")                       
        if card_id:                                                   
            cart_obj = Cart.objects.get(id=card_id)                     
            if request.user.is_authenticated and request.user.customer: 
                try:
                    pre_cart_obj = Cart.objects.get(customer=self.request.user.customer)
                    if pre_cart_obj:
                        cart_obj.cartproduct_set.all().delete()
                        cart_obj.delete()
                        self.request.session['cart_id'] = None
                except:
                    cart_obj.customer = request.user.customer               
                    cart_obj.save()    
                    self.request.session['cart_id'] = None

        return super().dispatch(request, *args, **kwargs)             

class HomeView(Ecommerce_Mixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = Product.objects.all().order_by("-id")      
        paginator = Paginator(all_products, 4)
        page_no = self.request.GET.get('page')               

        product_list = paginator.get_page(page_no)
        context['product_list'] = product_list
        return context
    
class ProductDetailView(Ecommerce_Mixin, TemplateView):
    template_name = "productdetail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_url = self.kwargs['productslug']                              
        product = Product.objects.get(productslug=slug_url)
        product.save()                                                 
        context['product'] = product
        return context

class AddToCartView(Ecommerce_Mixin, TemplateView):   
    template_name = "addtocart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pro_id = self.kwargs['pro_id']       
        pro_obj = Product.objects.get(id=pro_id)                           
        if self.request.user.is_authenticated: 
            try:
                cart_obj = Cart.objects.get(customer=self.request.user.customer)
                this_product_in_cart = cart_obj.cartproduct_set.filter(product=pro_obj)      
                if this_product_in_cart.exists():                          
                    cartproduct = this_product_in_cart.last()              
                    cartproduct.quantity = 1                            
                    cartproduct.subtotal = pro_obj.productprice
                    cartproduct.save()
                    cart_obj.total += pro_obj.productprice
                    cart_obj.save()
                else:
                    cartproduct = CartProduct.objects.create(cart=cart_obj, product=pro_obj, rate=pro_obj.productprice, quantity=1, subtotal=pro_obj.productprice)        
                    cart_obj.total += pro_obj.productprice
                    cart_obj.save()
            except:
                cart_obj = Cart.objects.create(customer=self.request.user.customer, total=0)
                cartproduct = CartProduct.objects.create(cart=cart_obj, product=pro_obj, rate=pro_obj.productprice, quantity=1, subtotal=pro_obj.productprice)        
                cart_obj.total += pro_obj.productprice
                cart_obj.save()          
        return context

class MyCartView(Ecommerce_Mixin, TemplateView):
    template_name = "mycart.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            cart = Cart.objects.get(customer=self.request.user.customer)
            # cart = CartProduct.objects.get(product_id=self.request.user.id)
            print(self.request.user.customer)
        except:
            cart_id = self.request.session.get("cart_id", None)
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
            else:
                cart = None
        context['cart'] = cart
        return context

class ManageCartView(Ecommerce_Mixin, View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]                        
        action = request.GET.get("action")                  
        cp_obj = CartProduct.objects.get(id=cp_id)         
        cart_obj = cp_obj.cart                             
        if action == "inc":                                 
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":                                
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:                         
                cp_obj.delete()                             
            if cart_obj.total == 0:
                cart_obj.delete()
        elif action == "rmv":                                
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
            if cart_obj.total == 0:
                cart_obj.delete()
        else:
            pass
        return redirect("ecomapp:mycart")

class EmptyCartView(Ecommerce_Mixin, View):
    def get(self, request, *args, **kwargs):
        cart_obj = Cart.objects.get(customer=self.request.user.customer)
        if cart_obj and self.request.user.is_authenticated:  
            cart_obj.cartproduct_set.all().delete()                        
            cart_obj.delete()
        else:
            cart_id = request.session.get("cart_id", None)                 
            if cart_id:
                cart = Cart.objects.get(id=cart_id)
                cart.cartproduct_set.all().delete()                        
                cart_obj.delete()
        return redirect("ecomapp:mycart")

class CheckoutView(Ecommerce_Mixin, CreateView):                            
    template_name = "checkout.html"
    form_class = CheckoutForm                               
    success_url = reverse_lazy("ecomapp:payment-sucess")             
    def dispatch(self, request, *args, **kwargs):          
        if request.user.is_authenticated and request.user.customer:        
            pass                                                           
        else:                                                             
            return redirect("/login/?next=/checkout/")                    
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj = Cart.objects.get(customer=self.request.user.customer)
        if cart_obj:
            context['cart'] = cart_obj
        else:
            cart_obj = None
            context['cart'] = cart_obj       
        return context
    def form_valid(self, form):
        cart_obj = Cart.objects.get(customer=self.request.user.customer)
        if cart_obj:           
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.ostatus = "Order Received"
            pm = form.cleaned_data.get("payment_method")               
            order = form.save()                                                 
            order.customer = self.request.user.customer
            order.save()
            cart_obj.customer = None
            cart_obj.save()
        else:                   
            return redirect("ecomapp:home")
        return super().form_valid(form)            

class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("ecomapp:home")
    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        user = User.objects.create_user(username, email, password)     
        form.instance.user = user                                              
        login(self.request, user)
        return super().form_valid(form)   
    def get_success_url(self):
        if "next" in self.request.GET:                     
            next_url = self.request.GET.get("next")
            return next_url                                 
        else:                                               
            return self.success_url                         

class CustomerLogoutView(View):                         
    def get(self, request):
        logout(request)                                 
        return redirect("ecomapp:home")

class CustomerLoginView(Ecommerce_Mixin, FormView):                   
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("ecomapp:home")
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)                    
        if usr is not None and Customer.objects.filter(user=usr).exists():                  login(self.request, usr)
        else: return render(self.request, self.template_name, {"form": self.form_class, "error": "Incorrect credentials"})
        return super().form_valid(form)                 
    def get_success_url(self):                          
        if "next" in self.request.GET:                  
            next_url = self.request.GET.get("next")     
            return next_url                             
        else:                                          
            return self.success_url                     

class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"
    def dispatch(self, request, *args, **kwargs):                          
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists(): pass
        else:             return redirect("/login/?next=/profile/")
                          
        return super().dispatch(request, *args, **kwargs)               


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer                          
        context['customer'] = customer
        orders = Order.objects.filter(customer=customer).order_by("-id")
        context["orders"] = orders
        return context

class CustomerProfileEditView(View): 
    template_name = "customerprofileupdate.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        customer_obj = get_object_or_404(Customer, pk=id)       

        user_id = customer_obj.user_id

        user_obj = get_object_or_404(User, pk=user_id)

        try:
            child_obj = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            child_obj = None
        

        user_form = UserForm(instance=user_obj)
        child_form = CustomerEditForm(instance=child_obj)

        return render(request, self.template_name, {
                'user_form': user_form,
                'child_form': child_form,
            })

    
    def post(self,  request, *args, **kwargs):
        id = kwargs.get('id')
        customer_obj = get_object_or_404(Customer, pk=id)       

        user_id = customer_obj.user_id

        user_obj = get_object_or_404(User, pk=user_id)

        try:
            child_obj = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            child_obj = None

        user_form = UserForm(request.POST, instance=user_obj)
        child_form = CustomerEditForm(request.POST, instance=child_obj)

        if user_form.is_valid() and child_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                password = user_form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                user.save()
                child_instance = child_form.save(commit=False)
                child_instance.user = user_obj
                child_instance.save()
                logout(request)
            return redirect("ecomapp:home")
        else:
            return render(request, self.template_name, {
                'user_form': user_form,
                'child_form': child_form,
            })

class CustomerOrderDetailView(DetailView):

    template_name = "customerorderdetail.html"
    model = Order

    context_object_name = "ord_obj"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)

            if request.user.customer != order.customer:
                return redirect("ecomapp:customerprofile")

        else:
            return redirect("/login/?next=/profile/")
            
        return super().dispatch(request, *args, **kwargs)

class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        kw = self.request.GET.get("keyword")                    

        results = Product.objects.filter(Q(producttitle__icontains=kw) | Q(productdescription__icontains=kw))           
        print(results)
        
        context["results"] = results
        return context

########### ADMIN SECTION 

class AdminRegisterView(TemplateView):

    template_name = "adminpages/outadminregister.html"
    success_url = reverse_lazy("ecomapp:adminuserslist")

    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ['adminpages/adminregister.html'] 
        return [self.template_name]  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = UserForm(self.request.POST)
            context['child_form'] = AdminRegistrationForm(self.request.POST)
        else:
            context['user_form'] = UserForm()
            context['child_form'] = AdminRegistrationForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        child_form = AdminRegistrationForm(request.POST)
        
        if user_form.is_valid() and child_form.is_valid():
            return self.form_valid(user_form, child_form)
        else:
            return self.form_invalid(user_form, child_form)

    def form_valid(self, user_form, child_form):
        with transaction.atomic():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password']) 
            user.save()
            child = child_form.save(commit=False)
            child.user = user
            child.save()
        return redirect(self.success_url)

    def form_invalid(self, user_form, child_form):
        return self.render_to_response(self.get_context_data(user_form=user_form, child_form=child_form))
    
class AdminLoginView(FormView):
    template_name = "adminpages/adminlogin.html"
    form_class = CustomerLoginForm                      
    success_url = reverse_lazy("ecomapp:adminhome")

    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        
        usr = authenticate(username=uname, password=pword)

        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid credentials"})
        
        return super().form_valid(form)

class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect("/adminlogin/")
        return super().dispatch(request, *args, **kwargs)

class AdminListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminuserslist.html"
    context_object_name = "alladmins"

    def get_queryset(self):
        user = self.request.user
        queryset = Admin.objects.annotate(
            is_owner=Case(
                When(user=user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            )
        ).order_by('-is_owner')
        return queryset 

class AdminUserUpdateView(AdminRequiredMixin, View):
    template_name = "adminpages/adminregister.html"

    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        admin_obj = get_object_or_404(Admin, pk=id)      

        user_id = admin_obj.user_id
        user_obj = get_object_or_404(User, pk=user_id)

    
        try:
            child_obj = Admin.objects.get(id=id)
        except Admin.DoesNotExist:
            child_obj = None
        

        user_form = UserForm(instance=user_obj)
        child_form = AdminEditForm(instance=child_obj)

        return render(request, self.template_name, {
                'user_form': user_form,
                'child_form': child_form,
            })

 

    def post(self, request, *args, **kwargs):
        id = kwargs.get('id')
        admin_obj = get_object_or_404(Admin, pk=id)    

        user_id = admin_obj.user_id
        user_obj = get_object_or_404(User, pk=user_id)

        try:
            child_obj = Admin.objects.get(id=id)
        except Admin.DoesNotExist:
            child_obj = None

        user_form = UserForm(request.POST, instance=user_obj)
        child_form = AdminRegistrationForm(request.POST, instance=child_obj)

        if user_form.is_valid() and child_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                password = user_form.cleaned_data.get('password')
                if password:
                    user.set_password(password)
                user.save()
                child_instance = child_form.save(commit=False)
                child_instance.user = user_obj
                child_instance.save()
                logout(request)
            return redirect("ecomapp:home")
        else:
            return render(request, self.template_name, {
                'user_form': user_form,
                'child_form': child_form,
            })

class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = "adminpages/adminhome.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["pendingorders"] = Order.objects.filter(ostatus="Order Received").order_by("-id")
        context["totalusers"] = User.objects.all() 
        context["totalcategory"] = Category.objects.all() 
        context["totalproducts"] = Product.objects.all() 


        return context

class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = "adminpages/adminorderdetail.html"
    model = Order
    context_object_name = "ord_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["allstatus"] = ostatus

        return context

class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminorderlist.html"
    queryset = Order.objects.all().order_by("-id")
    context_object_name = "allorders"

class AdminOrderStatuChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        order_id = self.kwargs["pk"]

        order_obj = Order.objects.get(id=order_id)

        new_status = request.POST.get("status")
        order_obj.ostatus = new_status

        order_obj.save()

        return redirect(reverse_lazy("ecomapp:adminorderdetail", kwargs={"pk": order_id}))
 
class AdminProductListView(AdminRequiredMixin, ListView):
    template_name = "adminpages/adminproductlist.html"
    queryset = Product.objects.all().order_by("-id")
    context_object_name = "allproducts"

class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/adminproductcreate.html"
    form_class = ProductForm
    success_url = reverse_lazy("ecomapp:adminproductlist")                 

    def form_valid(self, form):
        p = form.save()                                                    

        images = self.request.FILES.getlist("more_images")                  
        
        for i in images:                                                   
            ProductImage.objects.create(product=p, image=i)                 

        return super().form_valid(form)

class AdminDeleteProduct(AdminRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("ecomapp:adminproductlist")  

class AdminUpdateProduct(AdminRequiredMixin, View):
    def get(self, request, id):              
                                              
        
        edit_record = Product.objects.get(id=id)         

        print (edit_record)
        form = ProductForm(instance=edit_record)
        return render(request, 'adminpages/adminproductcreate.html', {'form':form})
    
    def post(self, request, id):
        edit_record = Product.objects.get(pk=id)
        
     
        form = ProductForm(request.POST, instance=edit_record)  
            
        if form.is_valid():
            form.save()                                         
            return redirect("ecomapp:adminproductlist")   

class AdminCategoryCreateView(AdminRequiredMixin, CreateView):
    template_name = "adminpages/admincategorycreate.html"
    form_class = CategoryForm
    success_url = reverse_lazy("ecomapp:admincategorylist")               

    def form_valid(self, form):
        form.save()                                    
        return super().form_valid(form)
    
class AdminCategoryList(AdminRequiredMixin, ListView):
    template_name = "adminpages/admincategorylist.html"
    queryset = Category.objects.all()
    context_object_name = "allCategory"
    
class AdminDeleteCategory(AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy("ecomapp:admincategorylist")  
    
class AdminUpdateCategory(AdminRequiredMixin, View):   
    def get(self, request, id):                                                                   
        edit_record = Category.objects.get(id=id)                
        form = CategoryForm(instance=edit_record)
        return render(request, 'adminpages/admincategorycreate.html', {'form':form})
    
    def post(self, request, id):
        edit_record = Category.objects.get(pk=id) 
        form = CategoryForm(request.POST, instance=edit_record)             
        if form.is_valid(): return redirect("ecomapp:admincategorylist")   
        
class PaymentSucess(Ecommerce_Mixin, TemplateView):
    template_name = "payment-sucess.html"
    
class AllProductsView(Ecommerce_Mixin, TemplateView):
    template_name = "allproducts.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allcategories'] = Category.objects.all().order_by("-id")    
        return context

