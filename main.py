from redis_method import parser, return_keys
from jinja_function import write_xml
import time


start_time = time.time()
parser('XML/strings_4_3.xml')
write_xml(return_keys(parser('XML/strings_4_7.xml')))
print("--- %s seconds ---" % (time.time() - start_time))
