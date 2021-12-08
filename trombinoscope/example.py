"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""

from tkinter import *

class Foo(object):
    """
    Foo encapsulates a name and an age.
    """
    def __init__(self, name, age):
        """
        Construct a new 'Foo' object.

        :param name: The name of foo
        :param age: The ageof foo
        :return: returns nothing
        """
        self.name = name
        self.age = age

def bar(baz):
    """
    Prints baz to the display.
    """
    print(baz)


trombinoscope_main_window_title="Trombinoscope"
trombinoscope_main_window_initial_size='400x400'

if __name__ == '__main__':
  trombinoscope_main_window=Tk()
  trombinoscope_main_window.title(trombinoscope_main_window_title)
  trombinoscope_main_window.geometry(trombinoscope_main_window_initial_size)

  l1=Label(trombinoscope_main_window, text="My First Label")
  l1.grid(row=0, column=0)

  l1=Label(trombinoscope_main_window,text="Red Text",fg = "red",font = "Times")
  l1.grid(row=0,column=0)
  l2=Label(trombinoscope_main_window,text="Green Text",fg="light green",bg="green",font="Helvetica 14 bold")
  l2.grid(row=0,column=1)
  l3=Label(trombinoscope_main_window,text="blue Text",fg="blue",bg="green",font ="Times  14 bold")
  l3.grid(row=1,column=0)
  l4=Label(trombinoscope_main_window,text="Yellow Text",fg="yellow",bg="green",font="Times 14 bold")
  l4.grid(row=1,column=1)

  # Label with image
  # img=PhotoImage(file="python-logo.png")
  # l1=Label(win,image=img)
  # l1.grid(row=0,column=0)
  # win.mainloop()

  b1=Button(trombinoscope_main_window,text="Click Here",fg = "red")
  b1.grid(row=0,column=0)

  # Button with image
  # b=Button(win,image=img,width=100,height=100)
  # b.grid(row=2,column=2)

  quit_button=Button(trombinoscope_main_window, text="Quitter", command=quit)
  quit_button.grid(row=0, column=0)

  trombinoscope_main_window.mainloop()
