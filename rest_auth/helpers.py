from django.conf import settings
from django.contrib.auth import password_validation
from django.db.models.signals import post_save
from django.dispatch import receiver


def validate_credentials(username, email, password):
    if username is None:
        raise AttributeError('Username shouldn\'t be None')
    if email is None:
        raise AttributeError('Email shouldn\'t be None')
    if password is None:
        raise AttributeError('Password shouldn\'t be None')
    password_validation.validate_password(password)
    
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid='post_save_user')
def post_save_user(sender, instance, created, **kwargs):
    pass