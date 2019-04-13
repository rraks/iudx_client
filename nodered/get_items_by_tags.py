from iudx_client.client import Cat

tags = msg["payload"]["tags"] if "tags" in msg["payload"] else None
location = msg["payload"]["location"] if "location" in msg["payload"] else None 
filters = msg["payload"]["filters"] if "fiters" in msg["payload"] else None 



c = Cat("https://catalogue.iudx.org.in/cat/search")
l = c.getItems(attributes={"tags":tags}, location=location, filters=filters)
msg["payload"] = l

return msg

