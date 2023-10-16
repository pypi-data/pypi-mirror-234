import sqlite3
from sqlite3 import Error


class Database:

        try:
            global con
            con = sqlite3.connect('Expert.db')
            cur = con.cursor()
        except:
            print("connect error DB") 
        
        def sql_connection():
             try:
               con = sqlite3.connect('Expert.db')
               return con
             except:
              print("connect error DB") 
        
        def sql_table(con):
             cursorobj = con.cursor()
             cursorobj.execute("CREATE TABLE Epizode(ID integer primary key AUTOINCREMENT , candel_num text , Type text , point_Pattern json , point_7 text , point_7_time text , command text , candel_coler json , price_candel_open json , price_candel_close json , gap_point json , gap_amount json,gap_pip json,gap_word json , tension text , status text , chek text , time_start_search text , time_end_Pattern text , timestamp json , times json , ticket text , line_POS text , repetition_POS text , rep_candel_num text , Trust_patern text , Trust_patern_full text , Layout_patern text , Jump_patern text)")
             con.commit()
        
        def create_table():
             cone = Database.sql_connection()
             Database.sql_table(cone)    #create database
        
        def insert_table(value):
            # try: 
               cursorobj = con.cursor()
               cursorobj.execute('INSERT INTO Epizode (candel_num , Type , point_Pattern , point_7 , point_7_time  , command , candel_coler , price_candel_open , price_candel_close , gap_point , gap_amount , gap_pip , gap_word , tension , status , chek , time_start_search , time_end_Pattern , timestamp , times , ticket , line_POS , repetition_POS , rep_candel_num , Trust_patern , Trust_patern_full , Layout_patern , Jump_patern) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', value )
               con.commit()
               print("Record INSERT successfully")
               cursorobj.close()
            # except sqlite3.Error as error:
            #    print("Failed to INSERT reocord from a sqlite table", error)    

        def select_table_All():
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = """SELECT * from Epizode  """
               cursorobj.execute(sqlite_select_query)
               record = cursorobj.fetchall()
               # print("Select_All reocord from a sqlite table")
               return record
            except sqlite3.Error as error:
               print("Failed to Select_All reocord from a sqlite table", error)    
 
        def select_table_One(candel_num):
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = '''SELECT * from Epizode WHERE candel_num = ? '''
               cursorobj.execute(sqlite_select_query , (candel_num,))
               record = cursorobj.fetchall()
               # print("Record Select successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to select_one reocord from a sqlite table", error)  

        def select_table_Two(candel_num , type):
            try: 
               cursorobj = con.cursor()
               sqlite_select_query = '''SELECT * from Epizode WHERE candel_num = ? and Type = ?'''
               cursorobj.execute(sqlite_select_query , (candel_num , type,))
               record = cursorobj.fetchall()
               # print("Record Select successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to select_one reocord from a sqlite table", error)   

        def delete_table(candel_num ):
            try:
               cursorobj = con.cursor()
               sqlite_select_query = '''DELETE  from Epizode WHERE candel_num = ?  '''
               cursorobj.execute(sqlite_select_query , (candel_num , ))
               record = con.commit()
               print("Record Delete successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to delete reocord from a sqlite table", error)  
               
        def delete_table_All():
            try:
               cursorobj = con.cursor()
               sqlite_select_query = '''DELETE from Epizode '''
               cursorobj.execute(sqlite_select_query )
               record = con.commit()
               print("Record Delete_All successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to delete reocord from a sqlite table", error)        
             
        def update_table_gap(gap_point , gap_amount , gap_pip , gap_word , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET gap_point = ? , gap_amount = ? , gap_pip = ? , gap_word = ?  where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (gap_point , gap_amount , gap_pip , gap_word , candel_num) )
               record = con.commit()
               # print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)   

        def update_table_status(status  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET status = ?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (status  , candel_num) )
               record = con.commit()
               # print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)

        def update_table_repetition_pos(repetition_pos  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET repetition_pos = ?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (repetition_pos  , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)

        def update_table_trust_patern(trust_patern  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Trust_patern = ?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , ( trust_patern , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error) 

        def update_table_trust_patern_full(trust_patern_full  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET  Trust_patern_full = ?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (trust_patern_full , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)           

        def update_table_Layout_patern(Layout_patern  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Layout_patern =?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (Layout_patern , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)  

        def update_jump_patern(Jump_patern  , candel_num):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET Jump_patern =?   where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (Jump_patern , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)               

        def update_table_chek(point_7 , point_7_time  , command , chek , ticket , line_POS , candel_num ):
            try:
               cursorobj = con.cursor()
               sqlite_update_query = """UPDATE Epizode SET point_7 = ? , point_7_time =? , command = ? , chek = ? , ticket = ? , line_POS = ? where candel_num = ?"""
               cursorobj.execute(sqlite_update_query , (point_7 , point_7_time , command , chek , ticket , line_POS , candel_num) )
               record = con.commit()
               print("Record Update successfully")
               cursorobj.close()
               return record
            except sqlite3.Error as error:
               print("Failed to update reocord from a sqlite table", error)                   

        