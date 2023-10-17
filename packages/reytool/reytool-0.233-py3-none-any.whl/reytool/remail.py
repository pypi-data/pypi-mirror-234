# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:19
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : E-mail methods.
"""


from typing import Dict, Iterable, Optional, Union
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .rsystem import get_first_notnull


__all__ = (
    "REmail",
)


class REmail(object):
    """
    Rey's `E-mail` type.
    """


    def __init__(
        self,
        email_username: str,
        email_password: str,
        display_from_email: Optional[str] = None
    ) -> None:
        """
        Build `E-mail` instance.

        Parameters
        ----------
        email_username : E-mail user name.
        email_password : E-mail password.
        display_from_email : Displayed from E-mail.
            - `None` : Not set.
            - `str` : Set this value.
        """

        # Set parameter.
        self.email_username = email_username
        self.email_password = email_password
        self.display_from_email = display_from_email


    def create_email(
        self,
        text: Optional[str] = None,
        title: Optional[str] = None,
        attachment: Optional[Dict[str, Union[str, bytes]]] = None,
        display_from_email: Optional[str] = None,
        display_to_email: Optional[Union[str, Iterable[str]]] = None,
        display_cc_email: Optional[Union[str, Iterable[str]]] = None
    ) -> str:
        """
        `Create` string in E-mail format.

        Parameters
        ----------
        text : E-mail text.
        title : E-mail title.
        attachment : E-mail attachment.
            - `Dict[str, str]` : File name and path.
            - `Dict[str, bytes]` : File name and stream.

        display_from_email : Displayed from E-mail.
        display_to_email : Displayed to E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.

        display_cc_email : Displayed cc E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.

        Returns
        -------
        String in E-mail format.
        """

        # Get parameter by priority.
        display_from_email = get_first_notnull(display_from_email, self.display_from_email, self.email_username)

        # Create E-mail object.
        mime = MIMEMultipart()
        if title is not None:
            mime["subject"] = title
        if text is not None:
            mime_text = MIMEText(text)
            mime.attach(mime_text)
        if attachment is not None:
            for file_name, file_data in attachment.items():
                if file_data.__class__ == str:
                    with open(file_data, "rb") as file:
                        file_data = file.read()
                mime_file = MIMEText(file_data, _charset="utf-8")
                mime_file.add_header("content-disposition", "attachment", filename=file_name)
                mime.attach(mime_file)
        if display_from_email is not None:
            mime["from"] = display_from_email
        if display_to_email is not None:
            if display_to_email.__class__ == str:
                mime["to"] = display_to_email
            else:
                mime["to"] = ",".join(display_to_email)
        if display_cc_email is not None:
            if display_cc_email.__class__ == str:
                mime["cc"] = display_cc_email
            else:
                mime["cc"] = ",".join(display_cc_email)

        # Create string in E-mail format.
        email_str = mime.as_string()

        return email_str


    def send_email(
        self,
        to_email: Union[str, Iterable[str]],
        text: Optional[str] = None,
        title: Optional[str] = None,
        attachment: Optional[Dict[str, Union[str, bytes]]] = None,
        cc_email: Optional[Union[str, Iterable[str]]] = None,
        display_from_email: Optional[str] = None,
        display_to_email: Optional[Union[str, Iterable[str]]] = None,
        display_cc_email: Optional[Union[str, Iterable[str]]] = None
    ) -> None:
        """
        `Send` E-mail.

        Parameters
        ----------
        to_email : To E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.

        text : E-mail text.
        title : E-mail title.
        attachment : E-mail attachment.
            - `Dict[str, str]` : File name and path.
            - `Dict[str, bytes]` : File name and stream.

        cc_email : Cc E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.

        display_from_email : Displayed from E-mail.
        display_to_email : Displayed to E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.

        display_cc_email : Displayed cc E-mail.
            - `str` : Set this value.
            - `Iterable[str]` : Set multiple values.
        """

        # Get parameter by priority.
        display_from_email = get_first_notnull(display_from_email, self.display_from_email, self.email_username)
        display_to_email = get_first_notnull(display_to_email, to_email)
        display_cc_email = get_first_notnull(display_cc_email, cc_email)

        # Handle parameter.
        if to_email.__class__ == str:
            to_email = [to_email]
        if cc_email is not None:
            if cc_email.__class__ == str:
                cc_email = [cc_email]
            to_email.extend(cc_email)

        # Create string in E-mail format.
        email_str = self.create_email(title, text, attachment, display_from_email, display_to_email, display_cc_email)

        # Send E-mail.
        server_domain_name = self.email_username.split("@")[-1]
        server_host = "smtp." + server_domain_name
        server_port = 25
        smtp = SMTP(server_host, server_port)
        smtp.login(self.email_username, self.email_password)
        smtp.sendmail(self.email_username, to_email, email_str)
        smtp.quit()