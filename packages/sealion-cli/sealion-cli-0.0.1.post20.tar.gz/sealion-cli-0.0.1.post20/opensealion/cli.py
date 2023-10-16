import curses
import textwrap
import time
from subprocess import Popen, PIPE, STDOUT
import os
import opensealion.config as config


# 介绍
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

goodbye_show_seconds = 3
goodbyes = [
    "Thank you for using Sealion-CLI             ",
    "Find more in https://github.com/open-sealion",
    "Bye-Bye~                                    ",
    f"Closing in {goodbye_show_seconds} seconds...                     ",
]


# 定义菜单项
menu_items = [
    "frontend",
    "backend ",
    "install ",
    "network ",
    "theme   ",
    "exit    "
]
fe_items = [
    "mm-template     ",
    "mm-template-vite",
    "mm-lib-template ",
    "back            "
]
be_items = [
    "sealion-boot",
    "back        "
]
install_items = [
    "mvn          ",
    "nvm          ",
    "node         ",
    "back         "
]
themes = [
    "green  ",
    "red    ",
    "black  ",
    "cyan   ",
    "magenta",
    "white  ",
    "back   ",
]

break_flag = False
COLOR_TYPE = 1
height, width = 0, 0
mvn = ''


def show_introduction(stdscr, introduction: str) -> int:
    stdscr.clear()
    intro_lines = textwrap.wrap(introduction, width)
    # 计算开始打印的行数
    start_row = 5
    stdscr.attron(curses.color_pair(COLOR_TYPE))
    for idx, item in enumerate(logos):
        _x = max(width // 2 - len(item) // 2, 0)
        _y = max(start_row - len(logos) // 2 + idx, 1)
        stdscr.addstr(_y, _x, f"  {item}")
    for i, line in enumerate(intro_lines):
        _x = max(width // 2 - len(line) // 2, 0)
        start_row = start_row + len(logos) // 2 + 2
        stdscr.addstr(start_row, _x, line)
    start_row += 1
    _x = max(width//2 - len(config.version)//2, 0)
    stdscr.refresh()  # 刷新屏幕
    stdscr.addstr(start_row, _x, 'v-' + config.version)
    stdscr.attroff(curses.color_pair(COLOR_TYPE))
    stdscr.refresh()
    return start_row


def show_goodbye(stdscr: dict):
    stdscr.clear()
    for i, line in enumerate(goodbyes):
        x = max(width // 2 - len(line) // 2, 0)
        y = max(height // 2 - len(goodbyes) // 2 + i, 0)
        stdscr.addstr(y, x, f"  {line}", curses.color_pair(COLOR_TYPE))
    stdscr.refresh()


def show_version(stdscr: dict):
    stdscr.clear()
    ver = f'v-{config.version}'
    x = max(width // 2, 0)
    y = max(height // 2 - len(ver) // 2, 0)
    stdscr.addstr(y, x, ver, curses.color_pair(COLOR_TYPE))
    stdscr.refresh()


def press_anykey_exit(stdscr):
    stdscr.attron(curses.color_pair(COLOR_TYPE))
    to_quit = "press any key to quit"
    stdscr.addstr(max(height - 1, 0), width // 2 - len(to_quit) // 2, to_quit)
    stdscr.attroff(curses.color_pair(COLOR_TYPE))
    stdscr.getch()


def exe_shell(command: str, shell: str='/bin/bash'):
    return Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, executable=shell)


def exe_shell_curses(command: str, stdscr):
    stdscr.clear()
    command = "echo 'START running shell script...' && " + command
    process = exe_shell(command, shell="/bin/bash")
    try:
        with (process.stdout):
            y = 0
            for line in iter(process.stdout.readline, b''):
                # s = str(line).replace("b'", "").replace("'", "").replace("\\n", "")
                s = line.decode('utf-8')
                stdscr.addstr(y, 0, s)
                stdscr.refresh()
                y += 1
                if y >= height - 1:
                    stdscr.clear()
                    y = 0
        press_anykey_exit(stdscr)
    except Exception as e:
        stdscr.addstr(0, 0, f"error={e}")
        press_anykey_exit(stdscr)


def show_menu(stdscr, selected_row: int, menus: list):
    stdscr.clear()
    current_row = show_introduction(stdscr, introduction)
    # 显示菜单项
    for idx, item in enumerate(menus):
        x = max(width // 2 - len(item) // 2, 0)
        y = max((height + current_row) // 2 - len(menus) // 2 + idx, 0)
        if idx == selected_row:
            stdscr.attron(curses.color_pair(COLOR_TYPE))  # 设置高亮
            stdscr.addstr(y, x, f"-> {item}")
            stdscr.attroff(curses.color_pair(COLOR_TYPE))
        else:
            stdscr.addstr(y, x, f"  {item}")
    stdscr.refresh()  # 刷新屏幕


def get_inputs_and_echo(stdscr, y, x, allow_empty: bool = False):
    curses.curs_set(1)
    inputs = ""
    esc_flag = False
    while True:
        c = stdscr.getch()
        if c == 10:
            if inputs != "" or allow_empty:
                break
        elif c == 27:
            esc_flag = True
        elif c == 127 or c == 8:
            stdscr.delch(y, max(len(inputs) - 1, 0))
            inputs = inputs[:-1]
            stdscr.addstr(y, x, inputs)
        elif 32 <= c <= 126:
            inputs += chr(c)
            stdscr.addstr(y, x, inputs)
        stdscr.refresh()
    curses.curs_set(0)
    return inputs, esc_flag


def get_current_path():
    return os.getcwd()


def check_if_back(esc_flag, stdscr, menus):
    if esc_flag:
        sub_menu(stdscr, menus)


def do_sealion_boot(stdscr):
    y = 0
    x = 0
    stdscr.addstr(y, x, "> Input the project's groupId:\n", curses.color_pair(COLOR_TYPE))
    y += 1
    group_id, esc_flag = get_inputs_and_echo(stdscr, y, x)
    y += 1
    stdscr.addstr(y, x, f"> Input the project's ArtifactId:\n", curses.color_pair(COLOR_TYPE))
    y += 1
    artifact_id, esc_flag = get_inputs_and_echo(stdscr, y, x)
    y += 1
    stdscr.addstr(y, x, f"> Input the project's verison:\n", curses.color_pair(COLOR_TYPE))
    y += 1
    app_version, esc_flag = get_inputs_and_echo(stdscr, y, x)
    y += 1
    stdscr.addstr(y, x, f"> Input the sealion-boot version (optional, default version: 4.0-SNAPSHOT):\n",
                  curses.color_pair(COLOR_TYPE))
    y += 1
    sealion_boot_ver, esc_flag = get_inputs_and_echo(stdscr, y, x, allow_empty=True)
    if not sealion_boot_ver:
        sealion_boot_ver = '4.0-SNAPSHOT'
    current_path = get_current_path()
    y += 1
    stdscr.addstr(y, x,
                  f"> Input the project directory (optional, default directory is current path: {current_path}):\n",
                  curses.color_pair(COLOR_TYPE))
    y += 1
    project_dir, esc_flag = get_inputs_and_echo(stdscr, y, x, allow_empty=True)
    if project_dir:
        os.chdir(project_dir)
    do_install_maven(stdscr)
    command = f'''
    {mvn} archetype:generate \
    -DinteractiveMode=false \
    -DarchetypeGroupId=org.openmmlab.platform \
    -DarchetypeArtifactId=openmmlab-base-archetype \
    -DarchetypeVersion={sealion_boot_ver} \
    -DgroupId={group_id} \
    -DartifactId={artifact_id} \
    -Dversion={app_version} \
    '''
    # y += 1
    # stdscr.addstr(y, x, f"{command}")
    stdscr.clear()
    exe_shell_curses(command, stdscr)


def update_mvn_path():
    global mvn
    mvn = f'{config.sealion_cli_root}/maven/bin/mvn'


def do_install_maven(stdscr):
    command = f'''
    command -v mvn &> /dev/null && echo 'mvn is already installed.' || \
    (cd {config.sealion_cli_root} && \
    wget {config.maven_url} && \
    tar -xvzf apache-maven-3.9.5-bin.tar.gz && \
    mv apache-maven-3.9.5 maven&& \
    rm -rf apache-maven-3.9.5-bin.tar.gz 
    )
    '''
    update_mvn_path()
    exe_shell_curses(command, stdscr)


def do_install_nvm(stdscr):
    url = "https://oss.openmmlab.com/nvm_install.sh"
    command = f'''
    cd /tmp && \
    wget -qO- {url} | bash
    '''
    exe_shell_curses(command, stdscr)


def do_install_node(stdscr):
    y = 0
    x = 0
    stdscr.addstr(y, x, "TO INSTALL NODE, NVM SHOULD BE INSTALLED FIRST\n", curses.color_pair(COLOR_TYPE))
    y += 1
    stdscr.addstr(y, x, "Typing `nvm ls-remote` in new terminal to list all available node versions\n",
                  curses.color_pair(COLOR_TYPE))
    y += 1
    node_ver, y, x = interactive_input(
        stdscr, y, x,
        "> Input the node version (optional, default version is the latest LTS version)\n",
        curses.color_pair(COLOR_TYPE)
    )
    if not node_ver:
        node_ver = '--lts'
    command = f'''
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install --no-progress {node_ver}
    '''
    stdscr.clear()
    exe_shell_curses(command, stdscr)


def do_install_mm_cli(stdscr):
    command = f'''
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install v18.18.0 > /dev/null && \
    npm cache clear -f && \
    npm install -g create-mm-app --registry=https://nexus.openxlab.org.cn/repository/npm-all
    '''
    exe_shell_curses(command, stdscr)


def interactive_input(stdscr, y, x, display: str, color_pair: int):
    stdscr.addstr(y, x, display, color_pair)
    y += 1
    echo,_ = get_inputs_and_echo(stdscr, y, x)
    return echo, y + 1, x


def do_create_mm_app(stdscr, type: str):
    y = 0
    x = 0
    app_name, y, x = interactive_input(stdscr, y, x, "> Input the project's name:\n", curses.color_pair(COLOR_TYPE))
    app_dir, y, x = interactive_input(stdscr, y, x, "> Input the project's directory:\n", curses.color_pair(COLOR_TYPE))
    command = f'''
    mkdir -p {app_dir} && cd {app_dir} && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install --no-progress v16.18.0 > /dev/null && \
    npm install -g create-mm-app@^0.9.3 --registry=https://nexus.openxlab.org.cn/repository/npm-all && \
    create-mm-app create {app_name} -t {type}
    '''
    exe_shell_curses(command, stdscr)


def sub_menu(stdscr, sub_items) -> bool:
    sub_current_row = 0
    stdscr.clear()
    show_introduction(stdscr, introduction)
    show_menu(stdscr, sub_current_row, sub_items)
    global break_flag, COLOR_TYPE
    while not break_flag:
        sub_key = stdscr.getch()
        if sub_key == curses.KEY_UP:
            if sub_current_row > 0:
                sub_current_row -= 1
            else:
                sub_current_row = len(sub_items) - 1
        elif sub_key == curses.KEY_DOWN:
            if sub_current_row < len(sub_items) - 1:
                sub_current_row += 1
            else:
                sub_current_row = 0
        elif sub_key in [curses.KEY_ENTER, ord("\n")]:
            stdscr.clear()
            _row = sub_items[sub_current_row]
            if sub_current_row == len(sub_items) - 1:
                if main_menu(stdscr):
                    break_flag = True
            else:
                # use create-sealion-app
                if _row == fe_items[0]:
                    do_create_mm_app(stdscr, 'mm-template')
                if _row == fe_items[1]:
                    do_create_mm_app(stdscr, 'mm-template-vite')
                if _row == fe_items[2]:
                    do_create_mm_app(stdscr, 'mmm-lib-template')
                # use sealion-boot
                elif _row == be_items[0]:
                    do_sealion_boot(stdscr)
                # install maven
                elif _row == install_items[0]:
                    do_install_maven(stdscr)
                # install nvm
                elif _row == install_items[1]:
                    do_install_nvm(stdscr)
                # install node
                elif _row == install_items[2]:
                    do_install_node(stdscr)
                elif _row == themes[0]:
                    COLOR_TYPE = 1
                elif _row == themes[1]:
                    COLOR_TYPE = 2
                elif _row == themes[2]:
                    COLOR_TYPE = 3
                elif _row == themes[3]:
                    COLOR_TYPE = 4
                elif _row == themes[4]:
                    COLOR_TYPE = 5
                elif _row == themes[5]:
                    COLOR_TYPE = 6
                stdscr.refresh()
        show_menu(stdscr, sub_current_row, sub_items)
    return break_flag


def do_network_test(stdscr):
    stdscr.clear()
    exe_shell_curses("ping 8.8.8.8 -c 5", stdscr)
    stdscr.getch()


def main_menu(stdscr) -> bool:
    current_row = 0
    show_menu(stdscr, current_row, menu_items)
    global break_flag, COLOR_TYPE
    while not break_flag:
        # 获取键盘输入
        key = stdscr.getch()
        if key == curses.KEY_UP:
            if current_row > 0:
                current_row -= 1
            else:
                current_row = len(menu_items) - 1
        elif key == curses.KEY_DOWN:
            if current_row < len(menu_items) - 1:
                current_row += 1
            else:
                current_row = 0
        # 处理选中菜单项的逻辑
        elif key in [curses.KEY_ENTER, ord("\n")]:
            if current_row == len(menu_items) - 1:
                show_goodbye(stdscr)
                time.sleep(goodbye_show_seconds)
                break_flag = True
            # frontend
            elif current_row == 0:
                break_flag = sub_menu(stdscr, fe_items)
            # backend
            elif current_row == 1:
                break_flag = sub_menu(stdscr, be_items)
            # install
            elif current_row == 2:
                break_flag = sub_menu(stdscr, install_items)
            # network
            elif current_row == 3:
                do_network_test(stdscr)
            # theme
            elif current_row == 4:
                break_flag = sub_menu(stdscr, themes)
            else:
                show_goodbye(stdscr)
                # time.sleep(goodbye_show_seconds)
                break_flag = True
                break
        show_menu(stdscr, current_row, menu_items)
    return break_flag


def curses_wrapper(stdscr):
    curses.curs_set(0)  # 隐藏光标
    curses.start_color()
    # Start colors in curses
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    global height, width
    height, width = stdscr.getmaxyx()
    main_menu(stdscr)


def init_cli_dir():
    command = f'''
    mkdir -p {config.sealion_cli_root} && \
    touch {config.sealion_cli_root}/config.json
    '''
    exe_shell(command)


def main():
    init_cli_dir()
    curses.wrapper(curses_wrapper)


# 运行程序
if __name__ == "__main__":
    main()
