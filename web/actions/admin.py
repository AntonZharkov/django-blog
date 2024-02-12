from actions.models import Follower
from django.contrib import admin


# Register your models here.
@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass
