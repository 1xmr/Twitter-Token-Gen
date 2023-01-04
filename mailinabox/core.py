import requests
import base64
import uuid
import imaplib
import email
import time
import re
import typing as tp

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MailInABox(object):
    def __init__(self, username: str, password: str, hostname: str):
        """
            Parameters:
                    username (str): the admin's username (E.g: admin@example.com)
                    password (str): the admin's password
                    hostname (str): full hostname (E.g: box.example.com)
        """

        self._auth_token = base64.urlsafe_b64encode(f"{username}:{password}".encode()).decode()
        self._basic_url = f"https://{hostname}/admin"
        self._hostname = hostname

    @staticmethod
    def _get_random_string(length: int) -> str:
        return str(uuid.uuid4()).replace("-", "")[:length]

    def get_email(self, domain: str) -> "tp.Tuple[str, str]":
        email, password = self._get_random_string(16), self._get_random_string(12)
        email += f"@{domain}"

        requests.post(
            self._basic_url + "/mail/users/add",
            verify=False,
            headers={"authorization": f"Basic {self._auth_token}"},
            data={
                "email": email,
                "password": password,
                "privileges": ""
            }
        )

        return email, password

    def delete_email(self, email: str):
        requests.post(
            self._basic_url + "/mail/users/remove",
            verify=False,
            headers={"authorization": f"Basic {self._auth_token}"},
            data={"email": email}
        )

    def get_mailbox(
            self,
            subject_match: str,
            pattern: "tp.Union[tp.Pattern, str]",
            email_address: str,
            password: str,
            timeout: float = 60.0
    ) -> str:
        imap = imaplib.IMAP4_SSL(self._hostname, 993)
        imap.login(email_address, password)
        imap.select("Inbox")

        t0 = time.time()
        while time.time() - t0 < timeout:
            data = imap.search(None, "(UNSEEN)")[1]
            for num in data[0].split():
                data = imap.fetch(num, "(RFC822)")[1]
                em = email.message_from_bytes(data[0][1])

                if subject_match.lower() in em["subject"].lower():
                    for part in em.walk():
                        if part.get_content_type() == "text/plain":
                            part = part.get_payload(None, True)
                            found = re.search(pattern, part.decode())
                            if found is not None:
                                return found.group()

        raise TimeoutError("timeout of %.2f seconds exceeded" % timeout)


