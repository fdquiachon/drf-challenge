from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for custom user model.
    """

    class Meta:
        model = get_user_model()
        fields = ('first_name',)


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer class for custom user model.
    """

    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all()
            )
        ],
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = (
            'first_name', 'last_name', 'email'
        )
