from flask import request, jsonify
from app.customers import customers_bp
from app.customers.schemas import customer_schema, customers_schema, login_schema
from app.models import Customer, ServiceTicket
from app.extensions import db, cache, limiter
from app.utils.auth import encode_token, token_required
from app.service_tickets.schemas import service_tickets_schema
from werkzeug.security import generate_password_hash, check_password_hash

@customers_bp.route('/', methods=['POST'])
def create_customer():
    userdata = request.get_json()
    errors = customer_schema.validate(userdata)
    if errors:
        return jsonify(errors), 400

    # Extract password and hash, saving it
    raw_password = userdata.pop('password')
    userdata['password'] = generate_password_hash(raw_password)

    new_customer = customer_schema.load(userdata)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@customers_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    userdata = request.get_json()
    errors = login_schema.validate(userdata)
    if errors:
        return jsonify(errors), 400

    email = userdata.get('email', '').strip().lower()
    customer = db.session.query(Customer).filter(db.func.lower(Customer.email) == email).first()
    
    # Check hashed password using werkzeug
    if customer and check_password_hash(customer.password, userdata.get('password')):
        token = encode_token(customer.id)
        return jsonify({"token": token, "message": "Login successful"}), 200

    return jsonify({"message": "Invalid email or password"}), 401

@customers_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    tickets = db.session.query(ServiceTicket).filter_by(customer_id=customer_id).all()
    return service_tickets_schema.jsonify(tickets), 200


#PAGINATION
@customers_bp.route('/', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    paginated = db.paginate(db.select(Customer), page=page, per_page=per_page)
    return jsonify({
        "customers": customers_schema.dump(paginated.items),
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages
    }), 200

@customers_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"message": "Unauthorized action"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    userdata = request.get_json()
    for key, value in userdata.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200

@customers_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_customer(customer_id, id):
    if customer_id != id:
        return jsonify({"message": "Unauthorized action"}), 403

    customer = db.session.get(Customer, id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f"Customer {id} deleted"}), 200