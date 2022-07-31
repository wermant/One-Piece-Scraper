from asyncio.windows_events import NULL
from urllib.request import urlopen
import tkinter as tk
from functools import partial
import os

window = tk.Tk()
window.geometry("600x400")
url_base = "https://onepiece.fandom.com/wiki"

#finds the english name of the character searched for
def FindEngName(name):
    page=urlopen(url_base+'/'+name)
    html_bytes=page.read()
    html=html_bytes.decode('utf8')
    english_ind = html.find("Official English Name:")
    english_ind_start=english_ind+66
    english_ind=html[english_ind_start:].find('<')
    return html[english_ind_start:english_ind_start+english_ind]

#finds the devil fruit of a character if known
def FindDevilFruit(name):
    page=urlopen(url_base+'/'+name)
    html_bytes=page.read()
    html=html_bytes.decode('utf8')
    devil_ind=html.find("dfename")
    if devil_ind!=-1:
        devil_ind_start=devil_ind+115
        devil_ind=html[devil_ind_start:].find('Fruit')
        if devil_ind>30:
            devil_ind=html[devil_ind_start:].find('fruit')
        return html[devil_ind_start:devil_ind_start+devil_ind+5]
    else:
        return "No Devil Fruit"

#searches for character on button press
def CharacterSearch():
    for widget in window.winfo_children():
        if widget.winfo_class()=='Entry':
            name=widget.get()
    for widget in window.winfo_children():
        widget.destroy()
    nameLabel=tk.Label(text="Name: "+FindEngName(name)).pack()
    devilLabel = tk.Label(text="Devil Fruit: "+FindDevilFruit(name)).pack()
    menuButton = tk.Button(text="New Search",command=MainPage).pack()

#setup main gui page
def MainPage():
    for widget in window.winfo_children():
        widget.destroy()
    greeting = tk.Label(text="Welcome to the One Piece Web Scraper.", font=30)
    instructions= tk.Label(text="\n\nInsert a characters name and find some\ngeneral info on them in seconds.\n(Please replace spaces with an underscore)\n\n",font=25)
    namebox=tk.Entry(bg="gray",bd=6)
    searchButton = tk.Button(text="Search",command=CharacterSearch)
    greeting.pack()
    instructions.pack()
    namebox.pack()
    searchButton.pack()

MainPage()
window.mainloop()

