# Create your views here.
import json
from allauth.core.internal.httpkit import redirect
from django import http
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, DetailView, UpdateView, ListView
from django.urls import reverse

from apps.common.forms import AddressForm
from apps.common.models import AddressModel
from apps.orders.constants import OrderStatusEnum
from apps.orders.models import Order
from apps.products.forms import ProductReviewForm, ProductForm, ImageFormSet, DescriptionFormSet
from apps.products.models import ProductReview, Product
from django.contrib import messages
from django.db.models import Q
from apps.users.constants import UserTypeEnum
from apps.users.forms import UserSignupForm, UserProfileForm

User = get_user_model()


class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super(UserDashboardView, self).get_context_data(**kwargs)

        orders = Order.objects.filter(customer=self.request.user).order_by('-created')
        recent_orders = orders[:7]
        total_orders = orders.count()
        pending_orders = orders.filter(transaction__is_payment_success=False).count()
        completed_orders = orders.filter(transaction__is_payment_success=True).count()

        context.update({
            "recent_orders": recent_orders,
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "completed_orders": completed_orders,
            "active_nav": "dashboard",
        })
        return context


class UserOrdersView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders = Order.objects.filter(customer=self.request.user).order_by('-created')
        paginator = Paginator(orders, 12)
        page_num = self.request.GET.get("page")
        orders = paginator.get_page(page_num)

        context.update({
            "orders": orders,
            "active_nav": "order-history",
        })

        return context


class UserOrderDetailView(LoginRequiredMixin, DetailView):
    template_name = "dashboard/order_detail.html"
    model = Order
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review_forms = []

        products = self.object.products

        for key in products:
            product = Product.objects.get(pk=int(key))
            try:
                existing_review = ProductReview.objects.get(
                    product=product, review_from=self.request.user
                )
                form = ProductReviewForm(instance=existing_review, prefix=str(product.pk))
            except ProductReview.DoesNotExist:
                form = ProductReviewForm(prefix=str(product.pk))

            review_forms.append((product, form))

        context.update({
            "active_nav": "order-history",
            "review_forms": review_forms,
            "products": products,
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        valid = True
        review_forms = []

        products = json.loads(self.object.products)

        for key, product in products.items():
            try:
                existing_review = ProductReview.objects.get(
                    product_id=int(key), review_from=request.user
                )
                form = ProductReviewForm(
                    request.POST, instance=existing_review, prefix=str(key)
                )
            except ProductReview.DoesNotExist:
                form = ProductReviewForm(request.POST, prefix=str(key))

            if form.is_valid():
                review = form.save(commit=False)
                instance = get_object_or_404(Product, pk=int(key))
                review.product = instance
                review.review_from = request.user
                review.save()
                messages.success(request, "Review submitted Successfully. Thank You..")
            else:
                messages.success(request, "There was an Issue. Please Try Again..")
                valid = False

            review_forms.append((product, form))
            review_forms.append((product, form))

        if valid:
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context.update({
            "review_forms": review_forms
        })
        return self.render_to_response(context)


class UserOrderTrack(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/track_orders.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "active_nav": "track-order",
        })
        return context


class UserOrderTrackDetail(LoginRequiredMixin, DetailView):
    template_name = "dashboard/track_order_detail.html"
    model = Order
    slug_url_kwarg = "uuid"
    slug_field = "uuid"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = json.loads(self.object.products)

        logs = self.object.status_logs.all()

        steps = []
        all_statuses = [choice[0] for choice in OrderStatusEnum.choices]

        for status in all_statuses:
            log = logs.filter(status=status).first()
            steps.append({
                'key': status,
                'label': dict(OrderStatusEnum.choices)[status],
                'completed': log is not None,
                'timestamp': log.created if log else None,
            })

        completed_steps = sum(step['completed'] for step in steps)
        progress_percent = (completed_steps - 1) / (len(steps) - 1) * 100 if completed_steps > 0 else 0

        logs = self.object.status_logs.select_related("updated_by").all()

        context.update({
            "active_nav": "track-order",
            "products": products,
            "progress_percent": progress_percent,
            "steps": steps,
            "logs": logs,
        })

        return context


AddressFormSet = inlineformset_factory(
    User,
    AddressModel,
    form=AddressForm,
    extra=1,
    can_delete=True,
)


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "dashboard/profile.html"
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("users:profile", kwargs={"pk": self.object.pk})

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.method == "POST":
            context["address_formset"] = AddressFormSet(self.request.POST, instance=self.object)
        else:
            context["address_formset"] = AddressFormSet(instance=self.object)

        context["active_nav"] = "settings"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        address_formset = context["address_formset"]

        if address_formset.is_valid():
            self.object = form.save()
            address_formset.instance = self.object
            address_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        address_formset = context["address_formset"]

        print("Form errors:", form.errors)
        print("Formset errors:", address_formset.errors)
        return super().form_invalid(form)


class UserShopView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/my_shop.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(seller=self.request.user)

        total_products = products.count()

        product_ids = list(products.values_list('id', flat=True))
        q = Q()
        for pid in product_ids:
            q |= Q(**{"products__has_key": str(pid)})
            print(Order.objects.filter(products__has_key=str(pid)))


        seller_products_order_qs = Order.objects.filter(q)
        total_products_sold = seller_products_order_qs.count()

        total_shipping_completed = seller_products_order_qs.filter(status=OrderStatusEnum.DELIVERED).count()

        context.update({
            "active_nav": "seller-products",
            "products": products,
            "total_products": total_products,
            "total_products_sold": total_products_sold,
            "total_shipping_completed": total_shipping_completed,
            "orders": seller_products_order_qs,
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = self.request.user

        if user.user_type != UserTypeEnum.SELLER:
            raise http.Http404("Sorry, The Page was Not Found.")
        elif not user.is_verified_seller:
            raise http.Http404("Sorry, You are not verified yet. Please Contact the Admin To Resolve the Issue.")
        else:
            context.update({
                "seller": request.user,
            })

        return self.render_to_response(context)
