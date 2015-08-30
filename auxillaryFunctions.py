from sendgrid import SendGridClient
from sendgrid import Mail


def sendEmail(sender, recipient, subject, html, text) :
    sg= SendGridClient('ecpf', 'Iheart1!', secure=True)
    message = Mail()
    message.set_subject(subject)
    message.set_html(html)
    message.set_text(text)
    message.set_from(sender)
    message.add_to(recipient)
    sg.send(message)
    return True

