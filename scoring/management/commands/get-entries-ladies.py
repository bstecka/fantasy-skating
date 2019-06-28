from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
from ...models import Skater, Competitor, Category, Entry, Event
from .utils import handle_name, get_world_standings
import requests


class Command(BaseCommand):
    help = 'Get newest entries - Ladies'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, nargs='?', default="empty", help='Event results page base url')
        parser.add_argument('event_name', type=str, nargs='?', default="empty", help='Event name')

    def process_data(self, first_name, last_name, event_name, world_standings):
        db_skaters = Skater.objects.all()
        category = Category.objects.filter(name__contains='Ladies').first()
        event = Event.objects.get(name=event_name)
        if db_skaters.filter(name=first_name, surname=last_name).exists():
            self.stdout.write(self.style.SUCCESS(first_name))
            self.stdout.write(self.style.SUCCESS(last_name))
            competitor = Competitor.objects.filter(skater_1=(db_skaters.filter(name=first_name, surname=last_name)[0]))[0]
        else:
            self.stdout.write(self.style.SUCCESS(first_name))
            self.stdout.write(self.style.SUCCESS(last_name))
            new_skater = Skater.objects.create(name=first_name, surname=last_name, category=category)
            competitor = Competitor.objects.create(skater_1=new_skater, skater_2=new_skater)
        rank = world_standings.get(competitor.__str__(), 1000)
        competitor.world_standing = rank
        competitor.save()
        self.stdout.write(self.style.SUCCESS(rank.__str__()))
        db_entries = Entry.objects.all()
        if not db_entries.filter(competitor=competitor, event=event).exists():
            Entry.objects.create(competitor=competitor, event=event)

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        event_name = kwargs['event_name']
        self.stdout.write(self.style.SUCCESS(url))
        world_standings = get_world_standings('http://www.isuresults.com/ws/ws/wsladies.htm')
        if url.__contains__("jpn"):
            category = 'data0200.htm'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find('table', attrs={'class': 'Official'})
            skaters = table.find_all('tr')
            for skater in skaters:
                if skater is not None:
                    a = skater.find('a')
                    if not isinstance(a, int) and a is not None:
                        name = a.string
                        first_name, last_name = handle_name(name)
                        self.process_data(first_name, last_name, event_name, world_standings)
        else:
            category = 'CAT002EN.HTM'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            skaters = soup.find_all('td', attrs={'class': 'CellLeft'})
            for skater in skaters:
                if isinstance(skater.contents[0], NavigableString):
                    continue
                name = skater.contents[0].contents[0]
                if name.strip().__len__() > 0:
                    first_name, last_name = handle_name(name)
                    self.process_data(first_name, last_name, event_name, world_standings)
