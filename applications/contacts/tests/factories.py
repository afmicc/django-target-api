import factory
from faker import Faker
from faker.providers import lorem

from applications.contacts.models import Contact
from applications.users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(lorem)


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    email = fake.email()
    message = fake.text(max_nb_chars=500)

    class Params:
        with_writer = factory.Trait(
            writer=factory.SubFactory(UserFactory)
        )
