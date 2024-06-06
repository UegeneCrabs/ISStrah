from .forms import LifeInsuranceForm, LifeInsuranceSearchForm, LifeRecordForm, LifeInsuranceScheduleForm, LifeClaimForm, \
    HealthClaimScheduleForm, LifeInsuranceAgentForm, LifeInsuranceContractForm
from decimal import Decimal, InvalidOperation
from .models import LifeInsuranceRecord, HealthClaim
from django.db.models import Q
import logging
import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import render, get_object_or_404, redirect
from .models import LifeInsuranceContract, LifePayoutAssessment
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from datetime import date


def calculate_life_insurance_cost(duration, age, sport_coverage, sum_insurance, competition, additional_sports):
    base_rate = Decimal('500.0')  # Базовая ставка

    duration_rate = Decimal(duration)
    age_rate = Decimal(age)
    sport_coverage_rate = Decimal(sport_coverage)
    sum_insurance_rate = Decimal(sum_insurance)
    competition_rate = Decimal('1.2') if competition else Decimal('1.0')

    # Разделить additional_sports по запятой и посчитать количество видов спорта
    sports_list = additional_sports.split(',')
    sports_rate = Decimal('1.0') + Decimal('0.1') * len(sports_list)

    insurance_cost = base_rate * duration_rate * age_rate * sport_coverage_rate * sum_insurance_rate * competition_rate * sports_rate
    return insurance_cost.quantize(Decimal('0.01'))


def life_insurance_view(request):
    insurance_cost = None
    form = LifeInsuranceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        competition = form.cleaned_data['competition_participation']
        duration = form.cleaned_data['insurance_duration']
        age = form.cleaned_data['age_coefficient']
        sport_coverage = form.cleaned_data['sport_coverage']
        sum_insurance = form.cleaned_data['sum_insurance']
        additional_sports = form.cleaned_data['additional_sports']
        insurance_cost = calculate_life_insurance_cost(duration, age, sport_coverage, sum_insurance, competition,
                                                       additional_sports)
    else:
        form = LifeInsuranceForm()

    return render(request, 'life/client/applications contract/calc_ins_health.html',
                  {'form': form, 'insurance_cost': insurance_cost})


def create_life_insurance_record(request):
    if request.method == 'POST':
        form = LifeInsuranceForm(request.POST)
        if form.is_valid():
            try:
                insurance_cost = request.POST.get('insurance_cost').replace(',', '.')
                insurance_cost_decimal = Decimal(insurance_cost)
            except (InvalidOperation, ValueError):
                return redirect('life:life_insurance_view')

            competition_participation = form.cleaned_data['competition_participation']
            additional_sports = form.cleaned_data['additional_sports']
            insurance_duration = form.cleaned_data['insurance_duration']
            age_coefficient = form.cleaned_data['age_coefficient']
            sport_coverage = form.cleaned_data['sport_coverage']
            sum_insurance = form.cleaned_data['sum_insurance']

            life_insurance_record = LifeInsuranceRecord(
                client=request.user,
                competition_participation=competition_participation,
                additional_sports=additional_sports,
                insurance_duration=insurance_duration,
                age_coefficient=age_coefficient,
                sport_coverage=sport_coverage,
                sum_insurance=sum_insurance,
                insurance_cost=insurance_cost_decimal
            )

            life_insurance_record.save()
            return redirect('life:user_life_insurance_requests')

    return redirect('life:life_insurance_view')


def user_life_insurance_requests(request):
    life_insurance_records = LifeInsuranceRecord.objects.filter(client=request.user)
    return render(request, 'life/client/applications contract/life_insurance_requests.html',
                  {'life_insurance_records': life_insurance_records})


def search_request_life_insurance(request):
    form = LifeInsuranceSearchForm(request.GET)
    life_insurance_records = LifeInsuranceRecord.objects.filter(client=request.user)

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        insurance_duration = form.cleaned_data.get('insurance_duration')
        age_coefficient = form.cleaned_data.get('age_coefficient')
        sport_coverage = form.cleaned_data.get('sport_coverage')
        status = form.cleaned_data.get('status')
        sum_insurance = form.cleaned_data.get('sum_insurance')

        if search_query:
            life_insurance_records = life_insurance_records.filter(
                Q(additional_sports__icontains=search_query) |
                Q(insurance_duration__icontains=search_query) |
                Q(age_coefficient__icontains=search_query) |
                Q(sport_coverage__icontains=search_query) |
                Q(sum_insurance__icontains=search_query) |
                Q(insurance_cost__icontains=search_query)
            )

        if insurance_duration:
            life_insurance_records = life_insurance_records.filter(insurance_duration=insurance_duration)

        if age_coefficient:
            life_insurance_records = life_insurance_records.filter(age_coefficient=age_coefficient)

        if sport_coverage:
            life_insurance_records = life_insurance_records.filter(sport_coverage=sport_coverage)

        if status:
            life_insurance_records = life_insurance_records.filter(status=status)

        if sum_insurance:
            life_insurance_records = life_insurance_records.filter(sum_insurance=sum_insurance)

    return render(request, 'life/client/applications contract/life_insurance_requests.html',
                  {'form': form, 'life_insurance_records': life_insurance_records})


def client_life_insurance_contracts(request):
    contracts = LifeInsuranceContract.objects.filter(record__client=request.user)
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'life/client/contract/client_health_contracts.html', {'contracts': contracts})


def agent_life_contracts(request):
    contracts = LifeInsuranceContract.objects.all()
    today = datetime.date.today()
    for contract in contracts:
        if contract.start_date > today:
            contract.days_left = "Договор еще не вступил в силу"
        else:
            contract.days_left = f"{(contract.end_date - today).days} дней"
    return render(request, 'life/agent/contract/agent_health_contracts.html', {'contracts': contracts})


def client_life_claims(request):
    claims = HealthClaim.objects.filter(insurance_contract__record__client=request.user)
    return render(request, 'life/client/applications insurance/client_life_claims.html', {'claims': claims})


logger = logging.getLogger(__name__)


def edit_life_record(request, record_id):
    record = None
    try:
        record = get_object_or_404(LifeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = LifeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)  # Пока не сохраняем в базу
                # Обновляем стоимость страхования из скрытого поля
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()  # Сохраняем изменения
                return redirect('life:user_life_insurance_requests')  # Замените на нужную вам страницу
        else:
            form = LifeRecordForm(instance=record)
        return render(request, 'life/client/applications contract/edit_life_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'life/client/applications contract/edit_life_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def edit_life_record_agent(request, record_id):
    record = None
    try:
        record = get_object_or_404(LifeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = LifeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)  # Пока не сохраняем в базу
                # Обновляем стоимость страхования из скрытого поля
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()  # Сохраняем изменения
                return redirect('life:agent_requests_health')  # Замените на нужную вам страницу
        else:
            form = LifeRecordForm(instance=record)
        return render(request, 'life/agent/applications contract/edit_life_record_agent.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'life/agent/applications contract/edit_life_record_agent.html',
                      {'form': None, 'error': str(e), 'record': record})


def delete_life_record(request, record_id):
    user = request.user
    record = get_object_or_404(LifeInsuranceRecord, id=record_id)

    if request.method == 'POST':
        record.delete()
        # В зависимости от типа пользователя, перенаправляем на соответствующую страницу
        if user.user_type == 'agent':
            return redirect(reverse_lazy('life:agent_requests_health'))
        elif user.user_type == 'appraiser':
            return redirect(reverse_lazy('life:user_life_insurance_requests'))

    # Если метод не POST, перенаправляем на редактирование записи
    return redirect('edit_casco_record', record_id=record_id)


def schedule_life_insurance_appointment(request, record_id):
    record = LifeInsuranceRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = LifeInsuranceScheduleForm(request.POST, instance=record)
        if form.is_valid():
            availability = form.cleaned_data['availability']
            availability.available = False
            availability.save()

            form.save()
            return redirect('life:user_life_insurance_requests')  # Перенаправление после успешной обработки
    else:
        form = LifeInsuranceScheduleForm(instance=record)

    return render(request, 'life/client/applications contract/schedule_life_insurance_appointment.html',
                  {'form': form, 'record': record})


def edit_life_claim(request, claim_id):
    claim = get_object_or_404(HealthClaim, id=claim_id)
    if request.method == 'POST':
        form = LifeClaimForm(request.POST, instance=claim)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('life:client_life_claims')
    else:
        form = LifeClaimForm(instance=claim)
    return render(request, 'life/client/applications insurance/edit_life_claim.html', {'form': form, 'claim': claim})


def create_life_claim(request, contract_id):
    contract = LifeInsuranceContract.objects.get(id=contract_id)
    if request.method == 'POST':
        form = LifeClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.insurance_contract = contract
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('life:client_life_claims')
    else:
        form = LifeClaimForm()
    return render(request, 'life/client/applications insurance/create_life_claim.html',
                  {'form': form, 'contract': contract})


def choose_health_claim_schedule(request, claim_id):
    claim = get_object_or_404(HealthClaim, id=claim_id)
    if request.method == 'POST':
        form = HealthClaimScheduleForm(request.POST, instance=claim)
        if form.is_valid():
            chosen_schedule = form.cleaned_data['schedule']
            chosen_schedule.available = False
            chosen_schedule.save()

            claim = form.save(commit=False)
            claim.claim_date = datetime.date.today()
            claim.save()
            return redirect('life:client_life_claims')  # Перенаправление после успешного выбора времени
    else:
        form = HealthClaimScheduleForm(instance=claim)
    return render(request, 'life/client/applications insurance/choose_health_claim_schedule.html',
                  {'form': form, 'claim': claim})


def generate_pdf(request, contract_id):
    contract = get_object_or_404(LifeInsuranceContract, id=contract_id)
    assessments = LifePayoutAssessment.objects.select_related('theme').order_by('theme__name')

    sport_coverage_display = get_sport_coverage_display(contract.record.sport_coverage,
                                                        LifeInsuranceRecord.SPORT_COVERAGE_CHOICES)

    insurance_duration_display = get_display(contract.record.insurance_duration, LifeInsuranceRecord.DURATION_CHOICES)
    sum_insurance_display = get_display(contract.record.sum_insurance, LifeInsuranceRecord.SUM_INSURANCE_CHOICES)

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

    insurance_info = f"""
                    <b>1.4.1</b> Категория спортивного покрытия: {sport_coverage_display}.
                    Включенные виды спорта: {contract.record.additional_sports}
                    """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
                    <b>1.4.2</b> Длительность страхования: {insurance_duration_display}. Срок действия договора 
                    с {contract.start_date} по {contract.end_date}
                    """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
                    <b>1.4.3</b> Участие в соревнованиях: {'Включено' if contract.record.competition_participation
    else 'Не включено'}
                    """
    elements.append(Paragraph(insurance_info, styles['Normal']))
    elements.append(Spacer(1, 12))

    insurance_info = f"""
                        <b>1.4.4</b> Сумма страхования: {sum_insurance_display} рублей.
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


def get_sport_coverage_display(value, choices):
    return dict(choices).get(value, "Неизвестно")


def get_display(value, choices):
    return dict(choices).get(value, "Неизвестно")


@login_required
def agent_requests_health(request):
    requests = LifeInsuranceRecord.objects.all()
    user = request.user
    return render(request, 'life/agent/applications contract/agent_requests_health.html', {
        'title': 'personal_account_agent',
        'user': user,
        'requests': requests,
        'today': date.today()
    })


@login_required
def change_status_to_in_progress(request, record_id):
    record = get_object_or_404(LifeInsuranceRecord, id=record_id)
    if record.status == 'pending':
        record.status = 'in_progress'
        record.save()
        return redirect(reverse(
            'life:agent_requests_health'))
    else:
        return HttpResponse("Action not allowed.", status=403)


def search_request_life_insurance_agent(request):
    form = LifeInsuranceSearchForm(request.GET)
    requests = LifeInsuranceRecord.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        insurance_duration = form.cleaned_data.get('insurance_duration')
        age_coefficient = form.cleaned_data.get('age_coefficient')
        sport_coverage = form.cleaned_data.get('sport_coverage')
        status = form.cleaned_data.get('status')
        sum_insurance = form.cleaned_data.get('sum_insurance')

        if search_query:
            requests = requests.filter(
                Q(additional_sports__icontains=search_query) |
                Q(insurance_duration__icontains=search_query) |
                Q(age_coefficient__icontains=search_query) |
                Q(sport_coverage__icontains=search_query) |
                Q(sum_insurance__icontains=search_query) |
                Q(insurance_cost__icontains=search_query)
            )

        if insurance_duration:
            requests = requests.filter(insurance_duration=insurance_duration)

        if age_coefficient:
            requests = requests.filter(age_coefficient=age_coefficient)

        if sport_coverage:
            requests = requests.filter(sport_coverage=sport_coverage)

        if status:
            requests = requests.filter(status=status)

        if sum_insurance:
            requests = requests.filter(sum_insurance=sum_insurance)

    return render(request, 'life/agent/applications contract/agent_requests_health.html',
                  {'form': form, 'requests': requests})


def create_life_insurance_record_agent(request):
    if request.method == 'POST':
        form = LifeInsuranceAgentForm(request.POST)
        if form.is_valid():
            life_insurance_record = form.save(commit=False)
            life_insurance_record.status = 'in_progress'
            life_insurance_record.save()
            return redirect('life:agent_requests_health')
    else:
        form = LifeInsuranceAgentForm()
    return render(request, 'life/agent/applications contract/create_life_insurance_record.html', {'form': form})


def agent_edit_life_record(request, record_id):
    record = None
    try:
        record = get_object_or_404(LifeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = LifeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()  # Сохраняем изменения
                return redirect('life:agent_requests_health')
        else:
            form = LifeRecordForm(instance=record)
        return render(request, 'life/agent/applications contract/agent_edit_life_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_life_record view: {e}")
        return render(request, 'life/agent/applications contract/agent_edit_life_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def create_life_contract(request, record_id):
    life_record = get_object_or_404(LifeInsuranceRecord, id=record_id)

    if request.method == 'POST':
        form = LifeInsuranceContractForm(request.POST)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.agent = request.user
            contract.record = life_record
            contract.save()
            return redirect('life:agent_life_contracts')
    else:
        form = LifeInsuranceContractForm(initial={'record': life_record})

    return render(request, 'life/agent/contract/create_life_contract.html', {'form': form, 'life_record': life_record})
