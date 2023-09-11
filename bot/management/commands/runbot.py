from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message, GetUpdatesResponse


class Command(BaseCommand):
    """
    The Command class inherits from the base Command class from the django.users.management module. Designed
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

    def handle(self, *args, **options) -> None:
        """
        The handle function defines a class method to be called when entering a command. It contains the main
        functionality for organizing interaction with a telegram bot.
        """
        offset: int = 0
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
        if message is not None:
            tg_user, _ = TgUser.objects.get_or_create(chat_id=message.chat.id)

            if not tg_user.is_verified:
                self.handle_unauthorized_user(tg_user, message)

    def handle_unauthorized_user(self, tg_user: TgUser, message: Message) -> None:
        """
        The handle_unauthorized_user function defines a class method for working with an unauthenticated user.
        Accept objects of the TgUser and Message classes as arguments. Sends a welcome message to the user, calls
        the method of adding the verification code to the field of the current user and sends the verification code.
        """
        self.tg_client.send_message(chat_id=message.chat.id, text='Hello')
        tg_user.update_verification_code()
        self.tg_client.send_message(chat_id=message.chat.id, text=f'You verification code: {tg_user.verification_code}')
