from django.contrib.auth.models import User, Group
from users.apps import PLAN_BASIC, PLAN_PREMIUM, PLAN_ENTERPRISE


class TempUsers:
    basic = {'username': 'basicUser', 'email': 'user@basic.com', 'password': 'xDqz8JTxdZrClc7xOHq2Px'}
    premium = {'username': 'premiumUser', 'email': 'user@premium.com', 'password': 'dUR7aqq5Gt7kxWhHp8ew6e'}
    enterprise = {'username': 'enterpriseUser', 'email': 'user@enterprise.com', 'password': '9Q2nHRIenRLyUiLCRugQs9'}

    # Can't be populated in a standard pyTest fixture, because they are loaded before the post_migrate signal,
    # After which the standard user-tiers are loaded
    @staticmethod
    def populate_users():
        basic = User.objects.create_user(TempUsers.basic['username'], TempUsers.basic['email'], TempUsers.basic['password'])
        basic.groups.add(Group.objects.get(name=PLAN_BASIC))

        premium = User.objects.create_user(TempUsers.premium['username'], TempUsers.premium['email'],
                                           TempUsers.premium['password'])
        premium.groups.add(Group.objects.get(name=PLAN_PREMIUM))

        enterprise = User.objects.create_user(TempUsers.enterprise['username'], TempUsers.enterprise['email'],
                                              TempUsers.enterprise['password'])
        enterprise.groups.add(Group.objects.get(name=PLAN_ENTERPRISE))
