from django.contrib.gis.geos import Point
import factory
from faker import Faker
from faker.providers import geo, lorem

from applications.targets.models import Target, Topic
from applications.users.tests.factories import UserFactory

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(geo)


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Sequence(lambda n: 'topic%04d' % n)


class TargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Target

    latitude = float(fake.latitude())
    longitude = float(fake.longitude())
    owner = factory.SubFactory(UserFactory)
    radius = fake.random_number()
    title = fake.sentence()
    topic = factory.SubFactory(TopicFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        latitude = kwargs.pop('latitude', None)
        longitude = kwargs.pop('longitude', None)
        kwargs['location'] = Point(latitude, longitude)
        return super(TargetFactory, cls)._create(model_class, *args, **kwargs)
