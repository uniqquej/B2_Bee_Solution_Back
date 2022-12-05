import os
import csv
import django

from article.models import Rating

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

with open('ratings.csv', encoding="UTF-8") as csv_file_sub_categories:
    rows = csv.reader(csv_file_sub_categories)
    next(rows, None)
    for row in rows:
        Rating.objects.create(
            user = row[0],
            solution = row[1],
            rating = row[2],
        )
        print(row)
