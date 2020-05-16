from app import app, db
import unittest, os, time
from app.models import User, questions
from flask_login import current_user
from selenium import webdriver

basedir = os.path.abspath(os.path.dirname(__file__))


class FlaskTestCase(unittest.TestCase):
    driver = None
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=os.path.join(basedir, 'chromedriver'))
        if not self.driver:
            self.skipTest
        else:
            db.init_app(app)
            db.create_all()
            db.session.query(User).delete()
            self.app = app.test_client()
            db.session.query(User).delete()
            s1 = User(id = 1, username = 'username', email = 'user@name.com')
            s1.set_password('password')
            db.session.add(s1)
            db.session.commit()
            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')


    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.commit()
            db.session.remove()


    def test_correct_login(self):
        self.driver.get('http://127.0.0.1:5000/Login')
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username')
        password_field = self.driver.find_element_by_id('password')
        submit = self.driver.find_element_by_id('submit')

        user_field.send_keys('username')
        password_field.send_keys('password')
        submit.click()
        time.sleep(1)

        welcome = self.driver.find_element_by_class_name('welcome').get_attribute('innerHTML')
        self.assertIn("What's up, username", welcome)

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


    def test_logout(self):
        self.test_correct_login()
        logout = self.driver.find_element_by_partial_link_text('Logout')
        logout.click()

        text = self.driver.find_element_by_id('info').get_attribute('innerHTML')
        self.assertIn('Welcome to quiz page', text)

    def test_register(self):
        self.driver.get('http://127.0.0.1:5000/register')
        time.sleep(1)
        user_field = self.driver.find_element_by_id('username')
        email_field = self.driver.find_element_by_id('email')
        password_field = self.driver.find_element_by_id('password')
        confirm_field = self.driver.find_element_by_id('password2')
        submit = self.driver.find_element_by_id('submit')

        user_field.send_keys('username2')
        email_field.send_keys('user@name2.com')
        password_field.send_keys('password2')
        confirm_field.send_keys('password2')
        submit.click()
        time.sleep(1)

        label = self.driver.find_element_by_id('label').get_attribute('innerHTML')
        self.assertIn('Please fill your personal information:', label)



if __name__ == '__main__':
        unittest.main(verbosity=2)
