from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.generics import get_object_or_404

from apps.orders.constants import PaymentStatusEnum
from apps.orders.models import Order, KhaltiTransaction, Transaction


# Create your views here.
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

            if pidx:
                khalti_transaction = get_object_or_404(KhaltiTransaction, pidx= pidx, transaction=transaction)

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
