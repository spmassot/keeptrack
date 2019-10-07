from uuid import uuid4 as uuid
from flask import Blueprint, render_template, request, redirect, url_for
from src.models.customer import Customer
from src.constants import STATES


routes = Blueprint('customer', __name__, url_prefix='/customers')


@routes.route('', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        customers = Customer.scan()
        return render_template('customers.html', customers=customers)
    elif request.method == 'POST':
        new_customer = Customer(
            id=str(uuid()),
            name=request.form.get('customer_name'),
            email=request.form.get('customer_email'),
            attn=request.form.get('customer_attn'),
            address_1=request.form.get('customer_addr1'),
            address_2=request.form.get('customer_addr2'),
            city=request.form.get('customer_city'),
            state=request.form.get('customer_state'),
            zip_code=request.form.get('customer_zip'),
        )
        new_customer.save()
        return redirect(url_for('customer.index'))
    else:
        raise 404


@routes.route('/new', methods=['GET'])
def new():
    return render_template('new_customer.html', states=STATES)
