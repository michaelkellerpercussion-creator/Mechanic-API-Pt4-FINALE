import unittest
from app import create_app
from app.extensions import db
from app.models import Mechanic

class MechanicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.mechanic = Mechanic(name="Dan", email="dan@example.com", phone="555-3333", salary=50000.0)
        db.session.add(self.mechanic)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_mechanics(self):
        res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)

    def test_create_mechanic_positive(self):
        payload = {"name": "Mike", "email": "mike@example.com", "phone": "555-4444", "salary": 60000.0}
        res = self.client.post("/mechanics/", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_update_mechanic_negative(self):
        res = self.client.put("/mechanics/9999", json={"salary": 70000.0})
        self.assertEqual(res.status_code, 404)

    def test_get_most_active_mechanics(self):
        res = self.client.get("/mechanics/most-active")
        self.assertEqual(res.status_code, 200)