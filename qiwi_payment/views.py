from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from orders.models import Order

import requests
import uuid

public_key = '48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPsZ327fxQ33H4zJuzvSSgVnJTDqHfCJGk8DtWamh39JLs4nKXSxPjcoU6EKUMeo5gXjT8DqLq5uoEb3hwHqrQ4qA1mGyRyeMiYeFNjjWFx'
url = 'https://api.qiwi.com/partner/bill/v1/bills/'


def payment_process(request):
    # получаем наш заказ с сессии
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    # делаем уникальный идентификатор заказа
    order.billid = uuid.uuid4()
    order.save()

    data_raw = {
        "amount": {
            "currency": "RUB",
            "value": str(order.get_total_cost())
        },
        "comment": "PODKLUCHAEM api",
        "expirationDateTime": "2025-12-10T09:02:00+03:00"
        }
    billid = str(order.billid)
    r = requests.put(url+billid, headers={'content-type': 'application/json',
                                   'accept': 'application/json',
                                   'Authorization': 'Bearer'+settings.QIWI_API_KEY
                                   }, json=data_raw)
    redirect_to_form = r.json()
    return redirect(redirect_to_form['payUrl'])



class PaymentView(View):
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponse('sucess', status=200)


