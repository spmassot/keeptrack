from flask import Blueprint, render_template
from src.models.invoice import Invoice
from src.models.customer import Customer
import src.data_utils as du


routes = Blueprint('index', __name__)


@routes.route('/')
def index():
    invoices = sorted([i for i in Invoice.scan() if not i.archived], key=lambda x: x.issued_on)
    customers = Customer.scan()
    invoices = du.left_join(invoices, 'customer_id', customers, 'id', ['name'])
    return render_template('index.html', invoices=invoices)
