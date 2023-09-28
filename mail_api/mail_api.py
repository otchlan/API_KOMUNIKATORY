import imaplib
import email
from bs4 import BeautifulSoup

EMAIL = 'asystentai@deeptechlabs.pl'
PASSWORD = '12345678!'

# Nawiazuje polaczenie z serwerem IMAP i loguje sie na konto e-mail
def connect_to_server(email, password):
    mail = imaplib.IMAP4_SSL('imap.titan.email', 993)
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


def main():
    mail = connect_to_server(EMAIL, PASSWORD)
    email_nums = get_all_emails(mail)
    
    for num in email_nums:
         email_message = get_email_content(mail, num)
         subject, sender, recipients = extract_email_details(email_message)
         body = extract_email_body(email_message)
         
         main_content, footer = separate_footer_from_body(body)
         
         print("Temat:", subject)
         print("Nadawca:", sender)
         print("Adresaci:", recipients)
         print("Treść:", main_content)
         if footer:
             print("Stopka:", footer)
         print("------------------------------------------------------")
    
    mail.logout()

if __name__ == "__main__":
    main()
