from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Q
from .forms import RegistrationForm, ChangeTeamForm, ChoiceForm
from .models import Competitor, Placement, ClassAssignmentForEvent, CategoryClass, Event, Category, Choice, EventUserScore, FakeDate
from django.db.models import Sum
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
from operator import itemgetter
from itertools import groupby
from datetime import timedelta
import logging
logger = logging.getLogger(__name__)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'register_form.html', {'form': form})


def view_404(request):
    return redirect('/')


@login_required
def ranking_last(request, page):
    return ranking(request, page)


@login_required
def ranking_overall(request, page):
    return ranking(request, page, is_overall=True)


@login_required
def ranking_last_me(request):
    return ranking(request, is_me=True)


@login_required
def ranking_overall_me(request):
    return ranking(request, is_overall=True, is_me=True)


@login_required
def ranking(request, page=1, is_overall=False, is_me=False):
    number_per_page = 5
    current_user = request.user
    users = User.objects.all()
    user_scores = []
    event_name = None
    for user in users:
        if is_overall:
            user_sum = EventUserScore.objects.filter(user=user).aggregate(Sum('score'))['score__sum']
            if user_sum is None:
                user_sum = 0.0
        else:
            now = timezone.now()
            if FakeDate.objects.all().exists():
                now = FakeDate.objects.all().first().date
            ########################################################################DATES
            events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
            if len(events) > 0:
                user_sum = EventUserScore.objects.filter(user=user, event=events[0]).aggregate(Sum('score'))['score__sum']
                event_name = events[0].name
                if user_sum is None:
                    user_sum = 0.0
            else:
                user_sum = 0.0
        user_scores.append((user, user_sum))
    user_scores.sort(key=itemgetter(1), reverse=True)
    user_scores_enumerated = []
    for rank, (_, grp) in enumerate(groupby(user_scores, key=lambda xs: xs[1]), 1):
        for x in grp:
            user_scores_enumerated.append(x + (rank,))
    if is_me:
        user_page_num = 1
        for num, (user, score) in enumerate(user_scores):
            if user == current_user:
                user_num = num
                user_page_num = int(user_num / number_per_page) + 1
        paginated_users = Paginator(user_scores_enumerated, number_per_page).page(user_page_num)
        user_scores_enumerated = paginated_users
    else:
        paginated_users = Paginator(user_scores_enumerated, number_per_page).page(page)
        user_scores_enumerated = paginated_users
    return render(request, 'ranking.html', {'current_user': current_user, 'user_scores': user_scores_enumerated,
                                            'paginated_users': paginated_users, 'event_name': event_name})


@login_required
def ranking_last_ineffective(request, page):
    return ranking_ineffective(request, page, is_overall=False)


@login_required
def ranking_overall_ineffective(request, page):
    return ranking_ineffective(request, page, is_overall=True)


@login_required
def ranking_ineffective(request, page, is_overall):
    number_per_page = 5
    current_user = request.user
    users = User.objects.all()
    user_scores = []
    for user in users:
        if is_overall:
            user_choices = Choice.objects.filter(user=user)
        else:
            now = timezone.now()
            if FakeDate.objects.all().exists():
                now = FakeDate.objects.all().first().date
            events = Event.objects.filter(end_date__lte=now).order_by('-end_date')
            if len(events) > 0:
                user_choices = Choice.objects.filter(user=user, event=events[0])
            else:
                user_choices = Choice.objects.none()
        user_sum = 0
        for choice in user_choices:
            competitor = choice.competitor
            event = choice.event
            placement_model = Placement.objects.filter(competitor=competitor, event=event).first()
            if placement_model is not None:
                user_sum += placement_model.total_score
                if placement_model.placement < 4:
                    user_sum += 15 - 5 * (placement_model.placement - 1)
        user_scores.append((user, user_sum))
    user_scores.sort(key=itemgetter(1), reverse=True)
    user_scores_enumerated = []
    for num, user_score in enumerate(user_scores, start=1+number_per_page*(page-1)):
        user_scores_enumerated.append(user_score + (num,))
    paginated_users = Paginator(user_scores_enumerated, number_per_page).page(page)
    user_scores_enumerated = paginated_users
    return render(request, 'ranking.html', {'current_user': current_user, 'user_scores': user_scores_enumerated, 'paginated_users': paginated_users})


@login_required
def user_page(request):
    current_user = request.user
    total_score = 0
    user_choices = Choice.objects.filter(user=current_user)
    for choice in user_choices:
        competitor = choice.competitor
        event = choice.event
        placement_model = Placement.objects.filter(competitor=competitor, event=event).first()
        if placement_model is not None:
            total_score += placement_model.total_score
            if placement_model.placement < 4:
                total_score += 15 - 5 * (placement_model.placement - 1)
    if request.method == 'POST':
        form = ChangeTeamForm(request.POST)
        if form.is_valid():
            color = form.save()
            team = form.cleaned_data.get('team')
            return render(request, 'user_page.html', {'user': current_user, 'name_changed': 1,
                                                      'total_score': total_score, 'color': color, 'team': team})
    return render(request, 'user_page.html', {'user': current_user, 'name_changed': 0, 'total_score': total_score})


def get_class_assignments(event, category_class, category):
    return ClassAssignmentForEvent.objects.filter(event__name=event,
                                                  category_class__name=category_class,
                                                  competitor__skater_1__category__name=category)


def save_choice(user, competitor_id, event, category, category_class):
    competitor = Competitor.objects.get(id=competitor_id)
    if Choice.objects.filter(user=user, event=event, category=category, category_class=category_class).exists():
        choice = Choice.objects.filter(user=user, event=event, category=category, category_class=category_class).first()
        choice.competitor = competitor
        choice.save()
    else:
        choice = Choice.objects.create(user=user, competitor=competitor, event=event, category=category,
                                       category_class=category_class)
    print(choice.__str__())
    return


def save_choices(user, form, event):
    ladies = Category.objects.get(name='Ladies')
    men = Category.objects.get(name='Men')
    pairs = Category.objects.get(name='Pairs')
    dance = Category.objects.get(name='Ice Dance')
    A = CategoryClass.objects.get(name='A')
    B = CategoryClass.objects.get(name='B')
    C = CategoryClass.objects.get(name='C')
    save_choice(user, form.cleaned_data.get('LadiesA'), event, ladies, A)
    save_choice(user, form.cleaned_data.get('LadiesB'), event, ladies, B)
    save_choice(user, form.cleaned_data.get('LadiesC'), event, ladies, C)
    save_choice(user, form.cleaned_data.get('MenA'), event, men, A)
    save_choice(user, form.cleaned_data.get('MenB'), event, men, B)
    save_choice(user, form.cleaned_data.get('MenC'), event, men, C)
    save_choice(user, form.cleaned_data.get('PairsA'), event, pairs, A)
    save_choice(user, form.cleaned_data.get('PairsB'), event, pairs, B)
    save_choice(user, form.cleaned_data.get('PairsC'), event, pairs, C)
    save_choice(user, form.cleaned_data.get('DanceA'), event, dance, A)
    save_choice(user, form.cleaned_data.get('DanceB'), event, dance, B)
    save_choice(user, form.cleaned_data.get('DanceC'), event, dance, C)
    return


@login_required
def choice_form_next(request):
    current_user = request.user
    now = timezone.now()
    if FakeDate.objects.all().exists():
        now = FakeDate.objects.all().first().date
    events = Event.objects.filter(end_date__gte=now).order_by('start_date')
    if events.__len__() > 0:
        event = events[0]
        event_name = event.name
        events = Event.objects.all().order_by('start_date')
        LA = get_class_assignments(event_name, 'A', 'Ladies')
        LB = get_class_assignments(event_name, 'B', 'Ladies')
        LC = get_class_assignments(event_name, 'C', 'Ladies')
        MA = get_class_assignments(event_name, 'A', 'Men')
        MB = get_class_assignments(event_name, 'B', 'Men')
        MC = get_class_assignments(event_name, 'C', 'Men')
        PA = get_class_assignments(event_name, 'A', 'Pairs')
        PB = get_class_assignments(event_name, 'B', 'Pairs')
        PC = get_class_assignments(event_name, 'C', 'Pairs')
        DA = get_class_assignments(event_name, 'A', 'Ice Dance')
        DB = get_class_assignments(event_name, 'B', 'Ice Dance')
        DC = get_class_assignments(event_name, 'C', 'Ice Dance')
        choices = Choice.objects.filter(user=current_user, event=event)
        is_disabled = False
        if now > event.start_date:
            is_disabled = True
        if request.method == 'POST':
            form = ChoiceForm(LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, choices, is_disabled, request.POST)
            if form.is_valid():
                form.save()
                save_choices(current_user, form, event)
                return render(request, 'choice_form.html', {'user': current_user, 'form': form, 'events': events, 'next_event_name': event_name})
        else:
            form = ChoiceForm(LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, choices, is_disabled)
        return render(request, 'choice_form.html', {'user': current_user, 'form': form, 'events': events, 'next_event_name': event_name})
    return render(request, 'choice_form.html')


@login_required
def choice_form(request, event_path):
    current_user = request.user
    event = Event.objects.filter(Q(event_url__contains=event_path))[0]
    LA = get_class_assignments(event, 'A', 'Ladies')
    LB = get_class_assignments(event, 'B', 'Ladies')
    LC = get_class_assignments(event, 'C', 'Ladies')
    MA = get_class_assignments(event, 'A', 'Men')
    MB = get_class_assignments(event, 'B', 'Men')
    MC = get_class_assignments(event, 'C', 'Men')
    PA = get_class_assignments(event, 'A', 'Pairs')
    PB = get_class_assignments(event, 'B', 'Pairs')
    PC = get_class_assignments(event, 'C', 'Pairs')
    DA = get_class_assignments(event, 'A', 'Ice Dance')
    DB = get_class_assignments(event, 'B', 'Ice Dance')
    DC = get_class_assignments(event, 'C', 'Ice Dance')
    now = timezone.now()
    if FakeDate.objects.all().exists():
        now = FakeDate.objects.all().first().date
    events = Event.objects.all().order_by('start_date')
    choices = Choice.objects.filter(user=current_user, event=event)
    is_disabled = False
    if now > event.start_date:
        is_disabled = True
    if request.method == 'POST':
        form = ChoiceForm(LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, choices, is_disabled, request.POST)
        if form.is_valid():
            form.save()
            save_choices(current_user, form, event)
            return render(request, 'choice_form.html', {'user': current_user, 'form': form, 'events': events})
    else:
        form = ChoiceForm(LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, choices, is_disabled)
    return render(request, 'choice_form.html', {'user': current_user, 'form': form, 'events': events})

