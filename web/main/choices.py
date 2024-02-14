from django.db.models import IntegerChoices, TextChoices
from django.utils.translation import gettext_lazy as _


class UserGender(IntegerChoices):
    UNKNOWN = (0, _("Unknown"))
    MAN = (1, _("Man"))
    FEMALE = (2, _("Female"))


class SocialProvider(TextChoices):
    GITHUB = "github"
    GOOGLE = "google"
