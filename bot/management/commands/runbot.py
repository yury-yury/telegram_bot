from dataclasses import field
from typing import Callable, Dict, Any

from django.core.management import BaseCommand
from marshmallow_dataclass import dataclass

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message, GetUpdatesResponse
from goals.models import Goal, GoalCategory, BoardParticipant


@dataclass
class FSMData:
    """
    The FSMData dataclass is designed to validate incoming data and store the current state of the user dialog
    and the telegram bot.
    """
    next_handler: Callable
    data: Dict[str, Any] = field(default_factory=dict)


class Command(BaseCommand):
    """
    The Command class inherits from the base Command class from the django.core.management module. Designed
    to determine the functionality when working with a telegram bot.
    """
    help = 'The runbot command is designed to run the application with a telegram bot.'

    def __init__(self, *args, **kwargs) -> None:
        """
        The __init__ function is a method called when creating an instance of the Command class. Accepts
        any positional and named arguments. Makes a call to the base class method of the same name and supplements
        it with the creation of additional arguments.
        """
        super().__init__(*args, **kwargs)
        self.tg_client: TgClient = TgClient()
        self.client: Dict[int, FSMData] = {}

    def handle(self, *args, **options) -> None:
        """
        The handle function defines a class method to be called when entering a command. It contains the main
        functionality for organizing interaction with a telegram bot.
        """
        offset = 0
        self.stdout.write(self.style.SUCCESS('Bot started'))

        while True:
            res: GetUpdatesResponse = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset: int = item.update_id + 1
                self.handle_message(item.message)


    def handle_message(self, message: Message) -> None:
        """
        The handle_message function defines a class method for processing an incoming message. Takes as an argument
        an object of the Message class. Checks user authentication and, depending on the result, calls the appropriate
        methods of the class.
        """
        tg_user, _ = TgUser.objects.get_or_create(chat_id=message.chat.id)

        if tg_user.is_verified:
            self.handle_authorized_user(tg_user, message)
        else:
            self.handle_unauthorized_user(tg_user, message)

    def handle_unauthorized_user(self, tg_user: TgUser, message: Message) -> None:
        """

        """
        self.tg_client.send_message(chat_id=message.chat.id, text='Hello')
        tg_user.update_verification_code()
        self.tg_client.send_message(chat_id=message.chat.id, text=f'You verification code: {tg_user.verification_code}')

    def handle_authorized_user(self, tg_user: TgUser, message: Message) -> None:
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

    def handle_goals_command(self, tg_user: TgUser, message: Message) -> None:
        goals = Goal.objects.select_related('user').filter(
            category__board__participants__user=tg_user.user).exclude(is_deleted=True)
        if goals:
            text = 'Your goals:\n' + '\n'.join(f'{goal.id}) {goal.title}' for goal in goals)
        else:
            text = 'You have not goals'
        self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)

    def handle_create_command(self, tg_user: TgUser, message: Message) -> None:

        categories = GoalCategory.objects.filter(board__participants__user=tg_user.user).exclude(is_deleted=True)
        if not categories:
            self.tg_client.send_message(chat_id=tg_user.chat_id, text='You have not category')
            return

        text = 'Select category to create goal:\n' + '\n'.join(f'{category.id}) {category.title}'
                                                                for category in categories)
        self.tg_client.send_message(chat_id=tg_user.chat_id, text=text)
        self.client[tg_user.chat_id] = FSMData(next_handler=self.get_category)

    def get_category(self, tg_user: TgUser, message: Message, **kwargs) -> None:
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

    def create_goal(self, tg_user: TgUser, message: Message, **kwargs) -> None:
        category = kwargs['category']
        Goal.objects.create(category=category, user=tg_user.user, title=message.text)
        self.tg_client.send_message(chat_id=tg_user.chat_id, text='New goal created')
        self.client.pop(tg_user.chat_id, None)
