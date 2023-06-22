from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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