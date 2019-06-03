import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

def get_html_content(url):
    try:
        html = requests.get(url, timeout=200)
        html.raise_for_status()
        html.encoding = html.apparent_encoding
        # return r.text
        return html.text
    except:
        print("Can't fetch the HTML content")

def parse_html(current_page_html, container=[]):
    soup = BeautifulSoup(current_page_html, 'html.parser')
    search_now_prices = soup.find_all(name="span", attrs={'class': 'search_now_price'})
    names = soup.find_all(name="a", attrs={'class': 'pic'})
    # for name in names:
    #     print(name['title'])
    print(len(search_now_prices), len(names))
    for name, search_now_price in zip(names, search_now_prices):
        # print(name['title'], search_now_price.string)
        container.append([name['title'], search_now_price.string])
    return container

def print_info(names_prices_lists):
    for names_prices_list in names_prices_lists:
        print(names_prices_list[0], names_prices_list[1])

def web_crawl(*args):
    try:
        value_0 = key.get()  # get the key to search
        value_1 = num.get()  # get the number of pages we want

        url = "http://search.dangdang.com/?key="

        # target_key = "计算机"
        # pages = 2  # default value of page numbers

        if value_1 < 1:
            messagebox.showwarning('Alert', "Your input must bigger than 0")

        names_and_prices = []
        for i in range(1, int(value_1) + 1):
            current_page_html = get_html_content(url + value_0 + "&act=input" + "&page_index=" + str(i))
            # print(current_page_html)
            print(f"Starting To Crawl Page{i}")
            parse_html(current_page_html, names_and_prices)
        print_info(names_and_prices)
        print('Get ' + str(len(names_and_prices)) + ' items in total.')
        for index, name_and_price in enumerate(names_and_prices):
            tree.insert("", index, text=str(index), values=(name_and_price[0], name_and_price[1]))
    except ValueError:
        pass

root = Tk()
root.title('Search Book&Price From Dangdang')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# some main widgets
# default key and num
key = StringVar(mainframe, value="计算机")
num = IntVar(mainframe, value=1)
# key word entry
key_entry = ttk.Entry(mainframe, width=11, textvariable=key)
key_entry.grid(row=1, column=2, sticky=(N, E))
# number of pages we want to search entry
num_entry = ttk.Entry(mainframe, width=11, textvariable=num)
num_entry.grid(row=2, column=2, sticky=(N, E))
# search button
search_button = ttk.Button(mainframe, text="Search", command=web_crawl)
search_button.grid(row=3, column=2, sticky=E)
# Treeview a widget that can create a table
tree = ttk.Treeview(mainframe)
tree.grid(row=4, column=1, columnspan=2)
tree["columns"] = ['Item', 'Price']
tree.column('Item')
tree.column('Price')
tree.heading('Item', text='Item')
tree.heading('Price', text='Price')

# some static labels
ttk.Label(mainframe, text='Key:').grid(row=1, column=1, sticky=W)
ttk.Label(mainframe, text='Page number:').grid(row=2, column=1, sticky=W)

#
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)
key_entry.focus()
root.bind('<Return>', web_crawl)

root.mainloop()
