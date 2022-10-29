from mongoengine import connect, Document, StringField, ListField, EmailField, DictField
from decouple import config


class User(Document):
    email = EmailField(primary_key=True, required=True)
    username = StringField(required=True, max_length=20)
    password = StringField(required=True)
    unlocked_lesson = DictField(default={})
    unlocked_story = DictField(default={})
    bag = ListField(default=[])


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
        password="password",
    ).save()
