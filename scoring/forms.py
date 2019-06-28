from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from colorful.fields import RGBColorField


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=64, required=True, label="Team name",
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=30, required=True, label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=30, required=True,
                                label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2',)


class ChangeTeamForm(forms.Form):
    team = forms.CharField(label='team')
    username = forms.CharField(label='username')
    color = RGBColorField()

    def save(self):
        user = User.objects.get(username=self.data['username'])
        user.first_name = self.data['team']
        user.last_name = self.data['color']
        user.save()
        return self.data['color']


class ChoiceForm(forms.Form):
    LadiesA = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Ladies A")
    LadiesB = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Ladies B")
    LadiesC = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Ladies C")
    MenA = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Men A")
    MenB = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Men B")
    MenC = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Men C")
    PairsA = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Pairs A")
    PairsB = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Pairs B")
    PairsC = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Pairs C")
    DanceA = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Dance A")
    DanceB = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Dance B")
    DanceC = forms.ChoiceField(required=True, widget=forms.RadioSelect, label="Dance C")

    def set_field(self, field_name, query_set, choices, is_disabled):
        competitors = []
        for index, assignment in enumerate(query_set):
            competitors.append((assignment.competitor.id, assignment.competitor))
        self.fields[field_name].choices = competitors
        if choices.first() is not None:
            choice = choices.first().competitor
            self.fields[field_name].initial = (choice.id, choice)
        if is_disabled:
            self.fields[field_name].disabled = True

    def __init__(self, LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, choices, is_disabled, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        if choices.first() is not None:
            self.set_field('LadiesA', LA, choices.filter(category__name='Ladies', category_class__name='A'), is_disabled)
            self.set_field('LadiesB', LB, choices.filter(category__name='Ladies', category_class__name='B'), is_disabled)
            self.set_field('LadiesC', LC, choices.filter(category__name='Ladies', category_class__name='C'), is_disabled)
            self.set_field('MenA', MA, choices.filter(category__name='Men', category_class__name='A'), is_disabled)
            self.set_field('MenB', MB, choices.filter(category__name='Men', category_class__name='B'), is_disabled)
            self.set_field('MenC', MC, choices.filter(category__name='Men', category_class__name='C'), is_disabled)
            self.set_field('PairsA', PA, choices.filter(category__name='Pairs', category_class__name='A'), is_disabled)
            self.set_field('PairsB', PB, choices.filter(category__name='Pairs', category_class__name='B'), is_disabled)
            self.set_field('PairsC', PC, choices.filter(category__name='Pairs', category_class__name='C'), is_disabled)
            self.set_field('DanceA', DA, choices.filter(category__name='Ice Dance', category_class__name='A'), is_disabled)
            self.set_field('DanceB', DB, choices.filter(category__name='Ice Dance', category_class__name='B'), is_disabled)
            self.set_field('DanceC', DC, choices.filter(category__name='Ice Dance', category_class__name='C'), is_disabled)
        else:
            self.set_field('LadiesA', LA, choices, is_disabled)
            self.set_field('LadiesB', LB, choices, is_disabled)
            self.set_field('LadiesC', LC, choices, is_disabled)
            self.set_field('MenA', MA, choices, is_disabled)
            self.set_field('MenB', MB, choices, is_disabled)
            self.set_field('MenC', MC, choices, is_disabled)
            self.set_field('PairsA', PA, choices, is_disabled)
            self.set_field('PairsB', PB, choices, is_disabled)
            self.set_field('PairsC', PC, choices, is_disabled)
            self.set_field('DanceA', DA, choices, is_disabled)
            self.set_field('DanceB', DB, choices, is_disabled)
            self.set_field('DanceC', DC, choices, is_disabled)

    def save(self):
        return
