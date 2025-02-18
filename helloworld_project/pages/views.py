from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView 
from django.views import View
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product

class HomePageView(TemplateView): 
    template_name = "pages/home.html"

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context

class ProductIndexView(View):
    template_name = 'pages/products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View): 
    template_name = 'pages/products/show.html' 

    def get(self, request, id):
        try:
            product_id = int(id)

            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")

            product = get_object_or_404(Product, pk=product_id)
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))

        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm): 
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

class ProductCreateView(View): 
    template_name = 'pages/products/create.html'
    success_template = 'pages/products/product_created.html'

    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 

    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            product = form.save()  # Save the product instance
            viewData = {
                "title": "Product Created",
                "message": f"Product '{product.name}' created successfully!"
            }
            return render(request, self.success_template, viewData)
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' # This will allow you to loop through 'products' in your template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context

class ContactPageView(TemplateView):
    template_name= 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "email": "abc@cba.com",
            "adress" : "1234 Main St, Springfield, IL 62701",
            "phone": "123-456-7890",
        })

        return context

class CartView(View):
    template_name = 'pages/cart/index.html'

    def get(self, request):
        # Simulated database for products
        products = {}
        products[121] = {'name': 'Tv samsung', 'price': '1000'}
        products[11] = {'name': 'Iphone', 'price': '2000'}
        # Get cart products from session
        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        # Prepare data for the view
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Get cart products from session and add the new product
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')

class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')