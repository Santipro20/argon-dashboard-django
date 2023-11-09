# [Deki Argon Dashboard](https://www.deki.team) 

Open-source **[Django Template](https://www.creative-tim.com/templates/django)** crafted on top of **Argon Dashboard**, a modern Bootstrap 4 design. Start your development with a modern Bootstrap 4 Admin template for Django. Argon Dashboard is built with over 100 individual components, giving you the freedom of choosing and combining. If you want to code faster, with a smooth workflow, then you should try this template carefully developed with Django, a well-known Python Framework. **Django codebase** is crafted using a simple, modular structure that follows the best practices and provides authentication, database configuration, and deployment scripts for Docker and Gunicorn/Nginx stack. 

- Up-to-date [dependencies](./requirements.txt): **Django 3.2.6 LTS**
- [SCSS compilation](#recompile-css) via **Gulp**
- UI Kit: **Argon Dashboard** (Free Version)
- Django Codebase - provided by **[AppSeed](https://appseed.us/)**
- UI-Ready app, SQLite Database, Django Native ORM
- Modular design, clean code-base
- Session-Based Authentication, Forms validation
- Deployment scripts: Docker, Gunicorn / Nginx

<br />

## Table of Contents

* [Quick Start](#quick-start)
* [Documentation](#documentation)
* [File Structure](#file-structure)
* [Browser Support](#browser-support)
* [Resources](#resources)
* [Reporting Issues](#reporting-issues)
* [Technical Support or Questions](#technical-support-or-questions)
* [Licensing](#licensing)
* [Useful Links](#useful-links)

<br />

## Quick start

> UNZIP the sources or clone the private repository. After getting the code, open a terminal and navigate to the working directory, with product source code.

### Install all technologies
```bash 
$ # Run redis in the Terminal or cmd 
$ redis-server 
$
$ # Test the server  
$ redis-cli ping 
$
$ # Install PostgreSQL
$ brew install postgresql
$ brew services start postgresql
$
$
```

### 

```bash
$ # Get the code
$ git clone http://gitlab.deki.tech/Santi/argon-dashboard-django.git
$ cd argon-dashboard-django
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env #  python3 -m venv env
$ source env/bin/activate # source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Install modules - PostgreSQL Storage
$ pip3 install -r requirements.txt
$
$ # Create tables
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Start the application (development mode)
$ python manage.py runserver # default port 8000
$
$ # Start the app - custom port
$ # python manage.py runserver 0.0.0.0:<your_port>
$
$ # Access the web app in browser: http://127.0.0.1:8000/
$ # python manage.py shell interactive console 
```
celery worker -A core -l=info
> Note: To use the app, please access the registration page and create a new user. After authentication, the app will unlock the private pages.

<br />

## Documentation
The documentation for the **Deki Argon Dashboard** is hosted at our [website](https://www.deki.team).

<br />

## Code-base structure

The project is coded using a simple and intuitive structure presented bellow:

```bash
< PROJECT ROOT >
  .
├── .DS_Store
├── .env
├── .git
│   ├── COMMIT_EDITMSG
│   ├── FETCH_HEAD
│   ├── HEAD
│   ├── ORIG_HEAD
│   ├── config
│   ├── description
│   ├── hooks
│   ├── index
│   ├── info
│   ├── logs
│   ├── objects
│   ├── packed-refs
│   └── refs
├── .gitignore
├── CHANGELOG.md
├── Dockerfile
├── LICENSE.md
├── Procfile
├── README copy.md
├── README.md
├── apps
│   ├── .DS_Store
│   ├── __init__.py
│   ├── app2
│   ├── app3
│   ├── authentication
│   ├── config.py
│   ├── home
│   ├── static
│   └── templates
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── staticfiles
│   ├── urls.py
│   └── wsgi.py
├── datos_tm.csv
├── docker-compose.yml
├── env
│   ├── .Python -> /Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Python3
│   ├── .gitignore
│   ├── bin
│   ├── etc
│   ├── include
│   ├── lib
│   ├── pyvenv.cfg
│   └── share
├── estructura_proyecto.txt
├── get-pip.py
├── gunicorn-cfg.py
├── manage.py
├── media
│   ├── argon-dashboard-django-intro.gif
│   ├── argon-dashboard-django-screen-icons-low.png
│   ├── argon-dashboard-django-screen-icons.png
│   ├── argon-dashboard-django-screen-login-low.png
│   ├── argon-dashboard-django-screen-login.png
│   ├── argon-dashboard-django-screen-low.png
│   ├── argon-dashboard-django-screen-maps-low.png
│   ├── argon-dashboard-django-screen-maps.png
│   ├── argon-dashboard-django-screen-profile-low.png
│   ├── argon-dashboard-django-screen-profile.png
│   ├── argon-dashboard-django-screen-register-low.png
│   ├── argon-dashboard-django-screen-register.png
│   ├── argon-dashboard-django-screen-tables-low.png
│   ├── argon-dashboard-django-screen-tables.png
│   ├── argon-dashboard-django-screen.png
│   └── argon-dashboard-django-thumb-ct.jpg
├── nginx
│   └── appseed-app.conf
├── package-lock.json
├── package.json
├── requirements.txt
├── runtime.txt
├── staticfiles
│   └── .gitkeep

 ************************************************************************
```

<br />

> The bootstrap flow

- Django bootstrapper `manage.py` uses `core/settings.py` as the main configuration file
- `core/settings.py` loads the app magic from `.env` file
- Redirect the guest users to Login page
- Unlock the pages served by *app* node for authenticated users

<br />

## Recompile CSS

To recompile SCSS files, follow this setup:

<br />

**Step #1** - Install tools

- [NodeJS](https://nodejs.org/en/) 12.x or higher
- [Gulp](https://gulpjs.com/) - globally 
    - `npm install -g gulp-cli`
- [Yarn](https://yarnpkg.com/) (optional) 

<br />

**Step #2** - Change the working directory to `assets` folder

```bash
$ cd apps/static/assets
```

<br />

**Step #3** - Install modules (this will create a classic `node_modules` directory)

```bash
$ npm install
// OR
$ yarn
```

<br />

**Step #4** - Edit & Recompile SCSS files 

```bash
$ gulp scss
```

The generated file is saved in `static/assets/css` directory.

<br /> 

## Deployment

The app is provided with a basic configuration to be executed in [Docker](https://www.docker.com/), [Gunicorn](https://gunicorn.org/), and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### [Docker](https://www.docker.com/) execution
---

The application can be easily executed in a docker container. The steps:

> Get the code

```bash
$ git clone https://github.com/creativetimofficial/argon-dashboard-django.git
$ cd argon-dashboard-django
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:85` in your browser. The app should be up & running.

<br />

## Browser Support

At present, we officially aim to support the last two versions of the following browsers:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">


<br />

## Reporting Issues

We use GitHub Issues as the official bug tracker for the **Deki Dashboard**. Here are some advices for our users that want to report an issue:

1. Make sure that you are using the latest version of the **Deki Dashboard **. Check the CHANGELOG from your dashboard 
2. Providing us reproducible steps for the issue will shorten the time it takes for it to be fixed.
3. Some issues may be browser-specific, so specifying in what browser you encountered the issue might help.

<br />

## Technical Support or Questions

If you have questions or need help integrating the product please [contact us](https://www.creative-tim.com/contact-us) instead of opening an issue.

<br />

## Licensing

- Copyright 2019 - present [Creative Tim](https://www.creative-tim.com/)
- Licensed under [Creative Tim EULA](https://www.creative-tim.com/license)

<br />
