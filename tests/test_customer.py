import unittest
from app import create_app
from app.extensions import db
from app.models import Customer
from werkzeug.security import generate_password_hash
from app.utils.auth import encode_token

class CustomerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # initial customer
        self.customer = Customer(
            name="Mike Keller",
            email="Alice@example.com",
            phone="555-1111",
            password=generate_password_hash("password123")
        )
        db.session.add(self.customer)
        db.session.commit()
        self.token = encode_token(self.customer.id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_customer_positive(self):
        payload = {"name": "Joe", "email": "joe@example.com", "phone": "555-2222", "password": "pass"}
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_create_customer_negative(self):
        # Missing required field
        payload = {"name": "Invalid Customer"}
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_login_positive(self):
        res = self.client.post("/customers/login", json={"email": "alice@example.com", "password": "password123"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.get_json())

    def test_login_negative(self):
        res = self.client.post("/customers/login", json={"email": "alice@example.com", "password": "wrongpassword"})
        self.assertEqual(res.status_code, 401)

    def test_get_my_tickets_unauthorized(self):
        res = self.client.get("/customers/my-tickets")
        self.assertEqual(res.status_code, 401)

    def test_get_customers_paginated(self):
        res = self.client.get("/customers/?page=1&per_page=5")
        self.assertEqual(res.status_code, 200)
        self.assertIn("customers", res.get_json())