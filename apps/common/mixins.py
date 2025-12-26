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
        

class VerifiedProductMixin:
    product_field_name = "product"
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):  
        from apps.products.models import Product
          
        if db_field.name == self.product_field_name:
            kwargs["queryset"] = Product.objects.filter(is_verified=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        from apps.products.models import Product
        
        if db_field.name == self.product_field_name:
            kwargs["queryset"] = Product.objects.filter(is_verified=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)