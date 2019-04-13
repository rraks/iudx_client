'''
    Get's data for all items that are part of an array
'''
from iudx_client.client import Cat


items = msg["payload"]
c = Cat("https://catalogue.iudx.org.in/cat/search")

msg["payload"] = c.getLatestDataFromItems(items)

return msg

