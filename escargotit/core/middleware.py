# from django.core.exceptions import PermissionDenied
# from django.urls import reverse

# class UserAdminMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the request is a POST request
#         if request.method == 'POST':
#             # Get the URL where the POST request is being made to
#             current_url = request.path

#             # Define the URLs that are allowed for both User and Admin
#             allowed_urls = [
#                 reverse('submit_data'),  # Replace with the URL name for submitting data
#                 # Add more allowed URLs if needed
#             ]

#             # Check if the current URL is in the allowed URLs list
#             if current_url not in allowed_urls:
#                 # Check if the user is authenticated and is an Admin
#                 if request.user.is_authenticated and request.user.is_admin:
#                     # Allow Admin to submit data to any URL
#                     return self.get_response(request)
#                 else:
#                     # Raise PermissionDenied exception for User trying to submit data to Admin-only URL
#                     raise PermissionDenied("You don't have permission to access this page.")
        
#         return self.get_response(request)