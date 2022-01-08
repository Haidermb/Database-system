import datetime
import json
from os import access
from pprint import pprint 
import sqlite3

conn = sqlite3.connect('Access_Control.sqlite',check_same_thread=False)
conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name']
c = conn.cursor()
c.execute("PRAGMA foreign_keys = ON")


#################################################### USERS MODEL #################################################

class User:

    def __init__(self, userid=None, fname=None, lname=None, passw=None, dept=None, phone=None, isStudent=None,rollno=None, div=None,srno=None):
        self.srno = srno
        self.fname = fname
        self.lname = lname
        self.passw = passw
        self.userid = userid
        self.dept = dept
        self.rollno = rollno
        self.div = div
        self.phone = phone
        self.isStudent = isStudent

    # user json model
    def user_to_json(self):
        user_dict = {
            'userid': str(self.userid),
            'fname': self.fname,
            'lname':self.lname,
            'dept': self.dept,
            'rollno': self.rollno,
            'div': self.div,
            'phoneno': self.phone,
        }
        return user_dict

    # create user table
    def create_user():
        c.execute('''CREATE TABLE USERS
                (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    userid INTEGER NOT NULL,
                    fname TEXT NOT NULL,
                    lname TEXT NOT NULL,
                    passw TEXT NOT NULL,
                    rollno INTEGER,
                    div INTEGER,
                    dept TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    isStudent INTEGER NOT NULL
                ); ''')
        conn.commit()
            
    # insert user to table
    def insert_user(self,user):
        #TODOChinmay : To unpack data and plot it to insert command and to return the after process for eg (success, failed)

        c.execute("INSERT INTO USERS(userid,fname,lname,passw,rollno,div,dept,phone,isStudent) VALUES(:userid,:fname,:lname,:passw,:rollno,:div,:dept,:phone,:isStudent)",{'userid': user.userid,'fname': user.fname,'lname': user.lname,'passw':user.passw,'rollno': user.rollno,'div':user.div,'dept':user.dept,'phone': user.phone,'isStudent': user.isStudent})
        conn.commit()
        # dictdata = [dict(ix) for ix in sqldata]
        


    # Delete Data of table user
    def delete_user(user,c):
        c.execute("DELETE from USERS WHERE userid = :userid",{'userid': user.userid})
        conn.commit()


    # Update Data of table user
    def update_user(self,user,conn,c):
        with conn:
            c.execute(""" UPDATE USERS SET fname = :fname AND lname = :lname AND userid = :userid
                    WHERE id = :id""",{':userid':user.userid,'id': user.id, 'fname': user.fname, 'lname': user.lname})
            conn.commit()

    # get all users
    def getAllUsers(self):
        sqldata = c.execute(" SELECT * FROM USERS")
        dictdata = [dict(ix) for ix in sqldata]

        return dictdata
    
    # get a single user
    def getAUser(self,user):
        sqldata = c.execute("SELECT id,userid,fname,lname,rollno,div,dept,phone FROM USERS WHERE userid = :userid",{'userid':user})
        dictdata = [dict(ix) for ix in sqldata]
        # c.execute("SELECT * FROM USERS WHERE userid = ?",(user))
        # print(c.fetchall())
        return dictdata

    # get all students
    def getStudent():
        c.execute(" SELECT * FROM USERS WHERE isStudent = 1")
        print(c.fetchall())

    # get all professors
    def getProfessor(conn,c):
       profid =  c.execute(" SELECT * FROM USERS WHERE isStudent = 0")

        # pprint(c.fetchall())

    def __repr__(self):
        return f"Users('{self.fname}','{self.lname}','{self.userid}','{self.dept}','{self.rollno}','{self.phoneno}','{self.isStudent}')"

#################################################### ROOMS MODEL #################################################

class Rooms:

    def __init__(self, roomno=None, roomname=None):
        self.roomno = roomno
        self.roomname = roomname
       
    # create rooms
    def create_rooms(conn,c):
        with conn:   
            c.execute("""CREATE TABLE ROOMS
                        (
                            rid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            roomno INTEGER NOT NULL, 
                            roomname TEXT NOT NULL,
                            uid INTEGER NOT NULL,
                            profid INTEGER NOT NULL,
                            FOREIGN KEY(uid) 
                            REFERENCES USERS(id)
                        );
                    """)
            conn.commit()

    # Insert Data Into table rooms
    def insert_rooms(room,conn,c):
        with conn:
            c.execute("INSERT INTO ROOMS(roomno,roomname) VALUES(:roomno,:roomname);",{'roomno': room.roomno,'roomname':room.roomname})
            conn.commit()
    
    # Delete Data from table rooms
    def delete_rooms(room,conn,c):
        with conn:
            c.execute("DELETE FROM ROOMS WHERE roomno = :roomno",{'roomno': room.roomno})
            conn.commit()

    # Update Data Into table rooms
    def update_rooms_no(room,conn,c):
        with conn:
            c.execute("UPDATE ROOMS SET roomno = :roomno WHERE roomname = :roomname",{'roomno':room.roomno,'roomname':room.roomname})
            conn.commit()


    # get all rooms
    def getAllRooms(self):
        sqldata = c.execute("SELECT * FROM ROOMS")
        dictdata = [dict(ix) for ix in sqldata]

        return dictdata

    # get one room
    def getRoom(conn,room,c):
        with conn:
            c.execute(" SELECT * FROM ROOMS WHERE roomno = :roomno", {'roomno':room})
            pprint(c.fetchall())

    def __repr__(self):
        return f"Room('{self.id}','{self.roomno}','{self.uid}')"

#################################################### ACCESS-CONTROL MODEL #################################################

class Access_Control:

    def __init__(self,roomno=None,userid=None,profid=None,srno=None):
        self.srno = srno
        self.userid = userid
        self.roomno = roomno
        self.profid = profid

    # create access_control
    def create_access_control(conn,c):
        with conn:
            c.execute("""CREATE TABLE ACCESS_CONTROL
                        (
                            srno INTEGER PRIMARY KEY AUTOINCREMENT,
                            timein TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            timeout TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            userid INTEGER NOT NULL,
                            rid INTEGER NOT NULL,
                            FOREIGN KEY(userid) REFERENCES USERS(id),
                            FOREIGN KEY(rid) REFERENCES ROOMS(rid)
                        );
                    """)
            conn.commit()

    # def access_cont(conn,c):
    #     with conn:
    #         li = c.execute('SELECT userid,isStudent FROM users')
    #         li = c.fetchall()
    #         for i,k in li:
    #             userid = None
    #             profid = i
    #             if k == 1:
    #                 userid = i
    #                 profid = None
    #             c.execute("""INSERT INTO ACCESS_CONTROl(userid,rid,profid) VALUES(:userid,:rid,:profid)""",{'userid':userid,'rid': 801,'profid':profid})
    #             conn.commit()
    #     return None
    #insert data to table access_system
    def insert_access_control(ac,conn,c):
        with conn: 
            c.execute("INSERT INTO ACCESS_CONTROL(userid,profid,rid) VALUES(:userid,:profid,:rid)",{'userid':ac.userid,'profid':ac.profid,'rid':ac.roomno})
            conn.commit()
            # c.execute("INSERT INTO ACCESS_CONTROL(userid,roomid,timein,timeout) VALUES(:userid,:roomid,:timein,:timeout)",{'userid':ac.userid,'roomid':ac.roomid,'timein': ac.timein,'timeout': ac.timeout})


    # display all data
    def getAllACData(self):
        sqldata =c.execute("SELECT * FROM ACCESS_CONTROL")
        dictdata = [dict(ix) for ix in sqldata]

        return dictdata

    # update the timeout if timein exists 
    def update_access_data(data,conn,c):
        with conn:
            c.execute("UPDATE ACCESS_CONTROL SET old.timeout= new.timeout WHERE timein")

#################################################### LOGS MODEL #################################################

class Logs:

    def __init__(self,access_srno=None,timein=None,timeout=None,srno=None):
        self.srno = srno
        self.access_srno = access_srno
        self.timein = timein
        self.timeout = timeout

    # create logs table
    def create_logs(conn,c):
        with conn:
            c.executescript("""CREATE TABLE LOGS AS 
                SELECT USERS.userid AS 'LOGS_uid',
                ROOMS.roomno AS 'LOGS_roomno',
                ACCESS_CONTROL.timein AS 'LOGS_timein',
                ACCESS_CONTROL.timeout AS 'LOGS_timeout'
                FROM USERS,ROOMS,ACCESS_CONTROL
                WHERE USERS.id = ROOMS.uid
                AND ACCESS_CONTROL.timein AND ACCESS_CONTROL.timeout IS NOT NULL;
                """)

    # for inserting new data into logs
    def insert_trigger(conn,c):
        with conn:
            c.execute("""CREATE TRIGGER IF NOT EXISTS logs_trigger
                        AFTER INSERT ON ACCESS_CONTROL
                        WHEN new.rid AND new.profid OR new.rid AND new.userid IS NOT NULL
                        BEGIN
                            INSERT INTO LOGS(access_srno) VALUES(new.srno);
                        END;
                    """)

    # insert data to logs
    def insertDataToLog(conn,c,log):
        with conn:
            c.execute(" INSERT INTO LOGS(access_srno) VALUES(:access_srno);",{'access_srno': log.access_srno})

    # get all logs
    def getAllLogs():
        c.execute("SELECT * FROM LOGS")
        pprint(c.fetchall())
    


    def __repr__(self):
        return f"Logs('{self.userid}','{self.roomid}','{self.timein}','{self.timeout}')"

#############################################################################################################################