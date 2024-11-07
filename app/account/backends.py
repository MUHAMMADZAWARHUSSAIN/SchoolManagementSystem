
#! both username and email 

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try to get the user by username, case-insensitive
            user = User.objects.get(username__iexact=username) 
        except User.DoesNotExist:
            try:
                # If not found, try to get the user by email, case-insensitive
                user = User.objects.get(email__iexact=username)
            except User.DoesNotExist:
                # If still not found, return None
                return None
            except User.MultipleObjectsReturned:
                # Handle the case where multiple users have the same email
                return User.objects.filter(email__iexact=username).order_by('id').first()
