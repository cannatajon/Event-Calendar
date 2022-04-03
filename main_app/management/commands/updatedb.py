import os
import json
import requests
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import get_current_timezone
from main_app.models import Tag, Venue, Event


PLACES = {
    "toronto": "101735835",
    "montreal": "101736545",
    "calgary": "890458845",
    "ottawa": "101735873",
    "edmonton": "890458485",
    "mississauga": "101735893",
    "winnipeg": "101734959",
    "vancouver": "101741075",
    "brampton": "101740755",
    "quebec": "101737491",
}
url = "https://www.eventbrite.ca/api/v3/destination/search/"
headers = json.loads(os.getenv("EVENTBRITE_REQUEST_HEADERS"))


class Command(BaseCommand):
    help = "Update the db with most recenet data from eventbrite for given city"

    def add_arguments(self, parser):
        parser.add_argument("places", nargs="+", type=str, help="A list of cities to be updated")

    def handle(self, *args, **options):
        for place in options['places']:
            print(f"Updating db for {place}")

            payload = json.dumps({
                "event_search": {
                    "dates": "current_future",
                    "dedup": True,
                    "places": [
                        PLACES[place]
                    ],
                    "page": 1,
                    "page_size": 50,
                    "online_events_only": False,
                    "client_timezone": "America/Toronto"
                },
                "expand.destination_event": [
                    "primary_venue",
                    "image",
                    "ticket_availability",
                    "saves",
                    "event_sales_status",
                    "primary_organizer",
                    "public_collections"
                ]
            })

            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = json.loads(response.text)
                events = data["events"]["results"]
                for event in events:

                    # Create venue object
                    v, created = Venue.objects.get_or_create(
                        eventbrite_id=event["primary_venue"]["id"],
                        name=event["primary_venue"]["name"],
                        address=event["primary_venue"]["address"]["localized_address_display"]
                    )
                    if created == True:
                        print('added new venue')

                    # Create event object
                    e, created = Event.objects.get_or_create(
                        eventbrite_id=event["id"],
                        title=event["name"],
                        description=event["summary"],
                        start_time=datetime.datetime.fromisoformat(
                            f"{event['start_date']} {event['start_time']}:00"),
                        end_time=datetime.datetime.fromisoformat(
                            f"{event['end_date']} {event['end_time']}:00"),
                        image=event["image"]["url"],
                    )

                    if created:
                        print('added new event')
                        # Add venue
                        e.venue.add(v)

                        # Add tags
                        for tag in event["tags"]:
                            if tag["prefix"].startswith("Eventbrite"):
                                t, created = Tag.objects.get_or_create(name=tag["display_name"])
                            e.tags.add(t)
            else:
                print("There was an error calling the eventbrite api")
