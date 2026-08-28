from tests.base_test import BaseTestCase

class MechanicTestCase(BaseTestCase):
    def test_get_mechanics(self):
        self.create_test_mechanic()
        res = self.client.get("/mechanics/")
        self.assertEqual(res.status_code, 200)

    def test_create_mechanic_positive(self):
        payload = {"name": "Mike", "email": "mike@example.com", "phone": "555-4444", "salary": 60000.0}
        res = self.client.post("/mechanics/", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_update_mechanic_positive(self):
        mechanic = self.create_test_mechanic()
        payload = {"name": "Dan Updated", "email": "dan@example.com", "phone": "555-3333", "salary": 55000.0}
        res = self.client.put(f"/mechanics/{mechanic.id}", json=payload)
        self.assertEqual(res.status_code, 200)

    def test_update_mechanic_negative(self):
        res = self.client.put("/mechanics/9999", json={"name": "Dan", "email": "dan@example.com", "phone": "555-3333", "salary": 55000.0})
        self.assertEqual(res.status_code, 404)

    def test_delete_mechanic_positive(self):
        mechanic = self.create_test_mechanic()
        res = self.client.delete(f"/mechanics/{mechanic.id}")
        self.assertEqual(res.status_code, 200)

    def test_delete_mechanic_negative(self):
        res = self.client.delete("/mechanics/9999")
        self.assertEqual(res.status_code, 404)

    def test_get_most_active_mechanics(self):
        res = self.client.get("/mechanics/most-active")
        self.assertEqual(res.status_code, 200)