import json

file=open("kojs.json","r")
decoded = json.load(file)

def parserJson(jsonDict):
    for root_key,root_value in jsonDict.iteritems():
        if root_key in keywords.keys():
            if isinstance (root_value,dict):
                for leaf_key, leaf_value in root_value.iteritems():
                    if leaf_key in keywords[root_key]:
                        print "running:",keywords[root_key][leaf_key],leaf_value
                    else:
                        parserJson(leaf_value)

        elif isinstance(root_value,dict):
            parserJson(root_value)

        else:
            print root_value



parserJson(decoded)