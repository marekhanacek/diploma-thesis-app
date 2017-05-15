from smtplib import SMTPAuthenticationError

from django.core.mail import send_mail as django_send_mail
from django.template.loader import get_template

from dip import settings
from dip.settings import ALLOW_MAIL_SENDING


def send_offer_mail(folder, file, subject, user, other_user, offer):
    to_email = "marekhanacek1@gmail.com"  # user.email
    plaintext = get_template('web/email/' + folder + '/' + file + '.txt')
    context = {
        'other_user_name': other_user.get_full_name(),
        'other_user_phone': other_user.userprofile.phone,
        'other_user_email': other_user.email,
        'currency_from': offer.currency_from_formatted(),
        'currency_to': offer.currency_to_formatted(),
    }
    if ALLOW_MAIL_SENDING:
        try:
            django_send_mail(
                subject,
                plaintext.render(context),
                settings.EMAIL_HOST_USER,
                [to_email]
            )
        except SMTPAuthenticationError:
            pass