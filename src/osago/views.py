from django.db.models import Q

from .forms import CarForm, OsagoSearchForm, OsagoRecordForm, OsagoScheduleForm
from django.shortcuts import render, redirect, get_object_or_404

from .models import OsagoRecord, OsagoContract, OsagoClaim
from ..casco.models import CarModel, Brand
from decimal import Decimal
from django.http import JsonResponse


# @login_required
# def osago_form_view(request):
#     if request.method == 'POST':
#         form = OsagoRecordForm(request.POST)
#         if form.is_valid():
#             return redirect('users:personal_account_client')
#     else:
#         form = OsagoRecordForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'osago/client/applications contract/calc_ins_auto_osago.html', context)
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
    return render(request, 'osago/client/contract/client_osago_contracts.html', {'contracts': contracts})


def client_osago_claims(request):
    claims = OsagoClaim.objects.filter(osago_contract__osago_record__client=request.user)
    return render(request, 'osago/client/applications insurance/client_osago_claims.html', {'claims': claims})


import logging

logger = logging.getLogger(__name__)


def edit_osago_record(request, record_id):
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
        return redirect('casco:client_casco_requests')
    return redirect('edit_casco_record', record_id=record_id)


def schedule_osago_appointment(request, record_id):
    record = OsagoRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = OsagoScheduleForm(request.POST, instance=record)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            schedule.available = False
            schedule.save()

            form.save()
            return redirect('osago:client_osago_requests')  # Перенаправление после обработки
    else:
        form = OsagoScheduleForm(instance=record)

    return render(request, 'osago/client/applications contract/schedule_osago_appointment.html', {'form': form, 'record': record})

# def calculate_insurance_cost(horse_power, driver_option, age, experience):
#     tariff = 5000
#     kt = 1.8
#     if driver_option == 'one_person':
#         do = 1
#     else:
#         do = 1.8
#     if horse_power < 50:
#         km = 0.6
#     elif 50 <= horse_power < 70:
#         km = 1
#     elif 70 <= horse_power < 100:
#         km = 1.1
#     elif 100 <= horse_power < 120:
#         km = 1.2
#     elif 120 <= horse_power < 150:
#         km = 1.4
#     else:
#         km = 1.6
#
# if age <= 22 and experience <= 3:
#     kvs = 1.8
# elif age > 22 and experience <= 3:
#     kvs = 1.7
# elif age <= 22 and experience > 3:
#     kvs = 1.6
# else:
#     kvs = 1
#
#     insurance_cost = tariff * kt * km * kvs * do
#     return insurance_cost


# @login_required
# def calc_ins_auto_osago(request):
#     insurance_cost = None
#     context = {}
#     if request.method == 'POST':
#         car_insurance_form = OsagoRecordForm(request.POST)
#         if car_insurance_form.is_valid():
#             brand = car_insurance_form.cleaned_data['brand']
#             model = car_insurance_form.cleaned_data['model']
#             car_year = car_insurance_form.cleaned_data['car_year']
#             horse_power = car_insurance_form.cleaned_data['horse_power']
#             driver_option = car_insurance_form.cleaned_data['driver_option']
#             age = car_insurance_form.cleaned_data['age']
#             experience = car_insurance_form.cleaned_data['experience']
#
#             insurance_cost = calculate_insurance_cost(horse_power, driver_option, age, experience)
#             context = {
#                 'brand': brand,
#                 'model': model,
#                 'car_year': car_year,
#                 'horse_power': horse_power,
#                 'driver_option': driver_option,
#                 'age': age,
#                 'experience': experience,
#                 'insurance_cost': insurance_cost,
#             }
#
#     else:
#         car_insurance_form = OsagoRecordForm()
#
#     return render(request, 'osago/client/applications contract/calc_ins_auto_osago.html', {
#         'title': 'calc_ins_auto',
#         'car_insurance_form': car_insurance_form,
#         'insurance_cost': insurance_cost,
#         'context': context,
#     })
