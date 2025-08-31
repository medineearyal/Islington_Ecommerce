from itertools import product

from allauth.core.internal.httpkit import redirect
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404

from apps.common.admin import admin_site
from apps.common.utils import send_async_email
from apps.orders.constants import PaymentStatusEnum
from apps.orders.forms import SellerPaymentForm
from apps.orders.models import Order, KhaltiTransaction, Transaction, SellerPayment
from apps.orders.signals import payment_successful
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse

from apps.products.models import Product
from apps.users.constants import UserTypeEnum

# Create your views here.
User = get_user_model()


class SuccessView(LoginRequiredMixin, TemplateView):
    template_name = "pages/success_failure.html"
    login_url = reverse_lazy("account_login")

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)

        data = self.request.GET

        tid = data.get("tid")

        if tid:
            pidx = data.get("pidx")
            status = data.get("status")
            tidx = data.get("tidx")
            mobile = data.get("mobile")

            transaction = get_object_or_404(Transaction, uuid=tid)

            context.update({
                "tid": tid,
                "success": True,
            })

            recipient_list = []

            order = transaction.order
            if order.use_billing_address and order.customer.billing_address:
                recipient_list.append(order.customer.billing_address.email)
            else:
                recipient_list.append(order.email)

            if pidx:
                khalti_transaction = get_object_or_404(KhaltiTransaction, pidx=pidx, transaction=transaction)

                # modified field suggests at what time the actual Khalti Transaction Succeeed or Failed
                if status == PaymentStatusEnum.COMPLETED.label:
                    khalti_transaction.status = PaymentStatusEnum.COMPLETED
                    khalti_transaction.tidx = tidx
                    khalti_transaction.mobile = mobile
                    khalti_transaction.transaction.is_payment_success = True
                    khalti_transaction.modified = timezone.now()
                elif status == PaymentStatusEnum.CANCELED.label:
                    khalti_transaction.status = PaymentStatusEnum.CANCELED
                    khalti_transaction.modified = timezone.now()

                khalti_transaction.transaction.save()
                khalti_transaction.save()
                context.update({
                    "khalti_transaction": khalti_transaction,
                    "success": True if status == PaymentStatusEnum.COMPLETED.label else False,
                })
            payment_successful.send(sender=order.__class__, recipient_list=recipient_list, order=order)
            if order.multiple_sellers:
                sellers = User.objects.filter(pk__in=order.sellers.all())
                sellers_emails = set([seller.email for seller in sellers])

                for email in sellers_emails:
                    html_content = render_to_string("partials/email/seller_product_ordered.html", {
                        "order": order,
                        "seller": email
                    })
                    send_async_email([email], html_content, subject="One of your products has been purchased!")
            else:
                seller_id = order.sellers.first()
                seller = get_object_or_404(User, pk=seller_id)
                html_content = render_to_string("partials/email/seller_product_ordered.html", {
                    "order": order,
                    "seller": seller
                })
                send_async_email([seller.email], html_content, subject="One of your products has been purchased!")
                context.update({
                    "seller": seller,
                })
        else:
            context.update({
                "success": False
            })
        return context


class ManualPayQrView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("account_login")
    template_name = "orders/seller_qr.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        uuid = kwargs.get("uuid")
        order = get_object_or_404(Order, uuid=uuid)

        context.update({
            "order": order,
        })
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        order = context.get("order")

        # if not order.multiple_sellers:
        #     return redirect(reverse_lazy("orders:success"))

        recipient_list = []

        if order.use_billing_address and order.customer.billing_address:
            recipient_list.append(order.customer.billing_address.email)
        else:
            recipient_list.append(order.email)

        if not order.multiple_sellers:
            seller_id = order.sellers.first()
            seller = get_object_or_404(User, pk=seller_id)
            html_content = render_to_string("partials/email/seller_product_ordered.html", {
                "order": order,
                "seller": seller
            })
            send_async_email([seller.email], html_content, subject="One of your products has been purchased!")
            context.update({
                "seller": seller,
            })
        else:
            sellers = User.objects.filter(pk__in=order.sellers.all())
            sellers_emails = set([seller.email for seller in sellers])

            for email in sellers_emails:
                html_content = render_to_string("partials/email/seller_product_ordered.html", {
                    "order": order,
                    "seller": email
                })
                send_async_email([email], html_content, subject="One of your products has been purchased!")

        payment_successful.send(sender=order.__class__, recipient_list=recipient_list, order=order)
        return self.render_to_response(context)


# Admin
@staff_member_required
def distribute_seller_payments(request):
    if request.method == "POST":
        form = SellerPaymentForm(request.POST)
        print(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request,f"Paid {instance.total_amount} to {instance.seller}.")
        else:
            print(form.errors)
            messages.error(request,"Failed To Pay to The Seller")

        return redirect(reverse("orders:distribute-seller-amount"))
    else:
        form = SellerPaymentForm()

    # Fetch only multi-seller orders
    orders = Order.objects.filter(multiple_sellers=True).prefetch_related("transaction_set").order_by("-created")
    for order in orders:
        for pid, item in order.products.items():
            item["seller"] = get_object_or_404(User, pk=item["seller"])
            item["seller_payment"] = SellerPayment.objects.filter(transaction=order.transaction_set.first(), seller=item["seller"]).exists()

    # seller = request.GET.get("seller")
    # status = request.GET.get("status") == "True"

    # sellers = User.objects.filter(user_type=UserTypeEnum.SELLER)
    #
    # filtered_orders = []
    #
    # if seller:
    #     for order in orders:
    #         orders = orders.filter(products__icontains=seller)
    #         for pid, item in order.products.items():
    #             if item["seller"].email == seller:
    #                 filtered_orders.append(order)
    #
    # if status:
    #     for order in orders:
    #         orders = orders.filter(products__icontains=seller)
    #         for pid, item in order.products.items():
    #             if item["seller_payment"] == status:
    #                 filtered_orders.append(order)
    #
    # print(filtered_orders)
    #
    # orders = filtered_orders

    paginator = Paginator(orders, 10)
    page_number = request.GET.get("page")
    orders = paginator.get_page(page_number)

    context = {
        "title": "Distribute Money to Sellers",
        "orders": orders,
        "form": form,
        # "sellers": sellers
    }
    context.update(admin_site.each_context(request))
    return render(request, "admin/distribute_seller_amounts.html", context)
