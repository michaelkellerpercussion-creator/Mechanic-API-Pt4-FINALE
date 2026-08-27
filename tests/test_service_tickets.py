import unittest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Customer, ServiceTicket, Mechanic, Inventory

class ServiceTicketTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        customer = Customer(name="Sam", email="sam@example.com", phone="555-0000", password=generate_password_hash("pass"))
        mechanic = Mechanic(name="Tech", email="tech@example.com", phone="555-1111", salary=55000.0)
        part = Inventory(name="Rotor", price=79.99)

        db.session.add_all([customer, mechanic, part])
        db.session.commit()

        self.ticket = ServiceTicket(vin="12345678901234567", service_desc="Alignment", customer_id=customer.id)
        db.session.add(self.ticket)
        db.session.commit()

        self.mechanic_id = mechanic.id
        self.part_id = part.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_service_tickets(self):
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)

    def test_bulk_edit_ticket_mechanics(self):
        payload = {"add_ids": [self.mechanic_id], "remove_ids": []}
        res = self.client.put(f"/service-tickets/{self.ticket.id}/edit", json=payload)
        self.assertEqual(res.status_code, 200)

    def test_add_part_to_ticket(self):
        res = self.client.put(f"/service-tickets/{self.ticket.id}/add-part/{self.part_id}")
        self.assertEqual(res.status_code, 200)

    def test_add_part_to_nonexistent_ticket_negative(self):
        res = self.client.put(f"/service-tickets/9999/add-part/{self.part_id}")
        self.assertEqual(res.status_code, 404)