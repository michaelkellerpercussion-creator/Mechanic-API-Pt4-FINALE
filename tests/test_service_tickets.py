from tests.base_test import BaseTestCase

class ServiceTicketTestCase(BaseTestCase):
    def test_get_service_tickets(self):
        res = self.client.get("/service-tickets/")
        self.assertEqual(res.status_code, 200)

    def test_create_service_ticket_positive(self):
        customer, _ = self.create_test_customer()
        payload = {
            "vin": "1HGCR2F83HA123456",
            "service_desc": "Oil Change and Tire Rotation",
            "customer_id": customer.id
        }
        res = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(res.status_code, 201)

    def test_create_service_ticket_negative(self):
        # Invalid customer_id target
        payload = {
            "vin": "1HGCR2F83HA123456",
            "service_desc": "Oil Change",
            "customer_id": 9999
        }
        res = self.client.post("/service-tickets/", json=payload)
        self.assertEqual(res.status_code, 404)

    def test_bulk_edit_ticket_mechanics(self):
        customer, _ = self.create_test_customer()
        mechanic = self.create_test_mechanic()
        ticket = self.create_test_ticket(customer_id=customer.id)
        payload = {"add_ids": [mechanic.id], "remove_ids": []}
        res = self.client.put(f"/service-tickets/{ticket.id}/edit", json=payload)
        self.assertEqual(res.status_code, 200)

    def test_add_part_to_ticket(self):
        customer, _ = self.create_test_customer()
        part = self.create_test_part()
        ticket = self.create_test_ticket(customer_id=customer.id)
        res = self.client.put(f"/service-tickets/{ticket.id}/add-part/{part.id}")
        self.assertEqual(res.status_code, 200)

    def test_add_part_to_nonexistent_ticket_negative(self):
        part = self.create_test_part()
        res = self.client.put(f"/service-tickets/9999/add-part/{part.id}")
        self.assertEqual(res.status_code, 404)