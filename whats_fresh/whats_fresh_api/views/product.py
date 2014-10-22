from django.http import (HttpResponse,
                         HttpResponseNotFound,
                         HttpResponseServerError)
from whats_fresh.whats_fresh_api.models import Vendor, Product, VendorProduct
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required, user_passes_test

import json
from .serializer import FreshSerializer


def product_list(request):
    """
    */products/*

    Returns a list of all products in the database. The ?limit=<int> parameter
    limits the number of products returned.
    """
    error = {
        'status': False,
        'level': None,
        'debug': None,
        'text': None,
        'name': None
    }

    limit = request.GET.get('limit', None)
    if limit:
        try:
            limit = int(limit)
        except ValueError as e:
            error = {
                'debug': "{0}: {1}".format(type(e).__name__, str(e)),
                'status': True,
                'level': 'Warning',
                'text': 'Invalid limit. Returning all results.',
                'name': 'Bad Limit'
            }

    serializer = FreshSerializer()
    queryset = Product.objects.all()[:limit]

    if not queryset:
        error = {
            "status": True,
            "text": "No Products found",
            "name": "No Products",
            "debug": "",
            "level": "Error"
        }

    data = {
        "products": json.loads(
            serializer.serialize(
                queryset,
                use_natural_foreign_keys=True
            )
        ),
        "error": error
    }

    return HttpResponse(json.dumps(data), content_type="application/json")


def product_details(request, id=None):
    """
    */products/<id>*

    Returns the product data for product <id>.
    """
    data = {}

    try:
        product = Product.objects.get(id=id)
    except Exception as e:
        data['error'] = {
            'status': True,
            'level': 'Error',
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'text': 'Product id %s was not found.' % id,
            'name': 'Product Not Found'
        }
        return HttpResponseNotFound(
            json.dumps(data),
            content_type="application/json"
        )

    error = {
        'status': False,
        'level': None,
        'debug': None,
        'text': None,
        'name': None
    }

    serializer = FreshSerializer()

    data = json.loads(
            serializer.serialize(
                [product],
                use_natural_foreign_keys=True
            )[1:-1]
        )

    data['error'] = error

    return HttpResponse(json.dumps(data), content_type="application/json")



def product_vendor(request, id=None):
    """
    */products/vendors/<id>*

    List all products sold by vendor <id>. This information includes the details
    of the products, rather than only the product name/id and preparation name/id
    returned by */vendors/<id>*.
    """
    data = {}

    try:
        product_list = Product.objects.filter(
            productpreparation__vendorproduct__vendor__id__exact=id)
    except Exception as e:
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Important',
            'text': 'Vendor with id %s not found!' % id,
            'name': 'Vendor Not Found'
        }
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    data['products'] = []
    try:
        for product in product_list:
            data['products'].append(
                model_to_dict(product, fields=[], exclude=[]))
            del data['products'][-1]['preparations']
            del data['products'][-1]['image']

            try:
                data['products'][-1]['story'] = product.story.id
            except AttributeError:
                data['products'][-1]['story'] = None
            try:
                data['products'][-1]['image'] = product.image.image.url
            except AttributeError:
                data['products'][-1]['image'] = None
            data['products'][-1]['created'] = str(product.created)
            data['products'][-1]['modified'] = str(product.modified)
            data['products'][-1]['id'] = product.id

        data['error'] = {
            'status': False,
            'level': None,
            'debug': None,
            'text': None,
            'name': None
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    except Exception as e:
        text = 'An unknown error occurred processing product %s' % id
        data['error'] = {
            'debug': "{0}: {1}".format(type(e).__name__, str(e)),
            'status': True,
            'level': 'Severe',
            'text': text,
            'name': str(e)
        }
        return HttpResponseServerError(
            json.dumps(data),
            content_type="application/json"
        )
