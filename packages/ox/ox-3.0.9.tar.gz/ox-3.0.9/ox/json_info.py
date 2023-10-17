

def tree(obj, indent=""):
    if not obj:
        return
    if isinstance(obj, dict):
        for key in obj:
            print(indent, key)
            tree(obj[key], indent + " ")



def find(obj, value, path=""):
    if not obj:
        return
    if isinstance(obj, list):
        for i, v in enumerate(obj):
            find(v, value, path + '[%s]' )
    elif isinstance(obj, dict):
        for key in obj:
            if isinstance(obj[key], str) and obj[key] == value:
                print(path, key, value)
            else:
                find(obj[key], value, "%s['%s']" % (path, key))
