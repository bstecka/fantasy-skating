from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
from ...models import Skater, Competitor, Category, Placement, Event
from .utils import handle_name, split_skaters
import requests


class Command(BaseCommand):
    help = 'Get newest results - Ice Dance'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, nargs='?', default="empty", help='Event results page base url')
        parser.add_argument('event_name', type=str, nargs='?', default="empty", help='Event name')

    def process_data(self, first_name1, last_name1, first_name2, last_name2, score, event_name, rank, arg):
        db_skaters = Skater.objects.all()
        db_competitors = Competitor.objects.all()
        category = Category.objects.filter(name__contains='Ice').first()
        events = Event.objects.filter(name__contains=event_name)
        event = events[0]
        self.stdout.write(self.style.SUCCESS(str(category)))
        if db_skaters.filter(name=first_name1, surname=last_name1).exists():
            self.stdout.write(self.style.SUCCESS(first_name1))
            self.stdout.write(self.style.SUCCESS(last_name1))
            self.stdout.write(self.style.SUCCESS(str(score)))
            skater1 = db_skaters.filter(name=first_name1, surname=last_name1).first()
        else:
            self.stdout.write(self.style.SUCCESS(first_name1))
            self.stdout.write(self.style.SUCCESS(last_name1))
            self.stdout.write(self.style.SUCCESS(str(score)))
            skater1 = Skater.objects.create(name=first_name1, surname=last_name1, category=category)
        if db_skaters.filter(name=first_name2, surname=last_name2).exists():
            self.stdout.write(self.style.SUCCESS(first_name2))
            self.stdout.write(self.style.SUCCESS(last_name2))
            self.stdout.write(self.style.SUCCESS(str(score)))
            skater2 = db_skaters.filter(name=first_name2, surname=last_name2).first()
        else:
            self.stdout.write(self.style.SUCCESS(first_name2))
            self.stdout.write(self.style.SUCCESS(last_name2))
            self.stdout.write(self.style.SUCCESS(str(score)))
            skater2 = Skater.objects.create(name=first_name2, surname=last_name2, category=category)
        if not db_competitors.filter(skater_1=skater1, skater_2=skater2).exists():
            competitor = Competitor.objects.create(skater_1=skater1, skater_2=skater2)
        else:
            competitor = db_competitors.filter(skater_1=skater1, skater_2=skater2)[0]
        if not Placement.objects.filter(competitor=competitor, event=event).exists():
            placement = Placement.objects.create(competitor=competitor, event=event, total_score=score, placement=rank)
            self.stdout.write(self.style.SUCCESS(placement.__str__()))

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        event_name = kwargs['event_name']
        self.stdout.write(self.style.SUCCESS(url))
        if url.__contains__("jpn"):
            category = 'data0490.htm'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find('table', attrs={'class': 'Official'})
            skaters = table.find_all('tr')
            count = 0
            for skater in skaters:
                a = skater.contents[3].find('a')
                rights = skater.find_all('td', attrs={'class': 'Right'})
                if not isinstance(a, int):
                    name = a.string
                    score = rights[3].string
                    if score.strip().__len__() > 0:
                        score = float(score)
                    else:
                        score = 0.0
                    if name is not None:
                        skater1, skater2 = split_skaters(name)
                        first_name1, last_name1 = handle_name(skater1)
                        first_name2, last_name2 = handle_name(skater2)
                        count += 1
                        self.process_data(first_name1, last_name1, first_name2, last_name2, score, event_name, count, "")
        else:
            category = 'CAT004RS.HTM'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            skaters = soup.find_all('td', attrs={'class': 'CellLeft'})
            count = 0
            for skater in skaters:
                if isinstance(skater.contents[0], NavigableString):
                    continue
                name = skater.contents[0].contents[0]
                score = skater.nextSibling.nextSibling.contents[0]
                if name.strip().__len__() > 0:
                    if score.strip().__len__() > 0:
                        score = float(score)
                    else:
                        score = 0.0
                    if name is not None:
                        skater1, skater2 = split_skaters(name)
                        first_name1, last_name1 = handle_name(skater1)
                        first_name2, last_name2 = handle_name(skater2)
                        count += 1
                        self.process_data(first_name1, last_name1, first_name2, last_name2, score, event_name, count, "")
