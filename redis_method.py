from xml.dom import minidom
import redis


r = redis.StrictRedis(host='localhost', port=6379, db=1, encoding='utf-8')
r.flushdb()
parent_dict = {}


def parser(file: str):
    xml_doc = minidom.parse(file)
    xml_doc.normalize()
    item_list = xml_doc.getElementsByTagName('string')
    for i in item_list:
        try:
            r.set(str(i.attributes["name"].value), str(i.childNodes[0].nodeValue))
        except IndexError:
            r.set(str(i.attributes["name"].value), None)
    return r.keys()


def return_keys(import_list: list)->dict:
    for _ in import_list:
        parent_dict[_.decode('utf-8')] = r.get(_).decode('utf-8')
    return parent_dict
