from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import CarModel, CascoRecord, Brand, CascoContract, CascoClaim
from .forms import CarCascoForm, CarSearchForm, CascoRecordForm, CascoScheduleForm
from decimal import Decimal
from django.db.models import Q


# def calculate_casco_cost(car_cost, coverage, repair_type, mileage, cost_guarantee, horsepower, age, experience):
#     base_rate = Decimal('0.03')
#
#     # Модификаторы покрытия
#     if coverage == 'full':
#         coverage_rate = Decimal('1.3')
#     elif coverage == 'theft_destruction':
#         coverage_rate = Decimal('1.2')
#     else:
#         coverage_rate = Decimal('1.1')
#
#     # Модификаторы типа ремонта
#     if repair_type == 'dealer':
#         repair_rate = Decimal('1.3')
#     elif repair_type == 'specialized_service':
#         repair_rate = Decimal('1.2')
#     else:
#         repair_rate = Decimal('1.1')
#
#     # Модификатор пробега
#     if mileage < 50000:
#         mileage_rate = Decimal('1.1')
#     elif 50000 <= mileage < 100000:
#         mileage_rate = Decimal('1.2')
#     else:
#         mileage_rate = Decimal('1.3')
#
#     # Модификатор гарантии стоимости
#     guarantee_rate = Decimal('1000.0') if cost_guarantee else Decimal('0.0')
#
#     tariff = Decimal('5000.0')
#     kt = Decimal('1.8')
#
#     # Коэффициент мощности (km)
#     if horsepower < 50:
#         km = Decimal('0.6')
#     elif 50 <= horsepower < 70:
#         km = Decimal('1.0')
#     elif 70 <= horsepower < 100:
#         km = Decimal('1.1')
#     elif 100 <= horsepower < 120:
#         km = Decimal('1.2')
#     elif 120 <= horsepower < 150:
#         km = Decimal('1.4')
#     else:
#         km = Decimal('1.6')
#
#     # Коэффициент возраста и стажа (kvs)
#     if age <= 22 and experience <= 3:
#         kvs = Decimal('1.8')
#     elif age > 22 and experience <= 3:
#         kvs = Decimal('1.7')
#     elif age <= 22 and experience > 3:
#         kvs = Decimal('1.6')
#     else:
#         kvs = Decimal('1.0')
#
#     insurance_cost = car_cost * base_rate * coverage_rate * repair_rate * mileage_rate + guarantee_rate + (
#             tariff * kt * km * kvs)
#     return insurance_cost.quantize(Decimal('0.01'))


def car_view_casco(request):
    insurance_cost = None
    if request.method == 'POST':
        form = CarCascoForm(request.POST)
        if form.is_valid():
            horsepower = int(form.cleaned_data['horsepower'])
            age = form.cleaned_data['age']
            experience = form.cleaned_data['experience']
            car_cost = form.cleaned_data['car_cost']
            coverage = form.cleaned_data['coverage']
            repair_type = form.cleaned_data['repair_type']
            mileage = form.cleaned_data['mileage']
            cost_guarantee = form.cleaned_data['cost_guarantee']
            insurance_cost = calculate_casco_cost(car_cost, coverage, repair_type, mileage, cost_guarantee, horsepower,
                                                  age, experience)
    else:
        form = CarCascoForm()
    return render(request, 'casco/client/applications contract/calc_ins_auto_casco.html',
                  {'form': form, 'insurance_cost': insurance_cost})


def search_request_casco(request):
    form = CarSearchForm(request.GET)
    casco_records = CascoRecord.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        coverage = form.cleaned_data.get('coverage')
        repair_type = form.cleaned_data.get('repair_type')
        status = form.cleaned_data.get('status')
        cost_guarantee = form.cleaned_data.get('cost_guarantee')

        if search_query:
            casco_records = casco_records.filter(
                Q(car_model__brand__name__icontains=search_query) |
                Q(car_model__model_name__icontains=search_query) |
                Q(car_model__year__icontains=search_query) |
                Q(car_model__horsepower__icontains=search_query) |
                Q(age__icontains=search_query) |
                Q(experience__icontains=search_query) |
                Q(insurance_cost__icontains=search_query) |
                Q(mileage__icontains=search_query) |
                Q(cost_guarantee__icontains=search_query) |
                Q(car_cost__icontains=search_query)
            )

        if coverage:
            casco_records = casco_records.filter(coverage=coverage)

        if repair_type:
            casco_records = casco_records.filter(repair_type=repair_type)

        if status:
            casco_records = casco_records.filter(status=status)

        if cost_guarantee:
            casco_records = casco_records.filter(cost_guarantee=(cost_guarantee == 'True'))

    return render(request, 'casco/client/applications contract/client_casco_requests.html',
                  {'form': form, 'casco_records': casco_records})


def create_casco_record(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        model_name = request.POST.get('model_name')
        year = request.POST.get('year')
        horsepower = request.POST.get('horsepower')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        coverage = request.POST.get('coverage')
        repair_type = request.POST.get('repair_type')
        mileage = request.POST.get('mileage')
        cost_guarantee = request.POST.get('cost_guarantee') == 'on'
        car_cost = request.POST.get('car_cost')
        insurance_cost = request.POST.get('insurance_cost')

        # Преобразование insurance_cost и car_cost в Decimal
        insurance_cost = Decimal(insurance_cost.replace(',', '.'))
        car_cost = Decimal(car_cost.replace(',', '.'))

        brand = get_object_or_404(Brand, pk=brand_id)
        car_model = get_object_or_404(CarModel, brand=brand, model_name=model_name, year=year, horsepower=horsepower)

        CascoRecord.objects.create(
            client_id=request.user,
            car_model=car_model,
            age=age,
            experience=experience,
            coverage=coverage,
            repair_type=repair_type,
            mileage=mileage,
            cost_guarantee=cost_guarantee,
            car_cost=car_cost,
            insurance_cost=insurance_cost
        )
        return redirect('casco:client_casco_requests')

    return redirect('casco:car_view_casco')


def client_casco_requests(request):
    casco_records = CascoRecord.objects.filter(client_id=request.user)
    return render(request, 'casco/client/applications contract/client_casco_requests.html',
                  {'casco_records': casco_records})


def client_casco_contracts(request):
    contracts = CascoContract.objects.filter(casco_record__client_id=request.user)
    return render(request, 'casco/client/contract/client_casco_contracts.html', {'contracts': contracts})


def client_casco_claims(request):
    claims = CascoClaim.objects.filter(insurance_contract_id__casco_record__client_id=request.user)
    return render(request, 'casco/client/applications insurance/client_casco_claims.html', {'claims': claims})


import logging

logger = logging.getLogger(__name__)


def calculate_casco_cost(car_cost, coverage, repair_type, mileage, cost_guarantee, horsepower, age, experience):
    car_cost = Decimal(car_cost)
    mileage = int(mileage)
    horsepower = int(horsepower)
    age = int(age)
    experience = int(experience)
    cost_guarantee = bool(cost_guarantee)

    base_rate = Decimal('0.03')

    # Модификаторы покрытия
    if coverage == 'full':
        coverage_rate = Decimal('1.3')
    elif coverage == 'theft_destruction':
        coverage_rate = Decimal('1.2')
    else:
        coverage_rate = Decimal('1.1')

    # Модификаторы типа ремонта
    if repair_type == 'dealer':
        repair_rate = Decimal('1.3')
    elif repair_type == 'specialized_service':
        repair_rate = Decimal('1.2')
    else:
        repair_rate = Decimal('1.1')

    # Модификатор пробега
    if mileage < 50000:
        mileage_rate = Decimal('1.1')
    elif 50000 <= mileage < 100000:
        mileage_rate = Decimal('1.2')
    else:
        mileage_rate = Decimal('1.3')

    # Модификатор гарантии стоимости
    guarantee_rate = Decimal('1000.0') if cost_guarantee else Decimal('0.0')

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

    insurance_cost = car_cost * base_rate * coverage_rate * repair_rate * mileage_rate + guarantee_rate + (
            tariff * kt * km * kvs)
    return insurance_cost.quantize(Decimal('0.01'))


def edit_casco_record(request, record_id):
    try:
        record = get_object_or_404(CascoRecord, id=record_id)
        if request.method == 'POST':
            form = CascoRecordForm(request.POST, instance=record)
            if form.is_valid():
                # Получение данных из формы
                car_cost = form.cleaned_data['car_cost']
                coverage = form.cleaned_data['coverage']
                repair_type = form.cleaned_data['repair_type']
                mileage = form.cleaned_data['mileage']
                cost_guarantee = form.cleaned_data['cost_guarantee']
                horsepower = form.cleaned_data['horsepower']
                age = form.cleaned_data['age']
                experience = form.cleaned_data['experience']

                # Преобразование данных перед расчетом
                car_cost = Decimal(car_cost)
                mileage = int(mileage)
                horsepower = int(horsepower)
                age = int(age)
                experience = int(experience)
                cost_guarantee = bool(cost_guarantee)

                # Расчет стоимости страхования
                insurance_cost = calculate_casco_cost(
                    car_cost=car_cost,
                    coverage=coverage,
                    repair_type=repair_type,
                    mileage=mileage,
                    cost_guarantee=cost_guarantee,
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

                return redirect('casco:client_casco_requests')  # Замените на нужную вам страницу
        else:
            form = CascoRecordForm(instance=record)
        return render(request, 'casco/client/applications contract/edit_casco_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'casco/client/applications contract/edit_casco_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def load_models(request):
    try:
        brand_id = request.GET.get('brand')
        models = list(CarModel.objects.filter(brand_id=brand_id).values('model_name').distinct())
        return JsonResponse(models, safe=False)
    except Exception as e:
        logger.error(f"Error loading models: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def load_years(request):
    try:
        brand_id = request.GET.get('brand')
        model_name = request.GET.get('model_name')
        years = list(CarModel.objects.filter(brand_id=brand_id, model_name=model_name).values('year').distinct())
        return JsonResponse(years, safe=False)
    except Exception as e:
        logger.error(f"Error loading years: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def load_horsepowers(request):
    try:
        brand_id = request.GET.get('brand')
        model_name = request.GET.get('model_name')
        year = request.GET.get('year')
        horsepowers = list(
            CarModel.objects.filter(brand_id=brand_id, model_name=model_name, year=year).values(
                'horsepower').distinct())
        return JsonResponse(horsepowers, safe=False)
    except Exception as e:
        logger.error(f"Error loading horsepowers: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def delete_casco_record(request, record_id):
    record = get_object_or_404(CascoRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('casco:client_casco_requests')
    return redirect('edit_casco_record', record_id=record_id)


def schedule_casco_appointment(request, record_id):
    record = CascoRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = CascoScheduleForm(request.POST, instance=record)
        if form.is_valid():
            schedule = form.cleaned_data['schedule']
            schedule.available = False
            schedule.save()

            record.schedule = schedule
            record.save()
            form.save()
            return redirect('casco:client_casco_requests')  # Перенаправление после успешной обработки
    else:
        form = CascoScheduleForm(instance=record)

    return render(request, 'casco/client/applications contract/schedule_casco_appointment.html', {'form': form, 'record': record})
