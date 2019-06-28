from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
from ...models import Skater, Competitor, Category, Placement, Event
from .utils import handle_name
import requests


class Command(BaseCommand):
    help = 'Get newest results - Ladies'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, nargs='?', default="empty", help='Event results page base url')
        parser.add_argument('event_name', type=str, nargs='?', default="empty", help='Event name')

    def process_data(self, first_name, last_name, score, event_name, rank):
        db_skaters = Skater.objects.all()
        category = Category.objects.filter(name__contains='Ladies').first()
        events = Event.objects.filter(name__contains=event_name)
        event = events[0]
        self.stdout.write(self.style.SUCCESS(str(category)))
        if db_skaters.filter(name=first_name, surname=last_name).exists():
            self.stdout.write(self.style.SUCCESS(first_name))
            self.stdout.write(self.style.SUCCESS(last_name))
            self.stdout.write(self.style.SUCCESS(str(score)))
            competitor = Competitor.objects.filter(skater_1=(db_skaters.filter(name=first_name, surname=last_name)[0]))[0]
        else:
            self.stdout.write(self.style.SUCCESS(first_name))
            self.stdout.write(self.style.SUCCESS(last_name))
            self.stdout.write(self.style.SUCCESS(str(score)))
            new_skater = Skater.objects.create(name=first_name, surname=last_name, category=category)
            competitor = Competitor.objects.create(skater_1=new_skater, skater_2=new_skater)
        if not Placement.objects.filter(competitor=competitor, event=event).exists():
            placement = Placement.objects.create(competitor=competitor, event=event, total_score=score, placement=rank)
            self.stdout.write(self.style.SUCCESS(placement.__str__()))

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        event_name = kwargs['event_name']
        self.stdout.write(self.style.SUCCESS(url))
        if url.__contains__("jpn"):
            category = 'data0290.htm'
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
                    first_name, last_name = handle_name(name)
                    count += 1
                    self.process_data(first_name, last_name, score, event_name, count)

        else:
            category = 'CAT002RS.HTM'
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
                    first_name, last_name = handle_name(name)
                    count += 1
                    self.process_data(first_name, last_name, score, event_name, count)

