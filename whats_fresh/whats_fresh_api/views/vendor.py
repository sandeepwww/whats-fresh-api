from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
import json


def vendor_list(request):
    """
    */vendors/*

    Returns a list of all vendors in the database. In the future this function
    will support the ?limit=<int> parameter to limit the number of vendors
    returned, the ?lat=<float>&long=<float> parameters to sort by location, and
    the ?proximity=<int> parameter to limit the distance of the vendors.
    """
    data = {}
    vendor_list = Vendor.objects.all()

    if len(vendor_list) == 0:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Could not find any vendors!',
            'error_name': 'No Vendors'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )
    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(model_to_dict(vendor, fields=[], exclude=[]))
            data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')
            data['vendors'][-1]['id'] = vendor.id

            products = data['vendors'][-1]['products']
            data['vendors'][-1]['products'] = []
            for product_id in products:
                product = VendorProduct.objects.get(id=product_id)
                product_data = {
                    'id': product.product.id,
                    'preparation': product.preparation.name,
                    'name': product.product.name
                }
                data['vendors'][-1]['products'].append(product_data)

        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': str(e),
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )


def vendors_products(request, id=None):
    data = {}
    try:
        vendor_list = Vendor.objects.filter(products__id__contains=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': 'Product id is invalid',
            'error_name': 'Invalid product'
        }

    if len(vendor_list) == 0:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Could not find any vendors for product %s!' % id,
            'error_name': 'No Vendors for product %s' % id
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    try:
        data['vendors'] = []
        for vendor in vendor_list:
            data['vendors'].append(model_to_dict(vendor, fields=[], exclude=[]))
            data['vendors'][-1]['phone'] = data['vendors'][-1]['phone'].national_number

            data['vendors'][-1]['created'] = str(vendor.created)
            data['vendors'][-1]['updated'] = str(vendor.modified)
            data['vendors'][-1]['ext'] = {}
            data['vendors'][-1]['id'] = vendor.id

            data['vendors'][-1]['story'] = data['vendors'][-1].pop('story_id')

            products = data['vendors'][-1]['products']
            data['vendors'][-1]['products'] = []
            for product_id in products:
                product = VendorProduct.objects.get(id=product_id)
                product_data = {
                        'id': product.product.id,
                        'preparation': product.preparation.name,
                        'name': product.product.name
                        }
                data['vendors'][-1]['products'].append(product_data)

        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': str(e),
            'error_name': 'Unknown'
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )

def vendor_details(request, id=None):
    data = {}

    try:
        vendor = Vendor.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Important',
            'error_text': 'Vendor with id %s not found!' % id,
            'error_name': 'Vendor not found'
        }
        return HttpResponseNotFound(
                json.dumps(data),
                content_type="application/json"
        )

    try:
        data = (model_to_dict(vendor, fields=[], exclude=[]))
        data['phone'] = data['phone'].national_number

        data['created'] = str(vendor.created)
        data['updated'] = str(vendor.modified)
        data['ext'] = {}
        data['story'] = data.pop('story_id')
        data['id'] = vendor.id

        products = data['products']
        data['products'] = []
        for product_id in products:
            product = VendorProduct.objects.get(id=product_id)
            product_data = {
                'id': product.product.id,
                'preparation': product.preparation.name,
                'name': product.product.name
            }
            data['products'].append(product_data)

        data['error'] = {
            'error_status': False,
            'error_level': None,
            'error_text': None,
            'error_name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        data['error'] = {
            'error_status': True,
            'error_level': 'Severe',
            'error_text': str(e),
            'error_name': 'Unknown'
        }

        return HttpResponseServerError(
                json.dumps(data),
                content_type="application/json"
        )
