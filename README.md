# Clinic Management System [WIP]

This is my Diploma Final Year Project, Technology use:  
Frontend:
1. HTML
2. Bootstrap5
3. CSS

Backend:
1. Django 
2. Sqlite3 for database

Hows To:

Clone this repo  
`git clone https://github.com/rahimi-mohd/clinic-management-system.git`

Create virtual env (Optional but recommended)  
`$ python -m venv venv`

Install requirements  
`$ pip install -r requirements.txt`

Setup database  
```
$ ./manage makemigrations
$ ./manage migrate
```

**IMPORTANT**: Create super user   
`$ ./manage createsuperuser`  
You will be prompt with username, email, and password. And you have to use this account for first log in.  

Run server  
`$ ./manage runserver`

**NOTE**: There's a debate whether Function Based Views (FBVs) or Class Based Views (CBVs) is better for writing Django application. I choose  FBVs because it make my logic clearer and I find that I can think better by using it--this is clearly matter of personal thought and preference. **END**

Next Plan:
1. To add Unit Test.
2. To add test case with functional test using Playwright.
2. Refactor views.