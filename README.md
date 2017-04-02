# favmovies
Welcome to favmovies, a project where you are able to browse through movies, add them to your personal list and comment it.

# before setting up
We recommend you use [Virtualenv](https://docs.python.org/3/library/venv.html) before testing the system.
After you set your virtualenv (must be set with **python3**), just download **favmovies** to the folder you initialized
virtualenv and run ``pip install -r requirements.txt`` (the file is found in the root of the project). This will install
all dependencies needed by **favmovies**.

# setting up
The system is composed of a **frontend** and a **restful api**, in order for the system to work properly, we must have
both up and running.
* ## frontend:
  This is responsible for displaying the webpages and also to register the user. The core functionalities of **favmovies**
  are delegated to the **restful api**. In order to run it, just type ``python3 -m src.frontend_app`` from the root of the
  project.
* ## restful api:
  This is responsible for querying [OMDBApi](http://www.omdbapi.com) and also store/display/update/delete anything that
  have to do with the **favmovies** list of a given user. If you have access to this process, you will be able to edit
  the **favmovies** list of any user (I hope this server runs in a secure environment and the machine owner is 
  not malicious). In order to run it, just type ``python3 -m src.restful_app`` from the root of the project.
  
Besides running both projects individually, you are also able to type ``./run.sh`` (only works for **Linux** users). Note
however that both processes will run in background mode and in order to kill it, you will need to do a 
``ps aux | grep app.py`` to discover their PID and then issue command ``kill -9 <PID>``

# tests
There are some tests created for both **frontend** and **restful api**. Some tests use [Selenium](http://www.seleniumhq.org/)
and will need [Firefox](https://www.mozilla.org/). You are able to run all tests by just issuing command ``pytest`` in the
root of the project. 

However, it is possible that you face some PATH issues when trying to run the tests. There is a file
called **set_path.sh** that should be called by typing ``source set_path.sh`` (works only for **Linux** users). 

If you do not use windows, then you will need to set the root of the project in the **PYTHONPATH** variable and will need
to set ``tests/bin`` to the **PATH** environment variable.
## warning: 
  not all test scenarios were covered for the frontend (failures weren't faced while running the system, however,
  it is possible that you find something).

# usage
By default, favmovies will be running at port **5000** and run on **localhost**. After you started **frontend_app**
and **restful_app**, you should open your browser and access ``http://localhost:5000``.
For the unlogged users, there will be the following options available:
* ## register:
  In order to use the system, you will need to type your **firstname**, **lastname**, **email** and **password**. The system
  doesn't support password recovery. You shouldn't forget the password, otherwise, you will have to register another user.
* ## login:
  No secret here, just type your **email** and **password** previously registered and you will be able to use the nicest 
  features of **favmovies**.

After you have created your account and already logged to the system, you will have fun by finding a lot of movies that you
already watched, but for some reason, forgot it. So, here is the list of things you wil be able to do as a logged user:
* ## search:
  Pretty basic. Just type any title that you wish to save, check the titles that you like more and just add them to your
  **favmovies** list. (The button to add is at the bottom of the page).
* ## favmovies (browsing list and edition):
  After you have added some titles to your **favmovies** list, it is time to browse it. So, by clicking in this option, you
  will be able to see the whole list of added titles and to see your comments about the title (at first, these will be empty).
  * ### edit (update and delete):
    You will also be able to click at the **poster** image displayed alongside the basic info of the title. By doing it, you
    will be able to type any comment you have to make about the movie and will also be able remove the title from your
    **favmovies** list.
* ## logout:
  Pretty self-explanatory
