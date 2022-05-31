import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from users.utils import UserUtils


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Function to process post action to send token to registered user.
    """

    if created:
        token, created = Token.objects.get_or_create(user=instance)
        UserUtils.send_email(
            user_id=instance.id,
            email_address=instance.email,
            token=token.key
        )
    else:
        if instance:
            # Delete used token after update
            try:
                user_token = Token.objects.get(user=instance)
            except Token.DoesNotExist:
                logging.warning(f'Token not found for user {instance}')
            else:
                user_token.delete()
                logging.warning(
                    f'Successfully deleted activation token for {instance}'
                )
