from django.shortcuts import render, get_object_or_404
from django.views import View
# from django.core.paginator import Paginator
# from django.contrib.auth import login, authenticate, logout
# from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError

# import hashlib
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Client
# from .smsc_api import SMSC

from django.utils.decorators import method_decorator
import json

# Create your views here.
class MainView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'my_app/index.html')

@method_decorator(csrf_exempt, name='dispatch')
class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        print('in sender')
        if request.method == 'POST':
            phone = request.POST.get('phone')
            secret_key = "секретная строка"  # секретный ключ для генерации кода
            
            if not phone:
                return JsonResponse({"success": False, "error": "Телефон не указан"}, status=400)
            
            # Генерация кода
            code = str(random.randint(100000, 999999))  # случайный 6-значный код
            
            # Сохранение кода и телефона в базе данных
            # client, created = Client.objects.get_or_create(phone=phone)
            client, created = Client.objects.get_or_create(id=request.session.get('current_num'))
            client.phone = phone
            client.code = code
            client.save()
            request.session['phone'] = phone
            
            # Отправка SMS через SMSC API
            # smsc = SMSC()
            
            try:
                print(code)
                # result = smsc.send_sms(phone, f"Ваш код подтверждения: {code}", sender="SMSC.kz")
                # response = int(result[1])
                if code:
                    return JsonResponse({"success": True})
                else:
                    return JsonResponse({"success": False, "error": 'error'}, status=500)
            except Exception as e:
                print(e)
                return JsonResponse({"success": False, "error": "Некорректный ответ от SMSC"}, status=500)

            

@method_decorator(csrf_exempt, name='dispatch')
class VerifyCodeView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            phone = request.POST.get('phone')
            code = request.POST.get('code')
            
            if not phone or not code:
                return JsonResponse({"success": False, "error": "Телефон или код не указаны"}, status=400)
            
            # Проверка кода в базе данных
            verification = Client.objects.filter(phone=phone, code=code).first()
            if verification:
                return JsonResponse({"success": True, "message": "Номер активирован"})
            else:
                return JsonResponse({"success": False, "error": "Неверный код"}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ClientView(View):
    def post(self, request, *args, **kwargs):
        print('in client')
        if request.method == 'POST':
            # Получаем данные из POST-запроса
            phone = request.session.get('phone')  # Предположим, что номер телефона был сохранен в сессии после первого шага
            last_name = request.POST.get('last_name')
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name')
            email = request.POST.get('email')
            inn = request.POST.get('inn')
            document_id = request.POST.get('document_id')
            print(phone, last_name, first_name, middle_name, email, inn, document_id)

            # Проверяем, что все данные заполнены
            if not all([last_name, first_name, middle_name, email, inn, document_id]):
                return JsonResponse({"success": False, "error": "Все поля должны быть заполнены."}, status=400)

            try:
                # Логика сохранения данных в базе
                client, created = Client.objects.update_or_create(
                    phone=phone,  # Используем номер телефона для поиска записи
                    defaults={
                        'last_name': last_name,          # Обновляем поле 'Фамилия'
                        'first_name': first_name,        # Обновляем поле 'Имя'
                        'middle_name': middle_name,      # Обновляем поле 'Отчество'
                        'email': email,                  # Обновляем поле 'Электронная почта'
                        'inn': inn,                      # Обновляем поле 'ИНН'
                        'identity_document': document_id, # Обновляем поле 'Удостоверение личности'
                        'phone_verified': True           # Устанавливаем флаг подтверждения телефона
                    }
                )


                # Если клиент создан или обновлен успешно
                return JsonResponse({"success": True, "message": "Данные успешно сохранены."})

            except Exception as e:
                # Обработка ошибки при сохранении данных
                return JsonResponse({"success": False, "error": f"Ошибка сохранения данных: {str(e)}"}, status=500)

        return JsonResponse({"success": False, "error": "Недопустимый метод запроса."}, status=405)

@method_decorator(csrf_exempt, name='dispatch')
class FirstFormView(View):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            amount = request.POST.get('amount', '').replace('\xa0', '').replace('₸', '').replace(' ', '').strip()
            term = request.POST.get('term')
            currency = request.POST.get('currency')
            time = request.POST.get('time')

            # Сохранение инфы из первой формы в базе данных
            client, created = Client.objects.get_or_create(amount=amount, term=term, time_unit=time, currency=currency)
            client.save()
            request.session['current_num'] = Client.objects.last().id
            print(request.session.get('current_num'))

            # Проверяем, что все данные заполнены
            if not all([amount, term, currency, time]):
                return JsonResponse({"success": False, "error": "Все поля должны быть заполнены."}, status=400)
            # Если клиент создан или обновлен успешно
            return JsonResponse({"success": True, "message": "Данные успешно сохранены."})