from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from account.forms import RegistrationForm, OtpVerificationForm, LoginForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Email verification link
            verification_link = request.build_absolute_uri(f"/verify-email/{user.id}/")

            send_mail(
                'Verify your Email',
                f'Click here to verify your email: {verification_link}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            # Generate mobile OTP
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            # send_sms(user.mobile, f'Your OTP is {otp}')
            print(f"OTP for {user.mobile} is {otp}") 

            return redirect('verify_mobile', user.username)  # or wherever you want
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def verify_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if not user.is_email_verified:
        user.is_email_verified = True
        user.save()

    return render(request, 'verify_email.html', {'user': user})

def verify_mobile(request, username):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            user = User.objects.get(username=username, otp=otp)
            user.is_mobile_verified = True
            user.otp = ''
            user.save()

            return render(request, 'mobile_verified.html', {'user': user})
        
        except User.DoesNotExist:
            error = "Invalid mobile number or OTP."
            return render(request, 'verify_mobile.html', {'error': error})

    return render(request, 'verify_mobile.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data.get('password')
            otp = form.cleaned_data.get('otp')
            login_type = form.cleaned_data['login_type']

            if login_type == 'password':
                # Normal password login
                user = None
                try:
                    user = User.objects.get(username=identifier)
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email=identifier)
                    except User.DoesNotExist:
                        try:
                            user = User.objects.get(mobile=identifier)
                        except User.DoesNotExist:
                            user = None

                if user:
                    user_auth = authenticate(request, username=user.username, password=password)
                    if user_auth:
                        login(request, user_auth)
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Invalid password.")
                else:
                    messages.error(request, "User not found.")

            elif login_type == 'otp':
                # OTP login
                session_otp = request.session.get('otp')
                session_identifier = request.session.get('identifier')

                if not session_otp or not session_identifier:
                    messages.error(request, "OTP not sent or expired.")
                else:
                    if session_identifier == identifier and session_otp == otp:
                        # OTP is valid
                        try:
                            user = User.objects.get(username=identifier)
                        except User.DoesNotExist:
                            try:
                                user = User.objects.get(email=identifier)
                            except User.DoesNotExist:
                                user = User.objects.get(mobile=identifier)

                        login(request, user)
                        # Clear session otp
                        request.session.pop('otp')
                        request.session.pop('identifier')
                        user.otp = ''
                        return redirect('dashboard')
                    else:
                        messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def send_otp(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        identifier = data.get('identifier')

        if not identifier:
            return JsonResponse({'success': False, 'error': 'Email or Mobile number required'})

        user = None
        user_type = None

        # Check if identifier is email
        if "@" in identifier:
            try:
                user = User.objects.get(email=identifier)
                user_type = 'email'
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found'})
        # Check if identifier is mobile (digits only)
        elif identifier.isdigit():
            try:
                user = User.objects.get(mobile=identifier)
                user_type = 'mobile'
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'User not found'})
        else:
            # It's a username
            return JsonResponse({'success': False, 'error': 'OTP login not supported for username'})

        # User found
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp
        request.session['identifier'] = identifier
        user.otp = otp
        user.save()
        if user_type == 'mobile':
            # Print OTP in console
            print(f"Sending OTP {otp} to mobile {identifier}")
        elif user_type == 'email':
            # Send OTP via email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                'no-reply@yourdomain.com',
                [identifier],
                fail_silently=False,
            )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})



def logout_view(request):
    logout(request)
    return redirect('dashboard')

def dashboard_view(request):
    return render(request, 'dashboard.html')

# def verify_otp_view(request):
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('register')

#     user = User.objects.get(id=user_id)

#     if request.method == 'POST':
#         form = OtpVerificationForm(request.POST)
#         if form.is_valid():
#             if form.cleaned_data['email_otp'] == user.email_otp and form.cleaned_data['mobile_otp'] == user.mobile_otp:
#                 user.is_active = True
#                 user.is_verified = True
#                 user.email_otp = ''
#                 user.mobile_otp = ''
#                 user.save()
#                 return redirect('login')
#             else:
#                 form.add_error(None, "Invalid OTPs")
#     else:
#         form = OtpVerificationForm()
#     return render(request, 'otp.html', {'form': form})
