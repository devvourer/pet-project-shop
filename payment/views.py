from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from orders.models import Order
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO

import weasyprint
import braintree


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # receive token
        nonce = request.POST.get('payment_method_nonce', None)
        # creating and saving transaction
        result = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options': {'submit_for_settlement': True}
        })
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()

            subject = f'Shop - Invoice no. {order.id}'
            message = 'Please, find attached the invoice for your recent purchase'
            email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [order.email])

            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

            email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
            email.send()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        return render(request, 'payment/process.html', {'order': order, 'client_token': client_token})


def payment_done(request):
    return render(request, 'payment/done.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


class PaymentView(View):
    http_method_names = ['post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponse('sucess', status=200)