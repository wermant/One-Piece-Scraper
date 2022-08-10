from asyncio.windows_events import NULL
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
import tkinter as tk
from functools import partial
import os
import io

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

def FindBounty(name):
    page=urlopen(url_base+'/'+name)
    html_bytes=page.read()
    html=html_bytes.decode('utf8')
    if html.find('href="/wiki/Bounties"')!=-1:
        bounty_ind = html.find('key="Beli.png"')
        if bounty_ind != -1:
            bounty_ind_start=html[bounty_ind:].find("</span>")+bounty_ind+7
            bounty_end = html[bounty_ind_start:].find("<")+bounty_ind_start
            return html[bounty_ind_start:bounty_end]
    else:
        return "No Bounty"

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

#Gets image of character from website
def FindImage(name):
    url=url_base+'/'+name
    htmldata = urlopen(url)
    soup=BeautifulSoup(htmldata,'html.parser')
    images=soup.find_all('img')
    for item in images:
        if "Anime" in item['src'] and "Post" in item['src']:
            return item['src']
    for item in images:
        if "Anime" in item['src']:
            return item['src']

#Gets characters group affiliation if known
def FindAff(name):
    page=urlopen(url_base+'/'+name)
    html_bytes=page.read()
    html=html_bytes.decode('utf8')
    affind = html.find("Affiliations:")
    affind = html[affind:].find("<a ")+affind
    affind_start=html[affind:].find(">")+1+affind
    affind_end=html[affind_start:].find("<")+affind_start
    return html[affind_start:affind_end]

#searches for character on button press
def CharacterSearch():
    for widget in window.winfo_children():
        if widget.winfo_class()=='Entry':
            name=widget.get()

    #checks if character is valid to search for
    try:
        urlopen(url_base+"/"+name)
    except HTTPError as err:
        if err.code == 404:
            err_label = tk.Label(text="Character not found, please try different\nspelling or new character",font=25).pack()
            return
    
    for widget in window.winfo_children():
        widget.destroy()
    
    #gets and adds image to frame
    raw_data=urlopen(FindImage(name)).read()
    im=Image.open(io.BytesIO(raw_data))
    im=im.resize([int(im.size[0]*.75),int(im.size[1]*.75)])
    width=im.size[0]
    im=ImageTk.PhotoImage(im)
    picture=tk.Label(image=im)
    picture.image = im
    picture.pack()
    picture.place(x=0,y=0)

    #gets and adds text info to frame
    nameLabel=tk.Label(text="Name: "+FindEngName(name),font=30)
    nameLabel.pack()
    nameLabel.place(x=width+5,y=0)

    affLabel = tk.Label(text="Affilation: "+FindAff(name),font=30)
    affLabel.pack()
    affLabel.place(x=width+5,y=50)

    devilLabel = tk.Label(text="Devil Fruit: "+FindDevilFruit(name),font=30)
    devilLabel.pack()
    devilLabel.place(x=width+5,y=100)

    bountyLabel = tk.Label(text="Bounty: "+FindBounty(name),font=30)
    bountyLabel.pack()
    bountyLabel.place(x=width+5,y=150)
    
    menuButton = tk.Button(text="New Search",command=MainPage)
    menuButton.pack()
    menuButton.place(x=width+5,y=200)


#setup main gui page
def MainPage():
    for widget in window.winfo_children():
        widget.destroy()
    greeting = tk.Label(text="Welcome to the One Piece Web Scraper.", font=30)
    instructions= tk.Label(text="\n\nInsert a characters first name and find some\ngeneral info on them in seconds.\n(Please replace spaces with an underscore)\n\n",font=25)
    namebox=tk.Entry(bg="gray",bd=6)
    searchButton = tk.Button(text="Search",command=CharacterSearch)
    greeting.pack()
    instructions.pack()
    namebox.pack()
    searchButton.pack()

MainPage()
window.mainloop()

