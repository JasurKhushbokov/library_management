import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management.settings")
import django
django.setup()
from django.contrib.auth.models import User
u = User.objects.get(username="admin")
u.set_password("admin123")
u.save()
print("PASSWORD_SET_OK")
