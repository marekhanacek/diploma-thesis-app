from django.template.loader import get_template

from dip import settings
from dip.settings import ALLOW_MAIL_SENDING


def send_mail(folder, file, to_email, subject, context):
    plaintext = get_template('web/email/' + folder + '/' + file + '.txt')
    # html = get_template('web/email/' + folder + '/' + file + '.html')
    # message = EmailMultiAlternatives(subject, plaintext.render(context), settings.EMAIL_HOST_USER, [to_email])
    # message.attach_alternative(html.render(context), "text/html")
    # if ALLOW_MAIL_SENDING or True:
    #     message.send()

    if ALLOW_MAIL_SENDING:
        send_mail(
            subject,
            plaintext.render(context),
            settings.EMAIL_HOST_USER,
            [to_email]
        )
