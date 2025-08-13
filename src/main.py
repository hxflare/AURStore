import requests
import tkinter as tk
import customtkinter as cutk
from PIL import Image
import os
from tkhtmlview import HTMLLabel
import markdown
from deschandler import Desc
import threading
import subprocess
from pacman import PacmanHandler
descparse=Desc()
cutk.set_appearance_mode("system")
cutk.set_default_color_theme("blue")
# warning: ass code below

ui = cutk.CTk()
ui.geometry("1000x700")
ui.title("AURStore")
# initialized tabs
tabs = cutk.CTkTabview(ui)
tabs.add("Settings")
tabs.add("Description")
tabs.add("Installed")
tabs.add("Search")
tabs.pack(fill=tk.BOTH, expand=True)
maxammount=1000
selectedHelper="yay"
helperSpreadsheet={"yay": "-S"}
try:
    for child in tabs.winfo_children():
        if isinstance(child, cutk.CTkSegmentedButton):
            child.pack_forget()
            break
except:
    pass

try:
    tabs._segmented_button.configure(height=0)
    tabs._segmented_button.pack_configure(pady=0)
except:
    pass
# open the tab
def set_tab(value):
    print(f"opened tab: {value}")
    tabs.set(value)
# actual search
def search_for():
    query = searchEntry.get()
    print(f"searching for: {query}") 
    for child in searchResults.winfo_children():
        child.destroy()
    if query != "":
        url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}&limit=100"
        response = requests.get(url)
        data = response.json()
        if data["type"] == "search":
            ammount = 0
            data["results"].sort(key=lambda pkg: pkg.get("Popularity", 0), reverse=True)
            for pkg in data["results"]:
                if ammount <= maxammount:
                    def download_pkg(name=pkg["Name"]):
                        print("downloading package "+name)
                        commandOutput=subprocess.run([selectedHelper, helperSpreadsheet[selectedHelper],name],capture_output=True,text=True)
                        print("command output: "+commandOutput.stdout)
                    def open_description(url=pkg["URL"]):
                        tabs.set("Description")
                        htmltext.set_html("") 
                        progressbar=cutk.CTkProgressBar(
                            tabs.tab("Description"),
                            mode="indeterminate"
                        )
                        progressbar.pack()
                        progressbar.start()
                        ui.update_idletasks() 
                        def load_html():
                            html=html=descparse.getHtml(url)   
                            ui.after(0, lambda: (
                                htmltext.set_html(html),
                                progressbar.destroy()
                            ))
                        threading.Thread(target=load_html, daemon=True).start()                    
                    resultFrame = cutk.CTkFrame(
                        searchResults,
                        height=70,
                        width=340,
                        corner_radius=10,
                        fg_color="#636363"
                    )
                    download = cutk.CTkButton(
                        resultFrame, 
                        text="D", 
                        fg_color="green",
                        command=download_pkg,
                        height=30,
                        width=30,
                        corner_radius=100)
                    info=cutk.CTkButton(
                        resultFrame,text="I",
                        fg_color="orange",
                        text_color="white",
                        height=30,width=30,
                        corner_radius=100,
                        command=open_description,
                        )
                    info.pack(side=tk.BOTTOM,padx=30,anchor=tk.SE,pady=20)
                    download.pack(side=tk.TOP,padx=30,anchor=tk.NE,pady=20)
                    resultFrame.pack(padx=10, pady=10, fill=tk.X)
                    result = cutk.CTkLabel(
                        master=resultFrame,
                        text_color="white",
                        font=("Arial", 14),
                        text=f"{pkg['Name']} {pkg['Version']}",
                        width=300,
                        corner_radius=10
                    )
                    Desc = cutk.CTkLabel(
                        master=resultFrame,
                        text_color="white",
                        text=f"Description: {pkg['Description']}",
                        corner_radius=10,
                        width=300,
                        justify="left",
                        wraplength=450
                    )
                    result.pack(pady=10, padx=10, side=tk.LEFT, anchor=tk.NW)
                    Desc.pack(pady=20, padx=10, side=tk.LEFT, anchor=tk.SE)
                    ammount += 1
            print(f"search ended, found {ammount} results")
# why doesnt ctkscrollableframe have a mousewheel scrolling function?
def on_mousewheel(event):
    if event.num == 4:
        searchResults._parent_canvas.yview_scroll(-1, "units")
    elif event.num == 5:
        searchResults._parent_canvas.yview_scroll(1, "units")
# the search tab
menuBar = cutk.CTkFrame(tabs.tab("Search"), height=50,fg_color="#363636")
menuBar.pack(side=tk.TOP, fill=tk.X,)

tab_switcher = cutk.CTkSegmentedButton(
    menuBar,
    values=["Search", "Installed", "Settings"],
    command=set_tab,
    corner_radius=10,
    unselected_hover_color="#5a85e0"
)
tab_switcher.pack(side=tk.LEFT,pady=15, padx=90)
tab_switcher.set("Search")

searchResults = cutk.CTkScrollableFrame(tabs.tab("Search"), width=400, height=100, label_text="Results:")
searchBar = cutk.CTkFrame(menuBar, height=40, corner_radius=10)
searchEntry = cutk.CTkEntry(
    searchBar,
    height=20,
    placeholder_text="Find your package",
    fg_color="#2f2f2f",
    border_color="#3f6ad8",
    corner_radius=10
)

searchBar.pack(side=tk.RIGHT,anchor=tk.SE,padx=40, pady=10,)
searchEntry.pack(side=tk.LEFT, padx=5, pady=5)

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets/searchicon.png")
search_icon = cutk.CTkImage(light_image=Image.open(icon_path).convert("RGBA"), size=(20, 20))
searchButton = cutk.CTkButton(
    searchBar,
    image=search_icon,
    text="",
    command=search_for,
    width=20,
    height=20,
    corner_radius=10,
    fg_color="#3f6ad8",
    hover_color="#5a85e0"
)
searchButton.pack(side=tk.LEFT, padx=5, pady=5)

searchResults.pack(padx=20, pady=20, side=tk.RIGHT, anchor=tk.NE, fill=tk.BOTH, expand=True)
searchResults.bind_all("<Button-4>", on_mousewheel)
searchResults.bind_all("<Button-5>", on_mousewheel)
# description tab
def go_back():
    tabs.set("Search")
menuBardesc = cutk.CTkFrame(tabs.tab("Description"), height=50,fg_color="#363636")
menuBardesc.pack(side=tk.TOP, fill=tk.X,)
back=cutk.CTkButton(menuBardesc,text="⬅️",command=go_back,width=40,height=40)
back.pack(side=tk.LEFT,padx=10)
tab_switcherdesc = cutk.CTkSegmentedButton(
    menuBardesc,
    values=["Search", "Installed", "Settings"],
    command=set_tab,
    corner_radius=10,
    unselected_hover_color="#5a85e0"
)
tab_switcherdesc.pack(side=tk.LEFT,pady=15, padx=40)
htmltext=HTMLLabel(tabs.tab("Description"),html="",background="#636363",)
htmltext.pack(fill=tk.BOTH,expand=True,padx=20,pady=20)
#start with the search tab
tabs.set("Search")
ui.mainloop()