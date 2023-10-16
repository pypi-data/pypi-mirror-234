import os
import typing as T
from types import TracebackType #pylint: disable=no-name-in-module
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import qtc.env_config as ecfg
import qtc.utils.misc_utils as mu
from qtc.ext.logging import set_logger
logger = set_logger()

USER_FULLNAME_MAP = {}


def normalize_email(email_address: str, domain: str='heimdalgroup.com') -> str:
    """
    >>> import qtc.utils.email_utils as emailu
    >>> emailu.normalize_email('ahu')
    'ahu@***.com'
    """
    #at_domain = f'@{domain}'
    #if email_address.lower().endswith(at_domain):
    #    return email_address

    #if '@' in email_address:
    #    raise Exception(f'Invalid character "@" found in email {email_address}. '
    #                    f'Valid email addresses either are simple user names (ie. "jd") '
    #                    f'or end with {at_domain} (ie. jd{at_domain}).')

    if '@' in email_address:
        return email_address

    at_domain = f'@{domain}'
    user_full_name = USER_FULLNAME_MAP.get(email_address, None)
    email_address += at_domain
    return email_address if user_full_name is None else f'{user_full_name}<{email_address}>'


def normalize_email_list(email_list):
    if email_list is None:
        return list()

    return [normalize_email(ea) for ea in mu.iterable_to_tuple(email_list, raw_type='str') if len(ea) > 0]


def get_email_meta_field(field: str,
                         email_app=None,
                         default: str = None,
                         ) -> str:
    """
    >>> import qtc.utils.email_utils as emailu
    >>> emailu.get_email_meta_field(field='from', email_app='hedge_optimizer')
    'QTHO'
    >>> emailu.get_email_meta_field(field='from')
    """
    cfg = ecfg.get_env_config()
    default = cfg.get(f'email.{field}', default)
    if email_app is None:
        return default
    #
    # email_app_name = email_app.value if isinstance(email_app, ecfg.EmailApp) else email_app
    email_app_name = email_app
    return cfg.get(f'email.{email_app_name}.{field}', default)


def format_email_subject(subject: str, email_app=None) -> str:
    """
    Formats an email subject for a given EmailApp as specified for this environment.

    In most cases, that means emails in DEV will be:

    '[DEV] email subject'

    ... emails in UAT will be:

    '[UAT] email subject'

    ... and emails in PROD will be:

    'email subject'
    >>> import qtc.utils.email_utils as emailu
    >>> emailu.format_email_subject(subject='test subject', email_app='hedge_optimizer')
    """
    subject_fmt = get_email_meta_field(field='subject_fmt', email_app=email_app)
    if subject_fmt is None:
        return subject
    return subject_fmt.format(subject=subject)


class EmailMeta:
    def __init__(self, email_app=None,
                 smtp_server = None,
                 from_address = None,
                 to_address_list = None,
                 cc_address_list = None,
                 bcc_address_list = None):
        self.smtp_server = get_email_meta_field(field='smtp_server', email_app=email_app,
                                                default=smtp_server)
        self.from_address = normalize_email(email_address=get_email_meta_field(field='from', email_app=email_app,
                                                                               default=from_address))
        self.to_address_list = normalize_email_list(get_email_meta_field(field='to', email_app=email_app,
                                                                         default=to_address_list))
        self.cc_address_list = normalize_email_list(get_email_meta_field(field='cc', email_app=email_app,
                                                                         default=cc_address_list))
        self.bcc_address_list = normalize_email_list(get_email_meta_field(field='bcc', email_app=email_app,
                                                                          default=bcc_address_list))

    def __repr__(self):
        return f'SMTP: {self.smtp_server}\n' \
               f'From: {self.from_address}\n' \
               f'To  : {self.to_address_list}\n' \
               f'CC  : {self.cc_address_list}\n' \
               f'BCC : {self.bcc_address_list}\n'


class HtmlEmail:
    def __init__(self,
                 subject: str,
                 email_app=None,
                 *,
                 smtp_server = 'localhost:25', # set default smtp_server here!!!
                 from_address = None,
                 to_address_list = None,
                 cc_address_list = None,
                 bcc_address_list = None
                 ) -> None:
        # self._email_app = email_app
        self._subject = format_email_subject(subject=subject, email_app=email_app)
        self._email_meta = EmailMeta(email_app=email_app,
                                     smtp_server=smtp_server,
                                     from_address=from_address,
                                     to_address_list=to_address_list,
                                     cc_address_list=cc_address_list,
                                     bcc_address_list=bcc_address_list)

        # self._email_app_name = email_app.value if isinstance(email_app, ecfg.EmailApp) else email_app
        self._email_app_name = email_app

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self._subject
        msg['From'] = self._email_meta.from_address
        msg['To'] = ','.join(self._email_meta.to_address_list)
        msg['Cc'] = ','.join(self._email_meta.cc_address_list)
        msg['Bcc'] = ','.join(self._email_meta.bcc_address_list)

        self._msg = msg

    def add_html(self, html: str) -> None:
        text = MIMEText(html, 'html')
        self._msg.attach(text)

    def attach_file(self, attachment_name: str, attachment) -> None: #type: ignore
        part = MIMEApplication(attachment.read(), Name=attachment_name)
        part['Content-Disposition'] = f'attachment; filename="{attachment_name}"'
        self._msg.attach(part)

    def attach_file_from_filesystem(self,
                                    filename: str,
                                    *,
                                    attachment_name = None
                                    ) -> None:
        with open(filename, mode="rb") as attachement:
            if attachment_name is None:
                attachment_name = os.path.basename(filename)
            self.attach_file(attachment_name, attachement)

    def __enter__(self): #type: ignore
        return self

    def __exit__(self, exc_type: type, exc_val: T.Any, exc_tb: TracebackType) -> None:
        title = f'Email: {self._subject}'
        if self._email_app_name is not None:
            title += f' ({self._email_app_name})'

        if exc_val is None:
            logger.info(f"Email SMTP: ({self._email_meta.smtp_server})")
            logger.info(f"Email From: ({self._msg['From']})")
            logger.info(f"Email To  : ({self._msg['To']})")
            logger.info(f"Email Cc  : ({self._msg['Cc']})")
            logger.info(f"Email BCc : ({self._msg['Bcc']})")

            smtp = smtplib.SMTP(self._email_meta.smtp_server)
            smtp.send_message(self._msg)
            logger.info(f'Sent {title}')
            smtp.quit()
        else:
            logger.error(f'Failed in sending {title} with exc_val={exc_val}, exc_tb={exc_tb} !')