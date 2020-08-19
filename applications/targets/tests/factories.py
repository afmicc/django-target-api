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

    class Params:
        rootstrap_office = factory.Trait(
            title='Rootstrap office',
            latitude=-34.9071206,
            longitude=-56.2011391,
            radius=4,
        )


def default_target(user, topic):
    """Rootstrap office"""
    return TargetFactory(
        rootstrap_office=True,
        owner=user,
        topic=topic,
    )


def compatible_in_radius_target(topic):
    """
    Montenvideo Shopping
    Distance: 7km
    Compatible: Yes
    """
    return TargetFactory(
        title='Montenvideo Shopping',
        latitude=-34.9036534,
        longitude=-56.1449722,
        radius=4,
        topic=topic,
    )


def compatible_in_radius_target2(topic):
    """
    Nuevocentro Shopping
    Distance: 4.13 km
    Compatible: Yes
    """
    return TargetFactory(
        title='Nuevocentro Shopping',
        latitude=-34.8756006,
        longitude=-56.1771999,
        radius=2,
        topic=topic,
    )


def incompatible_in_radius_target(other_topic):
    """
    Rural del Prado
    Distance: 4.09 km
    Compatible: No, different topic
    """
    return TargetFactory(
        title='Rural del Prado',
        latitude=-34.8719561,
        longitude=-56.2144232,
        radius=4,
        topic=other_topic,
    )


def compatible_out_radius_target(topic):
    """
    Portones Shopping
    Distance: 11.3 km
    Compatible: No, out of range
    """
    return TargetFactory(
        title='Portones Shopping',
        latitude=-34.8811386,
        longitude=-56.0813423,
        radius=2,
        topic=topic,
    )
