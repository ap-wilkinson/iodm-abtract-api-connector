import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr
import os


def check_emails():
    # account credentials
    username = "support@apwilkinson.com"
    password = "Awaisfre123*"
    server = imaplib.IMAP4_SSL("imap.gmail.com")
    response = server.login(username, password)
    print(response)
    server.select("INBOX")

    # search for all emails
    status, messages = server.search(None, "ALL")
    messages = messages[0].split()
    print(messages)
    server.close()
    server.logout()
