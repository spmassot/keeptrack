from flask import Blueprint, render_template
from src.models.invoice import Invoice
import src.data_utils as du


routes = Blueprint('archive', __name__)


@routes.route('/archive')
def archive():
    invoices = sorted([i for i in Invoice.scan() if i.archived], key=lambda x: x.issued_on)
    return render_template('archive.html', invoices=invoices)
