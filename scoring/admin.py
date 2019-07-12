from django.contrib import admin
from .models import Category, CategoryClass, Skater, Competitor, Event, Placement, Choice, ClassAssignmentForEvent, Entry, EventUserScore
from django.contrib.auth.models import User
from django.core import management
from django.shortcuts import redirect
from datetime import timedelta
from django.utils import timezone


# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryClass)
admin.site.register(Skater)
admin.site.register(Competitor)
admin.site.register(Event)
admin.site.register(Entry)
admin.site.register(Choice)
admin.site.register(ClassAssignmentForEvent)
admin.site.register(EventUserScore)


EVENT = 'GP Helsinki'


def assign_class(event, entries):
    competitors = []
    for entry in entries:
        competitors.append(entry.competitor)
    competitors.sort(key=lambda x: x.world_standing, reverse=False)
    A = CategoryClass.objects.filter(name='A').first()
    B = CategoryClass.objects.filter(name='B').first()
    C = CategoryClass.objects.filter(name='C').first()
    print("Assign class")
    print(event.__str__())
    print(competitors.__str__())
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


def update_user_scores(event):
    users = User.objects.all()
    for user in users:
        if not EventUserScore.objects.filter(user=user, event=event).exists():
            user_choices = Choice.objects.filter(user=user, event=event)
            user_sum = 0
            for choice in user_choices:
                competitor = choice.competitor
                event = choice.event
                placement_model = Placement.objects.filter(competitor=competitor, event=event).first()
                if placement_model is not None:
                    user_sum += placement_model.total_score
                    if placement_model.placement < 4:
                        user_sum += 15 - 5 * (placement_model.placement - 1)
            EventUserScore.objects.create(user=user, event=event, score=user_sum)


class PlacementAdmin(admin.ModelAdmin):
    @admin.site.register_view('get-results', 'Get newest results')
    def get_results(request):
        now = timezone.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-results-men', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-results-ladies', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-results-pairs', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-results-icedance', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
                update_user_scores(last_event)
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-entries', 'Get next event entries')
    def get_entries(request):
        now = timezone.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            last_event = events[0]
            last_event = Event.objects.get(short_name=EVENT)
            try:
                management.call_command('get-entries-men', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-entries-ladies', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-entries-pairs', url=last_event.event_url, event_name=last_event.name)
                management.call_command('get-entries-icedance', url=last_event.event_url, event_name=last_event.name)
                message = 'successfully imported data from URL'
            except Exception as ex:
                message = 'Error importing from data from URL {}'.format(str(ex))
            print(message)
            entries = Entry.objects.filter(event=last_event)
            assign_class(last_event, entries)
        else:
            print('no upcoming events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-all-results', 'Get all results')
    def get_all_results(request):
        now = timezone.now()
        events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
        if len(events) > 0:
            for last_event in events:
                try:
                    management.call_command('get-results-men', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-results-ladies', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-results-pairs', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-results-icedance', url=last_event.event_url, event_name=last_event.name)
                    message = 'successfully imported data from URL'
                    update_user_scores(last_event)
                except Exception as ex:
                    message = 'Error importing from data from URL {}'.format(str(ex))
                print(message)
        else:
            print('no finished events this season')
        return redirect('admin:index')

    @admin.site.register_view('get-all-entries', 'Get all entries')
    def get_all_entries(request):
        now = timezone.now()
        now = now - timedelta(days=365)
        events = Event.objects.filter(start_date__gte=now).order_by('start_date')
        if len(events) > 0:
            for last_event in events:
                try:
                    management.call_command('get-entries-men', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-entries-ladies', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-entries-pairs', url=last_event.event_url, event_name=last_event.name)
                    management.call_command('get-entries-icedance', url=last_event.event_url, event_name=last_event.name)
                    message = 'successfully imported data from URL'
                except Exception as ex:
                    message = 'Error importing from data from URL {}'.format(str(ex))
                print(message)
                entries = Entry.objects.filter(event=last_event)
                assign_class(last_event, entries)
        else:
            print('no events this season')
        return redirect('admin:index')


admin.site.register(Placement, PlacementAdmin)
