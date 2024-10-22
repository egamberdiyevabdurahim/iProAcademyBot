from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


super_admin_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Users Management")],
    [KeyboardButton(text="Apple Management")],
    [KeyboardButton(text="Android Management")],
    [KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


before_user_management_menu_super = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="User Management")],
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


user_management_menu_super = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Delete User")],
    [KeyboardButton(text="Edit User"), KeyboardButton(text="Show Users")],
    [KeyboardButton(text="Show User Log"), KeyboardButton(text="Show All Users Log")],
    [KeyboardButton(text="Activate User"), KeyboardButton(text="InActivate User")],
    [KeyboardButton(text="Schedule Activate User"), KeyboardButton(text="Show Active Users")],
    [KeyboardButton(text="🔙Back to User Menu"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


activate_user_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="for a Month", callback_data="for_month")],
    [InlineKeyboardButton(text="for 3 Months", callback_data="for_three_month")],
    [InlineKeyboardButton(text="for 6 Months", callback_data="for_six_month")],
    [InlineKeyboardButton(text="for 9 Months", callback_data="for_nine_month")],
    [InlineKeyboardButton(text="for a Year", callback_data="for_year")]])
