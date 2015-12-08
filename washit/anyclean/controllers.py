from django.contrib.auth.models import User
from django.db.models import Q
from anyclean import models, send_sms, util

import config
import constants

import base64
import datetime
import random
import string
from dateutil.parser import parse


def random_pass_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def random_verification_code(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_party(user, name, party_type):
    party = models.Party()
    party.user = user
    party.name = name
    party.party_type = party_type
    party.is_active = True
    party.save()

    return party


def create_party_contact_mech(party, contact_type, info_string, region=None, pin_code=None):
    party_contact = models.PartyContactMech()
    party_contact.contact_type = contact_type
    party_contact.party = party
    party_contact.info_string = info_string
    party_contact.region = region
    party_contact.pin_code = pin_code
    party_contact.save()

    return party_contact


def get_party_contact(party_cont_mech_id):
    return models.PartyContactMech.objects.get(id=party_cont_mech_id)


def get_party_contacts(party, contact_type):
    contact_mech = models.PartyContactMech.objects.filter(thru_date=None, party=party, contact_type=contact_type)

    contacts = []
    for contact in contact_mech:
        data = {}
        data['id'] = contact.id
        data['contact'] = contact.info_string
        data['is_verified'] = contact.is_verified
        contacts.append(data)

    return contacts


def update_party_contact_mech(party_cont_mech_id, info_string, is_verified=None, region=None, pin_code=None):
    if party_cont_mech_id:
        party_contact = models.PartyContactMech.objects.get(id=party_cont_mech_id)
        if party_contact:
            party_contact.info_string = info_string
            party_contact.region = region
            party_contact.pin_code = pin_code
            party_contact.save()
    else:
        raise Exception("Party Contact not found.")

    return party_cont_mech_id


def update_mobile(party, info_string):
    contact_mech = models.PartyContactMech.objects.filter(thru_date=None, party=party, contact_type="MOBILE").first()

    if contact_mech:
        if not contact_mech.info_string == info_string:
            contact_mech.thru_date = datetime.datetime.utcnow()
            contact_mech.save()

            create_party_contact_mech(party, "MOBILE", info_string)
            return "Updated Successfully."
    else:
        create_party_contact_mech(party, "MOBILE", info_string)
        return "Updated Successfully."

    return "Number already present."


def delete_party_contact(party_cont_mech_id):
    if party_cont_mech_id:
        party_contact = models.PartyContactMech.objects.get(id=party_cont_mech_id)
        if party_contact:
            party_contact.thru_date = datetime.datetime.utcnow()
            party_contact.save()
    else:
        raise Exception("Party Contact not found.")

    return True


def update_party_address(party_id, address_id, address):
    party = models.Party.objects.get(party_id=party_id)

    party_contact = models.PartyContactMech.objects.get(id=address_id)
    party_contact.info_string = address
    party_contact.save()
    return True


def add_party(user, name, party_type, email_id, mobile):
    """Adds a party."""

    party = create_party(user, name, party_type)

    if email_id:
        create_party_contact_mech(party, 'EMAIL', email_id)

    if mobile:
        create_party_contact_mech(party, 'MOBILE', mobile)

    return party


def add_update_user_login(
    user_login_id, password, party, is_enabled=True, require_password_change=False):
    """Adds or updates User login."""

    if user_login_id:
        user_login = models.UserLogin.objects.filter(user_login_id=user_login_id).first()
        if not user_login:
            user_login = models.UserLogin()

    user_login.user_login_id = user_login_id
    user_login.password = base64.b64encode(password)
    user_login.party = party
    user_login.is_enabled = is_enabled
    user_login.require_password_change = require_password_change
    user_login.save()

    return user_login


def get_user_login(user_login_id):
    user_login = models.UserLogin.objects.get(user_login_id=user_login_id)
    if not user_login:
        raise Exception("UserLogin not found.")

    return user_login


def is_user_exists(user_login_id):
    if '@' in user_login_id:
        kwargs = {'email': user_login_id}
    else:
        kwargs = {'username': user_login_id}

    try:
        user = User.objects.get(**kwargs)
        return True
    except User.DoesNotExist:
        return False


def register_customer(first_name, last_name, party_type, email_id, mobile):
    password = random_pass_generator()
    if is_user_exists(email_id):
        raise Exception("Email already registered.")

    if is_user_exists(mobile):
        raise Exception("Mobile already registered.")

    name = first_name + ' ' + last_name
    user = User.objects.create_user(
        first_name=first_name, last_name=last_name, username=mobile, email=email_id, password=password)
    party = add_party(user, name, party_type, email_id, mobile)

    code = send_verification_code(mobile)
    send_welcome_email(name, password, email_id, code)

    return user


def send_welcome_email(name, password, to, otp):
    if config.DEV_ENV:
        to = config.TEST_TO_EMAIL

    subject = constants.WELCOME_SUBJECT
    content = constants.WELCOME_MSG % (name, password, otp, config.APP_URL)

    util.send_mail(to, subject, content)


def create_pickup_request(
    party, date, time_slot_id, request_type, party_contact_mech_id, mobile):
    if mobile:
        create_party_contact_mech(party, 'MOBILE', mobile)

    pickup = models.PickupRequest.objects.filter(customer=party)

    if pickup:
        for pick in pickup:
            assignment = models.PickupAssignment.objects.filter(pickup=pick).first()
            if not assignment or assignment.status in ['ASSIGNED', 'ACCEPTED']:
                return {'is_error': True, 'message': "One pickup is already scheduled. Contact customer care to update the slot."}

    time_slot = models.TimeSlot.objects.get(id=time_slot_id)
    party_contact_mech = models.PartyContactMech.objects.get(
        id=party_contact_mech_id)

    pickup = models.PickupRequest()
    pickup.customer = party
    pickup.date = parse(date)
    pickup.time_slot = time_slot
    pickup.request_type = request_type
    pickup.party_contact = party_contact_mech
    pickup.save()

    return {'message': 'Request created successfully.', 'is_error': False}



def get_all_orders(party):
    orders = []
    orders = models.OrderHeader.objects.filter(party=party)

    result = []
    for order in orders:
        order_data = {}
        order_data['id'] = 'AOD000' + order.order_id
        order_data['type'] = order.order_type.capitalize()
        order_data['date'] = format_date(order.order_date)
        order_data['status'] = order.order_status.capitalize()
        order_data['quantity'] = order.quantity
        order_data['weight'] = order.weight
        order_data['amount'] = order.grand_total
        order_data['discount'] = order.discount

        result.append(order_data)

    return result


def get_party_detail(party):
    party_contact_mech = models.PartyContactMech.objects.filter(thru_date=None, party=party)


    email, mob = '', ''
    address = []
    for contact in party_contact_mech:
        if contact.contact_type == 'EMAIL':
            email = contact.info_string
        elif contact.contact_type == 'MOBILE':
            mob = contact.info_string
        elif contact.contact_type == 'ADDRESS':
            data = {}
            data['id'] = contact.id
            data['address'] = contact.info_string
            data['pin_code'] = contact.pin_code
            data['region'] = contact.region.name
            address.append(data)

    return {
        'party_id': party.party_id,
        'name': party.name,
        'email_id': email,
        'mobile': mob,
        'address': address}


def get_time_slots(city):
    city = models.City.objects.get(id=city)
    time_slots = models.TimeSlot.objects.filter(city=city)

    slots = []
    for slot in time_slots:
        data = {}
        data['id'] = slot.id
        data['time'] = slot.from_time + ' - ' + slot.to_time
        slots.append(data)

    return slots


def get_cities():
    cities = models.City.objects.all()
    city = []

    for store in cities:
        data = {}
        data['id'] = store.id
        data['name'] = store.name
        city.append(data)

    return city


def update_password(user_login_id, old_password, new_password):
    try:
        user_login = models.UserLogin.objects.get(user_login_id=user_login_id)
        if user_login.password == old_password or user_login.password == base64.b64encode(old_password):
            user_login.password = new_password
            user_login.save()
            return HttpResponse('Password updated.')
        return HttpResponse("Password didn't match.")
    except models.UserLogin.DoesNotExist:
        return HttpResponse("Your username and password didn't match.")


def save_sms_report(
    receiver, sender, status, message_uuid, parent_message_uuid, part_info):

    sms_report = models.SMS_Report()
    sms_report.receiver = receiver
    sms_report.sender = sender
    sms_report.status = status
    sms_report.message_uuid = message_uuid
    sms_report.parent_message_uuid = parent_message_uuid
    sms_report.part_info = part_info
    sms_report.save()

    return sms_report.id


def verify_user(party, to, ver_type, code):
    verification = models.Verifcation_Code.objects.filter(to=to, ver_type=ver_type, is_verified=False).first()

    if verification:
        if not verification.is_verified:
            if verification.code == code:
                verification.is_verified = True
                verification.save()

                # update party contact mech for this number, is_verified=True
                contact_mech = models.PartyContactMech.objects.filter(
                    thru_date=None, party=party, contact_type=ver_type, info_string=to).first()
                if contact_mech:
                    contact_mech.is_verified = True
                    contact_mech.save()
                return True
            else:
                return False
        else:
            return True

    return False


def send_verification_code(mobile):
    '''Send verification code on mobile.'''
    code = random_verification_code()

    ver_code = models.Verifcation_Code.objects.filter(to=mobile, ver_type="MOBILE", is_verified=False).first()
    if ver_code:
        code = ver_code.code

    send_sms.send_text(mobile, 'Verification code is ' + code)
    save_verification_code(mobile, 'MOBILE', code)

    return code


def save_verification_code(to, ver_type, code):
    ver_code = models.Verifcation_Code()
    ver_code.to = to
    ver_code.ver_type = ver_type
    ver_code.code = code
    ver_code.save()

    return ver_code.id


def mail_communication(to, sub, msg):
    communication = models.Mail_Communication()
    communication.to = to
    communication.subject = sub
    communication.message = msg
    communication.save()

    return communication.id


def create_contact_us(name, email, sub, msg):
    contact_us = models.Contact_Us()
    contact_us.name = name
    contact_us.email = email
    contact_us.subject = sub
    contact_us.message = msg
    contact_us.save()

    util.send_mail(config.CONTACT_US_EMAIL, sub + ' From: ' + email, msg)
    util.send_mail(email, constants.CONTACT_US_SUB, constants.CONTACT_US_MSG)

    return contact_us.id


def subscribe_to_email(email):
    subs = models.Subscribe_To_Email.objects.filter(email=email).first()
    if subs:
        if not subs.is_subscribed:
            subs.is_subscribed = True
            subs.save()
            return "Subscribed."
        else:
            return "Already Subscribed."

    subs = models.Subscribe_To_Email()
    subs.email = email
    subs.save()

    return "Subscribed."


def unsubscribe_to_email(email):
    subs = models.Subscribe_To_Email.objects.filter(email=email).first()
    if subs:
        subs.is_subscribed = False
        subs.save()

    return True


def is_subscribed(email):
    subs = models.Subscribe_To_Email.objects.filter(email=email).first()
    if subs:
        return subs.is_subscribed

    return False


def get_party_address(party):
    contact_mech = models.PartyContactMech.objects.filter(thru_date=None, party=party, contact_type="ADDRESS")

    address = []
    for contact in contact_mech:
        data = {}
        data['id'] = contact.id
        data['address'] = contact.info_string
        data['pin_code'] = contact.pin_code
        data['city'] = contact.region.name
        data['region_id'] = contact.region_id
        address.append(data)

    return address


def send_refer_mail(email, referer):
    pass


def send_refer_sms(mobile, referer):
    pass


def save_refer_friend(contacts, referer):
    refer = models.ReferFriend()
    refer.contacts = contacts
    refer.referer = referer
    refer.save()

    return refer.id


def refer_friend(user, email, mobile):
    referer = user.first_name + ' ' + user.last_name
    if email:
        save_refer_friend(email, user)
        send_refer_mail(email, referer)

    if mobile:
        save_refer_friend(mobile, user)
        send_refer_sms(mobile, referer)

    return True


def get_faq():
    faqs = models.FAQ.objects.filter(show=True)

    return faqs


def track_requests(party):
    pickups = models.PickupRequest.objects.filter(customer__pk=party.party_id).order_by('-date')
    pick_req = []

    for pic in pickups:
        data = {}
        pickup_assignment = models.PickupAssignment.objects.filter(pickup=pic).first()
        if pickup_assignment:
            data['status'] = pickup_assignment.status.capitalize()
        else:
            data['status'] = 'Scheduled'

        data['request_id'] = 'PR000' + str(pic.pickup_id)
        data['date'] = format_date(pic.date)
        data['created_date'] = format_date(pic.created_timestamp)
        data['time'] = pic.time_slot.from_time + ' - ' + pic.time_slot.to_time
        data['address'] = pic.party_contact.info_string
        pick_req.append(data)

    return pick_req


def get_all_pickups():
    pickups = models.PickupRequest.objects.filter(is_assigned=False)

    pick_req = []

    for pic in pickups:
        data = {}
        pickup_assignment = models.PickupAssignment.objects.filter(pickup=pic).first()
        if pickup_assignment:
            data['status'] = pickup_assignment.status
        else:
            data['status'] = 'Scheduled'

        data['request_id'] = 'PR000' + str(pic.pickup_id)
        data['date'] = format_date(pic.date)
        data['created_date'] = format_date(pic.created_timestamp)
        data['time'] = pic.time_slot.from_time + ' - ' + pic.time_slot.to_time
        data['address'] = pic.party_contact.info_string
        pick_req.append(data)

    return pick_req


def get_pickup_boys():
    party = models.Party.objects.filter(party_type='DELIVERY_BOY')

    pickup_boy = []
    for boy in party:
        data = {}
        data['id'] = party.party_id
        data['name'] = ' '.join([party.user.first_name + ' ' + party.user.last_name])
        pickup_boy.append(data)

    return pickup_boy



# def search_customer(input, search_by):
#     result = []
#     if search_by == 'CID':
#         party = [models.Party.objects.get(party_id=input)]
#     elif search_by == 'NAME':
#         party = models.Party.objects.filter(name__contains=input, party_type='CUSTOMER')
#     else:
#         party_cont_mech = models.PartyContactMech.objects.filter(thru_date=None, contact_type=search_by, info_string=input).first()
#         if party_cont_mech:
#             party = [party_cont_mech.party]

#     if party:
#         for customer in party:
#             data = {}
#             data[]

#     return "Not found."


def format_date(date_obj):
    return date_obj.strftime('%d/%m/%Y')
