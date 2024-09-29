from django.core.mail import send_mail
from django.conf import settings

def send_profile_completion_email(teacher):
    subject = 'Teacher Profile Completed'
    message = f"""
    Dear {teacher.user.get_full_name()},

    Congratulations! Your teacher profile has been successfully completed.

    Here are the details we have on file:
    Employee ID: {teacher.employee_id}
    Phone Number: {teacher.phone_number}
    Address: {teacher.address}

    If you need to make any changes, please log in to your account and update your profile.

    Thank you for being a part of our educational community!

    Best regards,
    School Administration
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [teacher.user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
