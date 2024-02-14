from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from services import OAuthRedirectsParamsService

from . import serializers


class OAuthRedirectsParamsView(GenericAPIView):
    serializer_class = serializers.OAuthRedirectsParamsSerializer
    permission_classes = (AllowAny,)

    PROVIDER_DATA = {
        "google": {"client_id": settings.GOOGLE_CLIENT_ID},
        "github": {"client_id": settings.GITHUB_CLIENT_ID},
    }

    @extend_schema(
        parameters=[serializers.OAuthRedirectsParamsSerializer],
        responses={200: serializers.OAuthProviderParamsSerializer},
    )
    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        provider = serializer.validated_data["provider"]
        data = self.PROVIDER_DATA[provider]
        state = OAuthRedirectsParamsService.generate_state()
        data.update({"state", state})
        return Response(data)
