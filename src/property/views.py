from django.shortcuts import redirect
from .forms import HomeInsuranceForm, HomeRecordForm, ScheduleForm, HomeClaimForm, HomeInsuranceClaimScheduleForm, \
    HomeInsuranceContractForm
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from .models import HomeInsuranceRecord, HomeInsuranceContract, HomeInsuranceClaim, HomePayoutAssessment
from .forms import HomeInsuranceSearchForm
import logging
import datetime
from django.contrib.auth.decorators import login_required
from src.users.models import AgentSchedule
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.urls import reverse
from datetime import date


def calculate_home_insurance_cost(data):
    base_rate = Decimal('3000.00')
    total_value = sum([
        data['interior_finish'],
        data['structural_elements'],
        data['civil_liability'],
        data['household_property']
    ])

    # Дополнительные коэффициенты
    additional_protection_rate = Decimal('1.1') if data['additional_protection'] else Decimal('1.0')
    war_risk_rate = Decimal('1.2') if data['war_risk'] else Decimal('1.0')
    neighbor_repair_liability_rate = Decimal('1.15') if data['neighbor_repair_liability'] else Decimal('1.0')
    atmospheric_impact_rate = Decimal('1.1') if data['atmospheric_impact'] else Decimal('1.0')

    insurance_cost = base_rate + (Decimal(total_value) / Decimal('1000.00'))
    insurance_cost *= additional_protection_rate
    insurance_cost *= war_risk_rate
    insurance_cost *= neighbor_repair_liability_rate
    insurance_cost *= atmospheric_impact_rate

    return insurance_cost.quantize(Decimal('0.01'))


def home_insurance_view(request):
    insurance_cost = None
    if request.method == 'POST':
        form = HomeInsuranceForm(request.POST)
        if form.is_valid():
            insurance_cost = calculate_home_insurance_cost(form.cleaned_data)
    else:
        form = HomeInsuranceForm()

    return render(request, 'property/client/applications contract/calc_ins_home.html',
                  {'form': form, 'insurance_cost': insurance_cost})


def search_request_home_insurance(request):
    form = HomeInsuranceSearchForm(request.GET)
    home_insurance_records = HomeInsuranceRecord.objects.filter(client=request.user)

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        additional_protection = form.cleaned_data.get('additional_protection')
        war_risk = form.cleaned_data.get('war_risk')
        neighbor_repair_liability = form.cleaned_data.get('neighbor_repair_liability')
        atmospheric_impact = form.cleaned_data.get('atmospheric_impact')
        status = form.cleaned_data.get('status')

        if search_query:
            home_insurance_records = home_insurance_records.filter(
                Q(city__icontains=search_query) |
                Q(street__icontains=search_query) |
                Q(house__icontains=search_query) |
                Q(apartment__icontains=search_query) |
                Q(insurance_cost__icontains=search_query) |
                Q(interior_finish__icontains=search_query) |
                Q(structural_elements__icontains=search_query) |
                Q(civil_liability__icontains=search_query) |
                Q(household_property__icontains=search_query)
            )

        if additional_protection:
            home_insurance_records = home_insurance_records.filter(additional_protection=additional_protection)

        if war_risk:
            home_insurance_records = home_insurance_records.filter(war_risk=war_risk)

        if neighbor_repair_liability:
            home_insurance_records = home_insurance_records.filter(neighbor_repair_liability=neighbor_repair_liability)

        if atmospheric_impact:
            home_insurance_records = home_insurance_records.filter(atmospheric_impact=atmospheric_impact)

        if status:
            home_insurance_records = home_insurance_records.filter(status=status)

    return render(request, 'property/client/applications contract/home_insurance_requests.html',
                  {'form': form, 'home_insurance_records': home_insurance_records})


def delete_home_record_agent(request, record_id):
    record = get_object_or_404(HomeInsuranceRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('property:agent_home_insurance_requests')
    return redirect('property:agent_home_insurance_requests', record_id=record_id)


def create_home_insurance_record(request):
    if request.method == 'POST':
        form = HomeInsuranceForm(request.POST)
        insurance_cost = request.POST.get('insurance_cost')
        if form.is_valid():
            try:
                insurance_cost = insurance_cost.replace(',', '.').replace(' ', '')
                insurance_cost_decimal = Decimal(insurance_cost)
            except (InvalidOperation, ValueError):
                return redirect('property:home_insurance_view')

            home_insurance_record = form.save(commit=False)
            home_insurance_record.client = request.user
            home_insurance_record.insurance_cost = insurance_cost_decimal
            home_insurance_record.save()
            return redirect('property:user_home_insurance_requests')
    return redirect('property:home_insurance_view')


def user_home_insurance_requests(request):
    home_insurance_records = HomeInsuranceRecord.objects.filter(client=request.user)
    return render(request, 'property/client/applications contract/home_insurance_requests.html',
                  {'home_insurance_records': home_insurance_records})


def agent_home_insurance_requests(request):
    home_insurance_records = HomeInsuranceRecord.objects.all()
    return render(request, 'property/agent/applications contract/agent_requests_home.html',
                  {'home_insurance_records': home_insurance_records, 'today': date.today()})


@login_required
def change_status_property_to_in_progress(request, record_id):
    record = get_object_or_404(HomeInsuranceRecord, id=record_id)
    if record.status == 'pending':
        record.status = 'in_progress'
        record.save()
        return redirect(reverse(
            'property:agent_home_insurance_requests'))
    else:
        return HttpResponse("Action not allowed.", status=403)


def client_home_insurance_contracts(request):
    contracts = HomeInsuranceContract.objects.filter(record__client=request.user)
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'property/client/contract/client_home_insurance_contracts.html', {'contracts': contracts})


def agent_home_insurance_contracts(request):
    contracts = HomeInsuranceContract.objects.all()
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'property/agent/contract/agent_home_contracts.html', {'contracts': contracts})


def client_home_insurance_claims(request):
    claims = HomeInsuranceClaim.objects.filter(contract__record__client=request.user)
    return render(request, 'property/client/applications insurance/client_home_insurance_claims.html',
                  {'claims': claims})


logger = logging.getLogger(__name__)


def edit_home_record(request, record_id):
    try:
        record = get_object_or_404(HomeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = HomeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()
                return redirect('property:user_home_insurance_requests')  # Замените на нужную вам страницу
        else:
            form = HomeRecordForm(instance=record)
        return render(request, 'property/client/applications contract/edit_property_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'property/client/applications contract/edit_property_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def edit_home_record_agent(request, record_id):
    try:
        record = get_object_or_404(HomeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = HomeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()
                return redirect('property:agent_home_insurance_requests')  # Замените на нужную вам страницу
        else:
            form = HomeRecordForm(instance=record)
        return render(request, 'property/agent/applications contract/edit_home_record_agent.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'property/agent/applications contract/edit_home_record_agent.html',
                      {'form': None, 'error': str(e), 'record': record})


def delete_home_record(request, record_id):
    record = get_object_or_404(HomeInsuranceRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('property:user_home_insurance_requests')
    return redirect('property:edit_home_record', record_id=record_id)


@login_required
def schedule_appointment(request, record_id):
    record = HomeInsuranceRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.cleaned_data['schedule_time']
            schedule.available = False
            schedule.save()

            record.schedule = schedule
            record.save()

        return redirect('property:user_home_insurance_requests')
    else:
        form = ScheduleForm()

    available_times = AgentSchedule.objects.filter(available=True).values('id', 'date', 'time', 'agent__name')
    return render(request, 'property/client/applications contract/schedule_appointment.html',
                  {'form': form, 'record': record, 'available_times': available_times})


def create_home_claim(request, contract_id):
    contract = HomeInsuranceContract.objects.get(id=contract_id)
    if request.method == 'POST':
        form = HomeClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.contract = contract
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('property:client_home_insurance_claims')
    else:
        form = HomeClaimForm()
    return render(request, 'property/client/applications insurance/create_home_claim.html',
                  {'form': form, 'contract': contract})


def edit_home_claim(request, claim_id):
    claim = get_object_or_404(HomeInsuranceClaim, id=claim_id)
    if request.method == 'POST':
        form = HomeClaimForm(request.POST, instance=claim)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('property:client_home_insurance_claims')
    else:
        form = HomeClaimForm(instance=claim)
    return render(request, 'property/client/applications insurance/edit_home_claim.html',
                  {'form': form, 'claim': claim})


def choose_home_insurance_claim_schedule(request, claim_id):
    claim = get_object_or_404(HomeInsuranceClaim, id=claim_id)
    if request.method == 'POST':
        form = HomeInsuranceClaimScheduleForm(request.POST, instance=claim)
        if form.is_valid():
            chosen_schedule = form.cleaned_data['availability_id']
            chosen_schedule.available = False
            chosen_schedule.save()

            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('property:client_home_insurance_claims')
    else:
        form = HomeInsuranceClaimScheduleForm(instance=claim)
    return render(request, 'property/client/applications insurance/choose_home_insurance_claim_schedule.html',
                  {'form': form, 'claim': claim})


def generate_pdf(request, contract_id):
    contract = get_object_or_404(HomeInsuranceContract, id=contract_id)
    assessments = HomePayoutAssessment.objects.select_related('theme').order_by('theme__name')

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
            <b>1.2</b> Страхованным лицом является {contract.record.client.surname}  {contract.record.client.name} 
            {contract.record.client.secondname}.
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
    elements.append(Paragraph("Оценка выплаты по страхованию квартир", styles['Title']))

    current_theme = None
    theme_data = []

    for assessment in assessments:
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


def create_home_insurance_contract(request, record_id):
    home_record = get_object_or_404(HomeInsuranceRecord, id=record_id)

    if request.method == 'POST':
        form = HomeInsuranceContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.agent = request.user
            contract.record = home_record
            contract.save()
            return redirect('property:agent_home_insurance_contracts')
    else:
        form = HomeInsuranceContractForm(initial={'record': home_record})

    return render(request, 'property/agent/contract/create_home_insurance_contract.html',
                  {'form': form, 'home_record': home_record})
