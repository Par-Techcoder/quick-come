from django.db import models
from ..constants import PayType,PayStatus

class Payment(models.Model):
    booking_id = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='fk_booking_payments_bookings_id')
    type = models.IntegerField(
        choices=[(paytype.value, paytype.name) for paytype in PayType ],
        blank=True,null=True
    )
    amount = models.ForeignKey('Billing', on_delete=models.CASCADE)
    pay_status = models.IntegerField(
        chocices = [(paystatus.value,paystatus.name) for paystatus in PayStatus],
        blank=False,null=False
    )
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='fk_user_payments_users_id')
    paid_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_created=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f"ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"