# SmartWeather app
The goal of this project is to create an applciation to provide users a weather forecast of their local area. Additional requirmenets will be derived in the requirments documentation of the project - [requirments](https://drive.google.com/drive/folders/1N_JkxGc9pKiHF-Fs-VED2meeDsw3QrKc).

## Getting started
This section will explain the directory/project structure and identify important files. We will also cover some django commands that are important in getting the project started.

### Starting the server
Run the following command to start the developement server. This will allow you to open the web application in your browser.

Command:
```bash
python3 manage.py runserver
```
Address:
```
http://localhost:8000
```

### Migrating models to the database
Django communicates with databases via models. See the file discriptions later in this readme for more details, but the following commands will allow you to commit changes to the database.

Commands:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Super users
Django comes with a built in admin page located at /admin. By default, super users are the only ones who can access the admin page which allows you to create/edit/delete models. Use the command below to add a super user, or contact the architect/operations to have yourself added as a super user.

Command:
```bash
python3 manage.py createsuperuser
```

### Directories and files
This section will go in depth on where resources in the project are and point developers to their respective files. In the below file tree there are numerous directories/files. I have set up the project so that developers will only need to edit/add content to the files located in the weather directory. I will try to update this directory tree as content is added.

```
\---smart_weather
    |   db.sqlite3
    |   manage.py
    |
    +---smart_weather
    |   |   settings.py
    |   |   urls.py
    |   |   wsgi.py
    |   |   __init__.py
    |
    \---weather
        |   admin.py
        |   apps.py
        |   forms.py
        |   models.py
        |   tests.py
        |   urls.py
        |   views.py
        |   __init__.py
        |
        +---migrations
        |   |   __init__.py
        |
        +---static
        |   \---weather
        |       +---css
        |       |       main.css
        |       |
        |       \---js
        |               main.js
        |
        +---templates
        |   \---weather
        |           index.html
        |           login.html
        |           register.html
        |
```

#### admin.py
This file is used to register models in the admin interface which allows you to create/edit/delete objects. A commented line in the file exists to give an example of how to add an object. That line is copied below:

```python
admin.site.register(models.Foo)
```

#### apps.py
This file is configured by django when the project is started and should not be edited.

#### forms.py
Django has a convenient feature that allows you to create forms that can be passed to the templates. I have already created a form that allows users to register for the site as an example. The basic form definition will define the form class and then use a Meta class to connect the form to a database model, thus allowing you to create or edit a database object. See the following [form documentation](https://docs.djangoproject.com/en/3.0/topics/forms/) for info.

#### models.py
This file is used to define models that communicate with the database. For the SmartWeather project an example model might be "UserActivities" which is used to store the users activities based on weather events. The migration commands are required for the new models to be accessible. Examples can be found in the file. See the [model documentation](https://docs.djangoproject.com/en/3.0/topics/db/models/) in django for more details.

#### tests.py
This file is used to register tests from the django test suite. This will be used for testing and later validation on top of the UI testing.

#### urls.py
The urls.py file registers urls which will be used to call a view. The index url is already setup, but most additional urls can be developed in the same way. Contact the architect/operations if you are unsure of a URL and it can be added for you. Urls in django are also used to pass identification content to help render the appropriate view. The below pattern is an example. See the django [url dispatcher](https://docs.djangoproject.com/en/3.0/topics/http/urls/) documentation for more info.

```python
path('<int:pk>', views.foo, name='foo')
```
Where the int pk can now be referenced in a view:
```python
def foo(request, pk):
  pass
```

#### views.py
This is the heart of framework projects and links the model data with the front end templates. They are relatively simple when you get used to them, but most views have requirmenets that can be tricky. See the current views file for an example of the registration view. Most views however, will follow the structure below:

```python
def example(request):
  # Define a template to use for the view
  template_name = 'weather/template_name.html'
  # Get some data from the database
  data = Foo.objects.all()
  # Store the data in a context dictionary
  context = {
    'data': data,
  }
  # Render the template with the context data
  return render(request, template_name, context)
```

#### templates
This directory houses the templates that will be used for the project. You can see there are already some in there that are used to render the index, registration and login. The backend developer should communicate with the UI developer to identify when a template is needed. Templates are written in HTML, CSS and JS. Django has a lot of clever features that can be used to reduce duplicated work/code such as adding the same navbar to each template. See the django include and extend statements for more info.

#### static
This directory is used to store images, script files and CSS files. By default, there is a main.css and main.js file. If you make changes to these files, just know that they will need to be linked in your templates.

## Database
The default database in this project is sqlite and is included in this repo. Be sure to include it on future commits so that the super users and models can be retained without the need to re-create them. If it is determined that the projects needs to be production ready, we will set up a mysql database in a docker container to support the application.

## Tips
The server will update live, so if you you get an error when starting the server, simply editing and saving the correction to the error should restart the server and allow you to see your changes. This will not work on rare occations where you will need to escape the server with Ctrl + c and restart.

## Tools
* Python
* Django
* HTML
* CSS
* JS
* Apache
* Docker
* Mysql

## Contributors
* Chris Lockard
* Courtney Ripoll
* Aaron Pohl
* Casey Paver
* Evans Kountouris
