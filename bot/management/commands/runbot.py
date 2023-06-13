from dataclasses import field
from typing import Callable, Dict, Any

from django.core.management import BaseCommand
from marshmallow_dataclass import dataclass

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, Board, GoalCategory, BoardParticipant


@dataclass
class FSMData:
    next_handler: Callable
    data: Dict[str, Any] = field(default_factory=dict)


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()
        self.client: Dict[int, FSMData] = {}

    def handle(self, *args, **options):
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started'))
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)


    def handle_message(self, message: Message):
        # self.tg_client.send_message(chat_id=message.chat.id, text=message.text)
        tg_user, _ = TgUser.objects.get_or_create(chat_id=message.chat.id)
        if tg_user.is_verified:
            self.handle_authorized_user(tg_user, message)
        else:
            self.handle_unauthorized_user(tg_user, message)

    def handle_unauthorized_user(self, tg_user: TgUser, message: Message):
        self.tg_client.send_message(chat_id=message.chat.id, text='Hello')
        tg_user.update_verification_code()
        self.tg_client.send_message(chat_id=message.chat.id, text=f'You verification code: {tg_user.verification_code}')

    def handle_authorized_user(self, tg_user: TgUser, message: Message):
        if message.text and message.text.startswith('/'):

            if message.text == '/goals':
                self.handle_goals_command(tg_user=tg_user, message=message)

            elif message.text == '/create':
                self.handle_create_command(tg_user=tg_user, message=message)

            elif message.text == '/cancel':
                self.client.pop(tg_user.chat_id, None)
                self.tg_client.send_message(chat_id=tg_user.chat_id, text='Canceled')

            else:
                self.tg_client.send_message(chat_id=message.chat.id, text='Command not found')

        elif tg_user.chat_id in self.client:
            client = self.client[tg_user.chat_id]
            client.next_handler(tg_user=tg_user, message=message, **client.data)

    def handle_goals_command(self, tg_user: TgUser, message: Message):
        goals = Goal.objects.select_related('user').filter(
            category__board__participants__user=tg_user.user).exclude(is_deleted=True)
        if goals:
            text = 'Your goals:\n' + '\n'.join(f'{goal.id}) {goal.title}' for goal in goals)
        else:
            text = 'You have not goals'
        self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)

    def handle_create_command(self, tg_user: TgUser, message: Message):

        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user).exclude(is_deleted=True)
        if not categories:
            self.tg_client.send_message(chat_id=tg_user.chat_id, text='You have not category')
            return

        text = 'Select category to create goal:\n' + '\n'.join(f'{category.id}) {category.title}'
                                                                for category in categories)
        self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)
        self.client[tg_user.chat_id] = FSMData(next_handler=self.get_category)

    def get_category(self, tg_user: TgUser, message: Message, **kwargs):
        try:
            category = GoalCategory.objects.get(pk=message.text)
        except GoalCategory.DoesNotExist:
            self.tg_client.send_message(chat_id=tg_user.chat_id, text='Category not found')
        else:
            participant = BoardParticipant.objects.filter(board=category.board, user=tg_user.user)[0]
            if participant.role in [1, 2]:
                self.client[tg_user.chat_id].next_handler = self.create_goal
                self.client[tg_user.chat_id].data = {'category': category}
                self.tg_client.send_message(chat_id=tg_user.chat_id, text='Set goal title')

            else:
                self.tg_client.send_message(chat_id=tg_user.chat_id,
                                            text='You cannot create a goal in the selected category.')

    def create_goal(self, tg_user: TgUser, message: Message, **kwargs):
        category = kwargs['category']
        Goal.objects.create(category=category, user=tg_user.user, title=message.text)
        self.tg_client.send_message(chat_id=tg_user.chat_id, text='New goal created')
        self.client.pop(tg_user.chat_id, None)
