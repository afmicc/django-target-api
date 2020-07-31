import factory
from faker import Faker
from faker.providers import lorem

from applications.notifications.models import Notification
from applications.users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(lorem)


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    title = fake.text(max_nb_chars=20)
    message = fake.text(max_nb_chars=50)
