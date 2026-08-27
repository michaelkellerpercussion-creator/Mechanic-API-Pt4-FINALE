import unittest
from app import create_app
from app.extensions import db
from app.models import Inventory

class InventoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.TestingConfig")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.part = Inventory(name="Spark Plug", price=12.99)
        db.session.add(self.part)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_part_positive(self):
        res = self.client.post("/inventory/", json={"name": "Filter", "price": 19.99})
        self.assertEqual(res.status_code, 201)

    def test_create_part_negative(self):
        res = self.client.post("/inventory/", json={"name": "Missing Price"})
        self.assertEqual(res.status_code, 400)

    def test_delete_part_negative(self):
        res = self.client.delete("/inventory/9999")
        self.assertEqual(res.status_code, 404)