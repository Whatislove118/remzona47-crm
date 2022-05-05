"""
    Class with functions which called on startup process
"""
from django.conf import settings
from django.contrib.auth.models import Group


def create_base_groups():
    base_groups_names = (settings.MODERATOR_GROUP_NAME, settings.REGULAR_USERS_GROUP_NAME)
    for name in base_groups_names:
        _, created = Group.objects.get_or_create(name=name)
        if created:
            print(f"Create base group with name {name}")
