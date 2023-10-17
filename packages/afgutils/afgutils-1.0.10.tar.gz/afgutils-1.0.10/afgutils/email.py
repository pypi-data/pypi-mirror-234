from os import getenv
import win32com.client as win32


def send_email(to: str = None, subject: str = None, message: str = "Empty Message"):
    # initial check
    if to is None and getenv('mail_to') is None:
        raise Exception("to should be passed as parameter or defined as env variable as mail_to")
    if to is None and getenv('mail_to'):
        to = getenv('mail_to')
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Body = message

    # To send html content
    # mail.HTMLBody = '<h2>HTML Message body</h2>'

    # To attach a file to the email (optional):
    # attachment = "Path to the attachment"
    # mail.Attachments.Add(attachment)

    mail.Send()
