from django.views import View
from django.shortcuts import render
from ..decorators import auth_required, worker_required
from ..services import booking_service,work_service
from django.http import JsonResponse
import json


@auth_required(login_url='/sign-in/')
@worker_required
class BillingHomeView(View):
    def get(self, request):
        # Attempt to retrieve the booking object
        booking = booking_service.get_booking_by_id(request.user.id)
        
        # Check if the booking exists
        if not booking:
            # If no booking is found, return the cart page or any other page indicating no active booking
            return render(request, 'worker/cart.html')
        
        # Check if the work is completed (assuming booking exists here)
        is_work_done = work_service.is_work_complete(booking.id)
        
        # If the work is not done, return the cart page
        if not is_work_done:
            return render(request, 'worker/cart.html')  # No active booking or work not completed
        
        # Get services associated with the booking
        services = booking_service.get_services_by_id(booking.id)
        
        # Calculate the total price for the services
        total_price = booking_service.total_price(services)
        return render(request, 'worker/cart.html', {
            'booking_id': booking.id,
            'services': services,
            'total_price': total_price  
        })


@auth_required(login_url='/sign-in/')
@worker_required
class BillingUpdate(View):
    def post(self, request, booking_id):
        """Handles adding a service to an existing booking."""
        try:
            data = json.loads(request.body)
            service_id = data.get("service_id")

            if not service_id:
                return JsonResponse({"success": False, "error": "Missing service_id"}, status=400)

            response = booking_service.add_service_to_booking(booking_id, service_id)
            status_code = 200 if response["success"] else 400

            return JsonResponse(response, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
        
@auth_required(login_url='/sign-in/')
@worker_required
class BillingDelete(View):
    def delete(self, request, booking_id):
        try:
            data = json.loads(request.body)
            service_name = data.get("service_name")

            # Call service layer for deletion
            response = booking_service.remove_service_from_booking(booking_id, service_name)
            
            status_code = 200 if response["success"] else 404
            return JsonResponse(response, status=status_code)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"}, status=400)

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)