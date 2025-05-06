import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email_otp(email, otp):
    send_mail(
        subject="Your Email OTP",
        message=f"Your OTP is {otp}",
        from_email="noreply@yourdomain.com",
        recipient_list=[email],
        fail_silently=False,
    )

# Simulate mobile OTP (use actual SMS API like Twilio in production)
def send_mobile_otp(mobile, otp):
    print(f"Sending SMS to {mobile}: Your OTP is {otp}")
