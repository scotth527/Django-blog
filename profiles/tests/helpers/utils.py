from django.contrib.auth.models import User

def create_user():
    try:
        user = User.objects.create_user('john', 'youcantseeme@wwe.com', 'johnpassword')
        profile = Profile.objects.get_or_create(first_name="John", last_name="Cena", address="123 Fake Street", city="Miami", state="FL", user=user)
        return user
    except:
        # print("Exception was used")
        return User.objects.get(email = 'youcantseeme@wwe.com')

def login(client):
    client.login(username='john', password='johnpassword')