import mysql.connector, datetime
mycon = mysql.connector.connect(host='localhost',user='root',passwd='password',database='hotel')
if mycon.is_connected():
    print('Successfully connected.')

cursor = mycon.cursor()

# CREATING TABLES
createTable ='''CREATE TABLE IF NOT EXISTS C_DETAILS(CID VARCHAR(20) PRIMARY KEY,C_NAME VARCHAR(30),C_ADDRESS VARCHAR(100),C_AGE INT,
C_COUNTRY VARCHAR(30) ,P_NO VARCHAR(30),C_EMAIL VARCHAR(30))'''
cursor.execute(createTable)

createTable ="CREATE TABLE IF NOT EXISTS BOOKING_RECORD(CID VARCHAR(20),CHECK_IN DATE ,CHECK_OUT DATE, ROOM_CHOICE INT, ROOMNO INT, ROOMRENT INT)"
cursor.execute(createTable)

createTable = '''CREATE TABLE IF NOT EXISTS RESTAURANT(ROOMNO INT, CUISINE INT, QUANTITY INT, RESTAURANTBILL INT)'''
cursor.execute(createTable)

createTable ='''CREATE TABLE IF NOT EXISTS ENTERTAINMENT(ROOMNO INT, GAMES INT,HOURS INT,ENTERTAINMENT_BILL INT)'''
cursor.execute(createTable)

createTable = '''CREATE TABLE IF NOT EXISTS TOTAL(CID VARCHAR(20), C_NAME VARCHAR(30), ROOMNO INT, CHECK_IN DATE, CHECK_OUT DATE, ROOMRENT INT,
RESTAURANTBILL INT, ENTERTAINMENTBILL INT, TOTALAMOUNT INT)'''
cursor.execute(createTable)
mycon.commit()

def days(a,b):
    l1,l2 = a.split('-'), b.split('-')
    y1, m1, d1 = int(l1[0]),int(l1[1]),int(l1[2])
    y2, m2, d2 = int(l2[0]),int(l2[1]),int(l2[2])
    day1 = datetime.date(y1,m1,d1)
    day2 = datetime.date(y2,m2,d2)
    delta = day2 - day1
    return delta.days
    
def newuser():
    if mycon.is_connected():
        cursor=mycon.cursor()
        cid = input("Enter Customer Identification Number : ")
        if searchcid(cid) != True:
            name = input("Enter Customer Name : ")
            address = input("Enter Customer Address : ")
            age= input("Enter Customer Age : ")
            nationality = input("Enter Customer Country : ")
            phoneno= input("Enter Customer Contact Number : ")
            email = input("Enter Customer Email : ")
            sql = "INSERT INTO C_Details VALUES(%s,%s,%s,%s,%s,%s,%s)"
            values= (cid,name,address,age,nationality,phoneno,email)
            cursor.execute(sql,values)
            mycon.commit()
            print("\nNew Customer Entered In The System Successfully !")
            cursor.close()
        else:
            print("This customer ID already exists. Please allot another ID.")
        
def searchcid(x):
    if mycon.is_connected():
        cursor = mycon.cursor()
        query = "SELECT * FROM C_DETAILS WHERE CID = %s"
        cursor.execute(query,(x,))
        data = cursor.fetchall()
        if data:
            return True
        else:
            return False
        
def searchuser():
    if mycon.is_connected():
        cursor = mycon.cursor()
        print('''\n\tSEARCH BY: 1)Name    2)Phone no    3)Customer ID\n''')
        choice3 = int(input('Enter your choice: '))
        if choice3 == 1:
            name = input('Enter Customer Name: ')
            query = "SELECT * FROM C_DETAILS WHERE C_NAME = %s"
            cursor.execute(query,(name,))
            data = cursor.fetchall()
        
        elif choice3 == 2:
            phno = input('Enter Customer Contact Number: ')
            query = "SELECT * FROM C_DETAILS WHERE P_NO = %s"
            cursor.execute(query,(phno,))
            data = cursor.fetchall()
            
        elif choice3 == 3:
            cid = input('Enter Customer ID: ')
            query = "SELECT * FROM C_DETAILS WHERE CID = %s"
            cursor.execute(query,(cid,))
            data = cursor.fetchall()
        else:
            print('Invalid Input. Going Back to First Menu.')
            return

        if data:
            for row in data:
                print('\nID\t :',row[0])
                print('NAME\t :',row[1])
                print('ADDRESS  :',row[2])
                print('AGE\t :',row[3])
                print('COUNTRY  : ',row[4])
                print('PHONE NO :',row[5])
                print('EMAIL\t :',row[6])
        else:
            print("Record Not Found.")
        

def userEntry():
    print("""
        1---> New Customer
        2---> Existing Customer
    """)
    choice2 = int(input("Enter your choice: "))
    if choice2 == 1:
        newuser()
    elif choice2 == 2:
        searchuser()

def searchroom(x):
    if mycon.is_connected():
        cursor = mycon.cursor()
        query = "SELECT * FROM BOOKING_RECORD WHERE ROOMNO = %s"
        cursor.execute(query,(x,))
        data = cursor.fetchall()
        if data:
            return True
        else:
            return False
    
def bookingRecord():
    cid = input("Enter Customer ID: ")
    if searchcid(cid):
        cursor=mycon.cursor()
        checkin=input("\nEnter Customer CheckIN Date [ YYYY-MM-DD ] : ")
        checkout=input("Enter Customer CheckOUT Date [ YYYY-MM-DD ] : ")
        print ("\n##### We have The Following Rooms For You #####")
        print ("1. Ultra Royal ----> 5000 Rs.")
        print ("2. Royal ----> 4000 Rs. ")
        print ("3. Elite ----> 3000 Rs. ")
        print ("4. Budget ----> 2000 Rs. ")
        roomchoice=int(input("\nEnter Your Choice : "))
        while True:
            roomno=int(input("Enter Allotted Room No : "))
            if searchroom(roomno) != True:
                break
            else:
                print("Room is already reserved. Please allot another room.")
                
        query="INSERT INTO BOOKING_RECORD VALUES(%s,%s,%s,%s,%s,NULL)"
        values=(cid,checkin,checkout,roomchoice,roomno)
        cursor.execute(query,values)
        mycon.commit()
        noofdays = days(checkin,checkout)
        
        if roomchoice==1:
            roomrent = noofdays * 5000
            print("\nUltra Royal Room Rent : ",roomrent)
        elif roomchoice==2:
            roomrent = noofdays * 4000
            print("\nRoyal Room Rent : ",roomrent)
        elif roomchoice==3:
            roomrent = noofdays * 3000
            print("\nElite Royal Room Rent : ",roomrent)
        elif roomchoice==4:
            roomrent = noofdays * 2000
            print("\nBudget Room Rent : ",roomrent)
        else:
            print("Invalid Input. Going Back To First Menu.")
            return

        print("Thank You , Your Room Has Been Booked For : ",noofdays , "Days" )
        print("Your Total Room Rent is : Rs. ",roomrent)
        
        query3 = "UPDATE BOOKING_RECORD SET ROOMRENT = %s WHERE ROOMNO = %s"
        cursor.execute(query3,(roomrent,roomno))
        mycon.commit()
        
        print("\nCHECK-IN AND CHECK-OUT ENTRY MADE SUCCESSFULLY !")
        cursor.close()
    else:
        print("Customer ID does not exist. Kindly enter the correct customer ID.")
        
def Restaurant():
    if mycon.is_connected():
        cursor = mycon.cursor()
        roomno = int(input("Enter Room No: "))
        if searchroom(roomno):
            print("1. Vegetarian Combo                  -----> 300 Rs.")
            print("2. Non-Vegetarian Combo              -----> 500 Rs.")
            print("3. Vegetarian & Non-Vegetarian Combo -----> 750 Rs.")
            choice_dish = int(input("\nEnter Your Choice : "))
            quantity=int(input("Enter Quantity : "))
            if choice_dish==1:
                print("\nYou Have Ordered: Vegetarian Combo ")
                restaurantbill = quantity * 300
            elif choice_dish==2:
                print("\nYou Have Ordered: Non-Vegetarian Combo ")
                restaurantbill = quantity * 500
            elif choice_dish==3:
                print("\nYou Have Ordered: Vegetarian & Non-Vegetarian Combo ")
                restaurantbill= quantity * 750
            else:
                print("Invalid Input. Going Back To First Menu.")
                return
            
            sql= "INSERT INTO RESTAURANT VALUES(%s,%s,%s,%s)"
            values= (roomno,choice_dish,quantity,restaurantbill)
            cursor.execute(sql,values)
            mycon.commit()
            print("Your Total Bill Amount Is : Rs. ",restaurantbill)
            print("**** WE HOPE YOU WILL ENJOY YOUR MEAL ***\n" )
        else:
            print("Invalid Room Number.")

def Entertainment():
    if mycon.is_connected():
        cursor = mycon.cursor()
        roomno = int(input("Enter room no: "))
        if searchroom(roomno):
            print("""
            1. Table Tennis -----> 150 Rs./HR
            2. Bowling -----> 100 Rs./HR
            3. Snooker -----> 250 Rs./HR
            4. VR World Gaming -----> 400 Rs./HR
            5. Video Games -----> 300 Rs./HR
            6. Swimming Pool Games -----> 350 Rs./HR
            7. Exit
            """)
            game=int(input("Enter Game You Want To Play : "))
            hours=int(input("Enter No Of Hours : "))
            print("\n\n#################################################")
            if game==1:
                print("YOU HAVE SELECTED TO PLAY : Table Tennis")
                entertainmentbill = hours * 150
            elif game==2:
                print("YOU HAVE SELECTED TO PLAY : Bowling")
                entertainmentbill = hours * 100
            elif game==3:
                print("YOU HAVE SELECTED TO PLAY : Snooker")
                entertainmentbill = hours * 250
            elif game==4:
                print("YOU HAVE SELECTED TO PLAY : VR World Gaming")
                entertainmentbill = hours * 400
            elif game==5:
                print("YOU HAVE SELECTED TO PLAY : Video Games")
                entertainmentbill = hours * 300
            elif game ==6:
                print("YOU HAVE SELECTED TO PLAY : Swimming Pool Games")
                entertainmentbill = hours * 350
            else:
                print("Invalid Input. Going Back To First Menu.")
                return
            query= "INSERT INTO ENTERTAINMENT VALUES(%s,%s,%s,%s)"
            values= (roomno,game,hours,entertainmentbill)
            cursor.execute(query,values)
            mycon.commit()
            print("FOR : ",hours," HOURS")
            print("Your Total Entertainment Bill Is : Rs. ",entertainmentbill)
        else:
            print("Invalid Room Number.")

def totalAmount():
    if mycon.is_connected():
        cursor=mycon.cursor()
        roomno = int(input("Enter room no: "))
        if searchroom(roomno):
            query1 = "SELECT BOOKING_RECORD.CID, C_DETAILS.C_NAME, CHECK_IN, CHECK_OUT, ROOMRENT FROM BOOKING_RECORD, C_DETAILS WHERE BOOKING_RECORD.ROOMNO = %s AND C_DETAILS.CID = BOOKING_RECORD.CID"
            cursor.execute(query1,(roomno,))
            data = cursor.fetchone()
            cid,name,checkin,checkout,roomrent = data

            query2 = "SELECT SUM(RESTAURANTBILL) FROM RESTAURANT WHERE ROOMNO = %s"
            cursor.execute(query2,(roomno,))
            data = cursor.fetchone()
            restaurantbill = data[0]
            if restaurantbill == None:
                restaurantbill = 0

            query3 = "SELECT SUM(ENTERTAINMENT_BILL) FROM ENTERTAINMENT WHERE ROOMNO = %s"
            cursor.execute(query3,(roomno,))
            data = cursor.fetchone()
            entertainmentbill = data[0]
            if entertainmentbill == None:
                entertainmentbill = 0

            query4 = "INSERT INTO TOTAL VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            grandTotal = roomrent + restaurantbill + entertainmentbill
            values = (cid,name,roomno,checkin,checkout,roomrent,restaurantbill,entertainmentbill,grandTotal)
            cursor.execute(query4,values)
            mycon.commit()
            print("\n **** HOTEL AMBROSIA, TVM **** CUSTOMER BILLING ****")
            print("\nCUSTOMER NAME:",name)
            print("ROOMNO: ",roomno)
            print("CHECKIN DATE:",checkin)
            print("CHECKOUT DATE:",checkout)
            print("ROOM RENT: Rs.",roomrent)
            print("RESTAURANT BILL: Rs.",restaurantbill)
            print("ENTERTAINMENT BILL: Rs.",entertainmentbill)
            print("__________________________________________________")
            print("TOTAL AMOUNT : Rs.",grandTotal)
            query5 = "DELETE FROM BOOKING_RECORD WHERE ROOMNO = %s"
            query6 = "DELETE FROM RESTAURANT WHERE ROOMNO = %s"
            query7 = "DELETE FROM ENTERTAINMENT WHERE ROOMNO = %s"
            cursor.execute(query5,(roomno,))
            cursor.execute(query6,(roomno,))
            cursor.execute(query7,(roomno,))
            mycon.commit()
            cursor.close()
        else:
            print("Invalid Room Number.")
            
def searchOldBill():
    if mycon.is_connected():
        cursor = mycon.cursor()
        print('''\n\tSEARCH BY: 1)Customer ID    2)Name\n''')
        choice = int(input('Enter your choice: '))
        if choice == 1:
            cid = input('Enter Customer ID: ')
            query = "SELECT * FROM TOTAL WHERE CID = %s"
            cursor.execute(query,(cid,))
            data = cursor.fetchall()
        elif choice == 2:
            name = input('Enter Customer Name: ')
            query = "SELECT * FROM TOTAL WHERE C_NAME = %s"
            cursor.execute(query,(name,))
            data = cursor.fetchall()
        else:
            print('Invalid Input. Please Try Again.')
            return

        if data:
            for row in data:
                print('\nID\t\t   :',row[0])
                print('NAME\t\t   :',row[1])
                print('ROOMNO\t\t   :',row[2])
                print('CHECKIN DATE\t   :',row[3])
                print('CHECKOUT DATE\t   :',row[4])
                print('ROOM RENT\t   :',row[5])
                print('RESTAURANT BILL    :',row[6])
                print('ENTERTAINMENT BILL :',row[7])
                print('TOTAL AMOUNT\t   :',row[8])
                
        else:
            print("Record Not Found. Please Try Again.")
        

# Main program

print("""
*************** HOTEL MANAGEMENT SYSTEM *************************
***************** HOTEL AMBROSIA, TVM ***************************

******** HMS Software Designed By: ******************************
******** THOMAS BIJU CHEERAMVELIL, ADHVAY SANKAR, SRIRAM ********
""")

while True:
    print("""
        1---> Customer Details
        2---> Proceed for Booking and Room Selection
        3---> Restaurant Billing
        4---> Entertainment Bill
        5---> Generate Total Bill and Checkout
        6---> Search Old Bills
        7---> Exit \n""")

    choice = int(input("Enter Your Choice: "))
    if choice == 1:
        userEntry()
    elif choice ==2:
        bookingRecord()
    elif choice ==3:
        Restaurant()
    elif choice ==4:
        Entertainment()
    elif choice ==5:
        totalAmount()
    elif choice ==6:
        searchOldBill()
    elif choice ==7:
        break
    else:
        print("Invalid Input.")
