class SearchBase(object):
    def __init__(self,fields="url",**kwargs):
        self.fields = fields
    async def search(self,**kwargs):
        pass

    def echo(self,item):
        if self.fields=="address":
            print(f"{item['ip']}:{item['port']}")
        else:
            print(item[self.fields])
