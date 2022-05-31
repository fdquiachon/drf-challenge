from django.core.mail import EmailMessage

from registration import settings


class UserUtils:
    """
    User utility class
    """

    @staticmethod
    def send_email(user_id, email_address, token):
        """
        Utility function for sending email registration token for
        account activation.
        """
        email_body = """
            <html>
              <head></head>
              <body>
                <h2>%s</h2>
                <p>%s</p>
                <p>%s</p>
                <p>%s</p>
                <p>%s</p>
              </body>
            </html>
        """ % (
            'My Exercise Registration',
            'To activate your account, send an HTTP PATCH request',
            f'To API: http://127.0.0.1:8001/api/v1/users/{user_id}',
            f'Header: {{"Authorization" : "Token: {token}"}} ',
            'Body: {"action" : "activate"} '
        )

        message = EmailMessage(
            subject='My Exercise Registration',
            body=email_body,
            from_email=settings.EMAIL_HOST_USER,
            to=[email_address],
            # TODO: Remove CC, Only added for testing
            cc=[settings.DEV_SUPPORT],
        )
        message.content_subtype = 'html'
        message.send()
