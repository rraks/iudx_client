from iudx_client.client import Cat


def main():
    ''' Initialize the catalogue object '''
    c = Cat("https://catalogue.iudx.org.in/cat/search")

    ''' Get items by tags '''
    #items = c.getItemsByTags(["flood alert"], filters=None)

    ''' or  apply a geo search '''
    items = c.getItems(attributes={"tags":["feeder"]},location={"lat":18.528311,"long":73.874537,"radius":3}, filters=None)

    ''' Get data for those items '''
    data = c.getLatestDataFromItems(items)

    ''' Get only a few fields, like NAME and id '''
    #items = c.getItems(attributes={"tags":["flood alert"]},location={"lat":18.528311,"long":73.874537,"radius":2}, filters=["NAME","id"])

    print(data)




if __name__ == "__main__":
    main()
