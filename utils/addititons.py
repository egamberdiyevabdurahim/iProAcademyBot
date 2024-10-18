import os

PATTERN = r"^\+?[\d\s]{10,15}$"

ADMIN_LINK = "@iProServis"


# Setting the base path
BASE_PATH = os.path.dirname(__file__)


ALPHABETS = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
    "U", "V", "W", "X", "Y", "Z"
]


IMEI = [
    '86962503',
    '86024903',
    '35851102',
    '86644903',
    '35591104',
    '86963203',
    '86489501',
    '86099802',
    '01220700',
    '86547203',
    '86307101',
    '86520503',
]


FOR_IMEI = [
    "866XXX",
    "860XXX",
    "355XXX",
    "358XXX"
]


BUTTONS_AND_COMMANDS = [
    # Commands
    "/start",
    "/help",
    "/dev",

    # BUTTONS
    # ADMIN BUTTONS
    "Users Management",
    "Apple Management",
    "Android Management",
    "🔝Main Menu",
    "User Management",
    "Pending User Management",
    "🔙Back to Admin Menu Management",

    "Add User",
    "Delete User",
    "Edit User",
    "Show Users",
    "Show User Log",
    "Show All Users Log",
    "Activate User",
    "Show Active Users",
    "Show All Balances",
    "🔙Back to User Menu"
    
    "Add Pending User",
    "Delete Pending User",
    "Show Pending Users",

    "Panic Array Management",
    "Panic Management",
    "UserSpace Management",
    "Alphabet Management",
    "Chipset Management",
    "i2c Category Management",
    "i2c Management",
    "AOP Panic Management",
    "Model Management",
    "Swap Helper Management",
    "iTunes Management",

    "Add Panic Array",
    "Delete Panic Array",
    "Edit Panic Array",
    "Show Panic Arrays",
    "🔙Back To Apple Management",

    "Add Panic",
    "Delete Panic",
    "Edit Panic",
    "Show Panics",

    "Add User Space",
    "Delete User Space",
    "Edit User Space",
    "Show User Spaces",

    "Add Alphabet",
    "Delete Alphabet",
    "Edit Alphabet",
    "Show Alphabets",

    "Add Chipset",
    "Delete Chipset",
    "Edit Chipset",
    "Show Chipsets",

    "Add i2c Category",
    "Delete i2c Category",
    "Edit i2c Category",
    "Show i2c Categories",

    "Add i2c",
    "Delete i2c",
    "Edit i2c",
    "Show i2cs",

    "Add AOP Panic",
    "Delete AOP Panic",
    "Edit AOP Panic",
    "Show AOP Panics",

    "Add Model",
    "Delete Model",
    "Edit Model",
    "Show Models",

    "Add Swap Helper",
    "Delete Swap Helper",
    "Edit Swap Helper",
    "Show Swap Helpers",

    "Add iTunes",
    "Delete iTunes",
    "Edit iTunes",
    "Show All iTunes",

    # AUTH BUTTONS
    "📞Send Phone Number",
    "📞Отправить номер телефона",
    "📞Telefon Raqamingizni Jo'nating",

    # SUPER ADMIN BUTTONS
    "Admin Management",

    "Add Admin",
    "Delete Admin",
    "Show Admins",

    # USER BUTTONS
    "Ishni Boshlash",
    "Поехали",
    "Let's go",

    "Apple",
    "Android",
    "⚙️Tools",
    "⚙️Инструменты",
    "⚙️Uskunalar",
    "⚙️Setting",
    "⚙️Настройки",
    "⚙️Sozlamalar",
    "ADMIN",

    "Edit Phone Number",
    "Change Language",
    "Show My Data",
    "💵Balance",

    "Изменить Номер Телефона",
    "Изменить Язык",
    "Показать Мои Данные",
    "💵Баланс",
    "🔝Главное Меню",

    "Telefon Raqamini O'zgartirish",
    "Tilni O'zgartirish",
    "Ma'lumotlarimni ko'rish",
    "💵Balans",
    "🔝Asosiy Menyu",

    "PANIC",
    "SWAP",
    "iTunes",

    "SMC PANIC - ASSERTION",
    "Userspace watchdog timeout",
    "i2c",
    "AOP PANIC",

    "⚙️IMEI Generator",
    "⚙️IMEI Генератор",

    "866XXX",
    "860XXX",
    "355XXX",
    "358XXX",
    "Manual",
    "Вручной",

    "🔙Back To Tool Menu",
    "🔙Asboblar menyusiga qaytish",
    "🔙Вернуться в меню инструментов",

    "🔙Back To Choosing Menu",
    "🔙Вернуться к выбору меню",
    "🔙Tanlash menyusiga qaytish",

    "🔙Back To Swap Menu",
    "🔙Вернуться к меню swap",
    "🔙Swap menyuga qaytish",

    "🔝Main Menu",
    "🔝Главное Меню",
    "🔝Asosiy Menyu",

    "🔙Back To Apple Menu",
    "🔙Вернуться к Apple меню",
    "🔙Apple menyuga qaytish",

    "🔙Back To Array",
    "🔙Вернуться к Array меню",
    "🔙Array menyusiga qaytish",

    "🔙Back To i2c Menu",
    "🔙Вернуться к i2c меню",
    "🔙i2c menyusiga qaytish",
]