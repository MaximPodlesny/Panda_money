# from django.urls import path
# from .views import MainView

# urlpatterns = [
#     path('', MainView.as_view(), name='index'),
# ]

from django.urls import path
from .views import MainView, SendSmsView, VerifyCodeView, ClientView, FirstFormView

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('send_sms/', SendSmsView.as_view(), name='send_sms'),
    path('verify_code/', VerifyCodeView.as_view(), name='verify_code'),
    path('submit_client_data/', ClientView.as_view(), name='submit_client_data'),
    path('submit_first_form/', FirstFormView.as_view(), name='submit_first_form'),
]