import factory

from .models import Province, District, Subdistrict


class ProvinceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Province

    id = factory.Sequence(lambda n: n + 1)
    name_en = factory.Faker('city')
    name_th = factory.Faker('city')


class DistrictFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = District

    id = factory.Sequence(lambda n: n + 1)
    province = factory.SubFactory(ProvinceFactory)
    name_en = factory.Faker('city')
    name_th = factory.Faker('city')


class SubdistrictFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Subdistrict

    id = factory.Sequence(lambda n: n + 1)
    district = factory.SubFactory(DistrictFactory)
    name_en = factory.Faker('city')
    name_th = factory.Faker('city')
