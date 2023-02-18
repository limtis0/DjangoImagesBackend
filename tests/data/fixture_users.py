from django.contrib.auth.models import User, Group
from users.apps import PLAN_BASIC, PLAN_PREMIUM, PLAN_ENTERPRISE


class Users:
    basic = {'login': 'basicUser', 'email': 'user@basic.com', 'password': 'password'}
    premium = {'login': 'premiumUser', 'email': 'user@premium.com', 'password': 'password'}
    enterprise = {'login': 'enterpriseUser', 'email': 'user@enterprise.com', 'password': 'password'}

    # Can't be populated in a standard pyTest fixture, because they are loaded before the post_migrate signal,
    # After which the standard user-tiers are loaded
    @staticmethod
    def populate_users():
        basic = User.objects.create_user(Users.basic['login'], Users.basic['email'], Users.basic['password'])
        Group.objects.get(name=PLAN_BASIC).user_set.add(basic)

        premium = User.objects.create_user(Users.premium['login'], Users.premium['email'], Users.premium['password'])
        Group.objects.get(name=PLAN_PREMIUM).user_set.add(premium)

        enterprise = User.objects.create_user(Users.enterprise['login'], Users.enterprise['email'],
                                              Users.enterprise['password'])
        Group.objects.get(name=PLAN_ENTERPRISE).user_set.add(enterprise)
