from django.db.models.functions import Substr, Cast
from django.utils.text import slugify
from django.db.models import Q, IntegerField, Max


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

    qs = ModelClass.objects.filter(
        Q(**{f"{field_name}__regex": rf"^{base_slug}(-\d+)?$"})
    ).exclude(pk=instance.pk)

    if qs.exists():
        max_suffix = qs.annotate(
            suffix_num=Cast(
                Substr(field_name, len(base_slug) + 2),
                IntegerField()
            )
        ).aggregate(max_num=Max('suffix_num'))['max_num'] or 1

        return f"{base_slug}-{max_suffix + 1}"
    else:
        return base_slug


