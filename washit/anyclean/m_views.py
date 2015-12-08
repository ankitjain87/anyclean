from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from anyclean import controllers, models, decorators

from tokenapi.decorators import token_required
from tokenapi.http import JsonResponse, JsonError


def mGet_Pickups(request):
    username = request.REQUEST.get('username')
    user = ''
    if '@' in username:
        user = User.objects.filter(email=username).first()

    if user:
        party = user.profile
        pickupAssg = models.PickupAssignment.objects.filter(Q(status='ASSIGNED') | Q(status='ACCEPTED'), assigned_to=party)

        pickups = []
        for pic in pickupAssg:
            pickup = pic.pickup
            data = {}
            data['pickup_id'] = pickup.pickup_id
            data['status'] = pic.status
            data['date'] = controllers.format_date(pickup.date)
            data['time_slot'] = pickup.time_slot.from_time + '-' + pickup.time_slot.to_time
            data['customer'] = pickup.customer.user.first_name + ' ' + pickup.customer.user.last_name
            data['address'] = ' '.join([pickup.party_contact.info_string, pickup.party_contact.region.name, str(pickup.party_contact.pin_code)])
            data['mobile'] = controllers.get_party_contacts(pickup.customer, "MOBILE")[0]['contact']
            pickups.append(data)

        return JsonResponse(pickups)

    else:
        return JsonError('User Not found.')


