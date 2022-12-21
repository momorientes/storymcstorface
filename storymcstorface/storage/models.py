from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib import admin


class TimeStampMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Vendor(TimeStampMixin):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name


class ProductCategory(TimeStampMixin):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name


class Product(TimeStampMixin):
    """A product describes is a global entity which can be instanciated as StorageItem"""

    name = models.CharField(max_length=512)
    slug = models.SlugField(null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    vendor_pn = models.CharField(max_length=512, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Product: {self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class Facility(TimeStampMixin):
    """A Facility is a Building or Room in which a storage is set up"""

    name = models.CharField(max_length=512)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Facility, self).save(*args, **kwargs)


class Location(TimeStampMixin):
    """A location describes the position of an object using rows/colums within a facility"""

    row = models.CharField(max_length=4)
    column = models.CharField(max_length=4)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    class Meta:
        db_table = "location"
        constraints = [
            models.UniqueConstraint(
                fields=["row", "column", "facility"],
                name="unique row/column per location",
            )
        ]

    def __str__(self) -> str:
        return f"{self.row}:{self.column} ({self.facility})"


class StorageItem(TimeStampMixin):
    """A StorageItem is a an Instance of a Product in a given location"""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.product.name}"

    def add(
        self, qty: int = 1, user: settings.AUTH_USER_MODEL = None, comment: str = ""
    ) -> int:
        """Increase quantity by value, return new quantity"""
        self.quantity += qty
        log = StorageLog(
            item=self, action="ADD", user=user, quantity=qty, comment=comment
        )
        log.save()
        self.save()

        return self.quantity

    def remove(
        self, qty: int = 1, user: settings.AUTH_USER_MODEL = None, comment: str = ""
    ) -> int:
        """Decrease quantity by value, return new quantity"""
        if self.quantity - qty < 0:
            self.quantity = 0
        else:
            self.quantity -= qty
        log = StorageLog(
            item=self, action="REMOVE", user=user, quantity=qty, comment=comment
        )
        log.save()
        self.save()

        return self.quantity


class StorageLog(models.Model):
    ACTION_CHOICES = [("ADD", "ADD"), ("REMOVE", "REMOVE"), ("MODIFY", "MODIFY")]
    timestamp = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(StorageItem, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=10, choices=ACTION_CHOICES, default="REMOVE", blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    quantity = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=512)

    @admin.display(description="Facility")
    def get_facility(self):
        return self.item.location.facility

    @admin.display(description="Location")
    def get_location(self):
        return f"{self.item.location.row} {self.item.location.column}"

    def __str__(self) -> str:
        if self.user:
            username = self.user.username
        else:
            username = "ADMIN"
        return f"{self.timestamp};{self.action};{username};{self.item.location};{self.item.product};{self.quantity}"
