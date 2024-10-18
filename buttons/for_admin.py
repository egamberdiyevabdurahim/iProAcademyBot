from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


admin_main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Apple Management")],
    [KeyboardButton(text="Android Management")],
    [KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


# APPLE MANAGEMENT
apple_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Panic Array Management"), KeyboardButton(text="Panic Management")],
    [KeyboardButton(text="UserSpace Management"), KeyboardButton(text="Alphabet Management")],
    [KeyboardButton(text="Chipset Management"), KeyboardButton(text="i2c Category Management")],
    [KeyboardButton(text="i2c Management"), KeyboardButton(text="AOP Panic Management")],
    [KeyboardButton(text="Model Management"), KeyboardButton(text="Swap Helper Management")],
    [KeyboardButton(text="iTunes Management")],
    [KeyboardButton(text="🔙Back to Admin Menu Management"), KeyboardButton(text="🔝Main Menu")]],
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


user_space_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add User Space"), KeyboardButton(text="Delete User Space")],
    [KeyboardButton(text="Edit User Space"), KeyboardButton(text="Show User Spaces")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


alphabet_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Alphabet"), KeyboardButton(text="Delete Alphabet")],
    [KeyboardButton(text="Edit Alphabet"), KeyboardButton(text="Show Alphabets")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
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


aop_panic_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add AOP Panic"), KeyboardButton(text="Delete AOP Panic")],
    [KeyboardButton(text="Edit AOP Panic"), KeyboardButton(text="Show AOP Panics")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


model_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Model"), KeyboardButton(text="Delete Model")],
    [KeyboardButton(text="Edit Model"), KeyboardButton(text="Show Models")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


swap_helper_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add Swap Helper"), KeyboardButton(text="Delete Swap Helper")],
    [KeyboardButton(text="Edit Swap Helper"), KeyboardButton(text="Show Swap Helpers")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


itunes_management_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Add iTunes"), KeyboardButton(text="Delete iTunes")],
    [KeyboardButton(text="Edit iTunes"), KeyboardButton(text="Show All iTunes")],
    [KeyboardButton(text="🔙Back To Apple Management"), KeyboardButton(text="🔝Main Menu")]],
    resize_keyboard=True,
    input_field_placeholder="Choose")


# ANDROID MANAGEMENT
# COMING SOON
