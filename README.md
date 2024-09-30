# Clinic Management System [WIP]

This is my Diploma Final Year Project, Technology use:  
Frontend:
1. HTML
2. Bootstrap5
3. CSS

Backend:
1. Django 
2. Sqlite3 for database

## Hows To:

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

## Functional Test

I use Playwright to write my functional test, all code for FT can be found in tests folder. Before we can run our test, we have to setup Playwright. You should have all the modules and packages if you run `pip install -r requirements.txt`, now we just have to install the required browsers using `playwright install` command.  

I have my config for User and Patient class in config.py, but you have to register the data in the website or admin page(easier). You should change the list of users and list of patients in functional_test.py following your own data. Or you can register you users and patients based on my data as below, so that you don't have to think of any new name and password for each users and patient. 

```
# list of users
admin = User("admin", "12", "Admin")
clinic_staff = User("staff1", "bingo132$", "Staff")
doctor = User("doctor1", "dd-1-clinic", "Doctor")
not_existed_user = User("not_existed", "never_registered", "Not Existed")

# list of patients
patient1 = Patient("Patient1", "Generic", "121212121212", "090900901111")
```

To run the script, the easiest way is to go to tests directory, then run pytest command.

```
# assumming you clone this repo in your home directory
$ cd clinic-management-system/tests/
$ pytest # or
$ pytest -k test_user_can_login_and_logout # this only run the test that we specified, change to other test if you needed to
```

Lastly, I have a script which I use to run the test, it run in headed mode with slowmo=1000, you can use this script by running `./run_test.sh`.

**NOTE**: You can write Playwright with another language such as Typescript, Java, C# and Go (un-official), I choose Python because this is Python app, so I want to do it all in Python.**END**

## Next Plan:
1. To add Unit Test.
2. To add test case with functional test using Playwright.
2. Refactor views.