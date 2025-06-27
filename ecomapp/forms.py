from django import forms
from .models import Order, Customer, Product, Admin, Category
from django.contrib.auth.models import User

# user login form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    class Meta:
        model = User
        fields = ["username","email", "password"]
        
    # admin registration form          
class AdminRegistrationForm(forms.ModelForm):
    adminfullname = forms.CharField(widget=forms.TextInput())
    adminimage = forms.ImageField(required=False, widget=forms.FileInput(attrs={            
        "class": "form-control",            
        "multiple": True                   
    }))     
    adminmobile = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = Admin                   
        fields = ["adminfullname","adminmobile", "adminaddress","adminimage"]  
    def clean_username(self):              
        uname = self.cleaned_data.get("username")       
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "Adminname already taken")
        return uname



# customer registration form
class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())


    class Meta:
        model = Customer                    
        fields = ["username", "password", "email", "customerfullname", "customeraddress", "customermobile"]


    def clean_username(self):             
        uname = self.cleaned_data.get("username")
        
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError(
                "username already exists.")

        return uname



# customer login form
class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

# category creation for the product
class CategoryForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = ["categorytitle", "categoryslug"]
     

# individual product page
class ProductForm(forms.ModelForm):
    
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={           
        "class": "form-control",            
        "multiple": True                  
    }))

    class Meta:           
        model = Product     

        fields = ["producttitle", "productslug", "categoryname", "image", "productprice", "productdescription"]

         
        widgets = {
            "producttitle": forms.TextInput(attrs={                       
                "class": "form-control",                            
                "placeholder": "Product Title"    
            }),
            "productslug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product Slug"
            }),
            "categoryname": forms.Select(attrs={                       
                "class": "form-control"
            }),
            "image": forms.ClearableFileInput(attrs={                
                "class": "form-control"
            }),
            "productprice": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Price"
            }),
            "productdescription": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Product Description",
                "rows": 3
            }),

        }

# customer my profile edit
class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customerfullname", "customeraddress", "customermobile"]


# customer my profile edit
class AdminEditForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ["adminfullname", "adminaddress", "adminmobile"]

#form when user will place order
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["productorderedby", "productshippingaddress", "mobile", "email"]


