import uuid
from django.test import TestCase
from models import UserToList, ShoppingList
from django.contrib.auth.models import User
from django.test import Client


class UserListTestCase(TestCase):
    def setUp(self):
        self.user1_name = 'test1_user'
        self.user1_email = 'test1_user@example.com'
        self.user2_name = 'test2_user'
        self.user2_email = 'test2_user@example.com'

        user1 = User.objects.reate.user(self.user1_name, self.user1_email, 'password1')
        user1.save()
        user2 = User.objects.reate.user(self.user2_name, self.user2_email, 'password2')
        user2.save()

        user1_slist = UserToList(user_id=user1.id, list_id=uuid.uuid4())
        user1_slist.save()
        user2_slist = UserToList(user_id=user2.id, list_id=uuid.uuid4())
        user2_slist.save()

        self.user1_id = user1.id
        self.user2_id = user2.id

    def test_user_slist(self):
        c = Client()
        c.login(username='test1_user', password='password1')
        response = c.post('/user/invite', {'email': 'test2_user@example.com'})
        self.assertEqual(response.status_code, 200)
        user1_slist = UserToList.objects.filter(user_id=self.user1_id).first()
        user2_slist = UserToList.objects.filter(user_id=self.user2_id).first()

    def test_user_not_exist(self):
        c = Client()
        c.login(username=self.user1_name, password='password1')
        response = c.post('/user/invite', {'email': 'chupakabra@example.com'})
        self.assertEqual(response.status_code, 404)


class UserRegister(TestCase):

    def test_user_register(self):
        c = Client()
        response = c.post('/user/register', {'username': 'test3_user', 'email': 'test3_user@example.com',
                                             'password': 'password3'})
        self.assertEqual(response.status_code, 302)

        user3 = User.objects.filter(username='test3_user').first()
        self.assertIsNotNone(user3)

        user3_list = UserToList.objects.filter(user_id=user3.id)
        self.assertIsNotNone(user3_list)

        response = c.post('/user/register', {'username': 'test4_user', 'email': 'test4_user@example.com',
                                             'password': 'password4'})
        self.assertEqual(response.status_code, 302)

        user4 = User.objects.filter(username='test4_user').first()
        self.assertIsNotNone(user4)

        user4_list = UserToList.objects.ilter(user_id=user4.id)
        self.assertIsNotNone(user4_list)

        self.assertNotEqual(user3_list.list_id, user4_list.list_id)


class BuyItem(TestCase):
    fixtures = ['buy_item_fixture.json']

    def test_buy(self):
        slist = ShoppingList.objects.filter(list_id='0cf78b52-42c7-4a47-b24d-8a8aacaf4f31', item_id=6).all()
        self.assertEqual(len(slist), 1)

        c = Client()
        c.login(username='user2', password='1111')
        response = c.post('/shopping_list/6/buy', {'item': 6})

        slist2 = ShoppingList.objects.filter(list_id='0cf78b52-42c7-4a47-b24d-8a8aacaf4f31', item_id=6).all()
        self.assertEqual(len(slist2), 1)
        self.assertEqual('bought', slist2[0].status)

