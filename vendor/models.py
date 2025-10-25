from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from userauths.models import User
from django.utils.text import slugify

class Vendor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.FileField(upload_to="vendor", default="vendor.jpg", null=True, blank=True)
    name=models.CharField(max_length=100, help_text="Shop Name", null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    mobile=models.CharField(max_length=100, help_text="Shop Mobile Number", null=True, blank=True)
    active=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=True)
    slug=models.SlugField(null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'Vendors'
        ordering = ['-date']
        
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        if self.slug =="" or self.slug is None:
            self.slug=slugify(self.name)
        super(Vendor, self).save(*args, **kwargs)

class VendorRequest(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - Vendor Request"
    


@receiver(post_save, sender=VendorRequest)
def create_vendor_when_approved(sender, instance, **kwargs):
    if instance.is_approved:
        if not Vendor.objects.filter(user=instance.user).exists():
            Vendor.objects.create(
                user=instance.user,
                name=f"{instance.user.full_name or instance.user.username}'s Shop",
                active=True
            )
           
