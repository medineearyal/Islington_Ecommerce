from babel.numbers import format_decimal
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib import messages
import json
from .forms import ProductForm, ImageFormSet, DescriptionFormSet, CategoryForm, ProductColorsForm
from .models import Product, Category, ProductColors


# Create your views here.
class ProductDetailView(DetailView):
    template_name = "products/detail.html"
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        reviews = product.reviews.all().order_by("-created")

        try:
            related_categories = [child.pk for child in product.category.parent.get_children()]
            related_products = Product.objects.filter(category__pk__in=related_categories).exclude(pk=product.pk)
        except:
            related_products = Product.objects.none()

        paginator = Paginator(reviews, 5)

        try:
            page_number = int(self.request.GET.get("page"))
            all_reviews_so_far = reviews[:page_number * paginator.per_page]
            page = paginator.get_page(page_number)

            context = {
                "page": page,
                "reviews_so_far": all_reviews_so_far,
                "product": product,
            }

            if page_number:
                return render(request, "partials/products/reviews_list.html", context)

            return render(request, self.template_name, context=context)

        except TypeError:
            all_reviews_so_far = reviews[:1 * paginator.per_page]
            page = paginator.get_page(1)

            context = {
                "reviews_so_far": page,
                "page": page,
                "product": product,
                "related_products": related_products,
            }

            return render(request, self.template_name, context=context)

    def get_object(self, queryset=None):
        return get_object_or_404(
            Product.objects.prefetch_related(
                "product_image",
                "colors",
                "attribute_set__attributes",
                "descriptions"
            ), slug=self.kwargs["slug"])


def product_detail_modal(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return TemplateResponse(request, "partials/products/product_detail_modal.html",{"product": product,})


class CartView(TemplateView):
    template_name = "partials/products/cart.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        action = request.GET.get("action")
        product_id = kwargs.get("pk")
        cart = request.session.get("cart", {})
        quantity = request.GET.get("quantity")

        toast_message = {}

        if action == "add":
            product = get_object_or_404(Product, id=product_id)

            if product.stock <= 0:
                toast_message["text"] = "Sorry, the item has been sold out."
                toast_message["tag"] = "alert-info"
                response = HttpResponse()
                response["HX-Trigger"] = json.dumps({
                    "showMessage": {
                        "text": toast_message["text"],
                        "tag": toast_message["tag"],
                    }
                })
                return response

            if product.seller == request.user:
                toast_message["text"] = "Sorry, you can't buy your own product"
                toast_message["tag"] = "alert-info"
                response = HttpResponse()
                response["HX-Trigger"] = json.dumps({
                    "showMessage": {
                        "text": toast_message["text"],
                        "tag": toast_message["tag"],
                    }
                })
                return response

            if str(product_id) in cart:
                if quantity:
                    cart[str(product_id)]["quantity"] += int(quantity)
                else:
                    cart[str(product_id)]["quantity"] += 1
            else:
                cart[str(product_id)] = {
                    "name": product.name,
                    "quantity": int(quantity) if quantity else 1,
                    "price": float(product.price),
                    "discounted_price": float(product.discounted_price),
                    "discount": product.discount,
                    "thumbnail": product.thumbnail.url,
                    "stock": product.stock,
                    "category": product.category.name,
                }
            request.session["cart"] = cart
            toast_message["text"] = "Product Successfully Added To The Cart."
            toast_message["tag"] = "alert-success"
        elif action == "remove":
            cart = request.session.get("cart")
            cart.pop(str(product_id), None)
            request.session["cart"] = cart
            toast_message["text"] = "Product Successfully Removed From The Cart."
            toast_message["tag"] = "alert-success"
        elif action == "update":
            if str(product_id) in cart:
                if cart[str(product_id)]["quantity"] != quantity:
                    cart[str(product_id)]["quantity"] = quantity
                    toast_message["text"] = "Product Successfully Updated In The Cart."
                    toast_message["tag"] = "alert-success"

        total_price = sum(
            [int(item["quantity"]) * float(item["price"] if not item["discount"] else item["discounted_price"]) for item
             in cart.values()])

        extra_update_html = f"""
        <span id="cart-count" hx-swap-oob="true" class="absolute -top-1 -right-1 bg-[var(--clr-gray-00)] text-[var(--clr-secondary-700)] text-xs w-5 h-5 flex items-center justify-center rounded-full">
            {len(cart)}
        </span>
        
        <span id="total-price" hx-swap-oob="true">
            Rs. {format_decimal(total_price, format="#,##,##0.00", locale="ne_NP")}
        </span>
        
        <span class="text-[var(--clr-gray-600)]" id="cart-items-inner" hx-swap-oob="true">({len(cart)})</span>
        """

        context.update({
            "cart": cart,
            "total_price": total_price,
        })

        template_string = render_to_string(self.template_name, context, request=request)
        final_html = template_string + extra_update_html

        response = HttpResponse(final_html, content_type="text/html")
        response["HX-Trigger"] = json.dumps({
            "showMessage": {
                "text": toast_message["text"],
                "tag": toast_message["tag"],
            }
        })
        return response


def add_to_compare(request, product_id):
    compare = request.session.get('compare', [])

    if product_id in compare:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    if len(compare) >= 3:
        messages.error(request, "You can only compare up to 3 products.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    compare.append(product_id)
    request.session['compare'] = compare
    messages.success(request, "Product added to compare.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_compare(request, product_id):
    compare = request.session.get('compare', [])
    if product_id in compare:
        compare.remove(product_id)
        request.session['compare'] = compare
        messages.success(request, "Product removed from comparison.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


def compare_products(request):
    compare_ids = request.session.get('compare', [])
    products = Product.objects.filter(id__in=compare_ids)
    products = sorted(products, key=lambda p: compare_ids.index(p.id))

    request.session['compare'] = [p.id for p in products]

    return render(request, 'dashboard/compare_items.html', {'products': products, "active_nav": "compare"})


@login_required
def product_create(request):
    product = Product(seller=request.user)
    form = ProductForm(request.POST or None, instance=product)
    image_fs = ImageFormSet(request.POST or None, request.FILES or None, instance=product, prefix="images")
    description_fs = DescriptionFormSet(request.POST or None, instance=product, prefix="descriptions")

    if request.method == "POST":
        if all([form.is_valid(), image_fs.is_valid(), description_fs.is_valid()]):
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            image_fs.instance = product
            description_fs.instance = product
            image_fs.save()
            description_fs.save()
            return redirect("users:seller_products")

    return render(request, "partials/products/product_create_modal.html", {
        "form": form,
        "image_fs": image_fs,
        "description_fs": description_fs,
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, instance=product)
    image_fs = ImageFormSet(request.POST or None, request.FILES or None, instance=product, prefix="img")
    description_fs = DescriptionFormSet(request.POST or None, instance=product, prefix="desc")

    if request.method == "POST":
        if all([form.is_valid(), image_fs.is_valid(), description_fs.is_valid()]):
            form.save()
            image_fs.save()
            description_fs.save()
            return redirect("users:seller_products")

    return render(request, "partials/products/product_create_modal.html", {
        "form": form,
        "image_fs": image_fs,
        "description_fs": description_fs,
    })


class CategoryView(CreateView):
    model = Category
    template_name = "products/category_create.html"
    form_class = CategoryForm
    success_url = reverse_lazy("products:create_category")


class ProductColorsView(CreateView):
    model = ProductColors
    template_name = "products/colors_create.html"
    form_class = ProductColorsForm
    success_url = reverse_lazy("products:create_color")
