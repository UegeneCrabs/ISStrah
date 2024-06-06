from django.db.models import Q

from .forms import CarForm, OsagoSearchForm, OsagoRecordForm, OsagoScheduleForm, OsagoClaimForm, OsagoClaimScheduleForm, \
    OsagoRecordAgentForm, OsagoContractForm
from django.shortcuts import redirect

from .models import OsagoRecord, OsagoContract, OsagoClaim, OsagoAutoPayoutAssessment, OsagoLifePayoutAssessment
from ..authorization.models import CustomUser
from ..casco.models import CarModel, Brand
from decimal import Decimal
from django.http import JsonResponse
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import logging
from django.urls import reverse
from datetime import date


def calculate_insurance_cost(horsepower, age, experience):
    horsepower = int(horsepower)
    age = int(age)
    experience = int(experience)
    tariff = Decimal('5000.0')
    kt = Decimal('1.8')

    # Коэффициент мощности (km)
    if horsepower < 50:
        km = Decimal('0.6')
    elif 50 <= horsepower < 70:
        km = Decimal('1.0')
    elif 70 <= horsepower < 100:
        km = Decimal('1.1')
    elif 100 <= horsepower < 120:
        km = Decimal('1.2')
    elif 120 <= horsepower < 150:
        km = Decimal('1.4')
    else:
        km = Decimal('1.6')

    # Коэффициент возраста и стажа (kvs)
    if age <= 22 and experience <= 3:
        kvs = Decimal('1.8')
    elif age > 22 and experience <= 3:
        kvs = Decimal('1.7')
    elif age <= 22 and experience > 3:
        kvs = Decimal('1.6')
    else:
        kvs = Decimal('1.0')

    insurance_cost = tariff * kt * km * kvs
    return insurance_cost.quantize(Decimal('0.01'))


def search_request_osago(request):
    form = OsagoSearchForm(request.GET)
    osago_records = OsagoRecord.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            osago_records = osago_records.filter(
                Q(car_model__brand__name__icontains=search_query) |
                Q(car_model__model_name__icontains=search_query) |
                Q(car_model__year__icontains=search_query) |
                Q(car_model__horsepower__icontains=search_query) |
                Q(age__icontains=search_query) |
                Q(experience__icontains=search_query) |
                Q(insurance_cost__icontains=search_query) |
                Q(status__icontains=search_query)
            )
    return render(request, 'osago/client/applications contract/client_osago_requests.html',
                  {'form': form, 'osago_records': osago_records})


def car_view(request):
    insurance_cost = None
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            horsepower = int(form.cleaned_data['horsepower'])
            age = form.cleaned_data['age']
            experience = form.cleaned_data['experience']
            insurance_cost = calculate_insurance_cost(horsepower, age, experience)
    else:
        form = CarForm()
    return render(request, 'osago/client/applications contract/calc_ins_auto_osago.html',
                  {'form': form, 'insurance_cost': insurance_cost})


def client_osago_requests(request):
    osago_records = OsagoRecord.objects.filter(client=request.user)
    return render(request, 'osago/client/applications contract/client_osago_requests.html',
                  {'osago_records': osago_records})


def create_osago_record(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        model_name = request.POST.get('model_name')
        year = request.POST.get('year')
        horsepower = request.POST.get('horsepower')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        insurance_cost = request.POST.get('insurance_cost')

        # Преобразование insurance_cost в Decimal
        insurance_cost = Decimal(insurance_cost.replace(',', '.'))

        brand = get_object_or_404(Brand, pk=brand_id)
        car_model = get_object_or_404(CarModel, brand=brand, model_name=model_name, year=year, horsepower=horsepower)

        OsagoRecord.objects.create(
            client=request.user,
            car_model=car_model,
            age=age,
            experience=experience,
            insurance_cost=insurance_cost,
            status='pending'
        )
        return redirect('osago:client_osago_requests')
    return redirect('osago:car_view')


def load_models(request):
    brand_id = request.GET.get('brand')
    models = CarModel.objects.filter(brand_id=brand_id).values('model_name').distinct().order_by('model_name')
    return JsonResponse(list(models), safe=False)


def load_years(request):
    brand_id = request.GET.get('brand')
    model_name = request.GET.get('model_name')
    years = CarModel.objects.filter(brand_id=brand_id, model_name=model_name).values('year').distinct().order_by('year')
    return JsonResponse(list(years), safe=False)


def load_horsepowers(request):
    brand_id = request.GET.get('brand')
    model_name = request.GET.get('model_name')
    year = request.GET.get('year')
    horsepowers = CarModel.objects.filter(brand_id=brand_id, model_name=model_name, year=year).values(
        'horsepower').distinct().order_by('horsepower')
    return JsonResponse(list(horsepowers), safe=False)


def client_osago_contracts(request):
    contracts = OsagoContract.objects.filter(osago_record__client=request.user)
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'osago/client/contract/client_osago_contracts.html', {'contracts': contracts})


def agent_osago_contracts(request):
    contracts = OsagoContract.objects.all()
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'osago/agent/contract/agent_osago_contracts.html', {'contracts': contracts})


def create_osago_claim(request, contract_id):
    contract = OsagoContract.objects.get(id=contract_id)
    if request.method == 'POST':
        form = OsagoClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.osago_contract = contract
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('osago:client_osago_claims')
    else:
        form = OsagoClaimForm()
    return render(request, 'osago/client/applications insurance/create_osago_claim.html',
                  {'form': form, 'contract': contract})


def client_osago_claims(request):
    claims = OsagoClaim.objects.filter(osago_contract__osago_record__client=request.user)
    return render(request, 'osago/client/applications insurance/client_osago_claims.html', {'claims': claims})


logger = logging.getLogger(__name__)


def edit_osago_record(request, record_id):
    record = None
    try:
        record = get_object_or_404(OsagoRecord, id=record_id)
        if request.method == 'POST':
            form = OsagoRecordForm(request.POST, instance=record)
            if form.is_valid():
                # Получение данных из формы

                horsepower = form.cleaned_data['horsepower']
                age = form.cleaned_data['age']
                experience = form.cleaned_data['experience']

                # Преобразование данных перед расчетом

                horsepower = int(horsepower)
                age = int(age)
                experience = int(experience)

                # Расчет стоимости страхования
                insurance_cost = calculate_insurance_cost(
                    horsepower=horsepower,
                    age=age,
                    experience=experience
                )
                # Сохранение стоимости страхования в запись
                form.instance.insurance_cost = insurance_cost

                # Сохранение выбранной модели автомобиля
                brand_id = form.cleaned_data['brand'].id
                model_name = form.cleaned_data['model_name']
                year = form.cleaned_data['year']
                car_model = CarModel.objects.get(brand_id=brand_id, model_name=model_name, year=year,
                                                 horsepower=horsepower)
                form.instance.car_model = car_model

                form.save()

                return redirect('osago:client_osago_requests')
        else:
            form = OsagoRecordForm(instance=record)
        return render(request, 'osago/client/applications contract/edit_osago_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'osago/client/applications contract/edit_osago_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def delete_osago_record(request, record_id):
    record = get_object_or_404(OsagoRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('osago:client_osago_requests')
    return redirect('osago:edit_osago_record', record_id=record_id)


def delete_osago_record_agent(request, record_id):
    record = get_object_or_404(OsagoRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('osago:agent_requests_osago')
    return redirect('osago:agent_requests_osago', record_id=record_id)


def schedule_osago_appointment(request, record_id):
    record = OsagoRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = OsagoScheduleForm(request.POST, instance=record)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            schedule.available = False
            schedule.save()

            form.save()
            return redirect('osago:client_osago_requests')
    else:
        form = OsagoScheduleForm(instance=record)

    return render(request, 'osago/client/applications contract/schedule_osago_appointment.html',
                  {'form': form, 'record': record})


def edit_osago_claim(request, claim_id):
    claim = get_object_or_404(OsagoClaim, id=claim_id)
    if request.method == 'POST':
        form = OsagoClaimForm(request.POST, instance=claim)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('osago:client_osago_claims')
    else:
        form = OsagoClaimForm(instance=claim)
    return render(request, 'osago/client/applications insurance/edit_osago_claim.html', {'form': form, 'claim': claim})


def choose_osago_claim_schedule(request, claim_id):
    claim = get_object_or_404(OsagoClaim, id=claim_id)
    if request.method == 'POST':
        form = OsagoClaimScheduleForm(request.POST, instance=claim)
        if form.is_valid():
            chosen_schedule = form.cleaned_data['availability_id']
            chosen_schedule.available = False
            chosen_schedule.save()

            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('osago:client_osago_claims')
    else:
        form = OsagoClaimScheduleForm(instance=claim)
    return render(request, 'osago/client/applications insurance/choose_osago_claim_schedule.html',
                  {'form': form, 'claim': claim})


def generate_pdf(request, contract_id):
    contract = get_object_or_404(OsagoContract, id=contract_id)
    assessments_auto = OsagoAutoPayoutAssessment.objects.select_related('theme').order_by('theme__name')
    assessments_life = OsagoLifePayoutAssessment.objects.select_related('theme').order_by('theme__name')

    # sport_coverage_display = get_sport_coverage_display(contract.record.sport_coverage,
    #                                                     LifeInsuranceRecord.SPORT_COVERAGE_CHOICES)
    # insurance_duration_display = get_display(contract.record.insurance_duration, LifeInsuranceRecord.DURATION_CHOICES)
    # sum_insurance_display = get_display(contract.record.sum_insurance, LifeInsuranceRecord.SUM_INSURANCE_CHOICES)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Путь к файлу шрифта Times New Roman
    font_path = "static/fonts/DejaVuSans.ttf"

    # Регистрация шрифта Times New Roman
    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))

    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'DejaVuSans'
    styles['Heading1'].fontName = 'DejaVuSans'
    styles['Heading2'].fontName = 'DejaVuSans'
    styles['Normal'].fontName = 'DejaVuSans'
    styles.add(ParagraphStyle(name='CoverTitle', fontName='DejaVuSans', fontSize=18, spaceAfter=6, spaceBefore=12,
                              alignment=1))
    styles.add(ParagraphStyle(name='CoverSubTitle', fontName='DejaVuSans', fontSize=14, spaceAfter=12, spaceBefore=6,
                              alignment=1))

    # Заголовок и подзаголовок
    elements.append(Paragraph("ДОГОВОР", styles['CoverTitle']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("страхования", styles['CoverSubTitle']))

    # Место и дата заключения договора
    elements.append(Paragraph(f"г. Казань, {contract.conclusion_date.strftime('%d.%m.%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Предмет договора
    elements.append(Paragraph("1. ПРЕДМЕТ ДОГОВОРА", styles['Heading2']))
    insurance_info = f"""
        <b>1.1</b> По настоящему Договору Страховщик обязуется при наступлении страхового случая выплачивать 
        Страхованному лицу страховое возмещение, а Страхователь обязуется платить Страховщику страховую премию в 
        размере, в порядке и в сроки, предусмотренные Договором.
        """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
            <b>1.2</b> Застрахованным лицом является {contract.osago_record.client.surname}  
            {contract.osago_record.client.name} 
            {contract.osago_record.client.secondname}.
            """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
                <b>1.3</b> Страхователем является {contract.agent.surname} {contract.agent.name} 
                {contract.agent.secondname}, лицо, представляющее интересы страховой компании
                """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
                <b>1.4</b> Данные страхового договора
                """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Страховой случай
    elements.append(Paragraph("2. СТРАХОВОЙ СЛУЧАЙ. ПРАВА И ОБЯЗАННОСТИ СТОРОН", styles['Heading2']))
    insurance_case_info = """
        <b>2.1</b> Не являются страховыми случаями события наступившие в результате:
        """
    elements.append(Paragraph(insurance_case_info, styles['Normal']))
    insurance_case_info = """ - Умышленных действий Страхователя, Страхованного лица или Выгодоприобретателя;"""
    elements.append(Paragraph(insurance_case_info, styles['Normal']))
    insurance_case_info = """ - Нахождение Застрахованного лица в состоянии алкогольного, 
    наркотического или токсического опьянения;"""
    elements.append(Paragraph(insurance_case_info, styles['Normal']))
    # Добавляем отступ перед новой страницей
    elements.append(Spacer(1, 20))
    elements.append(PageBreak())

    # Оценка выплат по страхованию жизни
    elements.append(Paragraph("Оценка выплаты по страхованию жизни", styles['Title']))
    elements.append(Paragraph("Травмы, полученные в результате ДТП", styles['Title']))

    current_theme = None
    theme_data = []

    for assessment in assessments_life:
        theme_name = assessment.theme.name if assessment.theme else 'Без темы'
        if theme_name != current_theme:
            if current_theme is not None:
                elements.append(Paragraph(f"{current_theme}", styles['Heading2']))
                table = Table(theme_data, colWidths=[350, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                theme_data = []
            current_theme = theme_name
            theme_data.append(['Травма/заболевание', 'Процент'])

        # Создайте объект Paragraph для текста и примените стиль
        damage_character_paragraph = Paragraph(assessment.damage_character, styles['Heading2'])
        theme_data.append([damage_character_paragraph, str(assessment.percentage_of_insurance_amount)])

    # Добавляем последнюю таблицу с данными
    if theme_data:
        elements.append(Paragraph(f"{current_theme}", styles['Heading2']))
        table = Table(theme_data, colWidths=[350, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

    current_theme = None
    theme_data = []
    elements.append(Spacer(1, 20))
    elements.append(PageBreak())
    elements.append(Paragraph("Повреждения автомобиля, полученные в результате ДТП", styles['Title']))
    for assessment in assessments_auto:
        theme_name = assessment.theme.name if assessment.theme else 'Без темы'
        if theme_name != current_theme:
            if current_theme is not None:
                elements.append(Paragraph(f"{current_theme}", styles['Heading2']))
                table = Table(theme_data, colWidths=[350, 100])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                elements.append(table)
                theme_data = []
            current_theme = theme_name
            theme_data.append(['Травма/заболевание', 'Процент'])

        # Создайте объект Paragraph для текста и примените стиль
        damage_character_paragraph = Paragraph(assessment.damage_character, styles['Heading2'])
        theme_data.append([damage_character_paragraph, str(assessment.percentage_of_insurance_amount)])

    # Добавляем последнюю таблицу с данными
    if theme_data:
        elements.append(Paragraph(f"{current_theme}", styles['Heading2']))
        table = Table(theme_data, colWidths=[350, 100])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    # Создание PDF-документа
    doc.build(elements)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="contract.pdf"'
    return response


def search_request_osago_insurance_agent(request):
    form = OsagoSearchForm(request.GET)
    requests = OsagoRecord.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            requests = requests.filter(
                Q(client__name__icontains=search_query) |
                Q(client__surname__icontains=search_query) |
                Q(client__secondname__icontains=search_query) |
                Q(client__email__icontains=search_query) |
                Q(client__phone_number__icontains=search_query) |
                Q(car_model__brand__name__icontains=search_query) |
                Q(car_model__model_name__icontains=search_query) |
                Q(car_model__year__icontains=search_query) |
                Q(car_model__horsepower__icontains=search_query) |
                Q(age__icontains=search_query) |
                Q(experience__icontains=search_query) |
                Q(insurance_cost__icontains=search_query) |
                Q(status__icontains=search_query)
            )
    return render(request, 'osago/agent/applications contract/agent_requests_osago.html',
                  {'form': form, 'requests': requests})


def change_status_to_in_progress_casco(request, record_id):
    record = get_object_or_404(OsagoRecord, id=record_id)
    if record.status == 'pending':
        record.status = 'in_progress'
        record.save()
        return redirect(reverse(
            'osago:agent_requests_osago'))
    else:
        return HttpResponse("Action not allowed.", status=403)


def agent_requests_osago(request):
    requests = OsagoRecord.objects.all()
    user = request.user
    return render(request, 'osago/agent/applications contract/agent_requests_osago.html', {
        'title': 'personal_account_agent',
        'user': user,
        'requests': requests,
        'today': date.today()
    })


def agent_edit_osago_record(request, record_id):
    record = None
    try:
        record = get_object_or_404(OsagoRecord, id=record_id)
        if request.method == 'POST':
            form = OsagoRecordForm(request.POST, instance=record)
            if form.is_valid():
                # Получение данных из формы

                horsepower = form.cleaned_data['horsepower']
                age = form.cleaned_data['age']
                experience = form.cleaned_data['experience']

                # Преобразование данных перед расчетом

                horsepower = int(horsepower)
                age = int(age)
                experience = int(experience)

                # Расчет стоимости страхования
                insurance_cost = calculate_insurance_cost(
                    horsepower=horsepower,
                    age=age,
                    experience=experience
                )
                # Сохранение стоимости страхования в запись
                form.instance.insurance_cost = insurance_cost

                # Сохранение выбранной модели автомобиля
                brand_id = form.cleaned_data['brand'].id
                model_name = form.cleaned_data['model_name']
                year = form.cleaned_data['year']
                car_model = CarModel.objects.get(brand_id=brand_id, model_name=model_name, year=year,
                                                 horsepower=horsepower)
                form.instance.car_model = car_model

                form.save()

                return redirect('osago:agent_requests_osago')
        else:
            form = OsagoRecordForm(instance=record)
        return render(request, 'osago/agent/applications contract/edit_osago_record_agent.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'osago/agent/applications contract/edit_osago_record_agent.html',
                      {'form': None, 'error': str(e), 'record': record})


def create_osago_contract(request, record_id):
    osago_record = get_object_or_404(OsagoRecord, id=record_id)

    if request.method == 'POST':
        form = OsagoContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.agent = request.user
            contract.osago_record = osago_record
            contract.save()
            return redirect(
                'osago:agent_osago_contracts')
    else:
        form = OsagoContractForm(initial={'osago_record': osago_record})

    return render(request, 'osago/agent/contract/create_osago_contract.html',
                  {'form': form, 'osago_record': osago_record})
