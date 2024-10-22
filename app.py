import asyncio
import schedule

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from aiomisc import ThreadPoolExecutor

from database_config.config import TOKEN

from auth.auth_hendler import router

from queries.for_running import if_not_used

from main import main_router
from user.super_admin.handlers_for_sending_message import message_sender_super_router

from user.super_admin.handlers_for_user import router_for_user_super
from user.super_admin.super_admin_handlers import super_router

from user.admin.admin_handlers import adm_router
from user.admin.handlers_for_alphabets import router_for_alphabets
from user.admin.handlers_for_aop_panic import router_for_aop_panic
from user.admin.handlers_for_chipset import router_for_chipset
from user.admin.handlers_for_i2c import router_for_i2c
from user.admin.handlers_for_i2c_category import router_for_i2c_category
from user.admin.handlers_for_itunes import router_for_itunes
from user.admin.handlers_for_model import router_for_model
from user.admin.handlers_for_panic import router_for_panic
from user.admin.handlers_for_panic_array import router_for_panic_array
from user.admin.handlers_for_swap import router_for_swap
from user.admin.handlers_for_userspace import router_for_userspace

from user.user.handers_for_settings import user_setting_router
from user.user.handlers_for_alphabets import user_alphabets_router
from user.user.handlers_for_aop_panic import user_aop_panic_router
from user.user.handlers_for_i2c import user_i2c_router
from user.user.handlers_for_itunes import user_itunes_router
from user.user.handlers_for_panic import user_panic_router
from user.user.handlers_for_swap import user_swap_router
from user.user.handlers_for_tools import user_tools_router
from user.user.handlers_for_userspace import user_userspace_router
from user.user.user_handlers import user_router

from user.for_end import end_router

from utils.database_dumper import dump_and_send
from utils.important import balance_calculater, end_date_checker, balance_activator, message_deleter

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


async def schedule_task_for_inactivate():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    if_not_used()
    dp.include_routers(main_router,
                       router,
                       # ADMIN
                       adm_router,
                       # USER
                       user_router,
                       # ADMIN HANDLERS
                       router_for_alphabets,
                       router_for_aop_panic,
                       router_for_chipset,
                       router_for_i2c,
                       router_for_i2c_category,
                       router_for_panic,
                       router_for_panic_array,
                       router_for_userspace,
                       router_for_model,
                       router_for_swap,
                       router_for_itunes,
                       # USER HANDLERS
                       user_panic_router,
                       user_userspace_router,
                       user_aop_panic_router,
                       user_i2c_router,
                       user_alphabets_router,
                       user_setting_router,
                       user_swap_router,
                       user_itunes_router,
                       user_tools_router,
                       # SUPER ADMIN
                       super_router,
                       router_for_user_super,
                       message_sender_super_router,
                       end_router,
                       )
    await dp.start_polling(bot)


async def init():
    # Schedule the async tasks
    schedule.every().day.at("01:00").do(lambda: asyncio.create_task(balance_activator()))  # schedule async task
    schedule.every().day.at("00:30").do(lambda: asyncio.create_task(balance_calculater()))  # schedule async task
    schedule.every().day.at("00:05").do(lambda: asyncio.create_task(message_deleter()))  # schedule async task
    schedule.every().day.at("12:00").do(lambda: asyncio.create_task(end_date_checker()))  # schedule async task
    schedule.every().day.at("00:00").do(lambda: asyncio.create_task(dump_and_send()))

    # Run asyncio tasks concurrently with the schedule
    await asyncio.gather(main(), schedule_task_for_inactivate())


if __name__ == '__main__':
    # Start the scheduler in a new thread
    with ThreadPoolExecutor() as executor:
        executor.submit(schedule_task_for_inactivate)  # Run the scheduler in a background thread

        try:
            asyncio.run(init())  # Start the async event loop
        except KeyboardInterrupt:
            print("Exit")