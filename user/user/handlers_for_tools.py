from time import sleep

import requests

from aiogram import Router, F
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from buttons.for_user import manual_imei_generator_menu_uz, manual_imei_generator_menu_ru, \
    manual_imei_generator_menu_en
from database_config.config import FIRST_API_KEY, FIRST_API_URL
from queries.for_imei import insert_imei_866_query, insert_imei_860_query, insert_imei_355_query, insert_imei_358_query, \
    get_imei_866_by_imei_query, get_imei_860_by_imei_query, get_imei_355_by_imei_query, get_imei_358_by_imei_query
from queries.for_users import get_user_by_telegram_id_query
from states.user_states import ImeiCheckerState, ImeiGeneratorState
from user.user.user_handlers import imei_generator_go
from utils.activity_maker import activity_maker
from utils.addititons import IMEI, FOR_IMEI, BUTTONS_AND_COMMANDS
from utils.for_auth import is_user_registered
from utils.proteceds import send_protected_message
from utils.validator import is_active, not_active_message, not_registered_message

user_tools_router = Router()


@user_tools_router.message(ImeiCheckerState.imei)
async def imei_checker_input(message: Message, state: FSMContext):
    if len(message.text) == 15:
        await state.update_data(imei=message.text)
        language = get_user_by_telegram_id_query(message.from_user.id)['language_code']

        api_url = f"{FIRST_API_URL}api.php"

        params = {
            'format': 'json',
            'key': FIRST_API_KEY,
            'imei': message.text,
            'service': 'demo'
        }

        headers = {
            'User-Agent': 'Your User Agent',
            'Accept': 'application/json',
        }

        response = requests.get(api_url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        if data['status'] is True:
            result = data['result'].split('<br>')
            a = ':'.join(result).split(':')
            b = '\n'.join(a).split('\n')
            full_uz = (f"{b[0]}:{b[1]}\n"
                       f"Ishlab chiqaruvchi:{b[3]}\n"
                       f"Model kodi:{b[5]}\n"
                       f"Model nomi:{b[7]}")

            full_ru = (f"{b[0]}:{b[1]}\n"
                       f"Производитель:{b[3]}\n"
                       f"Модель Код:{b[5]}\n"
                       f"Название модели:{b[7]}")

            full_en = (f"{b[0]}:{b[1]}\n"
                       f"Manufacturer:{b[3]}\n"
                       f"Model Code:{b[5]}\n"
                       f"Model Name:{b[7]}")

            if language == 'uz':
                await message.answer(text=full_uz, protect_content=True)

            elif language == 'ru':
                await message.answer(text=full_ru, protect_content=True)

            else:
                await message.answer(text=full_en, protect_content=True)

        else:
            await send_protected_message(message, content='Xatolik!')

        await state.clear()

    else:
        await send_protected_message(message, content='Imei 15 ta raqamli bo`lishmadingiz!')


async def imei_is_available(imei):
    if imei[:3] == '866':
        return get_imei_866_by_imei_query(imei) is not None

    elif imei[:3] == '860':
        return get_imei_860_by_imei_query(imei) is not None

    elif imei[:3] == '355':
        return get_imei_355_by_imei_query(imei) is not None

    elif imei[:3] == '358':
        return get_imei_358_by_imei_query(imei) is not None


async def get_imei_from_my_imei(imei):
    for i in IMEI:
        if i.startswith(imei):
            return i
    return None


import random


async def luhn(imei):
    step2a = 0
    step2b = 0

    while len(imei) < 14:
        imei += "0"

    for i in range(1, 14, 2):
        step1 = str(int(imei[i]) * 2).zfill(2)
        step2a += int(step1[0]) + int(step1[1])

    for i in range(0, 14, 2):
        step2b += int(imei[i])

    step2 = step2a + step2b

    if step2 % 10 == 0:
        step3 = 0
    else:
        step3 = 10 - step2 % 10

    return step3


async def generate_imei_suffix():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))


async def random_prefix(pre):
    return random.choice(pre)


async def generate_imei(prefix, user_id):
    pre = prefix.split('\n')
    imei = await random_prefix(pre)
    suffix = await generate_imei_suffix()
    gen = imei + suffix + str(await luhn(imei + suffix))

    if await imei_is_available(gen):
        return await generate_imei(prefix, user_id)

    if gen[:3] == '866':
        insert_imei_866_query(imei=gen, user_id=user_id)

    elif gen[:3] == '860':
        insert_imei_860_query(imei=gen, user_id=user_id)

    elif gen[:3] == '355':
        insert_imei_355_query(imei=gen, user_id=user_id)

    elif gen[:3] == '358':
        insert_imei_358_query(imei=gen, user_id=user_id)

    return gen


async def generate_all(imei_count, prefix, user_id):
    imei_list = dict()

    counter = 0
    for _ in range(imei_count):
        counter += 1
        imei_for_generate = await get_imei_from_my_imei(prefix)
        imei_list[str(counter)] = [str(await generate_imei(imei_for_generate, user_id))]

    counter = 0
    for _ in range(imei_count):
        counter += 1
        imei_list[str(counter)].append(await generate_second_imei(imei_list[str(counter)][0], user_id))

    return imei_list


async def luhn_second(imei):
    step2a = 0
    step2b = 0

    # Ensure the IMEI is 14 digits for Luhn check
    imei = imei.ljust(14, '0')

    # Step 2a: Multiply every second digit by 2 and sum their digits
    for i in range(1, 14, 2):
        step1 = int(imei[i]) * 2
        step2a += step1 // 10 + step1 % 10

    # Step 2b: Sum the other digits
    for i in range(0, 14, 2):
        step2b += int(imei[i])

    # Step 2: Total sum
    step2 = step2a + step2b

    # Step 3: Calculate check digit
    if step2 % 10 == 0:
        return 0
    else:
        return 10 - (step2 % 10)


# Function to generate the second IMEI based on the first one
async def generate_second_imei(first, user_id):
    # Extract the first 8 digits of the original IMEI (TAC code)
    tac = first[:8]

    # Generate a new random 6-digit serial number (can also increment existing)
    serial_number = first[8:14]
    new_serial = str(int(serial_number) + 1).zfill(6)  # Increment serial number

    # Generate a new IMEI by combining TAC and new serial number
    new_imei = tac + new_serial

    # Calculate the new Luhn check digit
    check_digit = await luhn_second(new_imei)
    imei = str(new_imei + str(check_digit))

    if await imei_is_available(imei):
        return await generate_second_imei(first, user_id)

    if imei[:3] == '866':
        insert_imei_866_query(imei=imei, user_id=user_id)

    elif imei[:3] == '860':
        insert_imei_860_query(imei=imei, user_id=user_id)

    elif imei[:3] == '355':
        insert_imei_355_query(imei=imei, user_id=user_id)

    elif imei[:3] == '358':
        insert_imei_358_query(imei=imei, user_id=user_id)

    # Return the complete second IMEI
    return imei


@user_tools_router.message(F.text.in_({"866XXX", "860XXX", "355XXX", "358XXX"}))
async def imei_generator_go2(message: Message):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            user_id = get_user_by_telegram_id_query(message.from_user.id)['id']
            imei = message.text[:3]
            imei_for_generate = await get_imei_from_my_imei(imei)
            first_imei = await generate_imei(imei_for_generate, user_id)
            second_imei = await generate_second_imei(first_imei, user_id)
            await message.answer(text=f"1) {first_imei}\n"
                                      f"2) {second_imei}")

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_tools_router.message(F.text.in_({"Manual", "Вручной"}))
async def imei_manual_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            language = get_user_by_telegram_id_query(message.from_user.id)['language_code']
            if language == "uz":
                await message.answer(reply_markup=manual_imei_generator_menu_uz,
                                     text="Ushbu IMEI lar uzimei tizimida Talab etilmaydigan imei lar!", protect_content=True)

            elif language == "ru":
                await message.answer(reply_markup=manual_imei_generator_menu_ru,
                                     text="Эти IMEI являются ненужными имейсами в системе uzimei!", protect_content=True)

            elif language == "en":
                await message.answer("These IMEIs are Unnecessary IMEI in the uzimei system!",
                                     reply_markup=manual_imei_generator_menu_en, protect_content=True)

            await state.set_state(ImeiGeneratorState.prefix)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_tools_router.callback_query(ImeiGeneratorState.prefix)
async def imei_prefix_go(callback: CallbackQuery, state: FSMContext):
    if is_user_registered(callback.from_user.id):
        if await is_active(callback.message, callback.from_user.id):
            await activity_maker(callback.message, callback.from_user.id)
            language = get_user_by_telegram_id_query(callback.from_user.id)['language_code']
            prefix = callback.data
            await callback.message.delete()
            if prefix not in FOR_IMEI:
                await callback.message.answer("Error!", protect_content=True)
                await state.clear()
                await imei_generator_go(callback.message)
                return

            if language == "uz":
                await callback.message.answer("Sonini Kiriting:", protect_content=True)
            elif language == "ru":
                await callback.message.answer("Введите количество:", protect_content=True)
            elif language == "en":
                await callback.message.answer("Enter Quantity:", protect_content=True)

            await state.update_data(prefix=str(prefix[:3]))

            await state.set_state(ImeiGeneratorState.count)

        else:
            await not_active_message(callback.message)

    else:
        await not_registered_message(callback.message)


@user_tools_router.message(ImeiGeneratorState.count)
async def imei_count_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)
            count = message.text
            if count in BUTTONS_AND_COMMANDS:
                await send_protected_message(message, f"Try Again!")
                await state.clear()
                await imei_generator_go(message)
                return

            if not count.isnumeric():
                await send_protected_message(message, f"Error!")
                await state.clear()
                await imei_generator_go(message)
                return

            if int(count) <= 0:
                await send_protected_message(message, f"Error!")
                await state.clear()
                await imei_generator_go(message)
                return

            await message.chat.do(action=ChatAction.TYPING)

            state_data = await state.get_data()
            prefix = state_data.get('prefix')

            imei_list = await generate_all(int(count), prefix, get_user_by_telegram_id_query(message.from_user.id)['id'])

            full_data = ""
            counter = 0
            for key, imei in imei_list.items():
                counter += 1
                if counter == int(count):
                    full_data += (f"{key}:\n"
                                  f"    1){imei[0]}\n"
                                  f"    2){imei[1]}\n")
                else:
                    full_data += (f"{key}:\n"
                                  f"    1){imei[0]}\n"
                                  f"    2){imei[1]}\n"
                                  f"-•-•-•-•-•-•-•-•-•-\n")

            split_messages = [full_data[i:i + 3390] for i in range(0, len(full_data), 3390)]
            for chunk in split_messages:
                await message.answer(chunk)
                sleep(1.5)

            await state.clear()

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)


@user_tools_router.message(F.text.in_({"🔙Back To IMEI generator Menu", "🔙IMEI generator menyusiga qaytish", "🔙Вернуться в IMEI Генератор меню"}))
async def imei_back_go(message: Message, state: FSMContext):
    if is_user_registered(message.from_user.id):
        if await is_active(message):
            await activity_maker(message)

            await imei_generator_go(message)

        else:
            await not_active_message(message)

    else:
        await not_registered_message(message)
