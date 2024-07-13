import os

import PySimpleGUI as Gui
from backend.sqlite import load_db, load_all, get
from windows import new_customer, work_order_window, customer_list, items, new_item, open_db

title = "Purl Point of Sale"
version = 1.0

Gui.theme('Dark Blue 3')

Menu = [['&File', ['Version', 'Exit']]]  # File top menu contents

#  Main page content

main_table = Gui.Table(headings=['#', 'Date', 'Company', 'First Name', 'Last Name', 'Total'],
                       values=[],
                       auto_size_columns=True, expand_x=True, expand_y=True, justification='center', key='-main_table-')

new_customer_button = Gui.Button(button_text="New Customer", key='new_customer')  # New Customer Button
customers_button = Gui.Button(button_text="Customers", key='customers')  # Customer list button
new_item_button = Gui.Button(button_text="New Item", key='new_item')  # New item button
items_button = Gui.Button(button_text="Items", key='items')  # Items button
new_workorder_button = Gui.Button(button_text="New Work Order", key='new_workorder')  # New Work Order Button


main_window = Gui.Window(title=title, layout=[[Gui.Menu(Menu)], [new_customer_button, customers_button, new_item_button,
                                                                 items_button, new_workorder_button], [main_table]],
                         margins=(100, 50), resizable=True, finalize=True)

main_window.Maximize()

workorders = []

loaded = False

while True:  # Event loop
    #  Grab all work orders from sqlite file, or from mysql database, update database from this.

    if not loaded:
        if not os.path.exists('./storage/'):
            os.mkdir('./storage/')
        db = open_db()
        load_all(db)
        info = load_db("workorders")
        db = open_db()
        for a in info:
            customer = get(db, "customer", a[2])
            workorders.append([a[0], a[1], customer[1], customer[2], customer[3], a[4]])
        #Gui.popup_auto_close("Loading Work Orders")
        main_table.update(values=workorders)
        loaded = True

    event, values = main_window.read()
    if event in (Gui.WIN_CLOSED, 'Quit', 'Exit'):
        break  # Window closes here

    if event == 'new_customer':
        new_customer(Gui)  # When "New Customer" button is clicked

    if event == 'customers':
        customer_list(Gui)

    if event == 'items':
        items(Gui)

    if event == 'new_item':
        new_item(Gui)

    if event == 'new_workorder':
        itemnames = []
        itemdb = load_db("items")
        for a in itemdb:
            itemnames.append(a[1])
        wo = work_order_window(Gui, itemnames, itemdb)  # When "New Work Order" button is clicked.
        if wo == "Submitted":
            workorders = []
            info = load_db("workorders")
            db = open_db()
            for a in info:
                customer = get(db, "customer", a[2])
                workorders.append([a[0], a[1], customer[1], customer[2], customer[3], a[4]])
            main_table.update(values=workorders)
    if event == 'Version':
        Gui.popup_scrolled(f"""Purl POS Version: {version}""", title=title)

main_window.close()
