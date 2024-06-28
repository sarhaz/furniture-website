from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Team, Blog, Comments
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPage(View):
    def get(self, request):
        search = request.GET.get('search')
        if not search:
            products = Product.objects.all()
            comments = Comments.objects.all()
            blogs = Blog.objects.all()
            context = {
                "products": products,
                "comments": comments,
                "blogs": blogs,
            }
            return render(request, 'index.html', context)
        else:
            products = Product.objects.filter(name__icontains=search)
            if products:
                context = {
                    "products": products,
                    "comments": Comments.objects.all(),
                    "blogs": Blog.objects.all()
                }
                return render(request, 'index.html', context)
            else:
                context = {
                    "products": products,
                    "comments": Comments.objects.all(),
                    "blogs": Blog.objects.all()
                }
                return render(request, 'index.html', context)


class UpdateProductView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        context = {
            "product": product,
        }
        return render(request, 'update_product.html', context)

    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.name = request.POST['name']
        product.price = request.POST['price']
        product.description = request.POST['description']
        product.price_type = request.POST['price_type']

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect("index")


class DeleteProductView(LoginRequiredMixin, View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        product.delete()
        return redirect("index")


class ShopPage(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search')
        if not search:
            products = Product.objects.all()
            context = {
                "products": products,
            }
            return render(request, 'shop.html', context)
        else:
            products = Product.objects.filter(name__icontains=search)
            if products:
                context = {
                    "products": products,
                }
                return render(request, 'shop.html', context)
            else:
                context = {
                    "products": products,
                }
                return render(request, 'shop.html', context)


class CartPage(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        total_price = 0
        for product in products:
            total_price += product.price
        total_shipping_price = total_price + 10
        context = {
            "products": products,
            "total_price": total_price,
            "total_shipping_price": total_shipping_price,
        }
        return render(request, 'cart.html', context)


class AboutPage(LoginRequiredMixin, View):
    def get(self, request):
        team = Team.objects.all()
        comments = Comments.objects.all()
        context = {
            "team": team,
            "comments": comments,
        }
        return render(request, 'about.html', context)


class ContactPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'contact.html')


class ServicePage(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        comments = Comments.objects.all()
        context = {
            'products': products,
            'comments': comments,
        }
        return render(request, 'services.html', context)


class BlogPage(LoginRequiredMixin, View):
    def get(self, request):
        blogs = Blog.objects.all()
        comments = Comments.objects.all()
        context = {
            "blogs": blogs,
            "comments": comments,
        }
        return render(request, 'blog.html', context)


class ThanksPage(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'thankyou.html')


class CheckoutPage(LoginRequiredMixin, View):
    def get(self, request):
        products = Product.objects.all()
        total_price = 0
        for product in products:
            total_price += product.price
        total_shipping_price = total_price + 10
        context = {
            "products": products,
            "total_price": total_price,
            "total_shipping_price": total_shipping_price,
        }
        return render(request, 'checkout.html', context)