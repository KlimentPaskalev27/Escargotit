from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import CreateView

class IndexCreateView(CreateView):
    def get(self, request):

        return render(request, 'index.html') 
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a success page
            return redirect('success')
        else:
            # Display an error message
            error_message = 'Invalid username or password.'
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')



# def api_data_export(request):
#     format = request.GET.get('format')

#     # Retrieve data from your API or database
#     data = YourModel.objects.all().values()

#     if format == 'csv':
#         # Generate CSV data
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="data.csv"'

#         # Write CSV data to response
#         writer = csv.DictWriter(response, fieldnames=data[0].keys())
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)

#         return response
#     elif format == 'json':
#         # Generate JSON data
#         response = HttpResponse(content_type='application/json')
#         response['Content-Disposition'] = 'attachment; filename="data.json"'

#         # Write JSON data to response
#         response.write(json.dumps(list(data), indent=4))

#         return response

#     return render(request, 'api_data_export.html', {'data': data})
