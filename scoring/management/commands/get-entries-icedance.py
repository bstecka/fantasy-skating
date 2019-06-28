from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup, NavigableString
from ...models import Skater, Competitor, Category, Entry, Event
from .utils import handle_name, split_skaters, get_world_standings
import requests


class Command(BaseCommand):
    help = 'Get newest entries - Ice Dance'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, nargs='?', default="empty", help='Event results page base url')
        parser.add_argument('event_name', type=str, nargs='?', default="empty", help='Event name')

    def process_data(self, first_name1, last_name1, first_name2, last_name2, world_standings, event_name):
        db_skaters = Skater.objects.all()
        db_competitors = Competitor.objects.all()
        category = Category.objects.filter(name__contains='Ice').first()
        event = Event.objects.get(name=event_name)
        if db_skaters.filter(name=first_name1, surname=last_name1).exists():
            skater1 = db_skaters.filter(name=first_name1, surname=last_name1).first()
        else:
            skater1 = Skater.objects.create(name=first_name1, surname=last_name1, category=category)
        if db_skaters.filter(name=first_name2, surname=last_name2).exists():
            skater2 = db_skaters.filter(name=first_name2, surname=last_name2).first()
        else:
            skater2 = Skater.objects.create(name=first_name2, surname=last_name2, category=category)
        if not db_competitors.filter(skater_1=skater1, skater_2=skater2).exists():
            competitor = Competitor.objects.create(skater_1=skater1, skater_2=skater2)
            self.stdout.write(self.style.SUCCESS(competitor.__str__()))
        else:
            competitor = db_competitors.filter(skater_1=skater1, skater_2=skater2)[0]
            self.stdout.write(self.style.SUCCESS(competitor.__str__()))
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
        world_standings = get_world_standings('http://www.isuresults.com/ws/ws/wsdance.htm')
        if url.__contains__("jpn"):
            category = 'data0400.htm'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for br in soup.find_all("br"):
                br.replace_with(" / ")
            table = soup.find('table', attrs={'class': 'Official'})
            skaters = table.find_all('tr')
            for skater in skaters:
                if skater is not None:
                    a = skater.find('a')
                    if not isinstance(a, int) and a is not None:
                        name = a.text
                        if name is not None:
                            skater1, skater2 = split_skaters(name)
                            first_name1, last_name1 = handle_name(skater1)
                            first_name2, last_name2 = handle_name(skater2)
                            self.process_data(first_name1, last_name1, first_name2, last_name2, world_standings, event_name)
        else:
            category = 'CAT004EN.HTM'
            url += category
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            skaters = soup.find_all('td', attrs={'class': 'CellLeft'})
            for skater in skaters:
                if isinstance(skater.contents[0], NavigableString):
                    continue
                name = skater.contents[0].contents[0]
                if name is not None:
                    skater1, skater2 = split_skaters(name)
                    first_name1, last_name1 = handle_name(skater1)
                    first_name2, last_name2 = handle_name(skater2)
                    self.process_data(first_name1, last_name1, first_name2, last_name2, world_standings, event_name)
