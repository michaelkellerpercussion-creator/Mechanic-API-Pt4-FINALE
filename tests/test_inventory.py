from tests.base_test import BaseTestCase

class InventoryTestCase(BaseTestCase):
    def test_get_inventory_positive(self):
        self.create_test_part()
        res = self.client.get("/inventory/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.get_json(), list)

    def test_create_part_positive(self):
        res = self.client.post("/inventory/", json={"name": "Filter", "price": 19.99})
        self.assertEqual(res.status_code, 201)

    def test_create_part_negative(self):
        res = self.client.post("/inventory/", json={"name": "Missing Price"})
        self.assertEqual(res.status_code, 400)

    def test_update_part_positive(self):
        part = self.create_test_part()
        res = self.client.put(f"/inventory/{part.id}", json={"name": "Premium Spark Plug", "price": 15.99})
        self.assertEqual(res.status_code, 200)

    def test_update_part_negative(self):
        res = self.client.put("/inventory/9999", json={"name": "Nonexistent Part", "price": 10.00})
        self.assertEqual(res.status_code, 404)

    def test_delete_part_positive(self):
        part = self.create_test_part()
        res = self.client.delete(f"/inventory/{part.id}")
        self.assertEqual(res.status_code, 200)

    def test_delete_part_negative(self):
        res = self.client.delete("/inventory/9999")
        self.assertEqual(res.status_code, 404)