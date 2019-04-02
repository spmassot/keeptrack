from io import BytesIO
import xlsxwriter
from os import getenv as e
from src.models.customer import Customer
from src.custom_filters import format_datetime


class InvoiceReportGenerator:
    def __init__(self, invoice, **kwargs):
        self.invoice = invoice
        self.output = BytesIO()
        self.workbook = xlsxwriter.Workbook(self.output)
        self.worksheet = self.workbook.add_worksheet(str(self.invoice.number))
        self.my_address = self.get_address()
        self.customer = Customer.get_one(self.invoice.customer_id)
        self.fmt = Formatters(self.workbook)

    def get_address(self):
        return [
            f"{e('ADDR_NAME')}",
            f"{e('ADDR_ADD1')} {e('ADDR_ADD2')}",
            f"{e('ADDR_CITY')}, {e('ADDR_STATE')} {e('ADDR_ZIP')}",
            f"{e('ADDR_PHONE')}",
            f"{e('ADDR_EMAIL')}"
        ]

    def write_report(self):
        self.format_sheet()
        self.render_address()
        self.render_customer()
        self.render_tasks()
        self.render_totals()
        self.render_metadata()
        self.workbook.close()
        self.output.seek(0)
        return (f'Invoice-{self.invoice.number}.xlsx', self.output)

    def format_sheet(self):
        self.worksheet.hide_gridlines(option=2)
        self.worksheet.set_column('A:A', 2)
        self.worksheet.set_column('B:B', 12)
        self.worksheet.set_column('C:C', 60)
        self.worksheet.set_column('D:D', 5)
        self.worksheet.set_column('E:E', 6)
        self.worksheet.set_column('F:F', 12)
        for i in range(1, 26):
            self.worksheet.set_row(i, 21)

    def render_address(self):
        self.worksheet.write_column('B1', self.my_address[:-1], self.fmt.make())
        self.worksheet.write_row('B5', [self.my_address[-1], '', '', ''], self.fmt.make('dotted'))

    def render_tasks(self):
        all_tasks = self.invoice.tasks + ['']*(6-len(self.invoice.tasks))
        for i, task in enumerate(all_tasks):
            if task == '':
                data = ['']*5
            else:
                data = [task.get(i) for i in ['date', 'description', 'hours', 'rate']]
                data.append(task['hours'] * task['rate'])
            if i == len(all_tasks) - 1:
                self.worksheet.write_row(f'B{i+11}', data, self.fmt.make('border', 'bottom', 'money'))
            else:
                self.worksheet.write_row(f'B{i+11}', data, self.fmt.make('border', 'money'))
        headers = ['Date', 'Description', 'Hours', 'Rate', 'Amount']
        self.worksheet.write_row('B10', headers, self.fmt.make('bold', 'bottom'))

    def render_totals(self):
        total = sum([t['hours'] * t['rate'] for t in self.invoice.tasks])
        self.worksheet.write('E17', 'Total', self.fmt.make('bold', 'ital'))
        self.worksheet.write('F17', total, self.fmt.make('bold', 'border', 'bg', 'top', 'money'))
        if self.invoice.paid_on:
            self.worksheet.write(
                'F18',
                f'PAID ON {format_datetime(self.invoice.paid_on)}',
                self.fmt.make('bold')
            )

    def render_customer(self):
        data = [
            i for i in [
                self.customer.attn,
                self.customer.address_1,
                self.customer.address_2,
                f'{self.customer.city}, {self.customer.state} {self.customer.zip_code}'
            ] if i is not None
        ]
        self.worksheet.write_column('C6', data, self.fmt.make())

    def render_metadata(self):
        self.worksheet.write('B6', 'Bill to:', self.fmt.make('bold'))
        self.worksheet.write('F5', 'Date:', self.fmt.make('bold'))
        self.worksheet.write('F6', format_datetime(self.invoice.issued_on), self.fmt.make('border', 'bg', 'center'))
        self.worksheet.write('F7', 'Invoice:', self.fmt.make('bold'))
        self.worksheet.write('F8', self.invoice.number, self.fmt.make('border', 'bg', 'center'))


class Formatters:
    _formatters_ = {}

    def __init__(self, workbook):
        self.workbook = workbook

    def base(self):
        f = self.workbook.add_format()
        f.set_font_name('Consolas')
        f.set_font_size(10)
        return f

    def bold(self, f):
        f.set_bold()
        return f

    def ital(self, f):
        f.set_italic()
        return f

    def dotted(self, f):
        f.set_bottom(3)
        return f

    def border(self, f):
        f.set_border(3)
        return f

    def bg(self, f):
        f.set_bg_color('#b8ddcc')
        return f

    def bottom(self, f):
        f.set_bottom(2)
        return f

    def top(self, f):
        f.set_top(2)
        return f

    def center(self, f):
        f.set_align('center')
        return f

    def money(self, f):
        f.set_num_format('0.00')
        return f

    def make(self, *args):
        props = tuple(sorted(set(args)))
        existing = self._formatters_.get(props, False)
        if existing: return existing

        f = self.base()
        for arg in args:
            f = getattr(self, arg)(f)
        return f

