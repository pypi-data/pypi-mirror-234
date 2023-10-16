=================
Nequi Integration
=================

A Django app to create Nequi integration.


Quick start
-----------

1. Add "artd_nequi" to your INSTALLED_APPS setting like this:
    
        INSTALLED_APPS = [
            ...
            "django_json_widget",
            "artd_location",
            "artd_partner",
            "artd_nequi",
        ]

2. Run ``python manage.py migrate`` to create the nequi models.

3. Run ``python manage.py create_countries`` to create countries.

4. Run ``python manage.py create_colombian_regions`` to create colombian regions.

5. Run ``python manage.py create_colombian_cities`` to create colombian cities.

6. Start the development server and visit http://127.0.0.1:8000/admin/