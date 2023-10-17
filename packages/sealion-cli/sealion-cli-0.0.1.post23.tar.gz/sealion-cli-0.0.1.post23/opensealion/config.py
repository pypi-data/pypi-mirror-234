import curses

version = "0.0.1.post23"
sealion_cli_root = "$HOME/.sealion-cli"
maven_url = "https://dlcdn.apache.org/maven/maven-3/3.9.5/binaries/apache-maven-3.9.5-bin.tar.gz"
introduction = 'Start to create your own project with the Sealion-CLI.'
logos = [
    "=================================================================",
    "|   _____            _ _                    _____ _      _____  |",
    "|  / ____|          | (_)                  / ____| |    |_   _| |",
    "| | (___   ___  __ _| |_  ___  _ __ ______| |    | |      | |   |",
    "|  \___ \ / _ \/ _` | | |/ _ \| '_ \______| |    | |      | |   |",
    "|  ____) |  __/ (_| | | | (_) | | | |     | |____| |____ _| |_  |",
    "| |_____/ \___|\__,_|_|_|\___/|_| |_|      \_____|______|_____| |",
    "|                                                               |",
    "================================================================="
]
menu_items = [
    "frontend",
    "backend ",
    "setting ",
    "exit    "
]
frontend = [
    "mm-template     ",
    "mm-template-vite",
    "mm-lib-template ",
    "back            "
]
backend = [
    "sealion-boot",
    "back        "
]
install = [
    "mvn          ",
    "nvm          ",
    "node         ",
    "back         "
]
setting = [
    "theme  ",
    "install",
    "network",
    "back   ",
]
theme = [
    "green  ",
    "red    ",
    "black  ",
    "cyan   ",
    "magenta",
    "white  ",
    "back   ",
]
goodbye_show_seconds = 3
goodbyes = [
    "Thank you for using Sealion-CLI             ",
    "Find more in https://github.com/open-sealion",
    "Bye-Bye~                                    ",
    f"Closing in {goodbye_show_seconds} seconds...                     ",
]

menu_dict = {
    "frontend": None,
    "backend": None,
    "setting": None,
    "mm-template": menu_items,
    "mm-template-vite": menu_items,
    "mm-lib-template": menu_items,
    "sealion-boot": menu_items,
    "theme": menu_items,
    "network": menu_items,
    "install": menu_items,
    "mvn": setting,
    "nvm": setting,
    "node": setting,
    "green": setting,
    "red": setting,
    "cyan": setting,
    "magenta": setting,
    "white": setting,
    "black": setting,
}

theme_types = [
    {
        "f": curses.COLOR_GREEN,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_RED,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_BLACK,
        "b": curses.COLOR_WHITE
    },
    {
        "f": curses.COLOR_CYAN,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_MAGENTA,
        "b": curses.COLOR_BLACK
    },
    {
        "f": curses.COLOR_WHITE,
        "b": curses.COLOR_BLACK
    },
]

def get_main_menu(current_row) -> list:
    if current_row == 0:
        return frontend
    elif current_row == 1:
        return backend
    elif current_row == 2:
        return setting


def create_menu_dict(*menu_lists):
    menu_dict = dict()
    for menu_list in menu_lists:
        for item in menu_list:
            # 去除字符串中的空格
            item = item.strip()
            menu_dict[item] = menu_list
    return menu_dict

