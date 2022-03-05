#############################################################################Imports

#import for graphical interface
import PySimpleGUI as sg

#import for SQL use
import sqlite3 as sql

#import to check network connection
import requests

#import to show database on shell
import pandas as pd

#import to look for data/files on the system
import os

#############################################################################Foundation

sg.theme('DarkBlue4')


#Variables for list items
DOS = 'Delete Data'
WA = 'Access Data'
SQLI = 'Insert Data'

#Variables for Demo
con = sql.connect('Demo.db')
cur = con.cursor()


#Layout
layout = [   [sg.Text('Demo Database or your Own:'), sg.Button('Demo Database'), sg.Button('Own Database')],
             [sg.Button(('Create Database'), disabled = True), sg.Text('Database:'), sg.InputText((), key= 'Database', disabled = True), sg.Button(('Connect'), disabled = True)],
             [sg.Button(('Latency Test'), disabled = True)],
             [sg.Listbox(values=(DOS, WA, SQLI), size=(30,3), key='Attacks', disabled = True),sg.Button(('i'),disabled = True), sg.Button(('Attack'), disabled = True)],
             [sg.Button(('Terminate Connection'), disabled = True),sg.Button('Close Application')]]

#Variables for Own Database
conn = sql.connect('Database')
cursor = conn.cursor()


window = sg.Window('Database Tester', layout)


event, values = window.read()

#############################################################################Functions

def Create():
    con = sql.connect('Demo.db')
    cur = con.cursor()
    #Creating the database table
    cur.execute('''
                 CREATE TABLE IF NOT EXISTS Demo
                 ([ID] INTEGER PRIMARY KEY, [Name] TEXT, [Password] CHAR, [Year] INT)''')

    #Inserting data into the Demo table of database
    cur.execute('''
                INSERT or REPLACE INTO Demo (ID, Name, Password, Year)

                     VALUES
                     (1, 'James Johannson', 'Shhsbwdjajhz736', 1974),
                     (2, 'Sarah Gordon', 'SjhddbiIDADUYU208!', 1987),
                     (3, 'Christopher Johnson', 'Sjsakjjbjkad058%', 1998),
                     (4, 'Marianna Pips','KSKNLSLkkncjai298*', 2000),
                     (5, 'Jacob Jordan', 'Starhcj209Hsyat$', 2003)
                 ''')

    #Commiting the SQL Queries
    con.commit()

    #Selecting  everything that there is in the Demo Table of the Database
    cur.execute('''
                SELECT * FROM Demo
                ''')

    #Print on command line shell what has been selected in using Select query
    df = pd.DataFrame(cur.fetchall())
    print(df)

    #GUI popup message box
    sg.popup("Database 'Demo' has been created")

    #Command Line Record
    print("Database 'Demo' has been created\n")


#Connecting to the database
def Connection():

    #set the input text as a variable
    conn = values['Database']

    #if this file in the variable is found connect to it
    if os.path.isfile(conn):
        sql.connect(values['Database'])
        
        #Command Line Record
        print("Connected to Database")
        
        #GUI popup message box
        sg.popup('Connected to Database')

    #if the file isn't found do this action
    else:
        
        #Command Line Record
        print("No Database has been found with this name\n")

        #GUI popup message box
        sg.popup('No Database has been found with this name')
    

#User decides whether using database created in the system or their own
def Decision():
    window['Create Database'].update(disabled=True)
    window['Connect'].update(disabled=True)
    window['Database'].update(disabled=True)
    window['i'].update(disabled=True)
    window['Latency Test'].update(disabled=True)
    window['Attacks'].update(disabled=True)
    window['Attack'].update(disabled=True)
    window['Terminate Connection'].update(disabled=True)
    
    #If clicked on demo database then create button will be enabled
    if event == 'Demo Database':
        window['Demo Database'].update(disabled=True)
        window['Own Database'].update(disabled=True)
        window['Create Database'].update(disabled=False)
        window['i'].update(disabled=False)
        window['Latency Test'].update(disabled=False)
        window['Attacks'].update(disabled=False)
        window['Attack'].update(disabled=False)
        window['Terminate Connection'].update(disabled=False)
        
        #GUI popup message box
        sg.popup('You have chosen Demo Database')
        
        #Command Line Record
        print("You have chosen Demo Database\n")
        
    #If clicked on Own Database then connect button will be enabled
    elif event == 'Own Database':
        window['Demo Database'].update(disabled=True)
        window['Own Database'].update(disabled=True)
        window['Connect'].update(disabled=False)
        window['Database'].update(disabled=False)
        window['i'].update(disabled=False)
        window['Latency Test'].update(disabled=False)
        window['Attacks'].update(disabled=False)
        window['Attack'].update(disabled=False)
        window['Terminate Connection'].update(disabled=False)
        
        #GUI popup message box
        sg.popup('You have chosen your own Database')
        
        #Command Line Record
        print("You have chosen your own Database\n")

#Testing connection to the network
def LatencyTest():
    try:

        #check the connection to internet by tryiing to access google.com using requests package
        requests.get('https://www.google.com/').status_code
        LatencyTest = 'PASS'

        #if the connection is successful show this popup
        #GUI popup message box
        sg.popup('PASS - Connection to the network is strong enough')
        
        #Command Line Record
        print('PASS - Connection to the network is strong enough\n')
    except:
        LatencyTest = 'FAIL'

        #if the connection isn't  successful show this popup
        #GUI popup message box
        sg.popup('FAIL - Connection to the network is too weak')
        
        #Command Line Record
        print('FAIL - Connection to the network is too weak\n')
        #exit()

#performing database  attack dependant on what was chosen from the list and the result of the attack, this function is performed when the database is generated inside the app
def AutoAttack():

    #ResultProcess variable affects the outcome of the function
    ResultProcess = False

    #If denial of service attack is picked do this action
    if values['Attacks'] == [DOS]:

        #try to complete these commands
        try:

            #Deleting records from database
            #looping the amount of times equal to number of rows
            cur.execute("DELETE FROM Demo")

        #if something isn't completed then do this
        except:
            ResultProcess = True

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("Attack Failed - The Data was protected")
            
            #Command Line Record
            print("Attack Failed - The Data was protected\n")
        else:
            
            #GUI popup message box
            sg.popup("Attack Successful - The Data has been deleted")

            #Command Line Record
            print("Attack Successful - The Data has been deleted\n")

    #if weak authentication attack is picked do this action
    elif values['Attacks'] == [WA]:

        #try to complete these commands
        try:
            
            #check if database can be accessed
            #looping the amount of times equal to number of rows
            for row in cur.execute("SELECT * FROM Demo"):
            #if there or no rows print this out and in popup message
                
                #GUI popup message box
                sg.popup(row)
                
                #Command Line Record
                print(row)

        #if something isn't completed then do this
        except:
            ResultProcess = True

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("Attack Failed - The Weak Authentication attack wasn't Successful")
            
            #Command Line Record
            print("Attack Failed - The Weak Authentication attack wasn't Successful\n")
        else:
            
            #GUI popup message box
            sg.popup("Attack Successful - The Weak Authentication attack was Successful")
            
            #Command Line Record
            print("Attack Successful - The Weak Authentication attack was Successful\n")

    #if SQL Injection attack is picked do this action
    elif values['Attacks'] == [SQLI]:

        #try to complete these commands
        try:

            #Inserting data into the Demo table of database via SQL Injection
            cur.execute('''
                        INSERT or REPLACE INTO Demo (ID, Name, Password, Year)

                             VALUES
                             (6, 'Andrew Clark', 'Shhsdfgsagajhz736', 1974),
                             (7, 'John Hiller', 'SjhddytrtdADUYU208!', 1987),
                             (8, 'Phil Johnsen', 'Sjs grtbjkad058%', 1999)
                         ''')

            #Selecting all files in the database file with added files
            cur.execute('''
                SELECT * FROM Demo
                ''')

        #if something isn't completed then do this
        except:
            ResultProcess = True

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("Attack Failed - The SQL Injection attack wasn't Successful")
            
            #Command Line Record
            print("Attack Failed - The SQL Injection attack wasn't Successful\n")
        else:
            
            #GUI popup message box
            sg.popup("Attack Successful - The SQL Injection attack was Successful")
            
            #Command Line Record
            print("Attack Successful - The SQL Injection attack was Successful\n")

    #If no attack types was selected print/popup message this 
    else:
        
        #GUI popup message box
        sg.popup("Error: Attack Type not Selected")
        
        #Command Line Record
        print("Error: Attack Type not Selected\n")


#performing database  attack dependant on what was chosen from the list and the result of the attack, this function is performed when the database isn't generated from app
def attack():

    #ResultProcess variable affects the outcome of the function
    ResultProcess = False

    #If denial of service attack is picked do this action
    if values['Attacks'] == [DOS]:

        #try to complete these commands
        try:
            pass


        #if something isn't completed then do this
        except:
            pass

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("PASS - The SQL Injection attack wasn't Successful")
            
            #Command Line Record
            print("PASS - The SQL Injection attack wasn't Successful\n")
        else:
            
            #GUI popup message box
            sg.popup("FAIL - The SQL Injection attack was Successful")
            
            #Command Line Record
            print("FAIL - The SQL Injection attack was Successful\n")
            
    #if weak authentication attack is picked do this action
    elif values['Attacks'] == [WA]:

        #try to complete these commands
        try:
            pass

        #if something isn't completed then do this
        except:
            pass

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("PASS - The SQL Injection attack wasn't Successful")
            
            #Command Line Record
            print("PASS - The SQL Injection attack wasn't Successful\n")
        else:
            
            #GUI popup message box
            sg.popup("FAIL - The SQL Injection attack was Successful")
            
            #Command Line Record
            print("FAIL - The SQL Injection attack was Successful\n")
        
    #if SQL Injection attack is picked do this action
    elif values['Attacks'] == [SQLI]:

        #try to complete these commands
        try:
            pass

        #if something isn't completed then do this
        except:
            pass

        #If test was successfully done print/popup 'Fail' otherwise print 'Pass'
        if ResultProcess == True:
            
            #GUI popup message box
            sg.popup("PASS - The SQL Injection attack wasn't Successful")
            
            #Command Line Record
            print("PASS - The SQL Injection attack wasn't Successful\n")
        else:
            
            #GUI popup message box
            sg.popup("FAIL - The SQL Injection attack was Successful")
            
            #Command Line Record
            print("FAIL - The SQL Injection attack was Successful\n")
        
    #If no attack types was selected print/popup message this 
    else:
        
        #GUI popup message box
        sg.popup("Error: Attack Type not Selected")
        
        #Command Line Record
        print("Error: Attack Type not Selected\n")

#Refreshes all the fields to prepare for the new attack on new database
def ConTermination():
    
    #remove the text from the user input field
    window['Database'].update("")
    
    #unselect values from list if any are selected
    window['Attacks'].set_value([])
    window.refresh()

    #close the connection with database
    con.close()
    
    #show this popup
    #GUI popup message box
    sg.popup('Connection with database was terminated')
    
    #Command Line Record
    print('Connection with database was terminated\n')

    #Reset all buttons and fields to how they were when booting the system up
    window['Demo Database'].update(disabled=False)
    window['Own Database'].update(disabled=False)
    window['Create Database'].update(disabled=True)
    window['Connect'].update(disabled=True)
    window['Database'].update(disabled=True)
    window['Latency Test'].update(disabled=True)
    window['Attacks'].update(disabled=True)
    window['Attack'].update(disabled=True)
    window['Terminate Connection'].update(disabled=True)


#Close the application
def CloseApp():
    
    #close the application
    window.close()
    
    #show this popup
    #GUI popup message box
    sg.popup('Application has been closed')
    
    #Command Line Record
    print('Application has been closed\n')

#Show information regarding each attack type
def information():

    #Show information about inserting attack
    sg.popup('Insert Data - this attack is about testing the database  against unathorized insertion of data into the connected database')
    print("Insert Data - this attack is about testing the database  against unathorized insertion of data into the connected database\n")

    #Show information about accessing database attack
    sg.popup('Access Data - this attack is about testing the database against unauthorized access to the database')
    print("Access Data - this attack is about testing the database against unauthorized access to the database\n")

    #Show information about deletion of data in database attack
    sg.popup('Delete Data - this attack is about testing the database against unauthorized deletion of data within database')
    print("Delete Data - this attack is about testing the database against unauthorized deletion of data within database\n")


#Functions in the correct order
#Decision function is so that the user can decide whether he want a test on demo database or his own
#Create function is to create the demo database
#Connection function to allow user to connect to already existing database
#LatencyTest function to see if internet connnection is strong enough - this is optional
#AutoAttack function to perform the attack and see what the result from the attack is with generated database
#AutoAttack function to perform the attack and see what the result from the attack is with foreign database
#ConTermination function to close the connection between the application and the database
#CloseApp function to close the entire app down

#########################################################################Main Event Loop

#Main event loop starts here
Decision()

#while this loop is true repeat all the events within this loop
while True:
    event, values = window.read()
    
    #if create database is clicked perform Create function
    if event == 'Create Database':
        Create()
        
    #if connect button is clicked perform Connection function
    elif event == 'Connect':
        Connection()

    #if latency test button is clicked perform Latency test
    if event == 'Latency Test':
        LatencyTest()

    #if attack button is clicked perform Attack function
    if event == 'Attack':

        #if create button was clicked at the beginning run autoattack function
        #if event == 'Create Database':
        AutoAttack()

        #if connect button was clicked at beginning run attack function
        #elif event == 'Connect':
           # Attack()

        #else do nothing
        #else:
            #pass
        
    #if terminate connection button is clicked perform ConTermination function
    if event == 'Terminate Connection':
        ConTermination()
        window.refresh()
        Decision()

    #if i button is clicked information about attacks will be shown and what the attack will do to the database.
    if event == 'i':
        information()
    
    #if close application button is clicked perform CloseApp function
    if event == 'Close Application':
        CloseApp()

    #if the application is closed break from the loop
    #this statement is important as without this the application will crash when closing the application
    if event == sg.WIN_CLOSED:
        break





    

    

