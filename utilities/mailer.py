from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class MailBot():
    def emailConfirm(self, email, token, site):
        full_url = f"http://{site}/complete/{token}"
        message = render_to_string('email-confirm.html', {'url': full_url})
        subject = 'Adwatch Email Confirmation'
        mail_subject = subject
        to_email = email
        raw_message = strip_tags(message)
        from_email = 'Adwatch <noreply@adwatch.ai'
        print(full_url)
        try:
            mail.send_mail(mail_subject, raw_message, from_email, [to_email], html_message=message)
            print('sent')
            return True
        except Exception as e:
            print(e)
            return False