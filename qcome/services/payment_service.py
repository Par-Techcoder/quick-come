import json
from django.shortcuts import get_object_or_404
from qcome.models import Payment, Booking, User, Worker
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from ..constants import PayType, PayStatus, Status
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from qcome.services import booking_service, user_service


    
def get_all_payments_created_by(user_id):
    """Retrieve all payments"""
    payments = Payment.objects.filter(created_by=user_id, is_active=True).values(
        'id', 'amount', 'type', 'paid_at', 'created_by', 'booking_id',
    ).order_by('-created_at')
    return list(payments)

def get_current_payment(booking_id):
    """Retrieve all payments"""
    payment = Payment.objects.filter(booking_id=booking_id,is_active=True,pay_status=PayStatus.COMPLETED.value).values()
    return list(payment)

def create_payment(request, booking_id, user_id):
    """Create a new payment for a given booking and deactivate the booking"""
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method. Use POST."}, status=405)

        data = json.loads(request.body)
        booking = Booking.objects.filter(id=booking_id, is_active=True).first()

        if not booking:
            return JsonResponse({"error": "❌ Booking not found or already inactive"}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "❌ User not found"}, status=400)

        required_fields = ["type", "amount", "pay_status"]
        if not all(field in data for field in required_fields):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        payment = Payment.objects.create(
            booking_id=booking,
            type=data["type"],
            amount=data["amount"],
            pay_status=PayStatus.COMPLETED.value,
            created_by=booking.customer,
        )

        booking.is_active = False
        booking.save(update_fields=["is_active"])


        channel_layer = get_channel_layer()
        # Create the data to send to the WebSocket
        async_to_sync(channel_layer.group_send)(
            "garage_bills",  # Group name
            {
                "type": "payment_status_update",  # Event type for handling in consumer
                "payment": json.dumps({
                    "booking_id": booking_id,
                    "pay_status": PayStatus(payment.pay_status).name,
                }),
            }
        )

        # Send real-time update to the specific user's WebSocket group
        channel_layer = get_channel_layer()
        payment_data = {
            "message": "✅ Payment created successfully",
            "user_id": payment.created_by.id,
            "payment_id": payment.id,
            "booking_id": booking.id,
            "amount": payment.amount,
            "work_status":Status(booking_service.get_booking_status(booking.id)).name,
            "type": PayType(payment.type).name,
            "paid_by": user_service.user_full_name(booking.customer),
            "paid_to": user_service.user_full_name(booking.assigned_worker.worker) if PayType.CASH.value == payment.type else "Quick-come Company",
        }

        # Log the payment data to verify it
        print("Sending payment data:", payment_data)

        async_to_sync(channel_layer.group_send)(
            f"user_{payment.created_by.id}",  # Send to the specific user's group
            {
                "type": "payment_update",
                "payment": payment_data  # Sending the payment data as an object
            }
        )

        return JsonResponse({"message": "✅ Payment created successfully", "payment_id": payment.id})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def update_payment(request, booking_id):
    """Update an existing payment"""
    try:
        data = json.loads(request.body)
        payment = get_object_or_404(Payment, booking_id=booking_id)

        payment.type = data.get('type', payment.type)
        payment.amount = data.get('amount', payment.amount)
        payment.pay_status = data.get('pay_status', payment.pay_status)
        payment.save()

        return {"message": "Payment updated successfully"}
    except Exception as e:
        return {"error": str(e)}

def delete_payment(booking_id):
    """Soft delete a payment (mark as inactive)"""
    try:
        payment = get_object_or_404(Payment, booking_id=booking_id)
        payment.is_active = False  # Correctly update the field
        payment.save()  # Save changes to the database

        return {"message": "Payment deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
    
def payment_details_by_payment_id(payment_id):
    return Payment.objects.filter(id=payment_id, is_active=True).values(
        'id', 'amount', 'type', 'paid_at', 'created_by__first_name', 'created_by__last_name','booking_id',
    ).first()  # This ensures only one result is returned


def get_worker_payments(worker_user_id):
    worker_id=Worker.objects.get(worker=worker_user_id)
    all_bookings_by_worker = Booking.objects.filter(assigned_worker=worker_id.id,is_active=False)
    payments = []
    for booking in all_bookings_by_worker:
        payment = Payment.objects.filter(
            booking_id=booking.id, 
            is_active=True,
        ).first()  # Fetch a single matching payment

        if payment:
            payments.append({
                "payment_id": payment.id,
                "amount": payment.amount,
                "paid_at": payment.paid_at.strftime('%Y-%m-%d'),
                "booking_id": booking.id,
                "customer": user_service.user_full_name(booking.customer),
                "pay_type": PayType(payment.type).name,
            })

    return payments



def get_all_payments():
    """Retrieve and customize all active payments."""
    # Use select_related to join Payment -> Booking -> assigned_worker -> worker (User)
    payments = Payment.objects.filter(is_active=True,pay_status=PayStatus.COMPLETED.value)\
        .select_related('booking_id__assigned_worker__worker')\
        .values(
            'id', 
            'amount', 
            'type', 
            'paid_at', 
            'created_by',
            'booking_id',
            'booking_id__assigned_worker__worker',
        )
    
    payments_data = []
    for payment in payments:
        # Convert the numeric payment type to its enum name
        payment_type = PayType(payment['type']).name if payment['type'] else "N/A"
        # Format the paid_at field as a string
        paid_at = payment['paid_at'].strftime('%Y-%m-%d %H:%M:%S') if payment['paid_at'] else "N/A"
        # Combine the created_by first and last name
        payment_by = user_service.user_full_name(payment.get('created_by'))
        
        assigned_worker = payment.get('booking_id__assigned_worker__worker')
        
        if assigned_worker:
            paid_to = user_service.user_full_name(assigned_worker)
        else:
            paid_to = "Unknown"
        
        # Build custom payment dictionary.
        payment_data = {
            'payment_id': payment['id'],
            'amount': payment['amount'],
            'payment_type': payment_type,
            'paid_at': paid_at,
            'payment_by': payment_by,
            'booking_id': payment['booking_id'],
            'paid_to': paid_to,
        }
        payments_data.append(payment_data)
    
    return payments_data


def get_total_revenue():
    """Calculate the total revenue from all payments."""
    qs = Payment.objects.filter(is_active=True).values_list('amount', flat=True).iterator()
    total_revenue = sum(qs) or 0  # Ensure 0 is returned if no records
    return total_revenue



def get_payment_status(booking_id):
    is_paid=Payment.objects.filter(booking_id=booking_id,is_active=True).exists()
    if is_paid:
        status=Payment.objects.filter(booking_id=booking_id,is_active=True).values('pay_status').first()
        status=status['pay_status']
        return status
    status= 4
    return status