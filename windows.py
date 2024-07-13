import datetime
import json
from backend.sqlite import insert_customer, create_customertable_sqlite, update_customer, \
    update_item, create_itemtable_sqlite, insert_item, open_db, load_db, get, delete, insert_workorder
from backend.mathutils import get_price

item_right_click = ['', ['Edit Item', 'Delete Item']]
customer_right_click = ['', ['Edit Customer', 'Delete Customer']]


def new_item(gui):
    item_name = gui.Input(key='itemname')
    item_price = gui.Input(key='itemprice')
    layout = [[gui.Text('Item Name '), item_name],
              [gui.Text('Item Price '), item_price],
              [gui.Submit(key='item_submit'), gui.Cancel()]]
    window = gui.Window('New Item', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit', 'Cancel'):
            break
        if not values['itemname']:
            gui.popup('An Item Name is required')
        if not values['itemprice']:
            gui.popup('A price is required')
        db = open_db()
        insert_item(db, [values['itemname'], values['itemprice']])
        break
    window.close()


def edit_item(gui, iteminfo):
    item_name = gui.Input(key='itemname')
    item_price = gui.Input(key='itemprice')
    layout = [[gui.Text('Item Name '), item_name],
              [gui.Text('Item Price '), item_price],
              [gui.Submit(key='item_submit'), gui.Cancel()]]
    window = gui.Window('Edit Item', layout, finalize=True)

    loaded = False

    while True:

        if not loaded:
            window['itemname'].update(iteminfo[1])
            window['itemprice'].update(iteminfo[2])
            loaded = True
        event, values = window.read()

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit', 'Cancel'):
            break
        if not values['itemname']:
            gui.popup('Item Name is required')
        if not values['itemprice']:
            gui.popup('Item Price is required')
        if event == 'item_submit':
            db = load_db("items")
            update_item(db, [values['itemname'], values['itemprice'],
                             iteminfo[0]])
        break
    window.close()


def items(gui):
    item_table = gui.Table(
        headings=['Item ID', 'Item Name', 'Item Price'], values=[],
        auto_size_columns=True, expand_x=True, expand_y=True, justification='center',
        key='item_table', right_click_menu=item_right_click)
    new_item_button = gui.Button(button_text="New Item", key='new_item')  # New item button
    layout = [[new_item_button],
              [item_table]]

    window = gui.Window('Item List', layout, finalize=True, keep_on_top=True)

    loaded = False

    while True:

        if not loaded:
            #gui.popup_auto_close("Loading Items", keep_on_top=True)
            item_table.update(values=load_db("items"))
            loaded = True

        event, values = window.read()
        if event in (gui.WIN_CLOSED, 'Quit', 'Exit'):
            break  # Customer selection list closes here

        if event == 'new_item':
            window.close()
            new_item(gui)

        if event == 'Edit Item':
            window.close()
            info = item_table.Values[values['item_table'][0]]
            edit_item(gui, info)

        if event == 'Delete Item':
            db = open_db()
            info = item_table.Values[values['item_table'][0]]  # Gets item ID to be deleted.
            delete(db, "items", info)
            item_table.update(values=load_db("items"))

    window.close()


def new_customer(gui):
    first_name = gui.Input(key='first')
    last_name = gui.Input(key='last')
    company = gui.Input(key='company')
    email = gui.Input(key='email')
    phone = gui.Input(key='phone')
    layout = [[gui.Text('First Name '), first_name],
              [gui.Text('Last Name '), last_name],
              [gui.Text('Company '), company],
              [gui.Text('Email Address '), email],
              [gui.Text('Phone Number '), phone],
              [gui.Submit(key='customer_submit'), gui.Cancel()]]
    window = gui.Window('New Customer', layout, finalize=True)

    while True:
        event, values = window.read()

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit', 'Cancel'):
            break  # New customer window closes here
        if not values['company']:
            values['company'] = ''
        if not values['first']:
            gui.popup('First Name is required')
        if not values['last']:
            gui.popup('Last Name is required')
        if not values['email']:
            values['email'] = ''
        if not values['phone']:
            gui.popup('Phone Number is required')
        db = open_db()
        create_customertable_sqlite(db)
        insert_customer(db, [values['company'], values['first'], values['last'], values['email'], values['phone']])
        break
    window.close()


def work_order_window(gui, data, items):
    customer_button = gui.Button(button_text="Customer", key='customer_button')
    customer_label = gui.Text(key='customer_label', expand_x=True)
    price_label = gui.Text(key='price_label', expand_x=True)
    work_order_table = gui.Table(headings=["Item Number", "Item Name", "Price"],
                                 values=[],
                                 auto_size_columns=False, expand_x=True, expand_y=True, justification='center',
                                 key='-work_order_Table-')
    item_combo = gui.Combo(data, key='-itemcombobox-', enable_events=True, expand_x=True, bind_return_key=True)
    layout = [[gui.Text('Customer: ', key=''), customer_button],
              [customer_label],
              [item_combo],
              [work_order_table],
              [price_label],
              [gui.Submit(key='work_order_submit'), gui.Cancel(key='cancel_button')]]
    window = gui.Window('New Work Order', layout, finalize=True, margins=(100, 50), resizable=True)

    window.Maximize()

    itemslist = []
    itemnumlist = []

    window['-itemcombobox-'].bind("<Right>", " rightarrow")

    while True:
        event, values = window.read()

        if event == '-itemcombobox- rightarrow':
            x = list(filter(lambda y: values["-itemcombobox-"].title() in y, data))
            if len(x):
                window['-itemcombobox-'].update(value=x[0])

        if event == '-itemcombobox-':
            if values["-itemcombobox-"] in data:
                itemslist.append(items[data.index(values["-itemcombobox-"])])
                price = get_price(itemslist)
                price_label.update(f"Subtotal: {price}")
                price_label.metadata = price
                itemnumlist.append(items[data.index(values["-itemcombobox-"])][0])
                work_order_table.update(values=itemslist)

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit'):
            break  # New work order window closes here

        if event == 'cancel_button':
            window.close()

        if event == 'customer_button':
            customer = customers(gui)
            if not customer:
                pass
            else:
                customer_label.metadata = customer
                customer_label.update(f"{customer[2]} {customer[3]}")

        if event == 'work_order_submit':
            if not customer_label.metadata:
                gui.popup('A Customer is required.')
            else:
                # Workorder assembly and database placement will go here.
                jsonitemlist = json.dumps(itemnumlist)
                # (customerid, items, total)
                db = open_db()
                insert_workorder(db, [datetime.date.today(), customer_label.metadata[0], jsonitemlist, price_label.metadata])
                window.close()
                return "Submitted"

    window.close()


def customers(gui):
    customer_table = gui.Table(
        headings=['Customer ID', 'Company', 'First Name', 'Last Name', 'Email Address', 'Phone Number'], values=[],
        auto_size_columns=True, expand_x=True, expand_y=True, justification='center',
        key='customer_table')
    layout = [[customer_table]]

    window = gui.Window('Customer List', layout, finalize=True, keep_on_top=True)

    loaded = False

    window['customer_table'].bind("<Double-Button-1>", " Double")

    while True:

        if not loaded:
            #gui.popup_auto_close("Loading Customers", keep_on_top=True)
            customer_table.update(values=load_db("customers"))
            loaded = True

        event, values = window.read()
        if event in (gui.WIN_CLOSED, 'Quit', 'Exit'):
            break  # Customer selection list closes here

        if event == 'customer_table Double':
            window.close()
            return customer_table.Values[values['customer_table'][0]]

    window.close()


def customer_list(gui):  # Customer button
    new_customer_button = gui.Button(button_text="New Customer", key='new_customer')  # New Customer Button
    customer_table = gui.Table(
        headings=['Customer ID', 'Company', 'First Name', 'Last Name', 'Email Address', 'Phone Number'], values=[],
        auto_size_columns=True, expand_x=True, expand_y=True, justification='center',
        key='customer_table', right_click_menu=customer_right_click)
    layout = [[new_customer_button],
              [customer_table]]

    window = gui.Window('Customer List', layout, finalize=True, keep_on_top=True)

    loaded = False

    while True:

        if not loaded:
            #gui.popup_auto_close("Loading Customers", keep_on_top=True)
            customer_table.update(values=load_db("customers"))
            loaded = True

        event, values = window.read()

        if event == 'new_customer':
            window.close()
            new_customer(gui)  # When "New Customer" button is clicked

        if event == 'Edit Customer':
            window.close()
            info = customer_table.Values[values['customer_table'][0]]
            edit_customer(gui, info)
        if event == 'Delete Customer':
            db = open_db()
            info = customer_table.Values[values['customer_table'][0]]  # Gets customer ID to be deleted.
            delete(db, "customers", info[0])
            customer_table.update(values=load_db("customers"))

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit'):
            break  # Customer List closes here

    window.close()


def edit_customer(gui, customerinfo):
    first_name = gui.Input(key='first')
    last_name = gui.Input(key='last')
    company = gui.Input(key='company')
    email = gui.Input(key='email')
    phone = gui.Input(key='phone')
    layout = [[gui.Text('First Name '), first_name],
              [gui.Text('Last Name '), last_name],
              [gui.Text('Company '), company],
              [gui.Text('Email Address '), email],
              [gui.Text('Phone Number '), phone],
              [gui.Submit(key='customer_submit'), gui.Cancel()]]
    window = gui.Window('New Customer', layout, finalize=True)

    loaded = False

    while True:

        if not loaded:
            window['first'].update(customerinfo[2])
            window['company'].update(customerinfo[1])
            window['last'].update(customerinfo[3])
            window['phone'].update(customerinfo[5])
            window['email'].update(customerinfo[4])
            loaded = True
        event, values = window.read()

        if event in (gui.WIN_CLOSED, 'Quit', 'Exit', 'Cancel'):
            break  # New customer window closes here
        if not values['company']:
            values['company'] = ''
        if not values['first']:
            gui.popup('First Name is required')
        if not values['last']:
            gui.popup('Last Name is required')
        if not values['email']:
            values['email'] = ''
        if not values['phone']:
            gui.popup('Phone Number is required')
        if event == 'customer_submit':
            db = open_db()
            update_customer(db, [values['company'], values['first'], values['last'], values['email'], values['phone'],
                                 customerinfo[0]])
        break
    window.close()
