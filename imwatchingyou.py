import PySimpleGUI as sg
import textwrap
import operator
import inspect

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

class Debugger():
    watcher_window = None       # type: sg.Window
    popout_window = None        # type: sg.Window
    local_choices = {}
    myrc = ''
    custom_watch = ''
    locals = {}
    globals = {}
    popout_choices = {}


#     #                    ######
##   ##   ##   # #    #    #     # ###### #####  #    #  ####   ####  ###### #####
# # # #  #  #  # ##   #    #     # #      #    # #    # #    # #    # #      #    #
#  #  # #    # # # #  #    #     # #####  #####  #    # #      #      #####  #    #
#     # ###### # #  # #    #     # #      #    # #    # #  ### #  ### #      #####
#     # #    # # #   ##    #     # #      #    # #    # #    # #    # #      #   #
#     # #    # # #    #    ######  ###### #####   ####   ####   ####  ###### #    #


def _build_main_debugger_window():
    sg.ChangeLookAndFeel(COLOR_SCHEME)
    def InVar(key1):
        row1 = [sg.T('    '),
                sg.I(key=key1, size=(WIDTH_VARIABLES,1)),
                sg.T('',key=key1+'CHANGED_', size=(WIDTH_RESULTS,1)),sg.B('Detail', key=key1+'DETAIL_'),sg.B('Obj', key=key1+'OBJ_'),]
        return row1

    variables_frame = [ InVar('_VAR1_'),
                        InVar('_VAR2_'),
                        InVar('_VAR3_'),]

    interactive_frame = [[sg.T('>>> ', size=(9,1), justification='r'), sg.In(size=(83,1), key='_INTERACTIVE_'),sg.B('Go', bind_return_key=True, visible=False)],
                         [sg.T('CODE >>> ',justification='r', size=(9,1)), sg.In(size=(83, 1), key='_CODE_')],
                         [sg.Multiline(size=(93,26),key='_OUTPUT_',autoscroll=True, do_not_clear=True)],]

    autowatch_frame = [[sg.Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                        sg.Button('Clear All Auto Watches'),
                        sg.Button('Show All Variables', key='_SHOW_ALL_'),
                        sg.Button('Locals', key='_ALL_LOCALS_'),
                        sg.Button('Globals', key='_GLOBALS_'),
                        sg.Button('Popout', key='_POPOUT_')]] + \
                      [
                        [sg.T('', size=(WIDTH_WATCHER_VARIABLES,1), key='_WATCH%s_'%i),
                         sg.T('', size=(WIDTH_WATCHER_RESULTS,2), key='_WATCH%s_RESULT_'%i, auto_size_text=True)] for i in range(1,NUM_AUTO_WATCH+1)]

    col1 = [
            [sg.Frame('Auto Watches', autowatch_frame, title_color='blue' )]
            ]

    col2 = [
        [sg.Frame('Variables or Expressions to Watch', variables_frame, title_color='blue'), ],
         [sg.Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue'), ]
            ]


    layout = [[sg.Pane([sg.Column(col1), sg.Column(col2)], size=(700, 640), orientation='h', background_color='red',show_handle=True, ),],
                [sg.Button('', image_data=red_x, key='_EXIT_', button_color=None),  sg.Text('Pull Red Line For REPL & Object Display Screen ---> ', size=(80,1), justification='r')]]

    window = sg.Window("I'm Watching You Debugger", layout, icon=PSGDebugLogo, margins=(0,0)).Finalize()
    window.Element('_VAR1_').SetFocus()
    Debugger.watcher_window = window
    sg.ChangeLookAndFeel('SystemDefault')
    return window


#     #                    #######                               #
##   ##   ##   # #    #    #       #    # ###### #    # #####    #        ####   ####  #####
# # # #  #  #  # ##   #    #       #    # #      ##   #   #      #       #    # #    # #    #
#  #  # #    # # # #  #    #####   #    # #####  # #  #   #      #       #    # #    # #    #
#     # ###### # #  # #    #       #    # #      #  # #   #      #       #    # #    # #####
#     # #    # # #   ##    #        #  #  #      #   ##   #      #       #    # #    # #
#     # #    # # #    #    #######   ##   ###### #    #   #      #######  ####   ####  #


def _refresh_main_debugger_window(mylocals, myglobals):
    if not Debugger.watcher_window:
        return False
    event, values = Debugger.watcher_window.Read(timeout=1)
    if event in (None, 'Exit', '_EXIT_'):                             # EXIT BUTTON / X BUTTON
        Debugger.watcher_window.Close()
        Debugger.watcher_window = None
        return False

    cmd_interactive = values['_INTERACTIVE_']
    cmd_code = values['_CODE_']
    cmd = cmd_interactive or cmd_code

    if event == 'Go':                                       # GO BUTTON
        Debugger.watcher_window.Element('_INTERACTIVE_').Update('')
        Debugger.watcher_window.Element('_CODE_').Update('')
        Debugger.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
        if cmd_interactive:
            expression = """imwatchingyou.Debugger.myrc = {} """.format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                Debugger.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(Debugger.myrc),append=True, autoscroll=True)

            except Exception as e:
                Debugger.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e),append=True, autoscroll=True)
        else:
            Debugger.watcher_window.Element('_CODE_').Update('')
            Debugger.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
            expression = """{}""".format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                Debugger.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(cmd), append=True, autoscroll=True)

            except Exception as e:
                Debugger.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e), append=True, autoscroll=True)

    elif event.endswith('_DETAIL_'):                        # DETAIL BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """imwatchingyou.Debugger.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + str(Debugger.myrc), title=var, non_blocking=True)
        except:
            pass
    elif event.endswith('_OBJ_'):                            # OBJECT BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """imwatchingyou.Debugger.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(sg.ObjToStringSingleObj(Debugger.myrc),title=var, non_blocking=True)
        except:
            pass
    elif event == '_LOCALS_':     # Show all locals BUTTON
        _choose_auto_watches(mylocals)
    elif event == '_ALL_LOCALS_':
        _display_all_vars(mylocals)
    elif event == '_GLOBALS_':
        _display_all_vars(myglobals)
    elif event == 'Clear All Auto Watches':
        if sg.PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
            Debugger.local_choices = {}
            Debugger.custom_watch = ''
            # Debugger.watcher_window.Element('_CUSTOM_WATCH_').Update('')
    elif event == '_POPOUT_':
        if not Debugger.popout_window:
            _build_floating_window()
    elif event == '_SHOW_ALL_':
        for key in Debugger.locals:
            Debugger.local_choices[key] = True if not key.startswith('_') else False

    # -------------------- Process the manual "watch list" ------------------
    for i in range(1, 4):
        key = '_VAR{}_'.format(i)
        out_key = '_VAR{}_CHANGED_'.format(i)
        Debugger.myrc =''
        if Debugger.watcher_window.Element(key):
            if values[key]:
                expression = """imwatchingyou.Debugger.myrc = {} """.format(values[key])
                try:
                    exec(expression, myglobals, mylocals)
                except Exception as e:
                    pass
                Debugger.watcher_window.Element(out_key).Update(Debugger.myrc)
            else:
                Debugger.watcher_window.Element(out_key).Update('')

    # -------------------- Process the automatic "watch list" ------------------
    slot = 1
    for key in Debugger.local_choices:
        if Debugger.local_choices[key] is True:
            Debugger.watcher_window.Element('_WATCH{}_'.format(slot)).Update(key)
            expression = """imwatchingyou.Debugger.myrc = {} """.format(key)
            try:
                exec(expression, myglobals, mylocals)
            except Exception as e:
                Debugger.myrc = ''
            Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(Debugger.myrc)
            slot += 1

            if slot + int(not Debugger.custom_watch in (None, '')) >= NUM_AUTO_WATCH:
                break

    if Debugger.custom_watch:
        Debugger.watcher_window.Element('_WATCH{}_'.format(slot)).Update(Debugger.custom_watch)
        expression = """imwatchingyou.Debugger.myrc = {} """.format(Debugger.custom_watch)
        try:
            exec(expression, myglobals, mylocals)
        except Exception as e:
            Debugger.myrc = ''
        Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(Debugger.myrc)
        slot += 1

    for i in range(slot, NUM_AUTO_WATCH+1):
        Debugger.watcher_window.Element('_WATCH{}_'.format(i)).Update('')
        Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

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


def _display_all_vars(dict):
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
        if cur_col +1 == num_cols:
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


def _choose_auto_watches(my_locals):
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
        line.append(sg.CB(key, key=key, size=(longest_line,1), default=Debugger.local_choices[key] if key in Debugger.local_choices else False))
        if cur_col +1 == num_cols:
            cur_col = 0
            layout.append(line)
            line = []
        else:
            cur_col += 1
    if cur_col:
        layout.append(line)

    layout += [[sg.Text('Custom Watch'),sg.Input(default_text=Debugger.custom_watch, size=(60,1), key='_CUSTOM_WATCH_')]]
    layout += [[sg.Ok(), sg.Cancel(), sg.Button('Clear All'), sg.Button('Select [almost] All', key='_AUTO_SELECT_')]]

    window = sg.Window('All Locals', layout, icon=PSGDebugLogo).Finalize()

    while True:             # event loop
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        elif event == 'Ok':
            Debugger.local_choices = values
            Debugger.custom_watch = values['_CUSTOM_WATCH_']
            break
        elif event == 'Clear All':
            sg.PopupQuickMessage('Cleared Auto Watches', auto_close=True, auto_close_duration=3, non_blocking=True, text_color='red', font='ANY 18')
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

#     #
#  #  # # #    # #####   ####  #    #
#  #  # # ##   # #    # #    # #    #
#  #  # # # #  # #    # #    # #    #
#  #  # # #  # # #    # #    # # ## #
#  #  # # #   ## #    # #    # ##  ##
## ##  # #    # #####   ####  #    #


def _build_floating_window():
    if Debugger.popout_window:
        Debugger.popout_window.Close()
    sg.ChangeLookAndFeel('Topanga')
    num_cols = 2
    width_var = 15
    width_value = 30
    layout = []
    line = []
    col = 0
    Debugger.popout_choices = Debugger.local_choices if Debugger.local_choices != {} else {}
    if Debugger.popout_choices == {}:
        for key in sorted(Debugger.locals.keys()):
            if not key.startswith('_'):
                Debugger.popout_choices[key] = True

    width_var = max([len(key) for key in Debugger.popout_choices])
    for key in Debugger.popout_choices:
        if Debugger.popout_choices[key] is True:
            value = str(Debugger.locals.get(key))
            line += [sg.Text(key, size=(width_var, 1), font='Sans 8'),sg.Text(' = ',font='Sans 8'), sg.Text(value, key=key, size=(width_value,1 if len(value) < width_value else 2 ), font='Sans 8'), sg.Text(' | ') if col +1 < num_cols else sg.T('')]
            col += 1
        if col >= num_cols:
            layout.append(line)
            line = []
            col = 0
    if col != 0:
        layout.append(line)
    layout = [[sg.Column(layout), sg.Column([[sg.Button('', key='_EXIT_',image_data=red_x,button_color=('#282923','#282923'), border_width=0)]])]]


    Debugger.popout_window = sg.Window('Floating', layout, alpha_channel=0, no_titlebar=True, grab_anywhere=True, element_padding=(0,0), margins=(0,0), keep_on_top=True,).Finalize()
    screen_size = Debugger.popout_window.GetScreenDimensions()
    Debugger.popout_window.Move(screen_size[0]-Debugger.popout_window.Size[0],0)
    Debugger.popout_window.SetAlpha(1)

    sg.ChangeLookAndFeel('SystemDefault')


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

def _refresh_floating_window():
    if not Debugger.popout_window:
        return
    for key in Debugger.popout_choices:
        if Debugger.popout_choices[key] is True:
            Debugger.popout_window.Element(key).Update(Debugger.locals.get(key))
    event, values = Debugger.popout_window.Read(timeout=1)
    if event in (None, '_EXIT_'):
        Debugger.popout_window.Close()
        Debugger.popout_window = None

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



def show_debug_window():
    frame = inspect.currentframe()
    try:
        Debugger.locals = frame.f_back.f_locals
        Debugger.globals = frame.f_back.f_globals
    finally:
        del frame

    Debugger.watcher_window = _build_main_debugger_window()
    return True

def show_popout_window():
    frame = inspect.currentframe()
    try:
        Debugger.locals = frame.f_back.f_locals
        Debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    if Debugger.popout_window:
        return
    if not Debugger.popout_window:
        _build_floating_window()

def refresh():
    frame = inspect.currentframe()
    try:
        Debugger.locals = frame.f_back.f_locals
        Debugger.globals = frame.f_back.f_globals
    finally:
        del frame
    _refresh_floating_window()
    rc = _refresh_main_debugger_window(Debugger.locals, Debugger.globals) if Debugger.watcher_window else False
    return rc


if __name__ == '__main__':
    # If running standalone, run until window closed by user
    show_debug_window()
    show_popout_window()
    while refresh():
        pass
