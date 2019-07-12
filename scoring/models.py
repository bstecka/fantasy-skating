from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import pathlib


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=64, default='Unknown')

    def __str__(self):
        return self.name.__str__()


@python_2_unicode_compatible
class CategoryClass(models.Model):
    name = models.CharField(max_length=1, default='X')

    def __str__(self):
        return self.name.__str__()


@python_2_unicode_compatible
class Skater(models.Model):
    name = models.CharField(max_length=64, default='')
    surname = models.CharField(max_length=64, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name.__str__() + ' ' + self.surname.__str__()


@python_2_unicode_compatible
class Competitor(models.Model):
    skater_1 = models.ForeignKey(Skater, on_delete=models.CASCADE, related_name="skater_1", null=True)
    skater_2 = models.ForeignKey(Skater, on_delete=models.CASCADE, related_name="skater_2", null=True)
    world_standing = models.IntegerField(blank=True, default=1000, null=True)
    full_name = models.CharField(max_length=64, default='')

    def __str__(self):
        if self.skater_1 == self.skater_2:
            return self.skater_1.__str__()
        return self.skater_1.__str__() + ' / ' + self.skater_2.__str__()


@python_2_unicode_compatible
class Event(models.Model):
    name = models.CharField(max_length=64, default='')
    short_name = models.CharField(max_length=64, default='')
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    event_url = models.CharField(max_length=64, default='')

    def get_internal_path(self):
        path = pathlib.PurePath(self.event_url.__str__())
        return '/event/' + path.name

    def __str__(self):
        return self.name.__str__()


@python_2_unicode_compatible
class Placement(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    total_score = models.FloatField(blank=True, default=None, null=True)
    placement = models.IntegerField()

    def __str__(self):
        return self.event.__str__() + ' ' + self.competitor.__str__() + ' ' + self.total_score.__str__()


@python_2_unicode_compatible
class Choice(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    category_class = models.ForeignKey(CategoryClass, on_delete=models.CASCADE, null=True)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + ' ' + self.event.__str__() + ' - ' + self.category.__str__() + ' ' +\
               self.category_class.__str__() + ': ' + self.competitor.__str__()


@python_2_unicode_compatible
class ClassAssignmentForEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=True)
    category_class = models.ForeignKey(CategoryClass, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.event.__str__() + ' - ' + self.competitor.__str__() + ': ' + self.category_class.__str__()


@python_2_unicode_compatible
class Entry(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.event.__str__() + ' ' + self.competitor.__str__()


@python_2_unicode_compatible
class EventUserScore(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.FloatField(blank=True, default=None, null=True)

    def __str__(self):
        return self.event.__str__() + ' ' + self.user.__str__() + ' ' + self.score.__str__()


@python_2_unicode_compatible
class FakeDate(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True)