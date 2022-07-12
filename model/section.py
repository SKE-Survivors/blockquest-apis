from mongoengine import *
from decouple import config


class Lesson(Document):
    section_id = StringField(required=True, unique=True, max_length=5)
    name = StringField(required=True, max_length=50)
    description = StringField(required=True, max_length=200)
    next_lesson = ListField(default=[])


class Story(Document):
    section_id = StringField(required=True, unique=True, max_length=5)
    name = StringField(required=True, max_length=50)


# ! temporary: tools to add sections
if __name__ == '__main__':
    connect(
        db=config('DB_NAME'),
        username=config('DB_USERNAME'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST'),
        authentication_source='admin',
        port=int(config('DB_PORT')),
    )

    Lesson(
        section_id="L1",
        name="intro",
        description="",
        next_lesson=["L2", "L3"],
    ).save()

    Lesson(
        section_id="L2",
        name="get start",
        description="happy101",
    ).save()

    Lesson(
        section_id="L3",
        name="go big or go home",
        description="what the hex",
    ).save()

    Story(
        section_id="S1",
        name="ติดเกาะ",
    ).save()

    Story(
        section_id="S2",
        name="หนีจากหมี",
    ).save()
