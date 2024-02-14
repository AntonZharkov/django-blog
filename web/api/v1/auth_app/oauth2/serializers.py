from main.choices import SocialProvider
from rest_framework import serializers


class OAuthRedirectsParamsSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=SocialProvider.choices)


class OAuthProviderParamsSerializer(serializers.Serializer):
    state = serializers.CharField()
    client_id = serializers.CharField()
