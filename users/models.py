from authemail.models import EmailAbstractUser
from authemail.models import EmailUserManager


class MyCustomEmailUser(EmailAbstractUser):
    """
    Abastract Class for changing default user model.
    """

    objects = EmailUserManager()
