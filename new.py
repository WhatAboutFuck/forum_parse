import psycopg2
from config import get_page
con = psycopg2.connect(
	database="wifi", 
	user="admin", 
	password="7818", 
	host="127.0.0.1", 
	port="5432"
)



# s = ['04:8d:38:c1:51:76', 'HTTP://RGHOST.NET/7SZCTYNXM', 'VLAD',5]
global db
db = con.cursor()

# db.execute(f"CREATE TABLE data (essid varchar(40) NOT NULL,bssid macaddr NOT NULL,http varchar(100),page smallint);")
# con.commit()
# db.execute("insert into data (essid,bssid,http,page) VALUES (%s,%s,%s,%s)",(s[2], s[0], s[1], s[3])) 
# db.execute(f"INSERT INTO http VALUES ({s[1]})")
# db.execute(f"INSERT INTO bssid VALUES ({s[0]})")

# try :
# 	db.execute("UPDATE data SET essid = (%s), http = (%s), page = (%s) WHERE bssid = (%s)",(s[2], s[1], s[3], s[0]))  
# 	con.commit()
# except:
# 	db.execute("insert into data (essid,bssid,http,page) VALUES (%s,%s,%s,%s)",(s[2], s[0], s[1], s[3]))
# 	con.commit()
# finally:
# 	pass

def exists(s):
    try:
        db.execute("SELECT bssid FROM data WHERE bssid = (%s)",(s[0],))
        return (db.fetchone() is not None)
    except:
        pass
def write_to_db(l,lst):
    for s in lst:
        if exists(s) == False:
            try:
                db.execute("insert into data (essid,bssid,http,page) VALUES (%s,%s,%s,%s)",(s[2], s[0], s[1],int(get_page()[1])))
                con.commit()
            except:
                pass   
        elif exists(s) == True:
            try:
                db.execute("UPDATE data SET essid = (%s), http = (%s), page = (%s) WHERE bssid = (%s)",(s[2], s[1], int(get_page()[1]), s[0]))
                con.commit()
            except:
                pass
    for j in l:
        if exists(j) == False:
            try:
                db.execute("insert into data (essid,bssid,page) VALUES (%s,%s,%s)",(j[1], j[0], int(get_page()[1])))
                con.commit()
            except:
                pass   
        elif exists(j) == True:
            try:
                db.execute("UPDATE data SET essid = (%s),page = (%s) WHERE bssid = (%s)",(j[1], int(get_page()[1]), j[0]))
                con.commit()
            except:
                pass
 
# db.execute("select essid,bssid,http,page from data")
# rows = db.fetchall()
# l = ["essid","bssid","http","page"]

# for r in rows:
# 	for i in range(len(r)):
# 		print(f" {l[i]} {r[i]}")
# print()
con.commit()
