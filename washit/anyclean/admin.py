from django.contrib import admin
from models import (Area, City, Party, Product, ProductPrice, LaundryDetail,
    TimeSlot, PartyContactMech, SMS_Report, Mail_Communication, OrderHeader,
    OrderItem, PickupRequest, PickupAssignment, Visit, Verifcation_Code,
    Laundry_Rating, Point, Contact_Us, Subscribe_To_Email, ReferFriend, FAQ
)

# Register your models here.

admin.site.register(Area)
admin.site.register(City)
admin.site.register(Party)
admin.site.register(Point)
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(LaundryDetail)
admin.site.register(Laundry_Rating)
admin.site.register(Mail_Communication)
admin.site.register(OrderHeader)
admin.site.register(OrderItem)
admin.site.register(PartyContactMech)
admin.site.register(PickupRequest)
admin.site.register(PickupAssignment)
admin.site.register(SMS_Report)
admin.site.register(TimeSlot)
admin.site.register(Verifcation_Code)
admin.site.register(Visit)
admin.site.register(Contact_Us)
admin.site.register(Subscribe_To_Email)
admin.site.register(ReferFriend)
admin.site.register(FAQ)
