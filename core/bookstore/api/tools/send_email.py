from django.core.mail import send_mail
from . import CustomException
from rest_framework import status


class Email:

    @staticmethod
    def send_token_by_template(
        receiver,
        template,
        message,
        subject='Mohammad Bana',
    ):
        try:
            send_mail(
                subject=f'{subject} verification',
                message=message,
                from_email="admin@admin.com",
                recipient_list=[receiver],
                fail_silently=False,
                html_message=template,
            )
            return True
        except Exception as e:
            raise CustomException(
                str(e), 'email_is_not_enabled', status_code=status.HTTP_400_BAD_REQUEST
            )
