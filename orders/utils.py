import requests
from django.conf import settings
import os


def pincode_check(pincode):
    """Check pincode is valid or not"""
    try:
        response = requests.get(f'https://api.postalpincode.in/pincode/{pincode}')
        if response.status_code == 200:
            status = response.json()[0].get('Status')
            if status and status == 'Success':
                return True
    except Exception as e:
        print('Exception pincode cheking, Error:', e)

def get_shiprocket_token():
    """Get auth token using email and password"""
    data = {
        "email": settings.SHIPROCKET_EMAIL,
        "password": settings.SHIPROCKET_PASSWORD,
    }
    response = requests.post(settings.SHIPROCKET_API_URL + 'auth/login', data=data)
    if response.status_code == 200:
        response = response.json()
        token = response.get('token')
        return token
    print(f'Token getting failed, Status: {response.status_code}, Error: {response.text}')

def get_shipping_charges(delivery_postcode, product_weight, cod=0, token=None):
    """Get shipping charges for given pin codes, product weight and cod"""
    params = {
        "pickup_postcode": int(settings.PICKUP_PINCODE),
        "delivery_postcode": int(delivery_postcode),
        "weight": product_weight,
        "cod": cod,
    }
    headers = {
        "Authorization": f"Bearer {token if token else settings.SHIPROCKET_TOKEN}"
    }
    response = requests.get(settings.SHIPROCKET_API_URL + 'courier/serviceability/', params=params, headers=headers)
    if response.status_code == 200:
        response = response.json()
        data = response.get('data')
        couriers = data['available_courier_companies']
        best = sorted(couriers, key=lambda x: x['rate'])[0]
        shipping_charge = best['rate']
        etd = best['etd']
        return {'charges': shipping_charge, 'etd': etd}
    if response.status_code == 401:
        token = get_shiprocket_token()
        if token:
            os.environ.setdefault('SHIPROCKET_TOKEN', token)
            return get_shipping_charges(delivery_postcode, product_weight, token=token)
    print(f'Shipping charges getting failed, Status: {response.status_code}, Error: {response.text}')
