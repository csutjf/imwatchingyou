import PySimpleGUI as sg
import inspect
import textwrap

"""
    A "Live Debugging Tool" - "Watch" your code without stopping it.  Graphical user interface
    Cointains a "REPL" that you can use to run code, etc
"""



PSGDebugLogo = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

red_x = b"R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="

COLOR_SCHEME = 'LightGreen'

WIDTH_VARIABLES = 23
WIDTH_RESULTS = 46

WIDTH_WATCHER_VARIABLES = 20
WIDTH_WATCHER_RESULTS = 58

WIDTH_LOCALS = 80
NUM_AUTO_WATCH = 13

MAX_LINES_PER_RESULT_FLOATING = 3
MAX_LINES_PER_RESULT_MAIN      = 3

POPOUT_WINDOW_FONT = 'Sans 8'

class Debugger():


    #     #                    ######
    ##   ##   ##   # #    #    #     # ###### #####  #    #  ####   ####  ###### #####
    # # # #  #  #  # ##   #    #     # #      #    # #    # #    # #    # #      #    #
    #  #  # #    # # # #  #    #     # #####  #####  #    # #      #      #####  #    #
    #     # ###### # #  # #    #     # #      #    # #    # #  ### #  ### #      #####
    #     # #    # # #   ##    #     # #      #    # #    # #    # #    # #      #   #
    #     # #    # # #    #    ######  ###### #####   ####   ####   ####  ###### #    #

    def __init__(self):
        self.watcher_window = None  # type: Window
        self.popout_window = None  # type: Window
        self.local_choices = {}
        self.myrc = ''
        self.custom_watch = ''
        self.locals = {}
        self.globals = {}
        self.popout_choices = {}


    # Includes the DUAL PANE (now 2 tabs)!  Don't forget REPL is there too!
    def _build_main_debugger_window(self):
        sg.ChangeLookAndFeel(COLOR_SCHEME)

        def InVar(key1):
            row1 = [sg.T('    '),
                    sg.I(key=key1, size=(WIDTH_VARIABLES, 1)),
                    sg.T('', key=key1 + 'CHANGED_', size=(WIDTH_RESULTS, 1)), sg.B('Detail', key=key1 + 'DETAIL_'),
                    sg.B('Obj', key=key1 + 'OBJ_'), ]
            return row1

        variables_frame = [InVar('_VAR1_'),
                           InVar('_VAR2_'),
                           InVar('_VAR3_'), ]

        interactive_frame = [[sg.T('>>> ', size=(9, 1), justification='r'), sg.In(size=(83, 1), key='_INTERACTIVE_'),
                              sg.B('Go', bind_return_key=True, visible=False)],
                             [sg.T('CODE >>> ', justification='r', size=(9, 1)), sg.In(size=(83, 1), key='_CODE_')],
                             [sg.Multiline(size=(93, 26), key='_OUTPUT_', autoscroll=True, do_not_clear=True)], ]

        autowatch_frame = [[sg.Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                            sg.Button('Clear All Auto Watches'),
                            sg.Button('Show All Variables', key='_SHOW_ALL_'),
                            sg.Button('Locals', key='_ALL_LOCALS_'),
                            sg.Button('Globals', key='_GLOBALS_'),
                            sg.Button('Popout', key='_POPOUT_')]] + \
                          [
                              [sg.T('', size=(WIDTH_WATCHER_VARIABLES, 1), key='_WATCH%s_' % i),
                               sg.T('', size=(WIDTH_WATCHER_RESULTS, MAX_LINES_PER_RESULT_MAIN), key='_WATCH%s_RESULT_' % i,
                                    auto_size_text=True)] for i in range(1, NUM_AUTO_WATCH + 1)]

        col1 = [
            [sg.Frame('Auto Watches', autowatch_frame, title_color='blue')]
        ]

        col2 = [
            [sg.Frame('Variables or Expressions to Watch', variables_frame, title_color='blue'), ],
            [sg.Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue'), ]
        ]


        # Pane based layout
        # layout = [[sg.Pane([sg.Column(col1), sg.Column(col2)], size=(700, 640), orientation='h', background_color='red',
        #                    show_handle=True, ), ],
        #           [sg.Button('', image_data=red_x, key='_EXIT_', button_color=None),
        #            sg.Text('Pull Red Line For REPL & Object Display Screen ---> ', size=(80, 1), justification='r')]]

        # Tab based layout
        layout = [[sg.TabGroup([[sg.Tab('Variables', col1), sg.Tab('REPL & Watches', col2)]])],
                  [sg.Button('', image_data=red_x, key='_EXIT_', button_color=None),]]

        # START the window with all variables chosen but the _ ones
        for key in self.locals:
            self.local_choices[key] = not key.startswith('_')


        window = sg.Window("I'm Watching You Debugger", layout, icon=PSGDebugLogo, margins=(0, 0)).Finalize()
        window.Element('_VAR1_').SetFocus()
        self.watcher_window = window
        sg.ChangeLookAndFeel('SystemDefault')
        return window

    #     #                    #######                               #
    ##   ##   ##   # #    #    #       #    # ###### #    # #####    #        ####   ####  #####
    # # # #  #  #  # ##   #    #       #    # #      ##   #   #      #       #    # #    # #    #
    #  #  # #    # # # #  #    #####   #    # #####  # #  #   #      #       #    # #    # #    #
    #     # ###### # #  # #    #       #    # #      #  # #   #      #       #    # #    # #####
    #     # #    # # #   ##    #        #  #  #      #   ##   #      #       #    # #    # #
    #     # #    # # #    #    #######   ##   ###### #    #   #      #######  ####   ####  #

    def _refresh_main_debugger_window(self, mylocals, myglobals):
        if not self.watcher_window:
            return False
        event, values = self.watcher_window.Read(timeout=1)
        if event in (None, 'Exit', '_EXIT_'):  # EXIT BUTTON / X BUTTON
            try:
                self.watcher_window.Close()
            except: pass
            self.watcher_window = None
            return False

        cmd_interactive = values['_INTERACTIVE_']
        cmd_code = values['_CODE_']
        cmd = cmd_interactive or cmd_code
        # BUTTON - GO
        if event == 'Go':  # GO BUTTON
            self.watcher_window.Element('_INTERACTIVE_').Update('')
            self.watcher_window.Element('_CODE_').Update('')
            self.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
            if cmd_interactive:
                expression = """{} = {} """.format(fullname(self.myrc), cmd)
                try:
                    exec(expression, myglobals, mylocals)
                    self.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(self.myrc), append=True,
                                                                       autoscroll=True)

                except Exception as e:
                    self.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e), append=True,
                                                                       autoscroll=True)
            else:
                self.watcher_window.Element('_CODE_').Update('')
                self.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
                expression = """{}""".format(cmd)
                try:
                    exec(expression, myglobals, mylocals)
                    self.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(cmd), append=True, autoscroll=True)
                except Exception as e:
                    self.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e), append=True,
                                                                       autoscroll=True)
        # BUTTON - DETAIL
        elif event.endswith('_DETAIL_'):  # DETAIL BUTTON
            var = values['_VAR{}_'.format(event[4])]
            expression = """ {} = {} """.format(fullname(self.myrc), var)
            try:
                exec(expression, myglobals, mylocals)
                sg.PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + str(self.myrc), title=var,
                                 non_blocking=True)
            except:
                pass
        # BUTTON - OBJ
        elif event.endswith('_OBJ_'):  # OBJECT BUTTON
            var = values['_VAR{}_'.format(event[4])]
            expression = """{} = {} """.format(fullname(self.myrc), cmd)
            try:
                exec(expression, myglobals, mylocals)
                sg.PopupScrolled(sg.ObjToStringSingleObj(self.myrc), title=var, non_blocking=True)
            except:
                pass
        # BUTTON - Choose Locals to see
        elif event == '_LOCALS_':  # Show all locals BUTTON
            self._choose_auto_watches(mylocals)
        # BUTTON - Locals (quick popup)
        elif event == '_ALL_LOCALS_':
            self._display_all_vars(mylocals)
        # BUTTON - Globals (quick popup)
        elif event == '_GLOBALS_':
            self._display_all_vars(myglobals)
        # BUTTON - clear all
        elif event == 'Clear All Auto Watches':
            if sg.PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
                self.local_choices = {}
                self.custom_watch = ''
                # self.watcher_window.Element('_CUSTOM_WATCH_').Update('')
        # BUTTON - Popout
        elif event == '_POPOUT_':
            if not self.popout_window:
                self._build_floating_window()
        # BUTTON - Show All
        elif event == '_SHOW_ALL_':
            for key in self.locals:
                self.local_choices[key] = not key.startswith('_')

        # -------------------- Process the manual "watch list" ------------------
        for i in range(1, 4):
            key = '_VAR{}_'.format(i)
            out_key = '_VAR{}_CHANGED_'.format(i)
            self.myrc = ''
            if self.watcher_window.Element(key):
                if values[key]:
                    self.watcher_window.Element(out_key).Update(values[key])
                else:
                    self.watcher_window.Element(out_key).Update('')

        # -------------------- Process the automatic "watch list" ------------------
        slot = 1
        for key in self.local_choices:
            if self.local_choices[key] is True:
                self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(key)
                try:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(mylocals[key])
                except:
                    self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(''
                                                                                            )
                slot += 1

                if slot + int(not self.custom_watch in (None, '')) >= NUM_AUTO_WATCH:
                    break
        # If a custom watch was set, displaythat value in the window
        if self.custom_watch:
            self.watcher_window.Element('_WATCH{}_'.format(slot)).Update(self.custom_watch)
            try:
                self.myrc = eval(self.custom_watch, myglobals, mylocals)
            except:
                self.myrc = ''
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(self.myrc)
            slot += 1
        # blank out all of the slots not used (blank)
        for i in range(slot, NUM_AUTO_WATCH + 1):
            self.watcher_window.Element('_WATCH{}_'.format(i)).Update('')
            self.watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

        return True

    ######                                 #     #
    #     #  ####  #####  #    # #####     #  #  # # #    # #####   ####  #    #
    #     # #    # #    # #    # #    #    #  #  # # ##   # #    # #    # #    #
    ######  #    # #    # #    # #    #    #  #  # # # #  # #    # #    # #    #
    #       #    # #####  #    # #####     #  #  # # #  # # #    # #    # # ## #
    #       #    # #      #    # #         #  #  # # #   ## #    # #    # ##  ##
    #        ####  #       ####  #          ## ##  # #    # #####   ####  #    #

    ######                                    #                     #     #
    #     # #    # #    # #####   ####       # #   #      #         #     #   ##   #####   ####
    #     # #    # ##  ## #    # #          #   #  #      #         #     #  #  #  #    # #
    #     # #    # # ## # #    #  ####     #     # #      #         #     # #    # #    #  ####
    #     # #    # #    # #####       #    ####### #      #          #   #  ###### #####       #
    #     # #    # #    # #      #    #    #     # #      #           # #   #    # #   #  #    #
    ######   ####  #    # #       ####     #     # ###### ######       #    #    # #    #  ####
    # displays them into a single text box
    def _display_all_vars(self, dict):
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        out_text = 'All of your Vars'
        longest_line = max([len(key) for key in dict])
        line = []
        sorted_dict = {}
        for key in sorted(dict.keys()):
            sorted_dict[key] = dict[key]
        for key in sorted_dict:
            value = dict[key]
            wrapped_list = textwrap.wrap(str(value), 60)
            wrapped_text = '\n'.join(wrapped_list)
            out_text += '{} - {}\n'.format(key, wrapped_text)
            if cur_col + 1 == num_cols:
                cur_col = 0
                num_lines += len(wrapped_list)
            else:
                cur_col += 1
        sg.ScrolledTextBox(out_text, non_blocking=True)

    #####                                        #     #
    #     # #    #  ####   ####   ####  ######    #  #  #   ##   #####  ####  #    #
    #       #    # #    # #    # #      #         #  #  #  #  #    #   #    # #    #
    #       ###### #    # #    #  ####  #####     #  #  # #    #   #   #      ######
    #       #    # #    # #    #      # #         #  #  # ######   #   #      #    #
    #     # #    # #    # #    # #    # #         #  #  # #    #   #   #    # #    #
    #####  #    #  ####   ####   ####  ######     ## ##  #    #   #    ####  #    #

    #     #                                                       #     #
    #     #   ##   #####  #   ##   #####  #      ######  ####     #  #  # # #    #
    #     #  #  #  #    # #  #  #  #    # #      #      #         #  #  # # ##   #
    #     # #    # #    # # #    # #####  #      #####   ####     #  #  # # # #  #
    #   #  ###### #####  # ###### #    # #      #           #    #  #  # # #  # #
    # #   #    # #   #  # #    # #    # #      #      #    #    #  #  # # #   ##
    #    #    # #    # # #    # #####  ###### ######  ####      ## ##  # #    #

    def _choose_auto_watches(self, my_locals):
        sg.ChangeLookAndFeel(COLOR_SCHEME)
        num_cols = 3
        output_text = ''
        num_lines = 2
        cur_col = 0
        layout = [[sg.Text('Choose your "Auto Watch" variables', font='ANY 14', text_color='red')]]
        longest_line = max([len(key) for key in my_locals])
        line = []
        sorted_dict = {}
        for key in sorted(my_locals.keys()):
            sorted_dict[key] = my_locals[key]
        for key in sorted_dict:
            line.append(sg.CB(key, key=key, size=(longest_line, 1),
                              default=self.local_choices[key] if key in self.local_choices else False))
            if cur_col + 1 == num_cols:
                cur_col = 0
                layout.append(line)
                line = []
            else:
                cur_col += 1
        if cur_col:
            layout.append(line)

        layout += [
            [sg.Text('Custom Watch'), sg.Input(default_text=self.custom_watch, size=(60, 1), key='_CUSTOM_WATCH_')]]
        layout += [
            [sg.Ok(), sg.Cancel(), sg.Button('Clear All'), sg.Button('Select [almost] All', key='_AUTO_SELECT_')]]

        window = sg.Window('All Locals', layout, icon=PSGDebugLogo).Finalize()

        while True:  # event loop
            event, values = window.Read()
            if event in (None, 'Cancel'):
                break
            elif event == 'Ok':
                self.local_choices = values
                self.custom_watch = values['_CUSTOM_WATCH_']
                break
            elif event == 'Clear All':
                sg.PopupQuickMessage('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True,
                                     text_color='red', font='ANY 18')
                for key in sorted_dict:
                    window.Element(key).Update(False)
                window.Element('_CUSTOM_WATCH_').Update('')
            elif event == 'Select All':
                for key in sorted_dict:
                    window.Element(key).Update(False)
            elif event == '_AUTO_SELECT_':
                for key in sorted_dict:
                    window.Element(key).Update(not key.startswith('_'))

        # exited event loop
        window.Close()
        sg.ChangeLookAndFeel('SystemDefault')

    ######                            #######
    #     # #    # # #      #####     #       #       ####    ##   ##### # #    #  ####
    #     # #    # # #      #    #    #       #      #    #  #  #    #   # ##   # #    #
    ######  #    # # #      #    #    #####   #      #    # #    #   #   # # #  # #
    #     # #    # # #      #    #    #       #      #    # ######   #   # #  # # #  ###
    #     # #    # # #      #    #    #       #      #    # #    #   #   # #   ## #    #
    ######   ####  # ###### #####     #       ######  ####  #    #   #   # #    #  ####

    #     #s
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
    ## ##  # #    # #####   ####  #    #

    def _build_floating_window(self):
        if self.popout_window:
            self.popout_window.Close()
        sg.ChangeLookAndFeel('Topanga')
        num_cols = 2
        width_var = 15
        width_value = 30
        layout = []
        line = []
        col = 0
        self.popout_choices = self.local_choices if self.local_choices != {} else {}
        if self.popout_choices == {}:
            for key in sorted(self.locals.keys()):
                self.popout_choices[key] = not key.startswith('_')

        width_var = max([len(key) for key in self.popout_choices])
        for key in self.popout_choices:
            if self.popout_choices[key] is True:
                value = str(self.locals.get(key))
                h = len(value)//width_value
                h = h if h <= MAX_LINES_PER_RESULT_FLOATING else MAX_LINES_PER_RESULT_FLOATING
                line += [sg.Text(key, size=(width_var, 1), font=POPOUT_WINDOW_FONT), sg.Text(' = ', font=POPOUT_WINDOW_FONT),
                         sg.Text(value, key=key, size=(width_value, h), font=POPOUT_WINDOW_FONT)]
                # line += [sg.Text(key, size=(width_var, 1), font='Sans 8'), sg.Text(' = ', font='Sans 8'),
                #          sg.Text(value, key=key, size=(width_value, int(len(value)/width_value) if len(value)/width_value<MAX_LINES_PER_RESULT_FLOATING else MAX_LINES_PER_RESULT_FLOATING),
                #                  font='Sans 8')]
                if col + 1 < num_cols:
                    line += [sg.VerticalSeparator(), sg.T(' ')]
                col += 1
            if col >= num_cols:
                layout.append(line)
                line = []
                col = 0
        if col != 0:
            layout.append(line)
        layout = [[sg.Column(layout), sg.Column(
            [[sg.Button('', key='_EXIT_', image_data=red_x, button_color=('#282923', '#282923'), border_width=0)]])]]

        self.popout_window = sg.Window('Floating', layout, alpha_channel=0, no_titlebar=True, grab_anywhere=True,
                                           element_padding=(0, 0), margins=(0, 0), keep_on_top=True, right_click_menu=['&Right', ['Debugger::RightClick', 'Exit::RightClick']], ).Finalize()
        screen_size = self.popout_window.GetScreenDimensions()
        self.popout_window.Move(screen_size[0] - self.popout_window.Size[0], 0)
        self.popout_window.SetAlpha(1)

        sg.ChangeLookAndFeel('SystemDefault')
        return True

    ######
    #     # ###### ###### #####  ######  ####  #    #
    #     # #      #      #    # #      #      #    #
    ######  #####  #####  #    # #####   ####  ######
    #   #   #      #      #####  #           # #    #
    #    #  #      #      #   #  #      #    # #    #
    #     # ###### #      #    # ######  ####  #    #

    #######
    #       #       ####    ##   ##### # #    #  ####
    #       #      #    #  #  #    #   # ##   # #    #
    #####   #      #    # #    #   #   # # #  # #
    #       #      #    # ######   #   # #  # # #  ###
    #       #      #    # #    #   #   # #   ## #    #
    #       ######  ####  #    #   #   # #    #  ####

    #     #
    #  #  # # #    # #####   ####  #    #
    #  #  # # ##   # #    # #    # #    #
    #  #  # # # #  # #    # #    # #    #
    #  #  # # #  # # #    # #    # # ## #
    #  #  # # #   ## #    # #    # ##  ##
    ## ##  # #    # #####   ####  #    #

    def _refresh_floating_window(self):
        if not self.popout_window:
            return
        for key in self.popout_choices:
            if self.popout_choices[key] is True:
                self.popout_window.Element(key).Update(self.locals.get(key))
        event, values = self.popout_window.Read(timeout=1)
        if event in (None, '_EXIT_', 'Exit::RightClick'):
            self.popout_window.Close()
            self.popout_window = None
        elif event == 'Debugger::RightClick':
            show_debugger_window()


# 888     888                                .d8888b.         d8888 888 888          888      888
# 888     888                               d88P  Y88b       d88888 888 888          888      888
# 888     888                               888    888      d88P888 888 888          888      888
# 888     888 .d8888b   .d88b.  888d888     888            d88P 888 888 888  8888b.  88888b.  888  .d88b.
# 888     888 88K      d8P  Y8b 888P"       888           d88P  888 888 888     "88b 888 "88b 888 d8P  Y8b
# 888     888 "Y8888b. 88888888 888         888    888   d88P   888 888 888 .d888888 888  888 888 88888888
# Y88b. .d88P      X88 Y8b.     888         Y88b  d88P  d8888888888 888 888 888  888 888 d88P 888 Y8b.
#  "Y88888P"   88888P'  "Y8888  888          "Y8888P"  d88P     888 888 888 "Y888888 88888P"  888  "Y8888

# 8888888888                            888    d8b
# 888                                   888    Y8P
# 888                                   888
# 8888888    888  888 88888b.   .d8888b 888888 888  .d88b.  88888b.  .d8888b
# 888        888  888 888 "88b d88P"    888    888 d88""88b 888 "88b 88K
# 888        888  888 888  888 888      888    888 888  888 888  888 "Y8888b.
# 888        Y88b 888 888  888 Y88b.    Y88b.  888 Y88..88P 888  888      X88
# 888         "Y88888 888  888  "Y8888P  "Y888 888  "Y88P"  888  888  88888P'


def show_debugger_window():
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame

    if not debugger.watcher_window:
        debugger.watcher_window = debugger._build_main_debugger_window()
    return True


def show_debugger_popout_window():
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame = inspect.getframeinfo(prev_frame)
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if debugger.popout_window:
        debugger.popout_window.Close()
        debugger.popout_window = None
    debugger._build_floating_window()


def refresh_debugger():
    sg.Window.read_call_from_debugger = True
    frame = inspect.currentframe()
    prev_frame = inspect.currentframe().f_back
    # frame, *others = inspect.stack()[1]
    try:
        debugger.locals = frame.f_back.f_locals
        debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    debugger._refresh_floating_window() if debugger.popout_window else None
    rc = debugger._refresh_main_debugger_window(debugger.locals, debugger.globals) if debugger.watcher_window else False
    sg.Window.read_call_from_debugger = False
    return rc


def fullname(o):
    # o.__module__ + "." + o.__class__.__qualname__ is an example in
    # this context of H.L. Mencken's "neat, plausible, and wrong."
    # Python makes no guarantees as to whether the __module__ special
    # attribute is defined, so we take a more circumspect approach.
    # Alas, the module name is explicitly excluded from __qualname__
    # in Python 3.

    module = o.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return o.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + '.' + o.__class__.__name__


debugger = Debugger()

