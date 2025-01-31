import imaplib
import email
from email.header import decode_header
from django.conf import settings
# kmlx zfox ibnx taoc
import imaplib
import email
from email.header import decode_header
import os

def check_emails():
    # Set up the connection to Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    
    try:
        # Login to Gmail (use an App Password if using 2FA)
        mail.login("support@apwilkinson.com", "kmlx zfox ibnx taoc")  # Replace with your credentials

        # Select the mailbox you want to read from (INBOX is the default)
        mail.select('inbox')

        # Search for all emails (you can filter by specific criteria, like UNSEEN for unread emails)
        status, messages = mail.search(None, 'ALL')
        
        # Convert messages to a list of email IDs
        email_ids = messages[0].split()

        for email_id in email_ids[-10:]:  # Retrieve the last 10 emails
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            
            # Parse the email content
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes) and subject:
                        subject = subject.decode(encoding if encoding else 'utf-8')

                    # Decode the sender's email address
                    from_ = msg.get("From")
                    
                    # Check if the email has attachments
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            # Check if the part is an attachment
                            if "attachment" in content_disposition:
                                filename = part.get_filename()
                                if filename and filename.lower().endswith(".pdf"):
                                    print(f"Found PDF attachment: {filename}")

                                    # Get the PDF content
                                    pdf_content = part.get_payload(decode=True)
                                    
                                    # Save the PDF content to a file (optional)
                                    if "invoice" in filename:
                                        pdf_path = os.path.join("/", 
                                                                )
                                        with open(pdf_path, "wb") as pdf_file:
                                            pdf_file.write(pdf_content)

                                        # Call the upload_attachment function with the PDF and sender's name
                                        sender_name = from_  # You can also extract the sender's name more explicitly if needed
                                        upload_attachment(pdf_path, sender_name)

                                        # Optionally delete the downloaded PDF after processing
                                        os.remove(pdf_path)

                    else:
                        # If it's not multipart, check if the email itself is a PDF attachment (less likely)
                        body = msg.get_payload(decode=True).decode()
                        
                        
        # Logout after processing
        mail.logout()

    except Exception as e:
        print(f"An error occurred: {e}")


# Dummy upload_attachment function (you can replace it with your actual implementation)
def upload_attachment(pdf_path, sender_name):
    print(f"Uploading PDF {pdf_path} from {sender_name}...")

# Example call
# check_emails()


# Example call to read emails
# read_emails()
