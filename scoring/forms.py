from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Competitor, ClassAssignmentForEvent


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

    def save(self):
        user = User.objects.get(username=self.data['username'])
        user.first_name = self.data['team']
        user.save()
        return


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

    def set_field(self, field_name, query_set):
        competitors = []
        for index, assignment in enumerate(query_set):
            competitors.append((assignment.competitor, assignment.competitor))
        self.fields[field_name].choices = competitors

    def __init__(self, LA, LB, LC, MA, MB, MC, PA, PB, PC, DA, DB, DC, *args, **kwargs):
        super(ChoiceForm, self).__init__(*args, **kwargs)
        self.set_field('LadiesA', LA)
        self.set_field('LadiesB', LB)
        self.set_field('LadiesC', LC)
        self.set_field('MenA', MA)
        self.set_field('MenB', MB)
        self.set_field('MenC', MC)
        self.set_field('PairsA', PA)
        self.set_field('PairsB', PB)
        self.set_field('PairsC', PC)
        self.set_field('DanceA', DA)
        self.set_field('DanceB', DB)
        self.set_field('DanceC', DC)

    def save(self):
        return
