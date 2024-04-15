from django.db import models
import uuid
from datetime import datetime
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
    username = models.CharField(max_length=150, editable=False)
    first_name = models.CharField(max_length=30, editable=False)
    last_name = models.CharField(max_length=100, editable=False)
    password = models.UUIDField(editable=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("Email address"), unique=True, null=False)
    bio = models.TextField(blank=True, null=True)
    class_year = models.IntegerField(
        _("Class year"),
        validators=[
            MinValueValidator(datetime.now().year),
            MaxValueValidator(datetime.now().year + 4),
        ],
        blank=False,
        null=False,
    )
    phone_number = PhoneNumberField(blank=True, null=True)
    create_date = models.DateTimeField(_("Created at"), auto_now_add=True)
    update_date = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Listing(models.Model):
    STATUS_DENIED = 0
    STATUS_ACCEPTED = 1
    STATUS_PENDING = 2

    STATUS_CHOICES = [
        (STATUS_DENIED, "Denied"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_PENDING, "Pending"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_type = models.BooleanField(
        _("Listing type"), default=False
    )
    title = models.CharField(_("Title"), max_length=255)
    location = models.CharField(_("Location"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    form = models.BooleanField(
        _("Form"), default=False
    )
    price = models.DecimalField(
        _("Price"),
        validators=[
            MinValueValidator(0),
        ],
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)
    payment_method = models.CharField(max_length=255)
    category = models.CharField(_("Category"), max_length=255, blank=False, null=False)
    condition = models.CharField(
        _("Condition"), max_length=255, blank=False, null=False
    )
    create_date = models.DateTimeField(_("Created at"), auto_now_add=True)
    update_date = models.DateTimeField(_("Updated at"), auto_now=True)
    clicked = models.IntegerField(
        _("Number of interaction"),
        validators=[MinValueValidator(0)],
        blank=True,
        null=False,
        default=0
    )

    def __str__(self):
        return self.title


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.URLField(_("Image_URL"))
    create_date = models.DateTimeField(_("Created at"), auto_now_add=True)
    update_date = models.DateTimeField(_("Updated at"), auto_now=True)
    listing_image = models.ForeignKey(Listing, on_delete=models.CASCADE)
    profile_image = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image {self.id}"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    buyer_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_transactions", default=""
    )
    seller_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seller_transactions"
    )
    time_posted = models.DateTimeField(auto_now_add=True)
    time_sold = models.DateTimeField()


class MyBids(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    offered_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)

