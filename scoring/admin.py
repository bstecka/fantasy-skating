from django.contrib import admin
from .models import Category, CategoryClass, Skater, Competitor, Event, Placement, Choice, ClassAssignmentForEvent, Entry
from django.core import management
from django.shortcuts import redirect
import datetime
from datetime import timedelta

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryClass)
admin.site.register(Skater)
admin.site.register(Competitor)
admin.site.register(Event)
admin.site.register(Entry)
admin.site.register(Choice)
admin.site.register(ClassAssignmentForEvent)


EVENT = 'NHK Trophy'


def assign_class(event, entries):
    competitors = []
    for entry in entries:
        competitors.append(entry.competitor)
    competitors.sort(key=lambda x: x.world_standing, reverse=False)
    A = CategoryClass.objects.filter(name='A').first()
    B = CategoryClass.objects.filter(name='B').first()
    C = CategoryClass.objects.filter(name='C').first()
    print(event.__str__())
    print(competitors.__str__())
    for index, competitor in enumerate(competitors):
        if ClassAssignmentForEvent.objects.filter(event=event, competitor=competitor).exists():
            continue
        else:
            if index < (len(competitors) / 3) - 1:
                assignment = ClassAssignmentForEvent.objects.create(event=event, competitor=competitor, category_class=A)
            elif index < (len(competitors) * 2 / 3) - 1:
                assignment = ClassAssignmentForEvent.objects.create(event=event, competitor=competitor, category_class=B)
            else:
                assignment = ClassAssignmentForEvent.objects.create(event=event, competitor=competitor, category_class=C)
            print(assignment.__str__())


class PlacementAdmin(admin.ModelAdmin):
    @admin.site.register_view('get-results-men', 'Get newest results - Men')
    def get_results_men(request):
        now = datetime.datetime.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            last_event = events[0]
            try:
                management.call_command('get-results-men', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-results-ladies', 'Get newest results - Ladies')
    def get_results_ladies(request):
        now = datetime.datetime.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            last_event = events[0]
            try:
                management.call_command('get-results-ladies', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-results-pairs', 'Get newest results - Pairs')
    def get_results_pairs(request):
        now = datetime.datetime.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            last_event = events[0]
            try:
                management.call_command('get-results-pairs', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-results-icedance', 'Get newest results - Ice Dance')
    def get_results_icedance(request):
        now = datetime.datetime.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            last_event = events[0]
            try:
                management.call_command('get-results-icedance', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-entries-men', 'Get next event entries - Men')
    def get_entries_men(request):
        now = datetime.datetime.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-entries-men', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
            entries = Entry.objects.filter(competitor__skater_1__category__name='Men', event=last_event)
            assign_class(last_event, entries)
        else:
            print('no upcoming events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-entries-ladies', 'Get next event entries - Ladies')
    def get_entries_ladies(request):
        now = datetime.datetime.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-entries-ladies', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
            entries = Entry.objects.filter(competitor__skater_1__category__name='Ladies', event=last_event)
            assign_class(last_event, entries)
        else:
            print('no upcoming events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-entries-pairs', 'Get next event entries - Pairs')
    def get_entries_pairs(request):
        now = datetime.datetime.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-entries-pairs', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
            entries = Entry.objects.filter(competitor__skater_1__category__name='Pairs', event=last_event)
            assign_class(last_event, entries)
        else:
            print('no upcoming events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-entries-icedance', 'Get next event entries - Ice Dance')
    def get_entries_icedance(request):
        now = datetime.datetime.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-entries-icedance', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
            entries = Entry.objects.filter(competitor__skater_1__category__name='Ice Dance', event=last_event)
            assign_class(last_event, entries)
        else:
            print('no upcoming events this season')
        return redirect('admin:index')


admin.site.register(Placement, PlacementAdmin)
