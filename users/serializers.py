from authemail.serializers import SignupSerializer


class CustomSignupSerializer(SignupSerializer):
    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    def get_email_options(self):
        return {
            'email_template_name': 'authemail/signup_email.txt',
            'html_email_template_name': 'authemail/signup_email.html',
        }
