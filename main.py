from urllib.request import urlopen

url_base = "https://onepiece.fandom.com/wiki"

#finds the english name of the character searched for
def Find_Eng_Name(name):
    page=urlopen(url_base+'/'+name)
    html_bytes=page.read()
    html=html_bytes.decode('utf8')
    english_ind = html.find("Official English Name:")
    english_ind_start=english_ind+66
    english_ind=html[english_ind_start:].find('<')
    return html[english_ind_start:english_ind_start+english_ind
