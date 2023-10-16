import logging
from typing import Optional, Union

import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ConversationHandler,
)

from config.settings import env, REST_FRAMEWORK

TG_TOKEN = env.str('TG_TOKEN')
SERVICE_URL = env.str('SERVICE_URL', 'http://127.0.0.1:8000/api/v1/')
CITIES_PAGE, CONFIRM_EXIT = range(2)
LIMIT = REST_FRAMEWORK.get('PAGE_SIZE')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


async def send_message(
        update: Update,
        text: str,
        context: CallbackContext,
        reply_markup: Optional[ReplyKeyboardMarkup] = None,
) -> None:
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup
    )


async def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message."""

    keyboard = ReplyKeyboardMarkup([['Узнать погоду', 'Список городов']])
    first_name = update.effective_chat.first_name or 'Незнакомец'

    await send_message(
        update,
        f"Привет, {first_name}! Могу сообщить текущую погоду в городе России.",
        context,
        reply_markup=keyboard,
    )


async def say_city(update: Update, context: CallbackContext) -> None:
    """Request the name of the city from the user."""

    await send_message(
        update, f"Напишите, в каком городе хотите узнать погоду?", context
    )


async def get_weather(update: Update, context: CallbackContext) -> None:
    """Get weather for city from service."""

    keyboard = ReplyKeyboardMarkup([['Узнать погоду', 'Список городов']])
    city_name = update.message.text.capitalize()
    url = SERVICE_URL + 'weather/'
    response = requests.get(url, params={'city': city_name})
    weather_data = response.json()
    error = weather_data.get('error')
    if error:
        if error == f'City with name {city_name} does not exist':
            msg = (
                f'К сожалению, города с названием "{city_name}" '
                'пока нет в нашей базе. Попробуйте название другого города.'
            )
        else:
            msg = (
                f'Неожиданная ошибка, статус {response.status_code}. '
                'Повторите попытку позже.'
            )
    else:
        msg = (
            f'Прогноз погоды для {city_name}:\n'
            f'температура {weather_data.get("temperature")} °C,\n'
            f'давление {weather_data.get("pressure_mm")} мм рт. ст,\n'
            f'скорость ветра {weather_data.get("wind_speed")} м/с.'
        )

    await send_message(update, msg, context, reply_markup=keyboard)


async def send_city_list_message(
        update: Update, page: int, context: CallbackContext
) -> None:
    """
    Send a message to the specified chat ID containing a formatted list
    of city names.
    """

    limit = LIMIT
    offset = (page - 1) * limit

    url = SERVICE_URL + 'cities_list/'
    params = {'limit': limit, 'offset': offset, 'city_names': True}
    response = requests.get(url, params)
    data = response.json().get('results')

    if not data:
        await send_message(update, 'Список городов пуст.', context)
        return

    city_names = [item['name'] for item in data]
    formatted_cities = '\n'.join(
        [
            f'{index}. {city}'
            for index, city in enumerate(city_names, start=offset + 1)
        ]
    )
    await send_message(
        update,
        f'Список городов (страница {page}):\n{formatted_cities}',
        context,
    )


async def show_cities_page(update: Update, context: CallbackContext) -> int:
    """
    Show a page of city names to the user along with
    navigation options (next page, exit).
    """

    page = 1  # beginning with first page
    await send_city_list_message(update, page, context)
    keyboard = ReplyKeyboardMarkup([['Следующая страница', 'Выйти']])

    await send_message(
        update,
        'Для следующей страницы нажмите "Следующая страница".\n'
        'Для выхода нажмите "Выйти".',
        context,
        reply_markup=keyboard,
    )
    return CITIES_PAGE


async def next_page(update: Update, context: CallbackContext) -> int:
    """SHow the next page of city names to the user."""

    page = context.user_data.get('page', 1) + 1
    context.user_data['page'] = page
    await send_city_list_message(update, page, context)
    return CITIES_PAGE


async def confirm_exit(update: Update, context: CallbackContext) -> int:
    """Provide the user with a choice."""

    keyboard = ReplyKeyboardMarkup([['Да', 'Нет']])
    await send_message(
        update,
        'Вы уверены, что хотите выйти?',
        context,
        reply_markup=keyboard,
    )
    return CONFIRM_EXIT


async def handle_exit_confirmation(
        update: Update, context: CallbackContext
) -> Union[int, None]:
    """Check the user's answer."""

    keyboard = ReplyKeyboardMarkup([['Узнать погоду', 'Список городов']])
    if update.message.text == 'Да':
        await send_message(
            update,
            'Вы вышли из списка городов. Выберите действие:',
            context,
            reply_markup=keyboard,
        )
        return ConversationHandler.END
    elif update.message.text == 'Нет':
        return CITIES_PAGE


if __name__ == '__main__':
    application = ApplicationBuilder().token(TG_TOKEN).build()

    handlers = [
        CommandHandler('start', start),
        MessageHandler(filters.Regex(r'^Узнать погоду$'), say_city),
        ConversationHandler(
            entry_points=[
                MessageHandler(
                    filters.Regex(r'^Список городов$'), show_cities_page
                )
            ],
            states={
                CITIES_PAGE: [
                    MessageHandler(
                        filters.Regex(r'^Следующая страница$'), next_page
                    ),
                    MessageHandler(filters.Regex(r'^Выйти'), confirm_exit),
                ],
                CONFIRM_EXIT: [
                    MessageHandler(filters.TEXT, handle_exit_confirmation)
                ],
            },
            fallbacks=[
                MessageHandler(
                    filters.TEXT
                    & ~filters.Regex(r'^(Следующая страница|Выйти)$'),
                    show_cities_page,
                )
            ],
        ),
        MessageHandler(
            ~filters.Regex(
                r'^(Узнать погоду|Список городов|Следующая страница|Выйти)$'
            ),
            get_weather,
        ),
    ]

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling()
