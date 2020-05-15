import unittest
from app import app, db
from app.models import User


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        # make sure database is empty
        #db.session.query(User).delete()
        db.create_all()
        u = User(id=1, username='username', email='user@name.com')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_set_pw(self):
        u = User.query.get(1)
        u.set_password('password')
        self.assertFalse(u.check_password('passw0rd'))
        self.assertTrue(u.check_password('password'))
        print('pw is ok')


if __name__ == '__main__':
    unittest.main(verbosity=2)
