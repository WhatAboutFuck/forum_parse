global db
db = con.cursor()

def exists(s):
    try:
        db.execute("SELECT bssid FROM data WHERE bssid = (%s)",(s[0],))
        return (db.fetchone() is not None)
    except:
        pass
        con.commit()
def write_to_db(l,lst,c_page):
    for s in lst:
        if exists(s) == False:
            try:
                db.execute("insert into data (essid,bssid,http,page) VALUES (%s,%s,%s,%s)",(s[2], s[0], s[1],c_page))
                con.commit()
            except:
                pass
                con.commit()
        elif exists(s) == True:
            try:
                db.execute("UPDATE data SET essid = (%s), http = (%s), page = (%s) WHERE bssid = (%s)",(s[2], s[1], c_page, s[0]))
                con.commit()
            except:
                pass
                con.commit()
    for j in l:
        if exists(j) == False:
            try:
                db.execute("insert into data (essid,bssid,page) VALUES (%s,%s,%s)",(j[1], j[0], c_page))
                con.commit()
            except:
                pass   
                con.commit()
        elif exists(j) == True:
            try:
                db.execute("UPDATE data SET essid = (%s),page = (%s) WHERE bssid = (%s)",(j[1],c_page, j[0]))
                con.commit()
            except:
                pass
                con.commit()



def get_page():
    db.execute("select max(page) from data")
    page = db.fetchone()[0]
    if page is None :
        return "https://forum.antichat.ru/threads/435763/page-" + '1'
    return "https://forum.antichat.ru/threads/435763/page-" + str(page + 1)
