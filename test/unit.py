import unittest
from app import app, db
from app.models import User, questions,answer


class UserModelTest(unittest.TestCase):

    def setUp(self):
     #Setting test_client()
        self.app = app.test_client()
        db.create_all()
        u = User.query.filter_by(username='username').first()
     #Checking if this account alrady in User table
        if u != None:
            db.session.delete(u)
            db.session.commit()
        u1 = User(username='username', email='user@name.com')
        db.session.add(u1)
        line = '1: HTML stands for?'
        q = questions.query.filter_by(content = line).first()
     #Checking if this questions already in questions table
        if q != None:
            db.session.delete(q)
            db.session.commit()
        q1 = questions(content=line, stand_answer='a', mark=1, tag='HTML1')
        db.session.add(q1)
        db.session.commit()


    def tearDown(self):
        pass
    
    #Testing if we can correctly set password
    def test_set_pw(self):
        u = User.query.get(1)
        u.set_password('password')
        self.assertFalse(u.check_password('passw0rd'))
        self.assertTrue(u.check_password('password'))
        
    #Testing if we can get correct result from questions table
    def test_guestions(self):
        line = '1: HTML stands for?'
        self.assertEqual('HTML1', questions.query.filter_by(content = line).first().tag)



if __name__ == '__main__':
    unittest.main(verbosity=2)
