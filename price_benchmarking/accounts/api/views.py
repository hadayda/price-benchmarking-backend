import rest_framework.views
import rest_framework.response
import rest_framework.status

from price_benchmarking.accounts.api import serializers


class LoginAPIView(rest_framework.views.APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return rest_framework.response.Response(serializer.data)


