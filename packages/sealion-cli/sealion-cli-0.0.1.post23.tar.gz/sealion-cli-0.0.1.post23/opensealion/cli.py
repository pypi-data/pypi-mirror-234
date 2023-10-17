import curses
import textwrap
import time
from subprocess import Popen, PIPE, STDOUT
import os
import opensealion.config as config
import config as config

break_flag = False
COLOR_TYPE = 1
height, width = 0, 0
mvn = ''
menu_dict = config.menu_dict


def show_introduction(stdscr, introduction: str) -> int:
    stdscr.clear()
    intro_lines = textwrap.wrap(config.introduction, width)
    start_row = 5
    stdscr.attron(curses.color_pair(COLOR_TYPE))
    for idx, item in enumerate(config.logos):
        _x = max(width // 2 - len(item) // 2, 0)
        _y = max(start_row - len(config.logos) // 2 + idx, 1)
        stdscr.addstr(_y, _x, f"  {item}")
    for i, line in enumerate(intro_lines):
        _x = max(width // 2 - len(line) // 2, 0)
        start_row = start_row + len(config.logos) // 2 + 2
        stdscr.addstr(start_row, _x, line)
    start_row += 1
    _x = max(width // 2 - len(config.version) // 2, 0)
    stdscr.refresh()
    stdscr.addstr(start_row, _x, 'v-' + config.version)
    stdscr.attroff(curses.color_pair(COLOR_TYPE))
    stdscr.refresh()
    return start_row


def show_goodbye(stdscr: dict):
    stdscr.clear()
    for i, line in enumerate(config.goodbyes):
        x = max(width // 2 - len(line) // 2, 0)
        y = max(height // 2 - len(config.goodbyes) // 2 + i, 0)
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
    stdscr.addstr(
        max(height - 1, 0), width // 2 - len(to_quit) // 2,
        to_quit,
                            curses.color_pair(COLOR_TYPE) | curses.A_BLINK
    )
    stdscr.attroff(curses.color_pair(COLOR_TYPE))
    stdscr.getch()


def exe_shell(command: str, shell: str = '/bin/bash'):
    return Popen(command, stdout=PIPE, stderr=STDOUT, shell=True, executable=shell)


def exe_shell_curses(command: str, stdscr, skip_press_anykey: bool = False):
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
        if not skip_press_anykey:
            press_anykey_exit(stdscr)
    except Exception as e:
        stdscr.addstr(0, 0, f"error={e}")
        press_anykey_exit(stdscr)


def show_menu(stdscr, selected_row: int, menus: list):
    stdscr.clear()
    current_row = show_introduction(stdscr, config.introduction)
    try:
        for idx, item in enumerate(menus):
            x = max(width // 2 - len(item) // 2, 0)
            y = max((height + current_row) // 2 - len(menus) // 2 + idx, 0)
            if idx == selected_row:
                stdscr.attron(curses.color_pair(COLOR_TYPE))  # 设置高亮
                stdscr.addstr(y, x, f"-> {item}")
                stdscr.attroff(curses.color_pair(COLOR_TYPE))
            else:
                stdscr.addstr(y, x, f"  {item}")
            stdscr.refresh()
    except Exception as e:

        pass


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
        display_menu(stdscr, menus)


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
    if not mvn:
        do_install_maven(stdscr, True)
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


def do_install_maven(stdscr, skip_press_anykey: bool = False):
    command = f'''
    command -v {mvn} &> /dev/null && echo 'mvn is already installed.' || \
    (cd {config.sealion_cli_root} && \
    wget {config.maven_url} && \
    tar -xvzf apache-maven-3.9.5-bin.tar.gz && \
    mv apache-maven-3.9.5 maven&& \
    rm -rf apache-maven-3.9.5-bin.tar.gz 
    )
    '''
    update_mvn_path()
    exe_shell_curses(command, stdscr, skip_press_anykey)


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
    echo, _ = get_inputs_and_echo(stdscr, y, x)
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


def do_network_test(stdscr):
    stdscr.clear()
    exe_shell_curses("ping 8.8.8.8 -c 5", stdscr)
    stdscr.getch()


def do_set_theme(stdscr):
    return display_menu(stdscr, config.theme)


def do_set_install(stdscr):
    return display_menu(stdscr, config.install)


def do_set_network(stdscr):
    do_network_test(stdscr)


def do_move_key(key, current_row, sub_items):
    if key == curses.KEY_UP:
        if current_row > 0:
            current_row -= 1
        else:
            current_row = len(sub_items) - 1
    elif key == curses.KEY_DOWN:
        if current_row < len(sub_items) - 1:
            current_row += 1
        else:
            current_row = 0
    return current_row


def is_move_key(key):
    return key == curses.KEY_UP or key == curses.KEY_DOWN


def do_menu_detail(stdscr, sub_items, menu_current_row) -> bool:
    global COLOR_TYPE

    stdscr.clear()
    _row = sub_items[menu_current_row]

    # use create-sealion-app
    if _row == config.frontend[0]:
        do_create_mm_app(stdscr, 'mm-template')
    elif _row == config.frontend[1]:
        do_create_mm_app(stdscr, 'mm-template-vite')
    elif _row == config.frontend[2]:
        do_create_mm_app(stdscr, 'mmm-lib-template')
    # use sealion-boot
    elif _row == config.backend[0]:
        do_sealion_boot(stdscr)
    # install maven
    elif _row == config.install[0]:
        do_install_maven(stdscr)
    # install nvm
    elif _row == config.install[1]:
        do_install_nvm(stdscr)
    # install node
    elif _row == config.install[2]:
        do_install_node(stdscr)
    elif _row == config.theme[0]:
        COLOR_TYPE = 1
    elif _row == config.theme[1]:
        COLOR_TYPE = 2
    elif _row == config.theme[2]:
        COLOR_TYPE = 3
    elif _row == config.theme[3]:
        COLOR_TYPE = 4
    elif _row == config.theme[4]:
        COLOR_TYPE = 5
    elif _row == config.theme[5]:
        COLOR_TYPE = 6
    # settting - theme
    elif _row == config.setting[0]:
        do_set_theme(stdscr)
    # setting - install
    elif _row == config.setting[1]:
        do_set_install(stdscr)
    # setting - network
    elif _row == config.setting[2]:
        do_set_network(stdscr)
    stdscr.refresh()
    return False


def is_enter_key(sub_key):
    return sub_key in [curses.KEY_ENTER, ord("\n")]


def is_back(menu: str):
    return "back" == menu.replace(" ", "")


def is_exit(menu: str):
    return "exit" == menu.replace(" ", "")


def get_parent_menu(current_menu):
    return menu_dict.get(current_menu)


def debugger(stdscr, y: int = 0, x: int = 0, debug: str = ""):
    stdscr.addstr(y, x, debug)
    stdscr.getch()


def display_menu(stdscr, curent_menu) -> bool:
    menu_current_row = 0
    stdscr.clear()
    show_introduction(stdscr, config.introduction)
    show_menu(stdscr, menu_current_row, curent_menu)
    global break_flag, COLOR_TYPE
    try:
        while not break_flag:
            sub_key = stdscr.getch()
            # debugger(stdscr, 0, 0, f"1current_menu={curent_menu[menu_current_row]}")
            if is_move_key(sub_key):
                menu_current_row = do_move_key(sub_key, menu_current_row, curent_menu)
            elif is_enter_key(sub_key):
                parent_menu = get_parent_menu(curent_menu[0].replace(" ", ""))
                # debugger(stdscr, 0, 0, f"2current_menu={curent_menu[menu_current_row]}")
                if is_exit(curent_menu[menu_current_row]):
                    show_goodbye(stdscr)
                    time.sleep(config.goodbye_show_seconds)
                    exit(0)
                if parent_menu is None:
                    display_menu(stdscr, config.get_main_menu(menu_current_row))
                    continue
                # debugger(stdscr, 0, 0, f"3current_menu={curent_menu[menu_current_row]}")
                if is_back(curent_menu[menu_current_row]):
                    display_menu(stdscr, parent_menu)
                    continue
                # debugger(stdscr, 0, 0, f"4current_menu={curent_menu[menu_current_row]}")
                break_flag = do_menu_detail(stdscr, curent_menu, menu_current_row)
            show_menu(stdscr, menu_current_row, curent_menu)
    except:
        pass
    return break_flag


def main_menu(stdscr) -> bool:
    current_row = 0
    show_menu(stdscr, current_row, config.menu_items)
    global break_flag, COLOR_TYPE
    while not break_flag:
        key = stdscr.getch()
        if is_move_key(key):
            current_row = do_move_key(key, current_row, config.menu_items)
            show_menu(stdscr, current_row, config.menu_items)
        elif is_enter_key(key):
            if current_row == len(config.menu_items) - 1:
                show_goodbye(stdscr)
                time.sleep(config.goodbye_show_seconds)
                break_flag = True
            break_flag = display_menu(stdscr, config.get_main_menu(current_row))
    return break_flag


def curses_wrapper(stdscr):
    curses.curs_set(0)  # 隐藏光标
    curses.start_color()
    # Start colors in curses
    for idx in range(len(config.theme_types)):
        curses.init_pair(idx + 1, config.theme_types[idx].get("f"), config.theme_types[idx].get("b"))
    global height, width
    height, width = stdscr.getmaxyx()
    main_menu(stdscr)


def init_cli():
    command = f'''
    mkdir -p {config.sealion_cli_root} && \
    touch {config.sealion_cli_root}/config.json
    '''
    exe_shell(command)


def main():
    init_cli()
    curses.wrapper(curses_wrapper)


if __name__ == "__main__":
    main()
