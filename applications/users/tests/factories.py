import factory
from allauth.account.models import EmailAddress
from faker import Faker
from faker.providers import misc, person

from applications.users.models import User

fake = Faker()
fake.add_provider(person)
fake.add_provider(misc)


class EmailAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    user = factory.SubFactory('aplications.users.factories.UserFactory', email_address=None)
    email = factory.SelfAttribute('user.email')
    primary = True
    verified = False


class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyFunction(fake.email)
    password = fake.password(length=8)
    name = factory.LazyFunction(fake.name)
    gender = factory.Iterator(User.Gender.choices, getter=lambda x: x[0])
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop('password', None)
        obj = super(BaseUserFactory, cls)._create(model_class, *args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj


class UserFactory(BaseUserFactory):
    email_address = factory.RelatedFactory(EmailAddressFactory, 'user')

    class Params:
        confirmed = factory.Trait(
            email_address=factory.RelatedFactory(EmailAddressFactory, 'user', verified=True)
        )
