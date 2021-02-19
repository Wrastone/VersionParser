import json
from dictor import dictor


def print_hi(name):
    result = dict()
    with open('db.json') as json_file:
        data = json.load(json_file)
        for p in data:
            service = str(p['service_name'])
            version = p['version']
            if version is not None:
                page = str(p['status_page'])
                version = str(version)
                if is_json(page):
                    version = version.rsplit('/')
                    pageJson = json.loads(page)
                    tmp = pageJson
                    for versStep in version:
                        tmp = tmp[versStep] if "." in versStep else dictor(tmp, versStep)

                    if tmp is not None:
                        result[service] = str(tmp).strip()
                else:
                    splitPage = page.splitlines()
                    filteredList = list(filter(lambda x: ':' in x and version in x, splitPage))
                    resDict = dict(map(lambda s: s.split(':'), filteredList))
                    for key in resDict:
                        if version in key:
                            result[service] = str(resDict[key]).strip()

    f = open("result.txt", "w")
    for key in result:
        resStr = "The version of " + str(key) + " is " + str(result[key] + '\n')
        f.writelines(resStr)
    f.close()

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


if __name__ == '__main__':
    print_hi('PyCharm')

