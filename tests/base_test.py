import unittest
from werkzeug.security import generate_password_hash
from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, Inventory, ServiceTicket
from app.utils.auth import encode_token

#Set Up
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

#Tear Down
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_customer(self, name="Alice Smith", email="alice@example.com", phone="555-1111", password="password123"):
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            password=generate_password_hash(password)
        )
        db.session.add(customer)
        db.session.commit()
        token = encode_token(customer.id)
        return customer, token

    def create_test_mechanic(self, name="Dan Mechanics", email="dan@example.com", phone="555-3333", salary=50000.0):
        mechanic = Mechanic(name=name, email=email, phone=phone, salary=salary)
        db.session.add(mechanic)
        db.session.commit()
        return mechanic

    def create_test_part(self, name="Spark Plug", price=12.99):
        part = Inventory(name=name, price=price)
        db.session.add(part)
        db.session.commit()
        return part

    def create_test_ticket(self, vin="12345678901234567", service_desc="Alignment", customer_id=1):
        ticket = ServiceTicket(vin=vin, service_desc=service_desc, customer_id=customer_id)
        db.session.add(ticket)
        db.session.commit()
        return ticket