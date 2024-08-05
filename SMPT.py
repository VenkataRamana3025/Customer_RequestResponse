import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body, to):
    msg = MIMEMultipart()
    msg['From'] = 'youremail@example.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('youremail@example.com', 'password')
    text = msg.as_string()
    server.sendmail('youremail@example.com', to, text)
    server.quit()

@app.route('/notify_customer', methods=['POST'])
def notify_customer():
    data = request.get_json()
    ticket = Ticket.query.get(data['ticket_id'])
    if ticket:
        send_email(
            subject=f"Update on your request #{ticket.id}",
            body=f"Dear {ticket.customer_name}, your request status is now '{ticket.status}'",
            to='customer@example.com'
        )
        return jsonify({"message": "Notification sent"})
    return jsonify({"message": "Ticket not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
