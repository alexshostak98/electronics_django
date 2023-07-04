import datetime
import os
from django.conf import settings
import qrcode

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'electronics_sales.settings')


def generate_qr_code(text, company_name):
    qr_code = qrcode.make(text, box_size=10, border=1)
    path_to_save = create_qr_code_images_path(company_name)
    try:
        qr_code.save(path_to_save)
    except FileNotFoundError:
        os.mkdir(os.path.dirname(path_to_save))
        qr_code.save(path_to_save)
    return path_to_save


def create_qr_code_images_path(company_name):
    current_date = datetime.date.today()
    qr_code_name = f'{company_name}_{current_date}.png'
    qr_code_images_path = os.path.join(settings.MEDIA_ROOT, f'qr_codes/{qr_code_name}')
    return qr_code_images_path
