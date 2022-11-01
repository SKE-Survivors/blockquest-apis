from mongoengine import connect, Document, StringField, ListField, EmailField, DictField, BinaryField
from decouple import config


class User(Document):
    email = EmailField(primary_key=True, required=True)
    username = StringField(required=True, max_length=20)
    password = BinaryField(required=True)
    bag = ListField(default=[])

    # todo: add default sections {section_id: False, ...}
    unlocked_lesson = DictField(default={})
    unlocked_story = DictField(default={})

    def to_dict(self):
        return {
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "bag": self.bag,
            "unlocked_lesson": self.unlocked_lesson,
            "unlocked_story": self.unlocked_story
        }


# ! temporary: just for testing
if __name__ == '__main__':
    connect(
        db=config('DB_NAME'),
        username=config('DB_USERNAME'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        authentication_source='admin',
        port=int(config('DB_PORT')),
    )

    User(
        email="first@gmail.com",
        username="username",
        password=b"password",
        unlocked_lesson={
            "L1": False,
            "L2": False,
            "L3": False,
        },
        unlocked_story={
            "S1": False,
            "S2": False,
        },
    ).save()
