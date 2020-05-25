from app import app, db
import unittest, os, time
from app.models import User, questions
from selenium import webdriver
from selenium.webdriver.support.select import Select

basedir = os.path.abspath(os.path.dirname(__file__))


class FlaskTestCase(unittest.TestCase):
    driver = None

    def setUp(self):
        #Using chrome driver
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'chromedriver'))
        if not self.driver:
            self.skipTest
        else:
            db.init_app(app)
            db.create_all()
        #If this account already in User table, then delete it.
            u = User.query.filter_by(username = 'username').first()
            if u != None:
                db.session.delete(u)
                db.session.commit()
            s1 = User(username = 'username', email = 'user@name.com', mark = 1)
            s1.set_password('password')
            db.session.add(s1)
            line = '1: HTML stands for?'
            q = questions.query.filter_by(content = line).first()
            #If this questions already in questions table, then delete it
            if q != None:
                db.session.delete(q)
                db.session.commit()
            q1 = questions(content=line, stand_answer='a', mark=1, tag='HTML1')
            db.session.add(q1)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')


    def tearDown(self):
        if self.driver:
            self.driver.close()

    #Testing if user correct log in
    def test_correct_login(self):
        #Giving login url to chrome driver
        self.driver.get('http://127.0.0.1:5000/Login')
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        #Filling username, password form and submit
        user_field.send_keys('username')
        password_field.send_keys('password')
        submit.click()
        time.sleep(1)

        #Making use of dom to get innertext by class_name 'welcome'
        welcome = self.driver.find_element_by_class_name('welcome').get_attribute('innerHTML')
        self.assertIn("What's up, username", welcome)

    #Testing if putting incorrect password, then it will return 'Invalid username or password'
    def test_incorrect_login(self):
        self.driver.get('http://127.0.0.1:5000/Login')
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        user_field.send_keys('user')
        password_field.send_keys('pass')
        submit.click()
        time.sleep(1)

        flashed = self.driver.find_element_by_id('get_flashed').get_attribute('innerHTML')
        self.assertIn('Invalid username or password', flashed)

    #Testing correct log out, if correct, it will back to welcome page
    def test_logout(self):
        self.test_correct_login()
        logout = self.driver.find_element_by_partial_link_text('Logout')
        logout.click()

        text = self.driver.find_element_by_id('info').get_attribute('innerHTML')
        self.assertIn('Welcome to quiz page', text)

    #Testing if correct register, if success, it will redirect to log in page.
    def test_register(self):
        self.driver.get('http://127.0.0.1:5000/register')
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username')
        email_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('password')
        confirm_field = self.driver.find_element_by_id('password2')
        submit = self.driver.find_element_by_id('submit')

        #If this count already in User table, then delete it
        u = User.query.filter_by(username='usernamerr').first()
        if u != None:
            db.session.delete(u)
            db.session.commit()

        user_field.send_keys('usernamerr')
        email_field.send_keys('user@namerr.com')
        password_field.send_keys('passworddd')
        confirm_field.send_keys('passworddd')
        submit.click()
        time.sleep(1)

        #Testing if we get correct rollback information
        label = self.driver.find_element_by_id('get_flashed').get_attribute('innerHTML')
        self.assertIn('Congratulations, you are now a registered user!', label)

    #Testing if we can see correct tag in link 'Quiz'
    def test_get_tag(self):
        self.test_correct_login()
        link = self.driver.find_element_by_link_text('Quiz')
        link.click()
        time.sleep(2)

        select = self.driver.find_element_by_name('tag').text
        self.assertIn('HTML1', select)



if __name__ == '__main__':
        unittest.main(verbosity=2)
