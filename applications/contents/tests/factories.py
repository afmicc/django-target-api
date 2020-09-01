import factory
from faker import Faker
from faker.providers import lorem

from applications.contents.models import Content

fake = Faker()
fake.add_provider(lorem)


class ContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Content

    key = factory.Sequence(lambda n: 'key%04d' % n)
    title = fake.text(max_nb_chars=100)
    body = fake.text(max_nb_chars=1000)
