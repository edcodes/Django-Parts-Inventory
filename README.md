# Django Parts Inventory
A parts inventory app built with Python and Django
Good example of Formset, User access, ForeignKey, Django template, Bootstrap.

**Make sure to install requirements.txt

**Add your ip to setting.py ( ALLOWED_HOSTS = [''] )


pip install -r requirements.txt


Create database:
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput


Create admin user:
python3 manage.py createsuperuser


Run:
python3 manage.py runserver 0.0.0.0:8000

