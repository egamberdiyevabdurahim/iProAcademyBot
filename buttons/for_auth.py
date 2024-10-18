from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


share_number_eng = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞Send Phone Number", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Send Phone Number"
)

share_number_rus = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞Отправить номер телефона", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Отправить номер телефона")

share_number_uz = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📞Telefon Raqamingizni Jo'nating", request_contact=True)]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Telefon Raqamingizni Jo'nating'")


choose_language_uz = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Inglizcha 🇺🇲", callback_data='en')],
    [InlineKeyboardButton(text="Ruscha 🇷🇺", callback_data='ru')],
    [InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data='uz')]])


choose_language_ru = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Английский 🇺🇲", callback_data='en')],
    [InlineKeyboardButton(text="Русский 🇷🇺", callback_data='ru')],
    [InlineKeyboardButton(text="Узбекский 🇺🇿", callback_data='uz')]])


choose_language_en = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="English 🇺🇲", callback_data='en')],
    [InlineKeyboardButton(text="Russian 🇷🇺", callback_data='ru')],
    [InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data='uz')]])