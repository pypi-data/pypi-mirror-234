import urllib3
from django.core.management import BaseCommand

from ...models import Province, District, Subdistrict
from ...types import LocationData

DEFAULT_JSON_DATABASE_URL = 'https://raw.githubusercontent.com/thailand-geography-data/thailand-geography-json/main/src/geography.json'


class Command(BaseCommand):
    help = 'Import Thailand geography from JSON database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            default=DEFAULT_JSON_DATABASE_URL,
            help='Specify custom database URL',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Downloading JSON file...'))

        request = urllib3.request('GET', options['url'])
        rows: list[LocationData] = request.json()

        self.stdout.write(self.style.NOTICE('Starting...'))

        for row in rows:
            province, _ = Province.objects.update_or_create(
                id=row['provinceCode'],
                name_en=row['provinceNameEn'],
                name_th=row['provinceNameTh'],
            )

            district, _ = District.objects.update_or_create(
                id=row['districtCode'],
                name_en=row['districtNameEn'],
                name_th=row['districtNameTh'],
                province=province,
            )

            Subdistrict.objects.update_or_create(
                id=row['subdistrictCode'],
                name_en=row['subdistrictNameEn'],
                name_th=row['subdistrictNameTh'],
                district=district,
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported from {len(rows)} rows.'))
