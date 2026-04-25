from django.core.management.base import BaseCommand
from game.models import Location


class Command(BaseCommand):
    help = "Seed initial locations"

    def handle(self, *args, **kwargs):
        locations = [
            ("Смолянски езера", 41.620889, 24.677050),
            ("Сливодолско Падало", 41.909664, 24.840473),
            ("Чудните мостове", 41.819616, 24.581546),
            ("Дяволския мост", 41.621834, 25.115691),
            ("Каньонът на водопадите", 41.584259, 24.644617),
            ("Водопада на сътворението", 41.560589, 25.640681),
            ("Бачковски манастир", 41.942144, 24.850064),
            ("Пещера Дяволското гърло", 41.615217, 24.379597),
            ("Ягодинска пещера", 41.628662, 24.329433),
            ("Меандрите на река Арда", 41.669127, 25.241648),
        ]

        for name, lat, lon in locations:
            Location.objects.get_or_create(
                name=name,
                defaults={
                    "latitude": lat,
                    "longitude": lon,
                    "allowed_radius_m": 120,
                },
            )

        self.stdout.write(self.style.SUCCESS("Locations seeded successfully."))