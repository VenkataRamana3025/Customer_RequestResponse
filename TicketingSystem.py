from gettext import install
pip install flask flask-sqlalchemy
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=False)
    request_detail = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    priority = db.Column(db.String(20), default='Low')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Ticket {self.id}>"

db.create_all()

@app.route('/create_ticket', methods=['POST'])
def create_ticket():
    data = request.get_json()
    new_ticket = Ticket(
        customer_name=data['customer_name'],
        request_detail=data['request_detail']
    )
    db.session.add(new_ticket)
    db.session.commit()
    return jsonify({"message": "Ticket created", "ticket_id": new_ticket.id})

@app.route('/get_tickets', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify([{
        'id': ticket.id,
        'customer_name': ticket.customer_name,
        'request_detail': ticket.request_detail,
        'status': ticket.status,
        'priority': ticket.priority,
        'created_at': ticket.created_at
    } for ticket in tickets])

if __name__ == '__main__':
    app.run(debug=True)
    def prioritize_ticket(ticket):
    if "urgent" in ticket.request_detail.lower():
        ticket.priority = 'High'
    elif "important" in ticket.request_detail.lower():
        ticket.priority = 'Medium'
    else:
        ticket.priority = 'Low'

@app.route('/update_priority', methods=['POST'])
def update_priority():
    tickets = Ticket.query.all()
    for ticket in tickets:
        prioritize_ticket(ticket)
    db.session.commit()
    return jsonify({"message": "Priorities updated"})

if __name__ == '__main__':
    app.run(debug=True)
class TicketUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    update_detail = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TicketUpdate {self.id}>"

db.create_all()

@app.route('/add_update', methods=['POST'])
def add_update():
    data = request.get_json()
    new_update = TicketUpdate(
        ticket_id=data['ticket_id'],
        update_detail=data['update_detail']
    )
    db.session.add(new_update)
    db.session.commit()
    return jsonify({"message": "Update added"})

@app.route('/get_ticket_updates/<int:ticket_id>', methods=['GET'])
def get_ticket_updates(ticket_id):
    updates = TicketUpdate.query.filter_by(ticket_id=ticket_id).all()
    return jsonify([{
        'id': update.id,
        'ticket_id': update.ticket_id,
        'update_detail': update.update_detail,
        'updated_at': update.updated_at
    } for update in updates])

if __name__ == '__main__':
    app.run(debug=True)

