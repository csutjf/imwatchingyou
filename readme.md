        
![Downloads](http://pepy.tech/badge/pysimpleguidebugger)

It's 2019 and this project is still actively developed.

# imwatchingyou
## A real-time Python debugger.  
## Watch your program work without interrupting flow or its operation 

![SNAG-0390](https://user-images.githubusercontent.com/13696193/58595929-3fb73580-8240-11e9-9865-7443d04b8f56.jpg)

  
# Version 2.

Sorry if you were one of the early users and have had to endure shifting API calls.  Thankfully there have never been more than 3 calls to the entire SDK.  There continues to be 3 and they've gotten significantly easier for the user to use.

This should be the last time you will have to endure a set of API changes as drastic as these have been. Software development is an iterative thing you know.               
        
# imwatchingyou     

A "debugger" that's based on.  It was developed to help debug PySimpleGUI based programs, but it can be used to debug any program.  The only "hard requirement" is that a `refresh()` function be called on a "periodic basis".

What you can do with this "debugger" is:
* Set "watch points" that update in realtime
* Write expressions / code that update in realtime
* Use a REPL style prompt to type in "code" / modify variables

All of this is done using a secondary and separate windows from your primary application window.  

        
## Installation

Installation is via pip:

`pip install imwatchingyou`

or if you need to upgrade later:

`pip install --upgrade --no-cache-dir imwatchingyou`


Note that you need to install the debugger using pip rather than downloading.  There are some detailed technical reasons for this.  

So, don't forget: __You must pip install imwatchingyou in order to use it.__



## Integrating imwatchingyou Into Your Application

There are 3 lines of code to add to a program in order to make it debugger ready - The import, an initialization, a refresh function called periodically.  

Copy and paste these lines of code into your code just as you see them written.  Don't get clever and rename anything.  Don't do an "import as".  Just copy the lines of code.

Here is an entire program including this integration code:

```python
import PySimpleGUI as sg
import imwatchingyou            # STEP 1

"""
    Demo program that shows you how to integrate the PySimpleGUI Debugger
    into your program.
    This particular program is a GUI based program simply to make it easier for you to interact and change
    things.
    
    In this example, the debugger is not started initiallly. You click the "Debug" button to launch it
    There are THREE steps, and they are copy and pastes.
    1. At the top of your app to debug add
            import imwatchingyou
    2. When you want to show a debug window, call one of two functions:
        imwatchingyou.show_debug_window()
        imwatchingyou.show_popout_window()
    3. You must find a location in your code to "refresh" the debugger.  Some loop that's executed often.
        In this loop add this call:
        imwatchingyou.refresh()
"""

layout = [
            [sg.T('A typical PSG application')],
            [sg.In(key='_IN_')],
            [sg.T('        ', key='_OUT_', size=(30,1))],
            [sg.Radio('a',1, key='_R1_'), sg.Radio('b',1, key='_R2_'), sg.Radio('c',1, key='_R3_')],
            [sg.Combo(['c1', 'c2', 'c3'], size=(6,3), key='_COMBO_')],
            [sg.Output(size=(50,6))],
            [sg.Ok(), sg.Exit(), sg.Debugger(key='Debug')],
        ]

window = sg.Window('This is your Application Window', layout)

counter = 0
timeout = 100

# Start the program with the popout window showing so you can immediately start debugging!
imwatchingyou.show_popout_window()

while True:             # Your Event Loop
    event, values = window.Read(timeout=timeout)
    if event in (None, 'Exit'):
        break
    elif event == 'Ok':
        print('You clicked Ok.... this is where print output goes')
        imwatchingyou.show_popout_window()  # STEP 2 also
    elif event == 'Debug':
        imwatchingyou.show_debug_window()   # STEP 2
    counter += 1
    # to prove window is operating, show the input in another area in the window.
    window.Element('_OUT_').Update(values['_IN_'])

    # don't worry about the "state" of things, just call this function "frequently"
    imwatchingyou.refresh()                 # STEP 3 - refresh debugger

window.Close()

```

## Showing the debugger

There are 2 primary GUI windows the debugger has to show.
1. A small "Popout" window that floats on top of your other windows

![SNAG-0388](https://user-images.githubusercontent.com/13696193/58594980-2cef3180-823d-11e9-807f-7d7076dfe0d9.jpg)

2. The primary "Debugger" window is like 2 windows in 1 because of the use of a 'Pane' element that allow the entire window's contents to be replaced by other layout.

This is the "main debugger" window that shows variables, etc

![SNAG-0384](https://user-images.githubusercontent.com/13696193/58594982-2cef3180-823d-11e9-9288-dd94e72b8962.jpg)

The is the REPL portion of the debugger  You can also examine objects in detail on this page using the "Obj" button

![SNAG-0385](https://user-images.githubusercontent.com/13696193/58594981-2cef3180-823d-11e9-84f4-0e48223b1a3c.jpg)




### Refreshing the debugger

The most important call you need to make is a `imwatchingyou.refresh()` call.  

If debugginer a PySimpleGUI based application, this "refresh" call that must be added to your event loop.  Your `window.Read` call should have a timeout value so that it does not block.  If you do not have a timeout value, the debugger will not update in realtime.

If you are debugging a non-PySimpleGUI program, no problem, just put this call __somewhere that it will be called several times a second__.  Or say once a second at minimum.  This frequency will determine how quickly the variable values will change in your debug windows.

Add this line to the top of your event loop.
`imwatchingyou.refresh(locals(), globals())`


### Accessing the debugger windows

Your task is to devise a way for your appliction to call the needed 2 or 3 functions.  

If you're making a GUI program, then make a hotkey or a button that will call `imwatchingyou.show_debugger()` and you're off to the races!

Or maybe call the `show_popout_window` at the start of your program and forget about it.  Look up at it when yuo want to see the current value of a variable, but ignore it the rest of the time.


## The Future

LOTS of plans for this debugger in the future.  One of the immediate things I want to do is to integrate this into the PySimpleGUI.py file itself.  To include the debugger with the SDK so that it doesn't have to be installed.

This will enable the use of a "hotkey" or other mechanism to "magically launch" the debugger.  

I'll be adding a "Launch debugger" button for sure so that it's trivial for you to add this capability to your code.  

Watch this space in the future!  COOL SHIT COMING SOON! 


## Release Notes

### imwatchingyou 1.1   26-May-2019

* Addition of "Code" line so that things like "import os" can be run from the repl

### imwatchingyou 1.2.1   27-May-2019

* Can press ENTER for both REPL fields and it'll execute them!  NICE
* Code cleanup
* STILL under 200 lines of code!  WITH a GUI.


### imwatchingyou 1.3.0   27-May-2019

* New "Auto Watcher" feature
    * New viewing area for these variables
    * Chosen using a page of checkboxes
* Other cool shit that I can't recall. Was up coding all night
* Up to 250 lines of code in total, but I've been extremely inefficient. Can be compacted quite a bit. I went for readability for now.
    * Still the only 250 lines of Python code, real-time, GUI, watcher with REPL that you'll find anywhere

### imwatchingyou 1.4.1   27-May-2019

* Forgot release notes

### imwatchingyou 1.5.0   28-May-2019

* Lots of nice code cleanup
* Rework of auto-watching
    * Clear capability in 2 places
    * Can cancel out of choosing to make changes
    * Confirmation when choosing to clear auto-watches in main interface
    * Choose autowatches now has a "real event loop"... it also means it BLOCKS waiting on your choices
* Shows non-blocking, "Message" when clearing checkboxes
     
### imwatchingyou 1.6.0   28-May-2019  

* No more globals!  Cheating and using a class instead. Same diff
* Working of all interfaces is the best way to sum it up
* there are 45 differences that I don't feel like listing
* lots of shit changed

     
### imwatchingyou 1.7.0   28-May-2019  

* User interface change - expect lots of those ahead.  This was a good enough one to make a new release
* Nice selection interface for auto display
    * Next is to create a tiny version of this output that is a floating, tiny window


### imwatchingyou 2.0.0   29-May-2019  

Why 2.0?  So soon?   Well, yea.  Been working my ass off on this project and a LOT
has happened in a short period of time.  Major new functionality AND it breaks the APIs badly.  That was a major reason for 2.0.  Completely different set of calls.

* There are now 3 and only 3 user callable functions:
    1. `imwatchingyou.show_debug_window()`
    2. `imwatchingyou.show_popout_window()`
    3. `imwatchingyou.refresh()`
* These functions can be called in any order. You do not have to show a window prior to refreshing
* All of the initializing and state handling are handled for you behind the scenes, making it trivial for you to add to your code.
* The famous "Red X" added to this program too
* Changed user interfaces in a big way
* Experimenting with a  "Paned" main intrterface
    * It really paned me to do it this way
    * Perhaps tabs will be better in the future?
    * It looks pretty bitching
    * It makes this code COMPLETELY un-portable to other PySimpleGUI ports
    * This is another reason tabs are a better choice
* Lots of large letter comments
* New "Auto choose" features that will choose variables to watch for you
* New "Clear" features
* New PopOut window!!
    * Displays in the upper right corner of your display automatially - perhaps can move in the future releases
    * Stays on top always
    * Can be used with or without main debugger window
    * Can be easily shown with `imwatchingyou.show_popout_window()`
* Every call to `refresh()` will automatically refresh the list of available varaiables along with the values



# Design        
# Author 
 Mike B.        
        
   
# License        
 GNU Lesser General Public License (LGPL 3) +        
