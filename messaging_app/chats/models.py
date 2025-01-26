from django.contrib.auth.models import AbstractBaseUser
from decimal import Decimal
from django.db import models
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, TimeStampedModel):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    ROLE_CHOICES = (("admin", "Admin"), ("host", "Host"), ("guest", "Guest"))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest", null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(unique=True, null=False)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=255, null=False)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"], name="idx_user_email"),
        ]

        constraints = [models.UniqueConstraint(fields=["email"], name="unique_email"), models.CheckConstraint(check=models.Q(role__in=["admin", "host", "guest"]), name="role_in_choices")]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number} ({self.email}) ({self.role})"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField("User", related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_emails = ", ".join([user.email for user in self.participants.all()])
        return f"Conversation {self.conversation_id} with participants: {participant_emails}"

    class Meta:
        db_table = "conversations"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender_id = models.ForeignKey(User, to_field="user_id", on_delete=models.SET_NULL, null=True)
    recipient_id = models.ForeignKey(User, related_name="received_messages", on_delete=models.SET_NULL, null=True)
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-sent_at"]
        indexes = [models.Index(fields=["sender_id"], name="idx_sender_id"), models.Index(fields=["recipient_id"], name="idx_recipient_id")]

    def __str__(self):
        return f"{self.sender_id} {self.message_body} {self.sent_at}"


class PaymentMethod(TimeStampedModel):
    pay_method_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_fee = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0.00)
    currency_conversion = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=1.00)
    name = models.CharField(max_length=36, null=False)

    class Meta:
        db_table = "PaymentMethod"
        indexes = [
            models.Index(fields=["name"], name="idx_paymentmethod_name"),
        ]

    def __str__(self):
        return f"{self.name} {self.transaction_fee} {self.currency_conversion} {self.created_at}"


class Location(TimeStampedModel):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=False, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=10, decimal_places=7, validators=[MinValueValidator(-180), MaxValueValidator(180)], null=False)
    city = models.CharField(max_length=36, null=False)
    state = models.CharField(max_length=36, null=True, blank=True)
    country = models.CharField(max_length=36, null=False)

    class Meta:
        db_table = "Location"
        indexes = [
            models.Index(fields=["city", "country"], name="idx_location_city_country"),
        ]

    def __str__(self):
        return f"{self.latitude} {self.longitude} {self.city} {self.state} {self.country} {self.created_at}"


class Property(TimeStampedModel):
    property_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE)
    location_id = models.ForeignKey(Location, to_field="location_id", on_delete=models.CASCADE)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    availability_status = models.CharField(max_length=12, choices=[("available", "Available"), ("unavailable", "Unavailable")], default="available")
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "Property"
        indexes = [
            models.Index(fields=["price_per_night"], name="idx_property_price"),
            models.Index(fields=["location_id"], name="idx_property_location"),
            models.Index(fields=["property_id"], name="idx_property_id"),
        ]

    def __str__(self):
        return f"{self.host_id} {self.location_id} {self.name} {self.description} {self.price_per_night} {self.availability_status} {self.created_at}"


class UserToken(TimeStampedModel):
    token_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=255, unique=True)
    token_expire_at = models.DateTimeField(null=False)
    is_used = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "UserToken"
        indexes = [
            models.Index(fields=["token", "token_expire_at", "is_used"], name="idx_token_validation"),
            models.Index(fields=["user_id"], name="idx_user_tokens"),
        ]

    def __str__(self):
        return f"{self.user} {self.token} {self.token_expire_at} {self.is_used}"


class Review(TimeStampedModel):
    review_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Property, to_field="property_id", on_delete=models.CASCADE, related_name="reviews")
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=10, choices=[("guest", "Guest"), ("host", "Host")], null=False, default="guest")

    class Meta:
        db_table = "Review"
        indexes = [
            models.Index(fields=["property_id"], name="idx_property_reviews"),
        ]

    def __str__(self):
        return f"{self.user} {self.property} {self.rating} {self.comment} {self.reviewed_by} {self.created_at}"


class Booking(TimeStampedModel):
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Property, to_field="property_id", on_delete=models.CASCADE, related_name="bookings")
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    booking_status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")], default="pending")
    payment_status = models.CharField(max_length=12, choices=[("in_progress", "In Progress"), ("paid", "Paid"), ("failed", "Failed")], default="in_progress")

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date cannot be before start date.")

    class Meta:
        db_table = "Booking"

        indexes = [models.Index(fields=["property_id"], name="idx_property_bookings"), models.Index(fields=["user_id"], name="idx_user_bookings")]

    def __str__(self):
        return f"{self.user} {self.property} {self.start_date} {self.end_date} {self.total_price} {self.booking_status} {self.payment_status} {self.created_at}"


class BookingCancellation(models.Model):
    cancellation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.ForeignKey(Booking, to_field="booking_id", on_delete=models.CASCADE, related_name="cancellations")
    cancelled_by = models.CharField(max_length=10, choices=[("guest", "Guest"), ("host", "Host")], null=False)
    cancel_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cancel_reason = models.TextField(null=True, blank=True)
    cancel_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "BookingCancellation"
        indexes = [models.Index(fields=["booking_id"], name="idx_booking_cancellations")]

    def __str__(self):
        return f"{self.booking} {self.cancelled_by} {self.cancel_reason} {self.cancel_fee} {self.cancel_at}"


class Payment(TimeStampedModel):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.ForeignKey(Booking, to_field="booking_id", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    pay_method_id = models.ForeignKey(PaymentMethod, to_field="pay_method_id", on_delete=models.CASCADE, related_name="payments")
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")], default="pending")
    transaction_id = models.CharField(max_length=36, unique=True, null=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Payment"
        indexes = [models.Index(fields=["booking_id"], name="idx_booking_payments"), models.Index(fields=["status"], name="idx_payment_status")]

    def __str__(self):
        return f"{self.booking} {self.amount} {self.status} {self.transaction_id} {self.payment_date}"


class Notification(models.Model):
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="notifications")
    event_type = models.CharField(max_length=20, choices=[("booking_confirmation", "Booking Confirmation"), ("payment_update", "Payment Update"), ("general_alert", "General Alert")], null=False)
    is_read = models.BooleanField(default=False)
    message = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "Notification"
        indexes = [
            models.Index(fields=["user_id"], name="idx_user_notifications"),
        ]


class Coupon(TimeStampedModel):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="coupons", null=True, blank=True)
    property_id = models.ForeignKey(Property, to_field="property_id", on_delete=models.CASCADE, related_name="coupons", null=True, blank=True)
    discount_type = models.CharField(max_length=15, choices=[("percentage", "Percentage"), ("fixed_amount", "Fixed Amount")], null=False)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    code = models.CharField(max_length=36, unique=True, null=False)
    description = models.TextField(null=True, blank=True)
    max_no_uses = models.PositiveIntegerField(null=False)
    valid_from = models.DateTimeField(null=False)
    valid_to = models.DateTimeField(null=False)

    class Meta:
        db_table = "Coupon"
        indexes = [models.Index(fields=["user_id"], name="idx_user_coupons"), models.Index(fields=["property_id"], name="idx_property_coupons")]


class CouponUsage(models.Model):
    coupon_usage_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon_id = models.ForeignKey(Coupon, to_field="coupon_id", on_delete=models.CASCADE, related_name="usages")
    user_id = models.ForeignKey(User, to_field="user_id", on_delete=models.CASCADE, related_name="coupon_usages")
    property_id = models.ForeignKey(Property, to_field="property_id", on_delete=models.SET_NULL, related_name="coupon_usages", null=True, blank=True)
    booking_id = models.ForeignKey(Booking, to_field="booking_id", on_delete=models.CASCADE, related_name="coupon_usages", null=True, blank=True)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "CouponUsage"
        indexes = [
            models.Index(fields=["user_id", "coupon_id"], name="idx_user_coupon_usage"),
        ]
        unique_together = ("coupon_id", "user_id")

    def __str__(self):
        return f"{self.coupon_id} - {self.user_id}"


class PropertyImages(TimeStampedModel):
    image_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Property, to_field="property_id", on_delete=models.CASCADE, related_name="images")
    image_url = models.TextField(null=False)
    alt_text = models.TextField(null=True, blank=True)
    image_type = models.CharField(max_length=15, choices=[("main", "Main"), ("gallery", "Gallery"), ("thumbnail", "Thumbnail")], null=False)

    class Meta:
        db_table = "PropertyImages"
        indexes = [models.Index(fields=["property_id"], name="idx_propertyImages_id")]

    def __str__(self):
        return f"{self.property_id} - {self.image_url}"
