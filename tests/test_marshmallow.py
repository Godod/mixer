from marshmallow import validate, fields, Schema
import pytest


class Person(Schema):
    name = fields.String()
    status = fields.String(
        required=True,
        validate=validate.OneOf(choices=('user', 'moderator', 'admin')))
    created = fields.DateTime()
    birthday = fields.Date()
    is_relative = fields.Bool()


class Pet(Schema):
    name = fields.String()
    animal_type = fields.String(default='cat')
    owner = fields.Nested(Person, many=True)
    awards = fields.List(fields.Str())


@pytest.fixture
def mixer():
    from mixer.backend.marshmallow import Mixer
    return Mixer(required=True)


def test_mixer(mixer):
    person = mixer.blend(Person)
    assert person['name']
    assert person['birthday']
    assert person['created']
    assert isinstance(person['is_relative'], bool)
    assert person['status'] in ('user', 'moderator', 'admin')

    pet = mixer.blend(Pet)
    assert pet['name']
    assert pet['animal_type'] == 'cat'
    assert pet['owner']
    assert pet['awards'] is not None
