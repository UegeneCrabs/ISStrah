from django.shortcuts import render, redirect, get_object_or_404
from .forms import HomeInsuranceForm, HomeRecordForm, ScheduleForm
from decimal import Decimal, InvalidOperation
from django.db.models import Q
from .models import HomeInsuranceRecord, HomeInsuranceContract, HomeInsuranceClaim
from .forms import HomeInsuranceSearchForm
import logging
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from src.users.models import AgentSchedule
from django.http import JsonResponse


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


def client_home_insurance_contracts(request):
    contracts = HomeInsuranceContract.objects.filter(record__client=request.user)
    return render(request, 'property/client/contract/client_home_insurance_contracts.html', {'contracts': contracts})


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
