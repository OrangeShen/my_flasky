import unittest
import threading
import re
from selenium import webdriver
from app import create_app, db
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @staticmethod
    def setUpClass(cls):
        # start firefox
        try:
            cls.client = webdriver.firefox()
        except:
            pass
        # if can not start browser, skip these tests
        if cls.client:
            # create app
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # forbid logging
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create database, and stuff with some fake data
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            # add admin
            admin_role = Role.query.filter_by(permission=16).first()
            admin = User(email='shenjiayu@qq.com', username='fish',
                         password='cat', role=admin_role, confirmed=True)
            db.session.add(admin)
            db.session.commit()

            # start flask server in a thread
            threading.Thread(target=cls.app.run).start()

    @staticmethod
    def tearDownClass(cls):
        # shutdown flask server and browser
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove app context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        # homepage
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Hello,\s+Stranger!', self.client.page_source))

        # login page
        self.client.find_element_by_link_text('Log in').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        # login
        self.client.find_element_by_name('email').send_keys('shenjiayu@qq.com')
        self.client.find_element_by_name('password').send_keys('cat')
        self.assertTrue(re.search('Helle,\s+fish!', self.client.page_source))

        # profile page
        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>fish</h1>' in self.client.page_source)
