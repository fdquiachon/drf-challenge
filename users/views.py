from authemail.views import Signup, Login, UserMe
from django.contrib.auth import get_user_model
from oauth2_provider.views import TokenView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import CustomSignupSerializer


class LoginUserView(TokenView):
    """
    User Login View
    """

    queryset = get_user_model().objects.filter(
        is_verified=True
    )
    permission_classes = (IsAuthenticated,)


class RegisterUserView(Signup):
    """
    View for user registration.
    """

    permission_classes = (AllowAny,)
    serializer_class = CustomSignupSerializer

    def post(self, request, format=None):
        """
        Function to customize post response of the user registration.
        """

        response = super().post(request, format)
        if response.status_code == status.HTTP_201_CREATED:
            custom_data = {
                    'user': response.data,
                    'errors': None
                }
        else:
            custom_data = {
                    'user': None,
                    'errors': response.data
                }
        response.data = custom_data
        return response
