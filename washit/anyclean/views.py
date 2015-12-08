from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from anyclean import controllers, models, send_sms, decorators, cc_views
from anyclean.forms import RegisterForm, VerificationForm
import base64
import datetime


def home(request):
    """Index page."""
    return render(request, 'index.html')


def enter_name(request):
    """Index page."""

    return render(request, 'index3.html')


def loginPage(request):
    """Login page."""
    return render(request, 'login.html')


def log_in(username, password):
    if '@' in username:
        user = User.objects.filter(email=username).first()
    else:
        user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return True
        else:
            return 'Account disabled.'

    else:
        return 'Invalid Login.'


def log_out(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    else:
        # A POST request: Handle Form Upload
        form = RegisterForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            try:
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email_id = form.cleaned_data['email']
                mobile = form.cleaned_data['mobile']
                party_type = 'CUSTOMER'

                customer = controllers.register_customer(
                    first_name, last_name, party_type, email_id, mobile)

                customer.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, customer)
                return redirect('/verification/')
                # return render(request, 'verification.html', {'form': form, 'mobile': mobile})

            except Exception as ex:
                # raise ex
                # Return user to same page with error message.
                return render(
                    request, 'register.html', {'message': ex, 'is_error': True})
 
    return render(request, 'register.html', {
        'form': form,
    })


@login_required
def dashboard_redirect(request):
    groups = [g.name for g in request.user.groups.all()]
    if "CR" in groups:
        return redirect('/ccDashboard/')
    else:
        return redirect('/dashboard/')


@login_required
@decorators.has_customer_permission
def dashboard(request, data=None):
    party = request.user.profile
    party_contact = controllers.get_party_contacts(party, "MOBILE")
    context = {
        'detail': party_contact,
    }
    if data:
        context.update(data)

    return render(request, 'dashboard.html', context)



@login_required
@decorators.has_customer_permission
def verification(request):
    otp = request.REQUEST.get('otp')
    party = request.user.profile
    mobile = controllers.get_party_contacts(party, "MOBILE")[0]['contact']

    verify_otp = controllers.verify_user(party, mobile, 'MOBILE', otp)

    if verify_otp:
        return JsonResponse({'is_error': False, 'message': 'Verified successfully.'})

    return JsonResponse({'is_error': True, 'message': 'Code is not correct.'})


@login_required
@decorators.has_customer_permission
def request_pickup(request, data=None):
    party = request.user.profile
    start_date = datetime.datetime.utcnow()
    start_date = start_date + datetime.timedelta(days=1)
    context = {
        'party_detail': controllers.get_party_detail(party),
        # get time slots for user 
        'time_slots': controllers.get_time_slots('BANGALORE'),
        'start_date': start_date.strftime('%Y-%m-%d')
    }
    if data:
        context.update(data)

    return render(request, 'pickup.html', context)


@login_required
def get_time_slots(request):
    city_id = request.REQUEST.get('city_id')

    return controllers.get_time_slots(city_id)


@login_required
@decorators.has_customer_permission
def create_pickup_request(request):
    party = request.user.profile
    date = request.REQUEST.get('date')
    time_slot_id = request.REQUEST.get('time_slot_id')
    party_contact_mech_id = request.REQUEST.get('address_id')
    mobile = request.REQUEST.get('mobile')
    request_type = request.REQUEST.get('request_type', 'ONLINE')

    try:
        pickup = controllers.create_pickup_request(
            party, date, time_slot_id, request_type, party_contact_mech_id, mobile)
    except Exception as ex:
        print ex

    return JsonResponse(pickup)


@login_required
@decorators.has_customer_permission
def profile(request, data=None):
    address_id = request.REQUEST.get('address_id')
    party = request.user.profile

    context = {
        'is_edit': True if address_id else False,
        'address': controllers.get_party_contact(address_id) if address_id else None,
        'cities': controllers.get_cities(),
        'addresses': controllers.get_party_address(party)
    }
    if data:
        context.update(data)

    return render(request, 'profile.html', context)


@login_required
@decorators.has_customer_permission
def update_info(request):
    first_name = request.REQUEST.get('first_name')
    last_name = request.REQUEST.get('last_name')
    user = request.user
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    context = {
        'message': 'Updated successfully.'
    }

    return profile(request, context)


@login_required
@decorators.has_customer_permission
def add_address(request):
    party = request.user.profile
    address = request.REQUEST.get('address')
    pin_code = request.REQUEST.get('pin_code')

    region = request.REQUEST.get('region')
    region = models.City.objects.get(id=region)

    party_contact = controllers.create_party_contact_mech(
        party, 'ADDRESS', address, region, pin_code)

    return redirect('/profile/')


@login_required
@decorators.has_customer_permission
def update_address(request):
    address_id = request.REQUEST.get('address_id')
    address = request.REQUEST.get('address')
    region = request.REQUEST.get('region')
    pin_code = request.REQUEST.get('pin_code')

    city = models.City.objects.get(id=region)
    party_contact = controllers.update_party_contact_mech(
        address_id, address, region=city, pin_code=pin_code)

    return redirect('/profile/')


@login_required
@decorators.has_customer_permission
def delete_address(request):
    address_id = request.REQUEST.get('address_id')
    controllers.delete_party_contact(address_id)

    return redirect('/profile/')


@login_required
@decorators.has_customer_permission
def send_otp(request):
    party = request.user.profile
    party_contact = controllers.get_party_contacts(party, "MOBILE")
    controllers.send_verification_code(party_contact[0]['contact'])

    return JsonResponse({"message": "Otp sent on mobile."})


@login_required
@decorators.has_customer_permission
def update_mobile(request):
    party = request.user.profile
    mobile = request.REQUEST.get('mobile')
    update_mob = controllers.update_mobile(party, mobile)
    context = {
        'message': update_mob
    }

    return JsonResponse(context)


@login_required
@decorators.has_customer_permission
def subscription(request):
    party = request.user.profile
    email = request.user.email

    context = {
        'is_subscribed': controllers.is_subscribed(email),
        'email': email
    }

    return render(request, 'subscribe.html', context)


def subscribe(request):
    email = request.REQUEST.get('email')
    subscribe = controllers.subscribe_to_email(email)

    return redirect('/subscription/')


def unsubscribe(request):
    email = request.REQUEST.get('email')
    unsubscribe = controllers.unsubscribe_to_email(email)

    return redirect('/subscription/')


def faq(request):
    faqs = controllers.get_faq()
    return render(request, 'faq.html', {'faqs': faqs})


@decorators.has_customer_permission
def refer(request):
    return render(request, 'refer.html')


@login_required
@decorators.has_customer_permission
def refer_friend(request):
    email = request.REQUEST.get('email')
    mobile = request.REQUEST.get('mobile')
    if email or mobile:
        refer = controllers.refer_friend(request.user, email, mobile)
        return JsonResponse({'message': "Message sent to your friends."})

    return JsonResponse({'message': "Enter Mobile or Email address."})


@login_required
@decorators.has_customer_permission
def track_request(request):
    party = request.user.profile
    track_requests = controllers.track_requests(party)

    return render(request, 'track_request.html', {'req': track_requests})


@login_required
@decorators.has_customer_permission
def order_history(request):
    party = request.user.profile
    orders = controllers.get_all_orders(party)

    return render(request, 'order_history.html', {'orders': orders})



def get_party_detail(request):
    return JsonResponse(controllers.get_party_detail(get_user_login_id(request)))


def get_all_orders(request):
    return JsonResponse(controllers.get_all_orders(get_user_login_id(request)))


def get_user_login_id(request):
    return request.session['user_login_id']


def is_logged_in(request):
    return True if 'user_login_id' in request.session else False


# def login(request):
#     if request.method != 'POST':
#         raise Http404('Only POST are allowed')
#     try:
#         user_login = models.UserLogin.objects.get(user_login_id=request.POST['user_login_id'])
#         if user_login.password == request.POST['password'] or user_login.password == base64.b64encode(request.POST['password']):
#             request.session['user_login_id'] = user_login.user_login_id
#             return HttpResponse('Welcome ' + user_login.party.name + ' you are loggedIn.')
#         return HttpResponse("Password didn't match." + user_login.password)
#     except models.UserLogin.DoesNotExist:
#         return HttpResponse("Your username and password didn't match.")


# def logout(request):
#     try:
#         del request.session['user_login_id']
#     except KeyError:
#         pass
#     return HttpResponse("You're logged out.")


def send_sms(request):
    response = send_sms.send_text('9717930151', 'Hi message.')
    print response
    return response


def sms_report(request):
    receiver = request.POST.get('To')
    sender = request.POST.get('From')
    status = request.POST.get('Status')
    message_uuid = request.POST.get('MessageUUID')
    parent_message_uuid = request.POST.get('ParentMessageUUID')
    part_info = request.POST.get('PartInfo')

    controller.save_sms_report(
        receiver, sender, status, message_uuid, parent_message_uuid, part_info)

    return True


def verify_email(request):
    email = request.REQUEST.get('email')
    code = request.Request.get('code')
    verify = controllers.verify_user(email, 'EMAIL', code)

    return verify


def contact_us(request):
    name = request.REQUEST.get('name')
    email = request.REQUEST.get('email')
    sub = request.REQUEST.get('subject')
    msg = request.REQUEST.get('message')

    controllers.create_contact_us(name, email, sub, msg)

    return JsonResponse({'message': "Thanks for contacting us."})

