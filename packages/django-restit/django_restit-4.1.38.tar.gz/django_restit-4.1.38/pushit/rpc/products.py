from rest import decorators as rd
from rest import views as rv
from pushit.models import Product, Release


@rd.url('product')
@rd.url('product/<int:pk>')
def rest_on_product(request, pk=None):
    return Product.on_rest_request(request, pk)


@rd.url('release')
@rd.url('release/<int:pk>')
def rest_on_release(request, pk=None):
    return Release.on_rest_request(request, pk)
