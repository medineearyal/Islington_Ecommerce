from email.mime.image import MIMEImage
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.functions import Substr, Cast, Coalesce
from django.utils.text import slugify
from django.db.models import Q, IntegerField, Max, Case, When, Value, CharField
import threading


def generate_unique_slug(instance, field_name="slug", from_name="name"):
    """
        Generates a unique slug for any model instance.

        Args:
            instance: The model instance to generate the slug for.
            field_name: The field name on the model to store the slug.
            from_name: The field name from which to generate the slug.

        Returns:
            A unique slug string.
        """
    ModelClass = instance.__class__
    base_slug = slugify(getattr(instance, from_name))

    if len(base_slug) > 50:
        base_slug = base_slug[:50]

    qs = ModelClass.objects.filter(
        Q(**{f"{field_name}__regex": rf"^{base_slug}(-\d+)?$"})
    ).exclude(pk=instance.pk)

    if qs.exists():
        max_suffix = qs.annotate(
            suffix_num=Cast(
                Coalesce(
                    Case(
                        When(
                            **{f"{field_name}__regex": rf'^{base_slug}-\d+$'},
                            then=Substr(field_name, len(base_slug) + 2)
                        ),
                        default=Value("0"),
                        output_field=CharField()
                    ),
                    Value("0")
                ),
                IntegerField()
            )
        ).aggregate(max_num=Max('suffix_num'))['max_num'] or 1

        return f"{base_slug}-{max_suffix + 1}"
    else:
        return base_slug


def send_invoice_email(recipient_emails, html_content):
    subject = "Your Order Has Been Successfully Placed"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = recipient_emails

    msg = EmailMultiAlternatives(subject, "", from_email, to)
    msg.attach_alternative(html_content, "text/html")

    logo_path = os.path.join(settings.BASE_DIR, "static/images/logo.PNG")
    with open(logo_path, "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo_image>")
        logo.add_header("Content-Disposition", "inline", filename="logo.PNG")
        msg.attach(logo)

    msg.send()


def send_invoice_email_async(recipient_email, html_content):
    thread = threading.Thread(
        target=send_invoice_email,
        args=(recipient_email, html_content)
    )
    thread.start()
