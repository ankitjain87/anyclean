from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount

import datetime
import hashlib


class City(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='BANGALORE')
    name = models.CharField(max_length=80)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.id, self.name])


class Point(models.Model):
    lat = models.CharField(max_length=30)
    long = models.CharField(max_length=30)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.lat, self.long])


class Area(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='BTM')
    name = models.CharField(max_length=180)
    pincode = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey(City)
    point = models.ForeignKey(Point, blank=True, null=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.pincode, self.name, self.city.name])


class Party(models.Model):
    PARTY_TYPE = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
        ('DELIVERY_BOY', 'Delivery Boy'),
    )

    user = models.OneToOneField(User, related_name='profile')
    party_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    party_type = models.CharField(choices=PARTY_TYPE, max_length=55)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([str(self.party_id), self.name])

    def profile_image_url(self):
        """
        Return the URL for the user's Facebook icon if the user is logged in via Facebook,
        otherwise return the user's Gravatar URL
        """
        sa_uid = SocialAccount.objects.filter(user_id=self.user.id)

        if len(sa_uid):
            if sa_uid[0].provider == 'facebook':
                return "http://graph.facebook.com/{}/picture?width=160&height=160".format(sa_uid[0].uid)
            elif sa_uid[0].provider == 'google':
                data_obj = sa_uid[0].extra_data
                pic_url = data_obj['picture'] + '?sz=160'
                return pic_url

        return "http://www.gravatar.com/avatar/{}?s=160".format(
            hashlib.md5(self.user.email).hexdigest())

    def account_verified(self):
        """
        If the user is logged in and has verified hisser email address, return True,
        otherwise return False
        """
        result = EmailAddress.objects.filter(email=self.user.email)
        if len(result):
            return result[0].verified
        return False


User.profile = property(lambda u: Party.objects.get_or_create(user=u)[0])


class PartyContactMech(models.Model):
    CONTACT_TYPE = (
        ('EMAIL', 'Email'),
        ('MOBILE', 'Mobile'),
        ('ADDRESS', 'Address'),
        ('ZIPPR', 'Zippr')
    )

    party = models.ForeignKey(Party)
    contact_type = models.CharField(choices=CONTACT_TYPE, max_length=55)
    info_string = models.TextField()
    region = models.ForeignKey(City, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    from_date = models.DateTimeField(default=datetime.datetime.utcnow())
    thru_date = models.DateTimeField(null=True, blank=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([str(self.party.party_id), self.contact_type])


# class UserLogin(models.Model):
#     user_login_id = models.CharField(primary_key=True, max_length=80)
#     password = models.CharField(max_length=100)
#     is_enabled = models.BooleanField(default=True)
#     require_password_change = models.BooleanField(default=False)
#     party = models.ForeignKey(Party)
#     created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
#     last_updated_timestamp = models.DateTimeField(auto_now=True)

#     def __unicode__(self):
#         return "-".join([self.user_login_id, self.party.name])


class Product(models.Model):
    product_id = models.CharField(primary_key=True, max_length=25, default='PR1000')
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.product_id, self.name])


class ProductPrice(models.Model):
    PRICE_TYPE = (
        ('LAUNDRY', 'Laundry'),
        ('DRY_CLEAN', 'Dry Clean')
    )

    product = models.ForeignKey(Product)
    price_type = models.CharField(choices=PRICE_TYPE, max_length=10)
    price = models.IntegerField()
    city = models.ForeignKey(City)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.city.name, self.product.product_id, self.price_type, str(self.price)])


class LaundryDetail(models.Model):
    laundry_id = models.CharField(primary_key=True, max_length=25, default='LY0001')
    name = models.CharField(max_length=80)
    contact_info = models.CharField(max_length=30)
    address = models.TextField()
    zippr_address = models.CharField(max_length=25, blank=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.laundry_id, self.name])


# class LaundryPricing(models.Model):
#     PRICING_TYPE = (
#         ('PER_CLOTH', 'Per Cloth'),
#         ('PER_PAIR', 'Per Pair'),
#         ('PER_KG', 'Per KG'))
#     laundry = models.ForeignKey(LaundryDetail)




# # Need to discuss how we can store it in proper way.
# class LaundryPricing(models.Model):
#     PRICING_TYPE = (
#         ('PER_CLOTH', 'Per Cloth'),
#         ('PER_PAIR', 'Per Pair'),
#         ('PER_KG', 'Per KG'))
#     laundry = models.ForeignKey(LaundryDetail)


class TimeSlot(models.Model):
    from_time = models.CharField(max_length=15)
    to_time = models.CharField(max_length=15)
    city = models.ForeignKey(City)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.city.name, self.from_time, self.to_time])


class PickupRequest(models.Model):
    REQUEST_TYPE = (
        ('CALL', 'Call'),
        ('ONLINE', 'Online'),
    )

    pickup_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Party)
    date = models.DateTimeField()
    time_slot = models.ForeignKey(TimeSlot)
    request_type = models.CharField(choices=REQUEST_TYPE, max_length=25)
    party_contact = models.ForeignKey(PartyContactMech)
    is_assigned = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([str(self.pickup_id), self.customer.name])


class PickupAssignment(models.Model):
    STATUS = (
        ('ASSIGNED', 'Assigned'),
        ('ACCEPTED', 'Acepted'),
        ('PICKED', 'Picked'),
        ('INWASH', 'In Wash'),
        ('CANCELLED', 'Cancelled'),
    )
    pickup = models.OneToOneField(PickupRequest)
    assigned_to = models.ForeignKey(Party)
    assigned_date = models.DateTimeField()
    nearest_laundry = models.ForeignKey(LaundryDetail)
    status = models.CharField(choices=STATUS, max_length=25)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([str(self.pickup.pickup_id), self.assigned_to.name])


class OrderHeader(models.Model):
    ORDER_TYPE = (
        ('LAUNDRY', 'Laundry'),
        ('DRY_CLEAN', 'Dry Clean'),
    )
    ORDER_STATUS = (
        ('PICKED', 'Picked'),
        ('IN_WASH', 'In wash'),
        ('DELIVERED', 'Delivered'),
    )
    PAYMENT_TYPE = (
        ('COD', 'Cash On Delivery'),
        ('WALLET', 'Wallet'),
        ('CREDIT_CARD', 'Credit Card'),
    )

    order_id = models.CharField(primary_key=True, max_length=25, default='AC0001')
    order_type = models.CharField(choices=ORDER_TYPE, max_length=30)
    order_date = models.DateTimeField(default=datetime.datetime.utcnow())
    order_status = models.CharField(choices=ORDER_STATUS, max_length=30)
    quantity = models.IntegerField()
    discount = models.DecimalField(max_digits=18, decimal_places=3, default=0)
    weight = models.DecimalField(max_digits=18, decimal_places=3)
    grand_total = models.DecimalField(max_digits=18, decimal_places=2)
    laundry = models.ForeignKey(LaundryDetail, blank=True)
    payment_menthod = models.CharField(choices=PAYMENT_TYPE, max_length=30, default="COD")
    estimated_delivery_date = models.DateTimeField()
    party = models.ForeignKey(Party)
    bill_no = models.CharField(max_length=80, blank=True)
    pickup = models.ForeignKey(PickupRequest)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.order_id, self.order_status])


class OrderItem(models.Model):
    order = models.ForeignKey(OrderHeader)
    order_item_seq_id = models.IntegerField()
    product = models.ForeignKey(Product)
    quantity = models.IntegerField()
    product_name = models.CharField(max_length=80)
    created_date = models.DateTimeField()
    list_price = models.IntegerField()
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '-'.join([self.order_id, self.product_id])


class Visit(models.Model):
    url = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=30)
    is_logged_in = models.BooleanField(default=False)
    party_id = models.CharField(max_length=25)
    timestamp = models.DateTimeField(auto_now=True)


class SMS_Report(models.Model):
    receiver = models.CharField(max_length=30)
    sender = models.CharField(max_length=30)
    status = models.CharField(max_length=80)
    message_uuid = models.CharField(max_length=80)
    parent_message_uuid = models.CharField(max_length=80)
    part_info = models.CharField(max_length=50)
    created_timestamp = models.DateTimeField(auto_now=True)


class Verifcation_Code(models.Model):
    VER_TYPE = (
        ('MOBILE', 'Mobile'),
        ('EMAIL', 'Email'),
    )
    to = models.CharField(max_length=30)
    ver_type = models.CharField(choices=VER_TYPE, max_length=10)
    code = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class Mail_Communication(models.Model):
    to = models.TextField()
    subject = models.CharField(max_length=256)
    message = models.TextField()
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class Laundry_Rating(models.Model):
    laundry = models.ForeignKey(LaundryDetail)
    customer = models.ForeignKey(Party)
    rating = models.IntegerField()
    comment = models.TextField()
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class Contact_Us(models.Model):
    name = models.CharField(max_length=60, default="")
    email = models.CharField(max_length=60)
    subject = models.CharField(max_length=80)
    message = models.TextField()
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class Subscribe_To_Email(models.Model):
    email = models.CharField(max_length=60, unique=True)
    is_subscribed = models.BooleanField(default=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class ReferFriend(models.Model):
    contacts = models.TextField()
    referer = models.ForeignKey(User)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


class FAQ(models.Model):
    title = models.CharField(max_length=255)
    ques = models.TextField()
    ans = models.TextField()
    show = models.BooleanField(default=True)
    created_timestamp = models.DateTimeField(default=datetime.datetime.utcnow())
    last_updated_timestamp = models.DateTimeField(auto_now=True)


