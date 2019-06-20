import os
import django

def populate():
    files = satelliteMetadataFiles().__class__.objects.all()
    # print(files)
    for file in files:
        file.filename = file.filename[3:]
        print(file.filename)
        file.save()

if __name__ == '__main__':
    print("Starting script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    from myapp.models import *
    populate()