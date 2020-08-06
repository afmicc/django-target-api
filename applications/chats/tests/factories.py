import factory

from applications.targets.tests.factories import TopicFactory
from applications.chats.models import Room


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
