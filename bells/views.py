from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BellSchedule
import uuid
from django.db.models import Min,Max

def bells_view(request):
    days = {
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'sunday': 'Воскресенье',
    }
    
    active_day = request.GET.get('day') or request.session.get('last_selected_day', 'monday')
    request.session['last_selected_day'] = active_day
    current_day = days.get(active_day, 'Понедельник')
    schedule = BellSchedule.objects.filter(day=active_day).order_by('order')
    
    # Получаем статистику по дням
    day_stats = {}
    for day in days:
        bells = BellSchedule.objects.filter(day=day)
        count = bells.count()
        if count > 0:
            first = bells.aggregate(Min('start_time'))['start_time__min']
            last = bells.aggregate(Max('end_time'))['end_time__max']
            day_stats[day] = {
                'count': count,
                'first': first.strftime('%H:%M'),
                'last': last.strftime('%H:%M')
            }
        else:
            day_stats[day] = {'count': 0, 'first': '', 'last': ''}
    
    return render(request, 'bells/index.html', {
        'days': days,
        'day_stats': day_stats,
        'active_day': active_day,
        'current_day_name': current_day,
        'schedule': schedule,
        'melodies': ['Звонок 1', 'Звонок 2', 'Звонок 3']
    })

@csrf_exempt
def save_bells(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        request.session['last_selected_day'] = day
        # Удаляем старые записи для этого дня
        BellSchedule.objects.filter(day=day).delete()
        
        # Получаем данные из формы
        bells_data = request.POST.getlist('bells[]')
        
        for i, bell_data in enumerate(bells_data):
            data = bell_data.split('|')
            BellSchedule.objects.create(
                id=uuid.uuid4(),
                day=day,
                start_time=data[0],
                end_time=data[1],
                melody=data[2],
                is_active=data[3] == 'true',
                order=i
            )
        
        return JsonResponse({
            'status': 'success',
            'redirect_url': f'/bells/?day={day}'
            })
    return JsonResponse({'status': 'error'})

@csrf_exempt
def delete_bell(request, bell_id):
    try:
        bell = BellSchedule.objects.get(id=bell_id)
        bell.delete()
        return JsonResponse({'status': 'success'})
    except BellSchedule.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Звонок не найден'})
    
def get_schedule(request):
    day = request.GET.get('day', 'monday')
    schedule = BellSchedule.objects.filter(day=day).order_by('order')
    
    data = {
        'day_name': 'Понедельник',
        'schedule': [
            {
                'id': str(bell.id),
                'start_time': bell.start_time.strftime('%H:%M'),
                'end_time': bell.end_time.strftime('%H:%M'),
                'melody': bell.melody,
                'is_active': bell.is_active,
                'order': bell.order
            }
            for bell in schedule
        ]
    }
    
    return JsonResponse(data)