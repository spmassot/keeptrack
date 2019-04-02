from uuid import uuid4 as uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from src.models.invoice import Invoice, Task
from src.models.customer import Customer
from src.reports.invoice import InvoiceReportGenerator



routes = Blueprint('invoice', __name__, url_prefix='/invoices')


@routes.route('/new', methods=['GET'])
def new():
    return render_template(
        'new_invoice.html',
        customers=Customer.scan()
    )


@routes.route('', methods=['POST'])
def create():
    tasks = [
        Task(
            date=request.form.get(f'task{i}_date'),
            hours=float(request.form.get(f'task{i}_hours')),
            description=request.form.get(f'task{i}_description'),
            rate=float(request.form.get(f'task{i}_rate'))
        ) for i in range(7) if request.form.get(f'task{i}_hours') != ''
    ]
    new_invoice = Invoice(
        id=str(uuid()),
        number=int(request.form.get('invoice_number')),
        customer_id=request.form.get('customer_select'),
        issued_on=datetime.now(),
        total=sum([t.hours * t.rate for t in tasks]),
        tasks=[t.__dict__ for t in tasks]
    )
    new_invoice.save()
    return redirect(url_for('index.index'))


@routes.route('/<invoice_id>/paid', methods=['POST'])
def mark_paid(invoice_id):
    invoice = Invoice.get_one(invoice_id)
    invoice.set_attributes(paid_on=datetime.now())
    return redirect(url_for('index.index'))


@routes.route('/<invoice_id>/delete', methods=['POST'])
def delete_invoice(invoice_id):
    invoice = Invoice.get_one(invoice_id)
    invoice.delete()
    return redirect(url_for('index.index'))


@routes.route('/<invoice_id>/download', methods=['POST'])
def download_invoice(invoice_id):
    invoice = Invoice.get_one(invoice_id)
    i = InvoiceReportGenerator(invoice)
    report = i.write_report()
    return send_file(report[1], attachment_filename=report[0], as_attachment=True)
