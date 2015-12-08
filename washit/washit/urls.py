from django.conf.urls import patterns, include, url
from django.contrib import admin

from anyclean import views, cc_views, m_views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'washit.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^accounts/', include('allauth.urls')),
    (r'', include('tokenapi.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^enterName/$', views.enter_name, name='enter_name'),
    url(r'^addAddress/', views.add_address, name='add_address'),
    url(r'^contactUs/', views.contact_us, name='contact_us'),
    url(r'^createPickup/', views.create_pickup_request, name='create_pickup'),
    url(r'^dashboard/', views.dashboard, name='dashboard'),
    url(r'^dashboard_redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    url(r'^deleteAddress/', views.delete_address, name='delete_address'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^getOrders/', views.get_all_orders, name='get_orders'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.log_out, name='logout'),
    url(r'^loginPage/', views.loginPage, name='login_page'),
    url(r'^orderHistory/', views.order_history, name='order_history'),
    url(r'^partyDetail/', views.get_party_detail, name='party_detail'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^refer/', views.refer, name='refer'),
    url(r'^referFriend/', views.refer_friend, name='refer_friend'),
    url(r'^register/', views.register, name='register'),
    # url(r'^registerUser/', views.add_customer),
    url(r'^requestPickup/', views.request_pickup, name='request_pickup'),
    url(r'^sendOTP/', views.send_otp),
    url(r'^smsReport/', views.sms_report, name='sms_report'),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^subscription/', views.subscription, name='subscription'),
    url(r'^trackRequest/', views.track_request, name='track_request'),
    url(r'^unsubscribe/', views.unsubscribe, name='unsubscribe'),
    url(r'^updateAddress/', views.update_address, name='update_address'),
    url(r'^updateInfo/', views.update_info, name='update_info'),
    url(r'^updateMobile/', views.update_mobile, name='update_mobile'),
    # url(r'^updatePassword/', views.update_password, name='update_password'),
    url(r'^verification/', views.verification, name='verification'),
    url(r'^verifyEmail/', views.verify_email, name='verify_email'),



    # CC App urls........
    url(r'^ccDashboard/', cc_views.dashboard, name='cc_dashboard'),
    url(r'^ccSearchPage/', cc_views.search_page, name='cc_search_page'),
    url(r'^ccAssignPickup/', cc_views.assign_pickup, name='cc_assign_pickup'),


    url(r'^zohoverify/verifyforzoho.html/', cc_views.zohoverify, name='zohoverify'),



# All mobile urls go here, and starts with 'm'

    # url(r'^mRegister/', views.mRegister),

    url(r'^mGet_Pickups/', m_views.mGet_Pickups, name='mGet_Pickups'),





)
