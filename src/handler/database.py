from mongoengine import connect
from decouple import config
from model.user import User
from model.section import Lesson, Story


class DatabaseHandler:
    def __init__(self):
        connect(
            db=config('DB_NAME'),
            username=config('DB_USERNAME'),
            password=config('DB_PASSWORD'),
            host=config('DB_HOST'),
            authentication_source='admin',
            port=int(config('DB_PORT')),
        )
        print("Connected to database")

    def add_user(self, mail, username, password) -> User:
        lessons = dict()
        for lesson in Lesson.objects():
            lessons[lesson.section_id] = False

        stories = dict()
        for story in Story.objects():
            stories[story.section_id] = False

        user = User(
            email=mail,
            username=username,
            password=password,
            unlocked_lesson=lessons,
            unlocked_story=stories,
        ).save()
        print(f"Added user: {mail}")
        return user

    def find_user(self, mail) -> User:
        return User.objects.get(email=mail)

    def delete_user(self, mail):
        user = self.find_user(mail)
        user.delete()
        print(f"Deleted user: {mail}")

    def update_profile(self, mail, **kwargs):
        user = self.find_user(mail)
        user.update(**kwargs)
        print(f"Updated [profile] user: {mail}")

    def unlock_section(self, mail, section_id, unlock=True):
        user = self.find_user(mail)
        section = section_id.upper()

        if section in user.unlocked_lesson.keys():
            user.unlocked_lesson[section] = unlock
            user.save()
        elif section in user.unlocked_story.keys():
            user.unlocked_story[section] = unlock
            user.save()
        else:
            raise ValueError("invalid section id")
        print(f"Updated [section status] user: {mail}")

    def update_bag(self, mail, item):
        user = self.find_user(mail)
        if item in user.bag:
            user.bag.remove(item)
        else:
            user.bag.append(item)
        user.save()
        print(f"Updated [bag item] user: {mail}")
