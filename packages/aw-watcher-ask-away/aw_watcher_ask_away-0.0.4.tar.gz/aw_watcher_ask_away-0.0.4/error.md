Traceback (most recent call last):
File "/home/jje/.local/bin/aw-watcher-ask-away", line 8, in <module>
sys.exit(main())
^^^^^^
File "/home/jje/Documents/github/Jeremiah-England/aw-watcher-ask-away/src/aw_watcher_ask_away/**main**.py", line 74, in main
if response := prompt(event):
^^^^^^^^^^^^^
File "/home/jje/Documents/github/Jeremiah-England/aw-watcher-ask-away/src/aw_watcher_ask_away/**main**.py", line 22, in prompt
return simpledialog.askstring(title, prompt)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.11/tkinter/simpledialog.py", line 411, in askstring
d = \_QueryString(title, prompt, **kw)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/usr/lib/python3.11/tkinter/simpledialog.py", line 388, in **init**
\_QueryDialog.**init**(self, \*args, **kw)
File "/usr/lib/python3.11/tkinter/simpledialog.py", line 283, in **init**
Dialog.**init**(self, parent, title)
File "/usr/lib/python3.11/tkinter/simpledialog.py", line 143, in **init**
self.wait_visibility()
File "/usr/lib/python3.11/tkinter/**init**.py", line 752, in wait_visibility
self.tk.call('tkwait', 'visibility', window.\_w)
\_tkinter.TclError: window ".!\_querystring" was deleted before its visibility changed
