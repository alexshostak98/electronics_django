from random import randint
from celery import shared_task
from django.db.models import F
from django.core.mail import EmailMessage
from company.models import Company
from company.qr_code import generate_qr_code
from electronics_sales.celery import app
from company.constants import (
    RANDOM_INCREASE_MIN,
    RANDOM_INCREASE_MAX,
    RANDOM_REDUCE_MAX,
    RANDOM_REDUCE_MIN,
)


@shared_task()
def send_email_with_qr_code(text_for_qr_code, company_name, emails):
    qr_code_image_path = generate_qr_code(text_for_qr_code, company_name)
    email_message = EmailMessage(
        subject='QR code with company contacts',
        body=f'In this email automatically generated qr code with {company_name} contacts data',
        to=emails,
    )
    email_message.attach_file(qr_code_image_path, mimetype='image/png')
    email_message.send()


@shared_task()
def reset_debt_to_supplier(company_ids):
    Company.objects.filter(id__in=company_ids).update(debt_to_supplier=0)


@app.task
def increase_debt_to_supplier():
    Company.objects.filter(supplier__isnull=False).update(
        debt_to_supplier=F('debt_to_supplier') + randint(RANDOM_INCREASE_MIN, RANDOM_INCREASE_MAX)
    )


@app.task
def reduce_debt_to_supplier():
    companies = Company.objects.filter(supplier__isnull=False).all()
    for company in companies:
        current_debt = company.debt_to_supplier
        if current_debt <= RANDOM_REDUCE_MIN:
            company.debt_to_supplier = 0
        else:
            max_reduce_value = current_debt if current_debt < RANDOM_REDUCE_MAX else RANDOM_REDUCE_MAX
            company.debt_to_supplier -= randint(RANDOM_REDUCE_MIN, max_reduce_value)
        company.save()
