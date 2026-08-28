from tests.base_test import BaseTestCase

class CustomerTestCase(BaseTestCase):
    def test_create_customer_positive(self):
        payload = {"name": "Bob", "email": "bob@example.com", "phone": "555-2222", "password": "pass"}
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_create_customer_negative(self):
        # Missing required field
        payload = {"name": "Invalid Customer"}
        res = self.client.post("/customers/", json=payload)
        self.assertEqual(res.status_code, 400)

    def test_login_positive(self):
        # Corrected: Login with alice@example.com matching the created setup customer
        customer, _ = self.create_test_customer(email="alice@example.com", password="password123")
        res = self.client.post("/customers/login", json={"email": "alice@example.com", "password": "password123"})
        self.assertEqual(res.status_code, 200)
        self.assertIn("token", res.get_json())

    def test_login_negative(self):
        self.create_test_customer(email="alice@example.com", password="password123")
        res = self.client.post("/customers/login", json={"email": "alice@example.com", "password": "wrongpassword"})
        self.assertEqual(res.status_code, 401)

    def test_get_my_tickets_unauthorized(self):
        res = self.client.get("/customers/my-tickets")
        self.assertEqual(res.status_code, 401)

    def test_get_my_tickets_authorized(self):
        customer, token = self.create_test_customer()
        self.create_test_ticket(customer_id=customer.id)
        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.get("/customers/my-tickets", headers=headers)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_get_customers_paginated(self):
        self.create_test_customer()
        res = self.client.get("/customers/?page=1&per_page=5")
        self.assertEqual(res.status_code, 200)
        self.assertIn("customers", res.get_json())

    def test_update_customer_positive(self):
        customer, token = self.create_test_customer()
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"phone": "555-9999"}
        res = self.client.put(f"/customers/{customer.id}", json=payload, headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_update_customer_forbidden_negative(self):
        customer1, token1 = self.create_test_customer(email="user1@example.com")
        customer2, token2 = self.create_test_customer(email="user2@example.com")
        headers = {"Authorization": f"Bearer {token1}"}
        # Attempting to edit customer2 while authenticated as customer1
        res = self.client.put(f"/customers/{customer2.id}", json={"phone": "555-0000"}, headers=headers)
        self.assertEqual(res.status_code, 403)

    def test_delete_customer_positive(self):
        customer, token = self.create_test_customer()
        headers = {"Authorization": f"Bearer {token}"}
        res = self.client.delete(f"/customers/{customer.id}", headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_delete_customer_forbidden_negative(self):
        customer1, token1 = self.create_test_customer(email="user1@example.com")
        customer2, token2 = self.create_test_customer(email="user2@example.com")
        headers = {"Authorization": f"Bearer {token1}"}
        res = self.client.delete(f"/customers/{customer2.id}", headers=headers)
        self.assertEqual(res.status_code, 403)