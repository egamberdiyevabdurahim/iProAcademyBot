from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


admin_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Users Management")],
    [KeyboardButton(text="Apple Management")],
    [KeyboardButton(text="Android Management")],
    [KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


before_user_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="User Management")],
    [KeyboardButton(text="Pending User Management")],
    [KeyboardButton(text="🔙Back to Admin Menu Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


user_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add User"), KeyboardButton(text="Delete User")],
    [KeyboardButton(text="Edit User"), KeyboardButton(text="Show Users")],
    [KeyboardButton(text="Show User Log"), KeyboardButton(text="Show All Users Log")],
    [KeyboardButton(text="Activate User"), KeyboardButton(text="Show Active Users")],
    [KeyboardButton(text="Show All Balances")],
    [KeyboardButton(text="🔙Back to User Menu"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


activate_user_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="for a Month", callback_data="for_month")],
    [InlineKeyboardButton(text="for 3 Months", callback_data="for_three_month")],
    [InlineKeyboardButton(text="for 6 Months", callback_data="for_six_month")],
    [InlineKeyboardButton(text="for 9 Months", callback_data="for_nine_month")],
    [InlineKeyboardButton(text="for a Year", callback_data="for_year")]])


edit_user_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="First Name"), KeyboardButton(text="Last Name")],
    [KeyboardButton(text="Phone Number")],
    [KeyboardButton(text="🔙Back"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


pending_user_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Pending User"), KeyboardButton(text="Delete Pending User")],
    [KeyboardButton(text="Show Pending Users")],
    [KeyboardButton(text="🔙Back to User Menu"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


# APPLE MANAGEMENT
apple_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Panic Array Management"), KeyboardButton(text="Panic Management")],
    [KeyboardButton(text="UserSpace Management"), KeyboardButton(text="Alphabet Management")],
    [KeyboardButton(text="Chipset Management"), KeyboardButton(text="i2c Category Management")],
    [KeyboardButton(text="i2c Management"), KeyboardButton(text="AOP Panic Management")],
    [KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


array_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Panic Array"), KeyboardButton(text="Delete Panic Array")],
    [KeyboardButton(text="Edit Panic Array"), KeyboardButton(text="Show Panic Arrays")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


panic_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Panic"), KeyboardButton(text="Delete Panic")],
    [KeyboardButton(text="Edit Panic"), KeyboardButton(text="Show Panics")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


edit_panic_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Name"), KeyboardButton(text="Code")],
    [KeyboardButton(text="Array")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


user_space_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add User Space"), KeyboardButton(text="Delete User Space")],
    [KeyboardButton(text="Edit User Space"), KeyboardButton(text="Show User Spaces")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


edit_user_space_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Name"), KeyboardButton(text="Code")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


alphabet_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Alphabet"), KeyboardButton(text="Delete Alphabet")],
    [KeyboardButton(text="Edit Alphabet"), KeyboardButton(text="Show Alphabets")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


edit_alphabet_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Name"), KeyboardButton(text="Code")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


chipset_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Chipset"), KeyboardButton(text="Delete Chipset")],
    [KeyboardButton(text="Edit Chipset"), KeyboardButton(text="Show Chipsets")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


i2c_category_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add i2c Category"), KeyboardButton(text="Delete i2c Category")],
    [KeyboardButton(text="Edit i2c Category"), KeyboardButton(text="Show i2c Categories")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


i2c_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add i2c"), KeyboardButton(text="Delete i2c")],
    [KeyboardButton(text="Edit i2c"), KeyboardButton(text="Show i2cs")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


edit_i2c_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Name")],
    [KeyboardButton(text="Chipset")],
    [KeyboardButton(text="Category")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


aop_panic_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add AOP Panic"), KeyboardButton(text="Delete AOP Panic")],
    [KeyboardButton(text="Edit AOP Panic"), KeyboardButton(text="Show AOP Panics")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


edit_aop_panic_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Name"), KeyboardButton(text="Code")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


# ANDROID MANAGEMENT
# COMING SOON
