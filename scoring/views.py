from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.db.models import Q
from .forms import RegistrationForm, ChangeTeamForm, ChoiceForm
from .models import Competitor, Placement, ClassAssignmentForEvent, CategoryClass, Event, Category, Choice
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from datetime import timedelta
# Create your views here.
import logging
logger = logging.getLogger(__name__)


class ChoicesList(ListView):
    model = CategoryClass
    context_object_name = 'classes'
    selected_tab = ''
    template_name = 'index_content.html'

    def get_context_data(self, **kwargs):
        context = super(ChoicesList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return CategoryClass.objects.all()


def ranking(request):
    return render(request, 'ranking.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('index'))
    else:
        form = RegistrationForm()
    return render(request, 'register_form.html', {'form': form})


def user_page(request):
    current_user = request.user
    logger.error('user_page')
    if request.method == 'POST':
        form = ChangeTeamForm(request.POST)
        logger.error('post')
        if form.is_valid():
            logger.error('valid')
            form.save()
            team = form.cleaned_data.get('team')
            logger.error(team)
            return render(request, 'user_page.html', {'user': current_user, 'name_changed': 1})
    return render(request, 'user_page.html', {'user': current_user, 'name_changed': 0})


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
    # 255 days -> skate america, 245 -> skate canada, 238 -> gp helsinki, 230 -> nhk trophy
    last_year = now - timedelta(days=245)
    event = Event.objects.filter(start_date__gte=last_year).order_by('start_date')[0]
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
    now = last_year
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


@login_required
def choice_form(request, event_path):
    current_user = request.user
    print(event_path)
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
    last_year = now - timedelta(days=245)
    events = Event.objects.all().order_by('start_date')
    choices = Choice.objects.filter(user=current_user, event=event)
    is_disabled = False
    now = last_year
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

