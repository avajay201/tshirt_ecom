from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import User
from .utils import send_verification_email


@receiver(post_save, sender=User)
def handle_new_chatbot(sender, instance, created, **kwargs):
    if created:
        send_verification_email(instance)
