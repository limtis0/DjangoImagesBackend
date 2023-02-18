from django.contrib.auth.models import User, Group
from users.apps import PLAN_BASIC, PLAN_PREMIUM, PLAN_ENTERPRISE


class Users:
    basic = {'username': 'basicUser', 'email': 'user@basic.com', 'password': 'password'}
    premium = {'username': 'premiumUser', 'email': 'user@premium.com', 'password': 'password'}
    enterprise = {'username': 'enterpriseUser', 'email': 'user@enterprise.com', 'password': 'password'}

    # Can't be populated in a standard pyTest fixture, because they are loaded before the post_migrate signal,
    # After which the standard user-tiers are loaded
    @staticmethod
    def populate_users():
        basic = User.objects.create_user(Users.basic['username'], Users.basic['email'], Users.basic['password'])
        basic.groups.add(Group.objects.get(name=PLAN_BASIC))

        premium = User.objects.create_user(Users.premium['username'], Users.premium['email'], Users.premium['password'])
        premium.groups.add(Group.objects.get(name=PLAN_PREMIUM))

        enterprise = User.objects.create_user(Users.enterprise['username'], Users.enterprise['email'],
                                              Users.enterprise['password'])
        enterprise.groups.add(Group.objects.get(name=PLAN_ENTERPRISE))
