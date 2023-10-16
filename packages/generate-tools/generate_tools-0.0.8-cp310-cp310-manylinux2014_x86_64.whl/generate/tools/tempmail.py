import html2text
import requests

import generate
from generate.exception import AuthorizedNeeded


class TempMail:
    def generate_email(self: 'generate.Generate', user_id: int):
        if not self.is_authorize:
            raise AuthorizedNeeded()

        email_addres = requests.get(
            "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=6).json()[0]
        username, domain = email_addres.split('@')
        self.insert(
            objec='email user_id username domain',
            data=(user_id, username, domain)
        )
        return email_addres


    def refresh_email(self: 'generate.Generate', username, domain):
        if not self.is_authorize:
            raise AuthorizedNeeded()

        response = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}", timeout=6).json()

        # if email have message
        if response:

            files = []
            # last message id
            email_id = response[0]["id"]
            # get message info
            response_msg = requests.get(
                f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={email_id}", timeout=6).json()
            email_from = response_msg["from"]
            email_subject = response_msg["subject"]
            email_date = response_msg["date"]
            email_html = response_msg["htmlBody"]
            email_text = html2text.html2text(email_html)
            attachments = response_msg["attachments"]

            # if message have attachments
            if attachments:
                files = [attachment["filename"] for attachment in attachments]
            return [email_id, email_from, email_subject, email_date, email_text, files]

        return "No Messages Were Received.."
