from flask import request, jsonify
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import service_ticket_schema, service_tickets_schema
from app.models import ServiceTicket, Mechanic, Inventory, Customer
from app.extensions import db

@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    userdata = request.get_json()
    errors = service_ticket_schema.validate(userdata)
    if errors:
        return jsonify(errors), 400

    if not db.session.get(Customer, userdata.get('customer_id')):
        return jsonify({"message": "Customer not found"}), 404

    new_ticket = service_ticket_schema.load(userdata)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201

@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    tickets = db.session.query(ServiceTicket).all()
    return service_tickets_schema.jsonify(tickets), 200

@service_tickets_bp.route('/<int:ticket_id>/edit', methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"message": "Service Ticket not found"}), 404

    userdata = request.get_json()
    add_ids = userdata.get('add_ids', [])
    remove_ids = userdata.get('remove_ids', [])

    for m_id in add_ids:
        mechanic = db.session.get(Mechanic, m_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for m_id in remove_ids:
        mechanic = db.session.get(Mechanic, m_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


@service_tickets_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket or not part:
        return jsonify({"message": "Service Ticket or Part not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200