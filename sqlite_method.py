import sqlite3
from xml.dom import minidom
import re
import xml.etree.ElementTree as xml
import time


start_time = time.time()
dict_4_3 = {}
dict_4_7 = {}

db = sqlite3.connect("table.db")
cursor = db.cursor()

# Create the table

cursor.executescript("""
 DROP TABLE IF EXISTS V_4_3;
 DROP TABLE IF EXISTS V_4_7;
 CREATE TABLE V_4_3 (ID integer primary key AUTOINCREMENT, TAG_NAME_4_3 TEXT, VALUE_4_3 TEXT);
 CREATE TABLE V_4_7 (ID integer primary key AUTOINCREMENT, TAG_NAME_4_7 TEXT, VALUE_4_7 TEXT)
""")

xmldoc = minidom.parse('XML/strings_4_3.xml')
xmldoc.normalize()
itemlist = xmldoc.getElementsByTagName('string')


for s in itemlist:
    try:
        dict_4_3[s.attributes['name'].value] = s.childNodes[0].nodeValue
        cursor.execute("""INSERT INTO V_4_3 (TAG_NAME_4_3, VALUE_4_3) VALUES (?, ?)""", (s.attributes['name'].value,
                                                                                         s.childNodes[0].nodeValue))
    except:
        cursor.execute("""INSERT INTO V_4_3 (TAG_NAME_4_3, VALUE_4_3) VALUES (?, ?)""", (s.attributes['name'].value,
                                                                                         None))

xmldoc_4_7 = minidom.parse('XML/strings_4_7.xml')
xmldoc_4_7.normalize()
itemlist_4_7 = xmldoc_4_7.getElementsByTagName('string')


for s_1 in itemlist_4_7:
    try:
        dict_4_7[s_1.attributes['name'].value] = s_1.childNodes[0].nodeValue
        re_find = re.search(r'&.*;', s_1.childNodes[0].nodeValue)
        if re_find.group(0) is True:
            nodevalue = s_1.childNodes[0].nodeValue
            nodevalue = nodevalue.encode("ascii", "xmlcharrefreplace").decode()
            cursor.execute("""INSERT INTO V_4_7 (TAG_NAME_4_7, VALUE_4_7) VALUES (?, ?)""", (s_1.attributes['name'].value,
                                                                                             nodevalue))
        else:
            cursor.execute("""INSERT INTO V_4_7 (TAG_NAME_4_7, VALUE_4_7) VALUES (?, ?)""", (s_1.attributes['name'].value,
                                                                                             s_1.childNodes[0].nodeValue))
    except:
        cursor.execute("""INSERT INTO V_4_7 (TAG_NAME_4_7, VALUE_4_7) VALUES (?, ?)""", (s_1.attributes['name'].value,
                                                                                         None))

db.commit()
db.close()


db = sqlite3.connect("table.db")
cursor = db.cursor()

i = 1
while i <= len(itemlist):
    cursor.execute("""SELECT TAG_NAME_4_3, VALUE_4_3 FROM V_4_3 WHERE ID = (?)""", (i,))
    result = cursor.fetchall()
    # print(result[0][0])
    cursor.execute("""UPDATE V_4_7 SET VALUE_4_7 = (?) WHERE TAG_NAME_4_7 = (?)""", (result[0][1], result[0][0]))
    i += 1
    # print(i)
db.commit()
db.close()


db = sqlite3.connect("table.db")
cursor = db.cursor()
j = 1

with open('XML/russian.xml', "w", encoding='utf-8') as f:
    while j <= len(itemlist_4_7):
        cursor.execute("""SELECT TAG_NAME_4_7, VALUE_4_7 FROM V_4_7 WHERE ID = (?)""", (j,))
        result = cursor.fetchall()
        example_string = '    <string name="' + str(result[0][0]) + '">' + str(result[0][1]) + '</string>\n'
        f.write(example_string)
        j += 1

db.close()
print("--- %s seconds ---" % (time.time() - start_time))
