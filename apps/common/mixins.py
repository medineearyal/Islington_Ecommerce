from apps.common.utils import generate_unique_slug

class SlugMixin:
    slug_field_name = "slug"
    slug_from_name = "name"

    def save(self, *args, **kwargs):
        if not getattr(self, self.slug_field_name, None):
            self_slug = generate_unique_slug(
                self,
                field_name=self.slug_field_name,
                from_name=self.slug_from_name,
            )
            setattr(self, self.slug_field_name, self_slug)
        super().save(*args, **kwargs)