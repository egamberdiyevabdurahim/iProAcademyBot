from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


before_user_management_menu_super = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="User Management")],
    [KeyboardButton(text="Pending User Management")],
    [KeyboardButton(text="Admin Management")],
    [KeyboardButton(text="🔙Back to Admin Menu Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


admin_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Admin"), KeyboardButton(text="Delete Admin")],
    [KeyboardButton(text="Show Admins")],
    [KeyboardButton(text="🔙Back to User Menu"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")
