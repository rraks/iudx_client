from iudx_client.client import Cat

c = Cat("https://catalogue.iudx.org.in/cat/search")
msg["payload"] = c.getTags()
return msg



