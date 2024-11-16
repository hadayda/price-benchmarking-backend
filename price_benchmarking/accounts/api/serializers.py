import rest_framework.serializers
import rest_framework.authtoken.models
from django.contrib.auth import authenticate


class LoginSerializer(rest_framework.serializers.Serializer):
    token = rest_framework.serializers.CharField(read_only=True)
    email = rest_framework.serializers.EmailField(write_only=True)
    password = rest_framework.serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(username=email, password=password)
        if not user:
            raise rest_framework.serializers.ValidationError('Invalid email or password.')
        token_object, _ = rest_framework.authtoken.models.Token.objects.get_or_create(user=user)
        attrs['token'] = token_object.key
        return attrs
