import MySQLdb
from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Phone


def index(request):
    phones = Phone.objects.all()
    paginator = Paginator(phones, 15)

    page = request.GET.get('page')
    phone_list = paginator.get_page(page)
    num_of_pages = list(range(1, phone_list.paginator.num_pages + 1))

    return render(request, 'phones/index.html', {'phone_list': phone_list, 'num_of_pages': num_of_pages})


def detail(request, phone_id):
    phone = get_object_or_404(Phone, pk=phone_id)
    return render(request, 'phones/detail.html', {'phone': phone})


def search(request):
    brand_list = []
    for phone in Phone.objects.all():
        if phone.brand not in brand_list:
            brand_list.append(phone.brand)

    device_type_list = []
    for phone in Phone.objects.all():
        if phone.deviceType not in device_type_list:
            device_type_list.append(phone.deviceType)

    os_list = []
    for phone in Phone.objects.all():
        if phone.os not in os_list:
            os_list.append(phone.os)

    if request.GET.get('advanced_search'):
        brand, device_type, os = None, None, None
        if request.GET.get('brand'):
            brand = request.GET.get('brand')
        if request.GET.get('device_type'):
            device_type = request.GET.get('device_type')
        if request.GET.get('os'):
            os = request.GET.get('os')

        print(brand, device_type, os)
        all_phones = Phone.objects.all()
        filtered_phone_list = []
        for phone in all_phones:
            if brand and phone.brand == brand:
                if device_type and phone.deviceType == device_type:
                    if os and phone.os == os:
                        filtered_phone_list.append(phone)
                    elif not os:
                        filtered_phone_list.append(phone)
                elif not device_type:
                    filtered_phone_list.append(phone)
            elif not brand:
                filtered_phone_list.append(phone)

        return render(request, 'phones/search.html', {
            'phones_search': filtered_phone_list,
            'brand_list': brand_list,
            'device_type_list': device_type_list,
            'os_list': os_list
        })
    elif request.POST:
        model_request = request.POST.get('model')
        all_phones = Phone.objects.all()
        phones_search = []
        for phone in all_phones:
            if model_request.lower() in phone.model.lower():
                phones_search.append(phone)

        return render(request, 'phones/search.html', {
            'phones_search': phones_search,
            'brand_list': brand_list,
            'device_type_list': device_type_list,
            'os_list': os_list
        })
    else:
        return render(request, 'phones/search.html', {
            'brand_list': brand_list,
            'device_type_list': device_type_list,
            'os_list': os_list
        })


'''
    Methods below are only for initial database filling use.
    DO NOT call them any time after initialization.
'''


def connect_to_db(to_do):
    try:
        connection = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="root",
            db="lab7python"
        )
        if connection.errno() == 0:
            print('Connection established.')
            to_do(connection)
        else:
            print('Connection failed.')
    except MySQLdb.Error as error:
        print("Connection error: {}".format(error))
    finally:
        connection.close()
        print('Connection closed.')


def read_products(connection):
    curr = connection.cursor(MySQLdb.cursors.DictCursor)

    sql_get_products = "SELECT * FROM phones;"
    curr.execute(sql_get_products)
    data = curr.fetchall()
    print(data)
    i = 0
    for phone in data:
        new_description = ""
        for char in phone["description"]:
            if (ord(char) > ord("A") and ord(char) < ord("z")) or (ord(char) == 46 or ord(char) == 44 or ord(char) == 32):
                new_description += char
        new_phone = Phone(
            brand=phone["brand"],
            model=phone["model"],
            price=phone["price"] or 100,
            deviceType=phone["deviceType"] or "symbian",
            os=phone["os"] or "no",
            imageUrl=phone["imageUrl"],
            description=new_description
        )
        new_phone.save()
