from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

from anyclean import util

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text


class DefaultAccountAdapter2(DefaultAccountAdapter):

    def send_mail(self, template_prefix, email, context):
        body = self.get_message(template_prefix, email, context)
        util.send_mail(email, body['subject'], body['txt'])
        return True


    def get_message(self, template_prefix, email, context):
        bodies = {}
        subject = render_to_string('{0}_subject.txt'.format(template_prefix),
                                   context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        site = context['site']
        subject = "[{name}] ".format(name=site.name) + force_text(subject)
        bodies['subject'] = subject

        for ext in ['html', 'txt']:
            try:
                template_name = '{0}_message.{1}'.format(template_prefix, ext)
                bodies[ext] = render_to_string(template_name,
                                               context).strip()
            except TemplateDoesNotExist:
                if ext == 'txt' and not bodies:
                    raise

        # if 'txt' in bodies:
        #     msg = EmailMultiAlternatives(subject,
        #                                  bodies['txt'],
        #                                  settings.DEFAULT_FROM_EMAIL,
        #                                  [email])
        #     if 'html' in bodies:
        #         msg.attach_alternative(bodies['html'], 'text/html')
        # else:
        #     msg = EmailMessage(subject,
        #                        bodies['html'],
        #                        settings.DEFAULT_FROM_EMAIL,
        #                        [email])
        #     msg.content_subtype = 'html'  # Main content is now text/html

        print bodies
        return bodies
