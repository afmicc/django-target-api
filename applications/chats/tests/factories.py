import factory
from faker import Faker
from faker.providers import lorem

from applications.chats.models import Message, Room
from applications.targets.tests.factories import TopicFactory
from applications.users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(lorem)


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    topic = factory.SubFactory(TopicFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for member in extracted:
                self.members.add(member)


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    content = fake.text(max_nb_chars=250)
    room = factory.SubFactory(RoomFactory)
    writer = factory.SubFactory(UserFactory)
