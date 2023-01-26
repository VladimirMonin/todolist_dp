import enum
import random
import string
import datetime

from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from core.models import User
from goals.models import Goal, GoalCategory
from todolist.settings import env


class BotCommands:
    goals = '/goals'
    create = '/create'
    cancel = '/cancel'


class State(enum.Enum):
    not_in_db = enum.auto()
    no_verify = enum.auto()
    wait_command = enum.auto()
    choice_category = enum.auto()
    create_goal = enum.auto()


class Command(BaseCommand):

    def handle(self, *args, **options) -> None:
        offset = 0
        tg_client = TgClient(env('TG_BOT_TOKEN'))
        state = None
        while True:
            try:
                res = tg_client.get_updates(offset=offset)
            except Exception as error:
                print(f'\n{error}', end='\n\n')
                continue
            for item in res.result:
                offset = item.update_id + 1
                chat_id = item.message.chat.id

                # Описываем состояния
                if not state and not TgUser.objects.filter(tg_id=chat_id):
                    state = State.not_in_db
                elif not TgUser.objects.get(tg_id=chat_id).user:
                    state = State.no_verify
                elif state not in (State.choice_category, State.create_goal):
                    state = State.wait_command

                # Действия в зависимости от состояний

                # Если пользователя еще нет в базе
                if state == State.not_in_db:
                    TgUser.objects.create(
                        tg_id=chat_id,
                        username=item.message.chat.username if item.message.chat.username else None,
                    )
                    state = State.no_verify

                tg_user = TgUser.objects.get(tg_id=chat_id)

                # Если пользователь не верифицирован
                if state == State.no_verify:
                    verification_code = self._generate_code(5)
                    tg_user.verification_code = verification_code
                    tg_user.save()
                    text = f'Привет! Кажется, мы еще не знакомы? Для подтверждения аккаунта ' \
                           f'введите этот код на сайте: *{verification_code}*'
                    tg_client.send_message(chat_id=chat_id, text=text)
                    continue

                # Бот ожидает команду
                if state == State.wait_command:
                    if item.message.text == BotCommands.goals:
                        text = self._get_goals(tg_user.user)
                        tg_client.send_message(chat_id=chat_id, text=text)
                    elif item.message.text == BotCommands.create:
                        categories = self._get_categories(tg_user.user)
                        text = categories['text']
                        tg_client.send_message(chat_id=chat_id, text=text)
                        state = State.choice_category
                        continue
                    else:
                        text = 'Неизвестная команда, попробуйте еще!'
                        tg_client.send_message(chat_id=chat_id, text=text)

                # Выбор категории
                if state == State.choice_category:
                    if item.message.text in [i.title for i in categories['categories']]:
                        goal_category = GoalCategory.objects.get(title=item.message.text, user=tg_user.user)
                        text = 'Введите название цели:'
                        tg_client.send_message(chat_id=item.message.chat.id, text=text)
                        state = State.create_goal
                        continue
                    elif item.message.text == BotCommands.cancel:
                        text = 'Создание цели отменено'
                        state = State.wait_command
                    else:
                        text = 'Неправильная категория. Попробуйте еще!'
                    tg_client.send_message(chat_id=item.message.chat.id, text=text)

                # Создание цели
                if state == State.create_goal:
                    goal_title = item.message.text
                    Goal.objects.create(
                        title=goal_title,
                        category=goal_category,
                        user=tg_user.user,
                        due_date=datetime.date.today() + datetime.timedelta(days=7)
                    )
                    text = 'Цель создана!'
                    tg_client.send_message(chat_id=item.message.chat.id, text=text)
                    state = State.wait_command

                print(f'{item.message.message_from.first_name}: {item.message.text}')

    @staticmethod
    def _generate_code(length: int) -> str:
        """Генерирует код верификации"""
        letters = string.digits
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def _get_goals(user: User) -> str:
        """Формирует список целей"""
        goals = Goal.objects.filter(user=user, is_deleted=False)
        return '\n'.join([f'#{i.id} - {i.title}' for i in goals])

    @staticmethod
    def _get_categories(user: User) -> dict:
        """Формирует список категорий"""
        categories = GoalCategory.objects.filter(user=user, is_deleted=False)
        cat_list = '\n'.join([f'  - _{i.title}_' for i in categories])
        text = 'Выберите категорию из списка:\n' + cat_list
        return {'categories': categories, 'text': text}
