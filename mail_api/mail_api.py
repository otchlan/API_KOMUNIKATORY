import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import imaplib
import email
from bs4 import BeautifulSoup
from database.db_session import SessionLocal
from database.models.message_model import Message

from config.config import Config  

EMAIL = Config.EMAIL_USERNAME_AI
PASSWORD = Config.EMAIL_PASSWORD
ATTACHMENTS_DIR = Config.ATTACHMENT_DIR
IMAP_SERVER = Config.IMAP_SERVER
IMAP_PORT = Config.IMAP_PORT

# Nawiazuje polaczenie z serwerem IMAP i loguje sie na konto e-mail
def connect_to_server(email, password):
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(email, password)
    return mail

# Pobiera wszystkie numery e-maili z "inbox"
def get_all_emails(mail):
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    return data[0].split()

# Pobiera zawartosc konkretnego e-maila na podstawie jego numeru
def get_email_content(mail, num):
    result, msg_data = mail.fetch(num, '(RFC822)')
    raw_email = msg_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    return email_message    

# Wyciaga podstawowe informacje z e-maila
def extract_email_details(email_message):
    subject = email_message['subject']
    sender = email_message['from']
    recipients = email_message['to']
    return subject, sender, recipients

def separate_footer_from_body(body):
    # Zakładamy, że stopka zaczyna się od frazy "Pozdrawiam"
    split_body = body.split("Pozdrawiam", 1)
    
    main_content = split_body[0].strip()
    footer = "Pozdrawiam" + split_body[1] if len(split_body) > 1 else None
    
    return main_content, footer

# Wyciaga tresc e-maila
def extract_email_body(email_message):
    content_type = None

    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if "attachment" not in content_disposition and (content_type == "text/plain" or content_type == "text/html"):
                body = part.get_payload(decode=True).decode()
                break
    else:
        body = email_message.get_payload(decode=True).decode()
    
    if content_type == "text/html":
        soup = BeautifulSoup(body, "html.parser")
        body = soup.get_text()
    
    return body.strip()

def extract_email_footer(email_message):
    body = extract_email_body(email_message)
    if "Pozdrawiam" in body:
        return body.split("Pozdrawiam", 1)[1].strip()
    return None

def extract_original_content(email_message):
    body = extract_email_body(email_message)
    # Zakładając, że oryginalna treść kończy się przed "Pozdrawiam"
    if "Pozdrawiam" in body:
        return body.split("Pozdrawiam", 1)[0].strip()
    return body  # Jeśli nie ma "Pozdrawiam", zwróć całą treść jako oryginalną

def save_attachments(email_message):
    """
    Save attachments from an email message.
    """
    attachments = []
    if not os.path.exists(ATTACHMENTS_DIR):
        os.makedirs(ATTACHMENTS_DIR)
    
    for part in email_message.walk():
        content_disposition = str(part.get("Content-Disposition"))
        if "attachment" in content_disposition:
            file_name = part.get_filename()
            if file_name:
                file_path = os.path.join(ATTACHMENTS_DIR, file_name)
                with open(file_path, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                attachments.append(file_path)
    return attachments

def save_email_to_db(subject, sender, recipients, content, footer, original_content):
    # Create a new session
    session = SessionLocal()

    # Create a new message instance
    new_message = Message(
        source="email",
        subject=subject,
        sender=sender,
        recipients=recipients,
        content=content,
        footer=footer,
        original_content=original_content
    )

    # Add the new message to the session
    session.add(new_message)

    # Commit the session to save the data
    session.commit()

    # Close the session
    session.close()

def main():
    mail = connect_to_server(EMAIL, PASSWORD)
    email_nums = get_all_emails(mail)
    
    for num in email_nums:
        email_message = get_email_content(mail, num)
        subject, sender, recipients = extract_email_details(email_message)
        body = extract_email_body(email_message)
        footer = extract_email_footer(email_message)
        original_content = extract_original_content(email_message)
        
        attachments = save_attachments(email_message)
        print(f"Saved attachments: {', '.join(attachments) if attachments else 'No attachments'}")
        
        save_email_to_db(subject, sender, recipients, body, footer, original_content)
        
        print("Subject:", subject)
        print("Sender:", sender)
        print("Recipients:", recipients)
        print("Body:", body)
        print("------------------------------------------------------")
    
    mail.logout()

if __name__ == "__main__":
    main()
