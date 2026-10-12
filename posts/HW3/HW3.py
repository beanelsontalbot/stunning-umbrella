#!/usr/bin/env python
# coding: utf-8

# In[51]:


import os
import sqlite3
import random

def get_message_db():
    """
    checks if there is already a messages database; if not then it creates one.
    returns connection to the database as variable named message_db
    
    """
    global message_db
    if os.path.isfile('messages_db.sqlite'):
        return sqlite3.connect('messages_db.sqlite')
    else:
        message_db = sqlite3.connect("messages_db.sqlite", check_same_thread=False)
        cursor = message_db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                   handle TEXT,
                   message TEXT);''')
        return message_db

def insert_message(handle, message):
    """
    inserts a message and handle into the messages database
    returns none
    """
    with get_message_db() as conn:
        cursor = conn.cursor()
        cmd = f"""INSERT INTO messages (handle, message)
        VALUES ('{handle}', '{message}');"""
        cursor.execute(cmd)
        conn.commit()


def random_messages(n):
    with get_message_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(rowid) FROM messages')
        length = cursor.fetchone()
        mylist = [x for x in range(1, length[0] + 1)]
        randoms = tuple(random.sample(mylist, n))
        messages = []
        for x in randoms:
            cursor.execute(f'SELECT handle, message FROM messages WHERE rowid = {x};')
            messages.append(cursor.fetchone())
        return messages


# In[54]:


# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
from textwrap import dedent


# Initialize the app
app = Dash()

markdown_text1 = '''
# Message Bank

## Submit a new message to the bank here:
'''
markdown_text2 = '''


## View:

'''

# App layout

app.layout = html.Div(children=[
    dcc.Markdown(children=markdown_text1, style={'color':'darkblue'}),
    dcc.Textarea(
        id='message-input',
        placeholder='Message',
        style={'width': '100%', 'height': 100},
    ),
    dcc.Textarea(
        id='name-input',
        placeholder='Name/Handle',
        style={'width': '100%', 'height': 50},
    ),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='message-output', style={'whiteSpace': 'pre-line'}),
    dcc.Markdown(children=markdown_text2, style={'color':'green'}),
    dcc.Markdown(id='random-messages', dangerously_allow_html = True),
    html.Button('Update', id='update-button', n_clicks=0)
], style={'backgroundColor':'#F5F5F5', 'fontFamily':'sans-serif'})

bank = []

@callback(
    Output('message-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('message-input', 'value'),
    State('name-input', 'value')
)
def submit(n_clicks, message, handle):
    if n_clicks > 0:
        insert_message(handle, message)
        return 'Message received!'
    
@callback(
    Output('random-messages', 'children'),
    Input('update-button', 'n_clicks')
)
def view(n_clicks):
    messages = random_messages(5)
    display = ''''''
    rainbow = ['#15317E', '#0000A5', '#0000CD', '#045F5F', '#006A4E']
    for x in range(5):
        display += f'''
        <span style="color:{rainbow[x]}" children="{messages[x][1]}" />  
        
        \- *{messages[x][0]}*   
        
        '''
    return dedent(display)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




