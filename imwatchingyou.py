import PySimpleGUI as sg
import textwrap
import operator

"""
    A "Live Debugging Tool" - "Watch" your code without stopping it.  Graphical user interface
    Cointains a "REPL" that you can use to run code, etc
"""

PSGDebugLogo = b'R0lGODlhMgAtAPcAAAAAADD/2akK/4yz0pSxyZWyy5u3zZ24zpW30pG52J250J+60aC60KS90aDC3a3E163F2K3F2bPI2bvO3rzP3qvJ4LHN4rnR5P/zuf/zuv/0vP/0vsDS38XZ6cnb6f/xw//zwv/yxf/1w//zyP/1yf/2zP/3z//30wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAP8ALAAAAAAyAC0AAAj/AP8JHEiwoMGDCBMqXMiwoUOFAiJGXBigYoAPDxlK3CigwUGLIAOEyIiQI8cCBUOqJFnQpEkGA1XKZPlPgkuXBATK3JmRws2bB3TuXNmQw8+jQoeCbHj0qIGkSgNobNoUqlKIVJs++BfV4oiEWalaHVpyosCwJidw7Sr1YMQFBDn+y4qSbUW3AiDElXiWqoK1bPEKGLixr1jAXQ9GuGn4sN22Bl02roo4Kla+c8OOJbsQM9rNPJlORlr5asbPpTk/RP2YJGu7rjWnDm2RIQLZrSt3zgp6ZmqwmkHAng3ccWDEMe8Kpnw8JEHlkXnPdh6SxHPILaU/dp60LFUP07dfRq5aYntohAO0m+c+nvT6pVMPZ3jv8AJu8xktyNbw+ATJDtKFBx9NlA20gWU0DVQBYwZhsJMICRrkwEYJJGRCSBtEqGGCAQEAOw=='

COLOR_SCHEME = 'LightGreen'

WIDTH_VARIABLES = 12
WIDTH_RESULTS = 36

WIDTH_LOCALS = 80
NUM_AUTO_WATCH = 13

class Debugger():
    watcher_window = None
    local_choices = {}
    myrc = ''
    custom_watch = ''

# done purely for testing / show
def func(x=''):
    return 'return value from func()={}'.format(x)


def _non_user_init():
    sg.ChangeLookAndFeel(COLOR_SCHEME)
    def InVar(key1):
        row1 = [sg.T('    '),
                sg.I(key=key1, size=(WIDTH_VARIABLES,1)),
                sg.T('',key=key1+'CHANGED_', size=(WIDTH_RESULTS,1)),sg.B('Detail', key=key1+'DETAIL_'),sg.B('Obj', key=key1+'OBJ_'),]
        return row1

    variables_frame = [ InVar('_VAR1_'),
                        InVar('_VAR2_'),
                        InVar('_VAR3_'),]

    interactive_frame = [[sg.T('>>> ', size=(9,1), justification='r'), sg.In(size=(83,1), key='_INTERACTIVE_'), sg.B('Go', bind_return_key=True, visible=False)],
                         [sg.T('CODE >>> ',justification='r', size=(9,1)), sg.In(size=(83, 1), key='_CODE_')],
                         [sg.Multiline(size=(88,12),key='_OUTPUT_',autoscroll=True, do_not_clear=True)],]

    autowatch_frame = [[sg.Button('Choose Variables To Auto Watch', key='_LOCALS_'),
                        sg.Button('Clear All Auto Watches'),
                        sg.Button('Locals', key='_ALL_LOCALS_'),
                        sg.Button('Globals', key='_GLOBALS_')]] + [
                        [sg.T('', size=(WIDTH_VARIABLES,1), key='_WATCH%s_'%i),
                         sg.T('', size=(WIDTH_RESULTS,2), key='_WATCH%s_RESULT_'%i)] for i in range(1,NUM_AUTO_WATCH+1)]

    layout = [  [sg.Frame('Variables or Expressions to Watch', variables_frame, title_color='blue' )],
                [sg.Frame('REPL-Light - Press Enter To Execute Commands', interactive_frame, title_color='blue' ),sg.Frame('Auto Watches', autowatch_frame, title_color='blue' )],
                [sg.Button('Exit')]]

    window = sg.Window("I'm Watching You Debugger", layout, icon=PSGDebugLogo).Finalize()
    window.Element('_VAR1_').SetFocus()
    Debugger.watcher_window = window
    sg.ChangeLookAndFeel('SystemDefault')
    return window

def _event_once(mylocals, myglobals):
    if not Debugger.watcher_window:
        return False
    event, values = Debugger.watcher_window.Read(timeout=1)
    if event in (None, 'Exit'):                             # EXIT BUTTON / X BUTTON
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
            expression = """
imwatchingyou.Debugger.myrc = {} """.format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                Debugger.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(Debugger.myrc),append=True, autoscroll=True)

            except Exception as e:
                Debugger.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e),append=True, autoscroll=True)
        else:
            Debugger.watcher_window.Element('_CODE_').Update('')
            Debugger.watcher_window.Element('_OUTPUT_').Update(">>> {}\n".format(cmd), append=True, autoscroll=True)
            expression = """
{}""".format(cmd)
            try:
                exec(expression, myglobals, mylocals)
                Debugger.watcher_window.Element('_OUTPUT_').Update('{}\n'.format(cmd), append=True, autoscroll=True)

            except Exception as e:
                Debugger.watcher_window.Element('_OUTPUT_').Update('Exception {}\n'.format(e), append=True, autoscroll=True)

    elif event.endswith('_DETAIL_'):                        # DETAIL BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """
imwatchingyou.Debugger.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(str(values['_VAR{}_'.format(event[4])]) + '\n' + str(Debugger.myrc), title=var, non_blocking=True)
        except:
            print('Detail failed')
    elif event.endswith('_OBJ_'):                            # OBJECT BUTTON
        var = values['_VAR{}_'.format(event[4])]
        expression = """
imwatchingyou.Debugger.myrc = {} """.format(var)
        try:
            exec(expression, myglobals, mylocals)
            sg.PopupScrolled(sg.ObjToStringSingleObj(Debugger.myrc),title=var, non_blocking=True)
        except:
            print('Detail failed')
    elif event == '_LOCALS_':     # Show all locals BUTTON
        _choose_auto_watches(mylocals)
    elif event == '_ALL_LOCALS_':
        display_all_vars(mylocals)
    elif event == '_GLOBALS_':
        display_all_vars(myglobals)
    elif event == 'Clear All Auto Watches':
        if sg.PopupYesNo('Do you really want to clear all Auto-Watches?', 'Really Clear??') == 'Yes':
            Debugger.local_choices = {}
            Debugger.custom_watch = ''

    # -------------------- Process the manual "watch list" ------------------
    for i in range(1, 4):
        key = '_VAR{}_'.format(i)
        out_key = '_VAR{}_CHANGED_'.format(i)
        Debugger.myrc =''
        if Debugger.watcher_window.Element(key):
            if values[key]:
                expression = """
imwatchingyou.Debugger.myrc = {} """.format(values[key])
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
            expression = """
imwatchingyou.Debugger.myrc = {} """.format(key)
            try:
                exec(expression, myglobals, mylocals)
                Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(Debugger.myrc)
            except Exception as e:
                Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update('')
            slot += 1

            if slot + int(not Debugger.custom_watch in (None, '')) >= NUM_AUTO_WATCH:
                break

    if Debugger.custom_watch:
        print(f'adding custom {Debugger.custom_watch}')
        Debugger.watcher_window.Element('_WATCH{}_'.format(slot)).Update(Debugger.custom_watch)
        expression = """imwatchingyou.Debugger.myrc = {} """.format(Debugger.custom_watch)
        try:
            exec(expression, myglobals, mylocals)
            Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update(Debugger.myrc)
        except Exception as e:
            Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(slot)).Update('')
        slot += 1


    for i in range(slot, NUM_AUTO_WATCH+1):
        Debugger.watcher_window.Element('_WATCH{}_'.format(i)).Update('')
        Debugger.watcher_window.Element('_WATCH{}_RESULT_'.format(i)).Update('')

    return True


def display_all_vars(dict):
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
        elif event == 'Select All':
            for key in sorted_dict:
                window.Element(key).Update(False)
        elif event == '_AUTO_SELECT_':
            for key in sorted_dict:
                window.Element(key).Update(not key.startswith('_'))

    # exited event loop
    window.Close()
    sg.ChangeLookAndFeel('SystemDefault')

def refresh(locals, globals):
    return _event_once(locals, globals)

def initialize():
    Debugger.watcher_window = _non_user_init()


if __name__ == '__main__':
    # If running standalone, run until window closed by user
    initialize()
    while refresh(locals(), globals()):
        pass
