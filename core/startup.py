'''
    Class with functions which called on startup process
'''
from django.conf import settings
from django.contrib.auth.models import Group

def create_base_groups():
    print("Delete base groups")
    Group.objects.all().delete() 
    for name in (settings.MODERATOR_GROUP_NAME, settings.REGULAR_USERS_GROUP_NAME):
        print(f"Create base group with name {name}")
        Group.objects.create(name=name)