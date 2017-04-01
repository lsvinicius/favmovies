import json
from flask_testing import TestCase, LiveServerTestCase
from flask_login import LoginManager
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src import frontend_app
from src import database
from src.model.user import User
from src.password import hash_password
import os
import subprocess

login_manager = LoginManager()
#this is the same as in app.load_user, I only
#put it here in order to test login access,
#since I must have a user_loader callback
#defined for login_manager
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

class BaseDo(LiveServerTestCase):

    def create_app(self):
        app = frontend_app.create_frontend_app()
        app.secret_key = os.urandom(24)
        login_manager.init_app(app)
        login_manager.login_view = 'site_views.login'
        database.db.init_app(app)
        return app

    def setUp(self, firefoxProfile = None):
        database.db.create_all()
        user = User(name='Vinicius Silva', email='vinicius5@gmail.com', password=hash_password('admin'))
        database.db.session.add(user)
        database.db.session.commit()
        self.app = self.create_app()
        if not firefoxProfile:
            self.browser = webdriver.Firefox()
        else:
            self.browser = webdriver.Firefox(firefox_profile=firefoxProfile)

    def tearDown(self):
        database.db.session.remove()
        database.db.drop_all()
        self.browser.quit()

    @classmethod
    def setUpClass(cls):
        #this process will be used to start the restful_app.
        #this is done as a new process instead of running
        #inside within the current process because
        #when frontend_app calls requests methods
        #to restful_app and they are both in the same process,
        # the requests method loops forever
        cls.restful_app = subprocess.Popen(['python3', '-m', 'src.restful_app'], stdout=subprocess.PIPE)

    @classmethod
    def tearDownClass(cls):
        cls.restful_app.terminate()

    def wait_submit(self, element, by=By.TAG_NAME, timeout=10):
        try:
            element_present = EC.presence_of_element_located((by, element))
            WebDriverWait(self.browser, timeout).until(element_present)
            el = None
            if by == By.TAG_NAME:
                el = self.browser.find_element_by_tag_name(element)
            elif by == By.ID:
                el = self.browser.find_element_by_id(element)
            return el
        except TimeoutException:
            assert False, "Timeout exception"
        return None

    def do_login(self, email='vinicius5@gmail.com', password='admin'):
        self.browser.get('http://localhost:5000/login')
        email = self.browser.find_element_by_name('email')
        password = self.browser.find_element_by_name('password')
        submit = self.browser.find_element_by_name('submit')
        email.send_keys('vinicius5@gmail.com')
        password.send_keys('admin')
        submit.click()
        p = self.wait_submit('p')
        return p

    def do_search(self, title='matrix'):
        self.do_login()
        self.browser.get('http://localhost:5000/search')
        search = self.browser.find_element_by_name('title')
        submit = self.browser.find_element_by_name('submit')
        search.send_keys(title)
        submit.click()
        el = self.wait_submit('search_response', By.ID)
        return el

    def do_add_movies(self):
        form = self.do_search()
        movies = form.find_elements_by_name('movies')[0:3]
        for el in movies:
            el.click()
        form.find_element_by_name('add_movies').click()
        p = self.wait_submit('p')
        return p

    def do_click_movie(self):
        self.do_add_movies()
        self.browser.get('http://localhost:5000/favmovies')
        movies = self.browser.find_elements_by_name('poster_link')[0].click()
        self.wait_submit('delete', By.ID)

    def do_accept_alert(self, timeout=10):
        try:
            WebDriverWait(self.browser, timeout).until(EC.alert_is_present())
            alert = self.browser.switch_to_alert()
            alert.accept()
        except TimeoutException:
            assert False, 'Timeout'


class FrontendTest(BaseDo):

    def test_index_not_logged(self):
        self.browser.get('http://localhost:5000')
        element = self.browser.find_element_by_tag_name('body')
        p_val = element.find_element_by_tag_name('p')
        links = element.find_elements_by_tag_name('a')
        assert p_val.text == 'We save your favorite movies, so you never forget them'
        assert links[0].get_attribute('href') == 'http://localhost:5000/' and links[1].get_attribute('href') == 'http://localhost:5000/register' and links[2].get_attribute('href') == 'http://localhost:5000/login'

    def test_index_logged(self):
        p = self.do_login()
        links = self.browser.find_elements_by_tag_name('a')
        assert p.text == 'Welcome Vinicius Silva' and links[0].get_attribute('href') == 'http://localhost:5000/' and links[1].get_attribute('href') == 'http://localhost:5000/search' and links[2].get_attribute('href') == 'http://localhost:5000/favmovies' and links[3].get_attribute('href') == 'http://localhost:5000/logout'

    def test_add_movies(self):
        self.do_add_movies()
        self.browser.get('http://localhost:5000/favmovies')
        movies = self.browser.find_elements_by_tag_name('li')
        assert len(movies) == 3

    def test_update_movie(self):
        self.do_click_movie()
        comment = self.browser.find_element_by_id('comment')
        user_comment = 'This is a new comment'
        comment.clear()
        comment.send_keys(user_comment)
        self.browser.find_element_by_id('update').click()
        self.do_accept_alert()
        self.browser.get('http://localhost:5000/favmovies')
        textarea = self.browser.find_elements_by_tag_name('textarea')[0]
        assert textarea.text == user_comment

    #TODO test movie deletion

    def get_register_form_elements(self):
        self.browser.get('http://localhost:5000/register')
        firstname = self.browser.find_element_by_name('firstname')
        lastname = self.browser.find_element_by_name('lastname')
        password = self.browser.find_element_by_name('password')
        email = self.browser.find_element_by_name('email')
        submit = self.browser.find_element_by_name('submit')
        firstname.send_keys('Vinicius')
        lastname.send_keys('Silva')
        password.send_keys('admin')
        email.send_keys('vinicius2@gmail.com')
        return (firstname, lastname, password, email, submit)

    def test_register_with_invalid_firstname(self):
        firstname, lastname, password, email, submit = self.get_register_form_elements()
        firstname.send_keys('0123')
        submit.click()
        #The returned content is not handled by method
        #frontend_app.bad_request_handler.
        #For the current situation, we will handle the
        #Bad Request issued by Firefox manually, however,
        #when the server is in production, Bad Request won't
        #reach the client, instead, a page describing the error
        #will be displayed.
        #See frontend_app.py, templates/error.jinja and bad_request.jinja
        #for a better understanding
        p = self.wait_submit('p')
        assert json.loads(p.text.replace("'", "\"")) == {'description':'Invalid firstname'}

    #TODO test other invalid fields when registering a new user

class FrontendTestWithoutJavascript(BaseDo):

    def setUp(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('javascript.enabled', False)
        profile.add_extension('tests/extensions/quickjava-2.1.2-fx.xpi')
        profile.set_preference('extensions.thatoneguydotnet.QuickJava.startupStatus.JavaScript', 2)
        profile.set_preference('extensions.thatoneguydotnet.QuickJava.curVersion', '2.1.2')
        super(FrontendTestWithoutJavascript, self).setUp(profile)

    def test_single_movie_without_javascript(self):
        self.do_click_movie()
        warning = self.browser.find_element_by_id('warning')
        assert warning is not None and warning.text == "Delete and Update won't work"
