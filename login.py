import customtkinter
import sqlite3
import bcrypt
from tkinter import *
from tkinter import messagebox
#import DaiImg

app = customtkinter.CTk()
app.title('login')
#app.geometry('450x360')
app.geometry('780x450')
app.config(bg='#001220')

font1 = ('helvetica',25 ,'bold')
font2 = ('arial',17,'bold')
font3 = ('arial',13,'bold')
font4 = ('arial',13,'bold','underline')

#connection
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
username TEXT NOT NULL,
password TEXT NOT NULL)
''')

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if username != '' and password != '':
        cursor.execute('SELECT username FROM users WHERE username=?',[username])
        if cursor.fetchone() is not None:
            messagebox.showerror('Error','Username already exists.')
        else:
            encoded_password = password.encode('utf-8')
            hashed_password = bcrypt.hashpw(encoded_password,bcrypt.gensalt())
            print(hashed_password)
            cursor.execute('INSERT INTO  users VALUES (?,?)',[username,hashed_password])
            conn.commit()
            messagebox.showinfo('successfully created','Account has been created.')
    else:
        messagebox.showerror('Error','Enter all data.')


def login_account():
    username = username_entry2.get()
    password = password_entry2.get()
    if username != '' and password != '':
        cursor.execute('SELECT password FROM users WHERE username=?',[username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode('utf-8'),result[0]):
                messagebox.showinfo('success','logged in successfully.')
                #DaiImg.generate()
            else:
                messagebox.showerror('Error','Invalid Password.')
        else:
            messagebox.showerror('Error', 'Invalid username.')
    else:
        messagebox.showerror('Error', 'Enter all data')

def login():
    frame1.destroy()
    frame2 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=770,height=450)
    frame2.place(x =0,y=0)

    image1 = PhotoImage(file='3.png')
    image1_label = Label(frame2,image=image1,bg = '#001220')
    image1_label.place(x=0,y=0)
    frame2.image1=image1

    login_label2=customtkinter.CTkLabel(frame2,font=font1,text='Log in ',text_color='#fff',bg_color='#001220')
    login_label2.place(x=580,y=20)

    global  username_entry2
    global password_entry2

    username_entry2 = customtkinter.CTkEntry(frame2,font=font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text_color='#a3a3a3',placeholder_text='Username',width=200,height=50)
    username_entry2.place(x=530,y=80)

    password_entry2 = customtkinter.CTkEntry(frame2,font=font2,show='*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='#004780',border_width=3,placeholder_text_color='#a3a3a3',placeholder_text='password',width=200,height=50)
    password_entry2.place(x=530,y=150)

    login_button2 = customtkinter.CTkButton(frame2,command=login_account,font=font2,text_color='#fff',text='Log in ',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
    login_button2.place(x=530,y=220)



frame1 = customtkinter.CTkFrame(app,bg_color='#001220',fg_color='#001220',width=770,height=460)
frame1.place(x = 0,y = 0)

#
image1 = PhotoImage(file='2.png')
image1_label = Label(frame1,image=image1,bg='#001220')
image1_label.place(x=0,y=0)

signup_entry = customtkinter.CTkLabel(frame1,font=font1,text='sign up',text_color='#fff',bg_color='#001220')
signup_entry.place(x = 580 ,y = 20)

username_entry = customtkinter.CTkEntry(frame1,font = font2,text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='orange',placeholder_text_color='#a3a3a3',placeholder_text='username',width=200,height=50)
username_entry.place(x=530,y=80)

password_entry = customtkinter.CTkEntry(frame1,font=font2,show = '*',text_color='#fff',fg_color='#001a2e',bg_color='#121111',border_color='orange',border_width=3,placeholder_text='password',placeholder_text_color='#a3a3a3',width=200,height=50)
password_entry.place(x = 530,y=150)

signup_button = customtkinter.CTkButton(frame1,command=signup,font =font2,text_color='#fff',text='sign up',fg_color='#00965d',hover_color='#006e44',bg_color='#121111',cursor='hand2',corner_radius=5,width=120)
signup_button.place(x=530,y=220)

login_label = customtkinter.CTkLabel(frame1,font = font3,text = 'already have an acounnt?',text_color='#fff',bg_color='black')
login_label.place(x=530,y=250)

login_button = customtkinter.CTkButton(frame1,command=login,font= font4,text_color='#00bf77',text='login',fg_color='#001220',hover_color='#001220',cursor='hand2',width=40)
login_button.place(x=695,y=250)

app.mainloop()