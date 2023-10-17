=====
TG Core from Oscar
=====

Telegram bot core, created in django style with routing and views(handlers) where you
can use included builders for menu or messages

Quick start
-----------

1. Install package::

    pip install django-oscarbot

2. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "oscarbot",
    ]

2. In ``settings.py`` file you need to specify application for tg use::

    OSCARBOT_APPS = ['main']

    # set Telegram api url:
    TELEGRAM_URL = ''
    # set Telegram message parse mode:
    TELEGRAM_PARSE_MODE = 'HTML'
    # or
    TELEGRAM_PARSE_MODE = 'MARKDOWN'


3. Run ``python manage.py migrate`` to create the oscarbot models.

4. Run django server and open http://localhost:8000/admin/ and create new bot,
at least fill bot token for testing ability

Features
--------

* User model::

    from oscarbot.models import User

    some_user = User.objects.filter(username='@maslov_oa').first()


* Menu and Buttons builder::

    from oscarbot.menu import Menu, Button


    button_list = [
        Button(text='Text for callback', callback='/some_callback/'),
        Button(text='Text for external url', url='https://oscarbot.site/'),
    ]

    menu = Menu(button_list)


* Message builder::

    from oscarbot.shortcut import QuickBot

    quick_bot = QuickBot(
        chat=111111111,
        message='Hello from command line',
        token='token can be saved in DB and not required'
    )
    quick_bot.send()

* Long polling server for testing::

    python manage.py runbot


* Update messages available::

    # TODO: work in progress


* Messages log::

    # TODO: work in progress
