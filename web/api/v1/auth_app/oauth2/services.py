import secrets
import string


class OAuthRedirectsParamsService:
    @classmethod
    def generate_state(cls) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(16))
