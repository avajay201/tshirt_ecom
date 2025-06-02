from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from cart.models import Cart


class VerificationToken:
    @staticmethod
    def generate_token(user):
        """
        Generate a unique token for a user.
        """
        return default_token_generator.make_token(user)

    @staticmethod
    def decode_token(token, uid):
        """
        Decode the token to check if it's valid.
        """
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = get_user_model().objects.get(pk=uid)
            return default_token_generator.check_token(user, token)
        except Exception as e:
            return False

def send_verification_email(user):
    """Send an account verification link to user"""

    # Generate token and UID
    token = VerificationToken.generate_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Construct the verification link
    verification_link = f"{settings.BASE_URL}/api/auth/verify-account/{uid}/{token}"

    # Prepare email content
    subject = "Verify Your Account"
    message = render_to_string("email/account_verification_email.html", {
        'username': user.username,
        'verification_link': verification_link,
    })

    # Send email
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

def verify_account(uidb64, token):
    """Verify account verification link"""
    # Decode the UID
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except Exception as e:
        print('Error:', e)
        return

    # Check the token validity
    if VerificationToken.decode_token(token, uidb64):
        if user.is_active:
            return 'exists'

        # Mark user as verified
        user.is_active = True
        Cart.objects.get_or_create(user=user)
        user.save()
        return 'verified'
