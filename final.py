import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
import datetime
import matplotlib.pyplot as pl
import numpy as np
from tkcalendar import DateEntry

## to return today's date to mysql

td=date.today()
d1=td.strftime("%Y-%m-%d")

## to establish connection betwwen mysql and python

conn = mysql.connector.connect(user='root', password='1234', host='localhost', charset='utf8')
cursor = conn.cursor()

## to create database and tables

cursor.execute("create database if not exists expense")
cursor.execute("use expense")
cursor.execute("CREATE TABLE IF NOT EXISTS admin (username varchar(20), password varchar(20))")
cursor.execute("CREATE TABLE IF NOT EXISTS addincome(source varchar(20), iamount float, explimit float, balance float)")
cursor.execute("CREATE TABLE IF NOT EXISTS addexpense(name varchar(20), purpose varchar(30), eamount float)")
cursor.execute("CREATE TABLE IF NOT EXISTS viewexp(name varchar(15), source varchar(20), amount float, purpose varchar(30),date varchar(15),balance float)")
cursor.execute("SELECT * FROM admin WHERE username = 'admin' AND password = 'admin'")

## inserting the username and password given by programmer into the admin table

if cursor.fetchone() is None:
    cursor.execute("INSERT INTO admin (username, password) VALUES('admin', 'admin')")

## traverse through all the windows

file2 = 'homeb.png'
file1 = 'get3.png'
font1='arialblack 35 bold'
font2 = 'arialblack 20 bold'
geo='1300x650+0+0'
msg = "Please complete the required field!"

def mainloop():
    global root,loginpg,vexp,addinc,addex,expense,dl,balance,curve,expmenu
    ## login page 
    def admin_login():
        root.destroy()
        loginpg = Tk()
        loginpg.title("EXPENSE TRACKER")
        loginpg.geometry(geo)
        loginpg.resizable(0,0)
        p2=PhotoImage(file='get2.png')
        Label(loginpg,image=p2).place(x=0,y=0)
        ## back button to go to the front page
        
        def call():
            loginpg.destroy()
            open_page()
        
        p3=PhotoImage(file = file2).subsample(3,3)
        Button(loginpg,image=p3,relief=SOLID,command=call).place(x=1200,y=20)
        ## to check if the user has input the correct name and password, if not, access is denied
        
        def login():
        
            if username.get() == "" or password.get() == "":
                messagebox.showinfo("MESSAGE",msg)
            else:
                cursor.execute("SELECT * FROM admin")
                b=cursor.fetchall()
                pl=[]
                for x in b:
                    for j in x:
                        pl.append(j)
                if username.get() == pl[0] or password.get() == pl[1]:
                    loginpg.destroy()
                    menu()
                else:
                    messagebox.showinfo("MESSAGE","Invalid username or password")
                    
        ## to create labels
        
        Label(loginpg, text = "USERNAME:",fg='black',bg='white',font=font1).place(x=320,y=250)            
        username = Entry(loginpg)
        username.configure(fg='black',font=font1,relief="solid")
        username.place(x=650,y=255,height=50,width=300)
        Label(loginpg, text = "PASSWORD:",fg='black',bg='white',font=font1).place(x=320,y=340)    
        password = Entry(loginpg)
        password.configure(fg='black',font=font1,show="*",relief="solid")
        password.place(x=650,y=343,height=50,width=300)
        Button(loginpg,text="LOGIN",fg="black",bg="white",font=("times","24","bold"),relief="solid",command=login).place(x=580,y=430)
        loginpg.mainloop()
    ## main menu page

    def menu():
        expmenu = Tk()
        expmenu.geometry(geo)
        expmenu.resizable(0,0)
        p1=PhotoImage(file=file1)
        Label(expmenu,image=p1).place(x=0,y=0)
        ## provides a logout button to go to the introduction page
        def call():
            expmenu.destroy()
            open_page()
        ## to create buttons
        addinc=Button(expmenu,text='Guide',bg='white',fg='black',font=font1,relief="solid",command=lambda:guide()).place(x=100,y=250,height=50,width=300)
        addex=Button(expmenu,text='Add Income',bg='white',fg='black',font=font1,relief="solid",command=lambda:addincome()).place(x=500,y=250,height=50,width=300)
        expense=Button(expmenu,text='Add Expense',bg='white',fg='black',font=font1,relief="solid",command=lambda:expensemenu).place(x=900,y=250,height=50,width=300)
        balance=Button(expmenu,text='View Expense',bg='white',fg='black',font=font1,relief="solid",command=lambda:viewexpense()).place(x=275,y=350,height=50,width=300)
        curve=Button(expmenu,text='Income-Expense Curve',bg='white',fg='black',font=font1,relief="solid",command=lambda:viewgraph()).place(x=675,y=350,height=50,width=300)
        Button(expmenu,text='LOGOUT',font=font1,bg='white',fg='black',relief="solid",command=call).place(x=1100,y=40,height=50,width=150)
        expmenu.mainloop()
    ## add income page
    def addincome():
        expmenu.destroy()
        addinc=Tk()
        addinc.geometry(geo)
        addinc.resizable(0,0)
        p1=PhotoImage(file='get4.png')
        l=Label(addinc,image=p1)
        l.place(x=0,y=0)
        
        ## back button helps you return to the main menu
        def call():
            addinc.destroy()
            menu()
        p3=PhotoImage(file =file2).subsample(3,3)
        b=Button(addinc,image=p3,relief=SOLID,command=call)
        b.place(x=1200,y=20)
        ## to save the info into the addincome table
        def save():
            so=source.get()
            am=amount.get()
            el=explim.get()
            if so == "" or am == "" or el == "":
                messagebox.showinfo("MESSAGE",msg)
            k="insert into addincome values('{}',{},{},{})".format(so,am,el,am)
            cursor.execute(k)
            conn.commit()
            addinc.destroy()
            menu()
        ## to create labels    
        
        Label(addinc, text = "SOURCE:",fg='black',bg='white',font=font1).place(x=380,y=235)            
        source = Entry(addinc)
        source.configure(fg='black',font=font1,relief="solid")
        source.place(x=660,y=235,height=40,width=270)
        
        Label(addinc, text = "AMOUNT:",fg='black',bg='white',font=font1).place(x=380,y=295)    
        amount = Entry(addinc)
        amount.configure(fg='black',font=font1,relief="solid")
        amount.place(x=660,y=295,height=40,width=270)
        Label(addex, text = "EXPENSE LIMIT:",fg='black',bg='white',font=font1).place(x=380,y=355)            
        explim= Entry(addex)
        explim.configure(fg='black',font=font1,relief="solid")
        explim.place(x=660,y=355,height=40,width=270)
        Button(addinc,text="UPDATE",fg="black",bg="white",font=("times","24","bold"),relief="solid",command=save).place(x=580,y=435)
        
        addinc.mainloop()
    ## add expense page
    def expensemenu():
        
        expmenu.destroy()
        vinc = Tk()
        vinc.geometry(geo)
        p1=PhotoImage(file=file1)
        Label(vinc,image=p1).place(x=0,y=0)
        def addexp(a):
            vinc.destroy()
            addex=Tk()
            addex.geometry(geo)
            addex.resizable(0,0)
            p1=PhotoImage(file='get5.png')
            Label(addex,image=p1).place(x=0,y=0)
            ## back button helps you return to the main menu
            def call():
                addex.destroy()
                menu()
            p3=PhotoImage(file = file2).subsample(3,3)
            Button(addex,image=p3,relief=SOLID,command=call).place(x=1200,y=20)
            ## to save the info into the addexpense table
            def save(a):
                na=name.get()
                pu=purpose.get()
                am=amount.get()
                
                if na == "" or pu == "" or am == "":
                    messagebox.showinfo("MESSAGE",msg)
                else:
                    
                    res = am.replace('.', '', 1).isdigit()
                    if (res):
                        if(float(a['values'][1])>=float(am) ):
        
                            ## updating expense limit after each entry in the addexpense table
                            amtspent=float(a['values'][1])-float(am)
                            cursor.execute("update addincome set explimit={} where source='{}'".format(amtspent,a['text']))
                            k="insert into addexpense values('{}','{}',{})".format(na,pu,am)
                            cursor.execute(k)
                            
                            ## fetching and calculating balance from the selected source in addincome table
                            k="select balance from addincome where source='{}'".format(a['text'])
                            cursor.execute(k)
                            balance=cursor.fetchone()[0]
                            balance=float(balance)-float(am)
                            ## updating the balance in addincome table using the selected source
                            ## inserting into viewexp table the respective datas  
                            cursor.execute("update addincome set balance={} where source='{}'".format(balance,a['text']))
                            k="insert into viewexp(name,source,amount,purpose,date,balance) values('{}','{}',{},'{}','{}',(select balance from addincome where source='{}'))".format(na,a['text'],am,pu,d1,a['text'])
                            cursor.execute(k)
                            conn.commit()
                            addex.destroy()
                            menu()
                        else:
                            messagebox.showinfo("MESSAGE","Expense limit exceeded!")
                    else:
                        messagebox.showinfo("MESSAGE","Enter amount in integer or float!")
                        
            ## to create labels 
            Label(addex, text = "EXPENSE LIMIT: {}".format(a['values'][1]),bg="#4D99A0",fg='white',font='arialblack 13 bold').place(x=570,y=160)
            Label(addex, text = "NAME:",fg='black',bg='white',font=font2).place(x=380,y=235)            
            name = Entry(addex)
            name.configure(fg='black',font=font2,relief="solid")
            name.place(x=660,y=235,height=40,width=270)
            Label(addex, text = "PURPOSE:",fg='black',bg='white',font=font2).place(x=380,y=295)            
            purpose = Entry(addex)
            purpose.configure(fg='black',font=font2,relief="solid")
            purpose.place(x=660,y=295,height=40,width=270)
            
            Label(addex, text = "AMOUNT:",fg='black',bg='white',font=font2).place(x=380,y=355)    
            amount = Entry(addex)
            amount.configure(fg='black',font=font2,relief="solid")
            amount.place(x=660,y=355,height=40,width=270)
            Button(addex,text="SUBMIT",fg="black",bg="white",font=("times","24","bold"),relief="solid",command=lambda:save(a)).place(x=580,y=435)
            addex.mainloop()
        ## back button helps you return to the main menu
        def call():
            vinc.destroy()
            menu()
        p3=PhotoImage(file = file2).subsample(3,3)
        Button(vinc,image=p3,relief=SOLID,command=call).place(x=1200,y=20)
        viewtv=ttk.Treeview(height=20,columns=('Source','Amount','Expense limit','Balance'))
        ## to carry the data selected from the add income table to the add expense page 
        def error():
            curitem = viewtv.focus()
            if (curitem):
                addexp(viewtv.item(curItem))
            else:
                messagebox.showinfo("MESSAGE","Please select the source field to continue!")
        
        ## getting the info from addincome table 
        def getallinc():
            records=viewtv.get_children()
            for j in records:
                viewtv.delete(j)
                
            conn=mysql.connector.connect(host='localhost',user='root',passwd='1234',db='expense',charset='utf8')
            cursor=conn.cursor(dictionary=True)
            query='select * from addincome'
            cursor.execute(query)
            data=cursor.fetchall()
                
            for i in data:
                viewtv.insert('','end',text=i['source'],values=(i['iamount'],i['explimit'],i['balance']))
            conn.close()        
        ## to display the info to the user using treeview
        def displayallinc():
            viewtv.place(x=20,y=100,width=1240,height=525)
            scrollbar = Scrollbar(vinc, orient="vertical",command=viewtv.yview)
            scrollbar.place(x=1258,y=100,height=525)
            viewtv.configure(yscrollcommand=scrollbar.set)
            viewtv.heading('#0',text='SOURCE')
            viewtv.column('#0',minwidth=0,width=312,anchor='center')
            viewtv.heading('#1',text="AMOUNT")
            viewtv.column('#1', minwidth=0, width=312,anchor='center')
            viewtv.heading('#2',text='EXPENSE LIMIT')
            viewtv.column('#2',minwidth=0,width=312,anchor='center')
            viewtv.heading('#3',text='BALANCE')
            viewtv.column('#3',minwidth=0,width=312,anchor='center')
            Label(addex, text = "PLEASE SELECT A SOURCE FIELD TO ADD EXPENSE!",bg="#4D99A0",fg='white',font='arialblack 15 bold').place(x=400,y=40)
            getallinc()
        displayallinc()
        
        ## helps you move to the add expense page using the selected source in income
        Button(addinc,text="NEXT",fg="black",bg="white",font=("times","24","bold"),relief="solid",command=error).place(x=580,y=435)
        vinc.mainloop()
    ## view expense page
    def viewexpense():
        expmenu.destroy()
        vexp = Tk()
        vexp.geometry(geo)
        p1=PhotoImage(file=file1)
        Label(vexp,image=p1).place(x=0,y=0)
        
        ## back button helps you return to the main menu
        def call():
            vexp.destroy()
            menu()
        p3=PhotoImage(file = file2).subsample(3,3)
        Button(vexp,image=p3,relief=SOLID,command=call).place(x=1200,y=20)
        viewtv=ttk.Treeview(height=20,columns=('name','source','amount','purpose','date','balance'))
        ## getting the info from addexpense table
        def getallexp():
            records=viewtv.get_children()
            
            for j in records:
                viewtv.delete(j)
                
            conn=mysql.connector.connect(host='localhost',user='root',passwd='1234',db='expense',charset='utf8')
            cursor=conn.cursor(dictionary=True)
            query='select * from viewexp'
            cursor.execute(query)
            data=cursor.fetchall()
                
            for i in data:
                viewtv.insert('','end',text=i['name'],values=(i['source'],i['amount'],i['purpose'],i['date'],i['balance']))
            conn.close()        
        ## to display the info to the user using treeview
        def displayallexp():
            viewtv.place(x=20,y=100,width=1240,height=525)
            scrollbar = Scrollbar(vexp, orient="vertical",command=viewtv.yview)
            scrollbar.place(x=1258,y=100,height=525)
            viewtv.configure(yscrollcommand=scrollbar.set)
            viewtv.heading('#0',text='NAME')
            viewtv.column('#0',minwidth=0,width=208,anchor='center')
            viewtv.heading('#1',text='SOURCE')
            viewtv.column('#1',minwidth=0,width=208,anchor='center')
            viewtv.heading('#2',text="AMOUNT")
            viewtv.column('#2', minwidth=0, width=208,anchor='center')
            viewtv.heading('#3',text='PURPOSE')
            viewtv.column('#3',minwidth=0,width=208,anchor='center')
            viewtv.heading('#4',text='DATE')
            viewtv.column('#4',minwidth=0,width=208,anchor='center')
            viewtv.heading('#5',text='BALANCE')
            viewtv.column('#5',minwidth=0,width=208,anchor='center')
            getallexp()
        displayallexp()
        vexp.mainloop()
        
    ## guide page
    def guide():
        expmenu.destroy()
        guide= Tk()
        guide.geometry(geo)
        p1=PhotoImage(file='get7.png')
        Label(guide,image=p1).place(x=0,y=0)
        
        ## back button helps you return to the main menu
        
        def call():
            guide.destroy()
            menu()
        p3=PhotoImage(file = file2).subsample(3,3)
        Button(guide,image=p3,relief=SOLID,command=call).place(x=1200,y=20)
        Label(guide, text = "If you want to add the income, which maybe from any source, into your log, simply click the add income \nbutton in the main menu and enter your source of income, the amount of income  and set the \nexpense limit of that particular source as per your desire. If you want to add an expense\n you get the choice of source of income that you wish to deduct money from. After clicking\n the back button, click the add expense button then the source. Then you need to enter the\n name, the purpose and the amount that you've spent. The expense limit will be displayed on the top\n for that particular source. So, if the expense exceeds the limit an error message will be thrown. If\n you want to view the expenses that you've made, click on the view expense button. If you want\n to view the income expense curve of that particular date, click on the button and choose\n the date from the calendar. If the date you've picked has no expenses, then an error\n mesage will be thrown.",bg="#458B98",fg='white',font='arialblack 17').place(x=115,y=250)
        guide.mainloop()
    ## income-expense graph page
    def viewgraph():
        expmenu.destroy()
        curve=Tk()
        curve.geometry(geo)
        curve.resizable(0,0)
        p1=PhotoImage(file='get6.png')
        l=Label(curve,image=p1)
        l.place(x=0,y=0)
        
        ## back button helps you return to the main menu
        
        def call():
            curve.destroy()
            menu()
        p3=PhotoImage(file = file2).subsample(3,3)
        b=Button(curve,image=p3,relief=SOLID,command=call)
        b.place(x=1200,y=20)
            
        ## gets data from the view expense table according to the date

        def plot(a):
            cursor.execute("select source,min(balance),date from viewexp group by date,source having date='{}'".format(a))
            data1=cursor.fetchall()
            if (data1==[]):
                messagebox.showinfo("MESSAGE","No expenses in the provided date. Try another date!")
            else:    
                x1=[]
                x2=[]
                so=[]
                c=0
                for j in data1:
                    ## gets data from addincome table for plotting the graph
                    
                    k="select source,balance,iamount from addincome where source='{}'".format(j[0])
                    cursor.execute(k)
                    data2=cursor.fetchall()   
                    
                    for f in data2:
                        x1.append(f[1])
                        x2.append(f[2])
                        so.append(f[0])
                        c+=1
                ## using matplotlib the graph is plotted on a daily basis
                x=np.arange(c)
                pl.bar(x,x2,color="#4D99A0",width=0.25,label="INCOME")
                pl.bar(x+0.25,x1,color="#265B68",width=0.25,label="BALANCE")
                pl.title("INCOME-BALANCE GRAPH")
                pl.xticks(x,so)
                pl.xlabel("Sources of income with balance")
                pl.ylabel("Amount")
                pl.legend(loc='upper right')
                pl.show()
        ## displays the calendar for the user to select the date
        
        cal = DateEntry(curve, width= 16, background= "black", foreground= "white",bd=2)
        cal.pack(pady=230)
        Label(addex, text = "PLEASE SELECT A DATE TO VIEW THE GRAPH!",bg="#4D99A0",fg='white',font='arialblack 20 bold').place(x=345,y=90)
        Button(curve, text = "NEXT",fg="black",bg="white",font=("times","15","bold"),relief="solid",command = lambda:plot(cal.get_date())).place(x=610,y=450)
        curve.mainloop()
    ## introduction page           

    def open_page():
        root = Tk()
        root.title("EXPENSE TRACKER")
        root.geometry(geo)
        root.resizable(0,0)
        p1=PhotoImage(file='get1.png')
        label(root,image=p1).place(x=0,y=0)
        Button(root,text='ADMIN LOGIN',bg='white',fg='black',font='arialblack 50 bold',relief="solid",command=lambda:admin_login()).place(x=600,y=125)
        root.mainloop()

    open_page()

mainloop()
