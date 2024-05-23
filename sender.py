import smtplib
import itertools
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

banner = """
    
    ██████╗  █████╗ ██╗  ██╗███████╗██████╗ 
    ██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗
    ██████╔╝███████║█████╔╝ █████╗  ██████╔╝
    ██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗
    ██████╔╝██║  ██║██║  ██╗███████╗██║  ██║
    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ Sender By https://t.me/BAK34_TMW / Discord: https://discord.com/users/825505380452925470
    """

def load_smtp_servers(smtp_file):
    if not os.path.isfile(smtp_file):
        raise FileNotFoundError(f"The SMTP file '{smtp_file}' does not exist.")
    with open(smtp_file, 'r') as f:
        lines = f.readlines()
        smtp_servers = []
        for line in lines:
            host, port, email, password = line.strip().split('|')
            smtp_servers.append({'host': host, 'port': int(port), 'email': email, 'password': password})
        return smtp_servers

def load_recipients(recipients_file):
    if not os.path.isfile(recipients_file):
        raise FileNotFoundError(f"The recipients file '{recipients_file}' does not exist.")
    with open(recipients_file, 'r') as f:
        recipients = f.read().splitlines()
    return recipients

def load_email_content(email_file):
    if not os.path.isfile(email_file):
        raise FileNotFoundError(f"The email HTML file '{email_file}' does not exist.")
    with open(email_file, 'r') as f:
        return f.read()

def send_email(smtp_server, to_email, sender_name, subject, email_content):
    try:
        server = smtplib.SMTP(smtp_server['host'], smtp_server['port'])
        server.starttls()
        server.login(smtp_server['email'], smtp_server['password'])

        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{smtp_server['email']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_content, 'html'))

        server.sendmail(smtp_server['email'], to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email} using {smtp_server['email']}")
    except Exception as e:
        print(f"Failed to send email to {to_email} using {smtp_server['email']}: {e}")
        return False
    return True

def main():
    print(banner)
    smtp_file = input("Enter the path to the SMTP file: ")
    recipients_file = input("Enter the path to the recipients file: ")
    email_file = input("Enter the path to the email HTML file: ")
    sender_name = input("Enter the sender name: ")
    subject = input("Enter the email subject: ")

    try:
        smtp_servers = load_smtp_servers(smtp_file)
        recipients = load_recipients(recipients_file)
        email_content = load_email_content(email_file)
    except FileNotFoundError as e:
        print(e)
        return

    smtp_cycle = itertools.cycle(smtp_servers)
    failed_servers = set()

    for recipient in recipients:
        for _ in range(len(smtp_servers)):
            smtp_server = next(smtp_cycle)
            smtp_server_tuple = (smtp_server['host'], smtp_server['port'], smtp_server['email'])
            if smtp_server_tuple in failed_servers:
                continue
            if send_email(smtp_server, recipient, sender_name, subject, email_content):
                break
            else:
                failed_servers.add(smtp_server_tuple)
        else:
            print(f"Failed to send email to {recipient}: No working SMTP servers left")

if __name__ == '__main__':
    main()
