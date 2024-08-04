# Bu E-Commerce Loyiha

## 1 - step 
**Clone the project from github**
```bash
git clone  https://github.com/davronbek-atadjanov/django_blog_project.git
```

## 2-step
**Enter the project directory**

## 3-step
**Create a virtual environment**
```bash
python3 -m venv venv
```

## 4-step
**Activate the virtual environment**
```bash
> For Linux
source venv/bin/activate 

> For Windows
venv\Scripts\activate
```

## 5-step
**Generate a secret key**
```bash
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## 6-step
**Install all requirements**
```bash
pip install -r requirements.txt
```

## 7-step
**Run the project**
```bash
python manage.py runserver
```
