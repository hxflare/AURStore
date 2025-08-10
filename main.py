import requests
import tkinter as tk
import customtkinter as cutk
from PIL import Image
import os
from tkhtmlview import HTMLLabel
import markdown

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
# the tabview is a dumbass, have to remove the inbuilt segmentedbutton
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
def setTab(value):
    print(f"opened tab: {value}")
    tabs.set(value)
#open the README.md
def open_md(url):
    get = requests.get(f"{url}/README.md").raise_for_status()
    content = get.text
    html_content = markdown.markdown(content)
# actual search
def searchFor():
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
                if ammount <= 100:
                    resultFrame = cutk.CTkFrame(
                        searchResults,
                        height=100,
                        width=340,
                        corner_radius=10,
                        fg_color="#636363"
                    )
                    download = cutk.CTkButton(resultFrame, text="download", fg_color="green")
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
    command=setTab,
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

icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "searchicon.png")
search_icon = cutk.CTkImage(light_image=Image.open(icon_path).convert("RGBA"), size=(20, 20))
searchButton = cutk.CTkButton(
    searchBar,
    image=search_icon,
    text="",
    command=searchFor,
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
#start with the search tab
tabs.set("Search")
ui.mainloop()