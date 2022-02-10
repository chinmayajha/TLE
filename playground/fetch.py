import requests

cp1 = dict()
cp2 = dict()
#score = get_dict_from_db()
def check(handle : str, link : str):
    try:
        index = link.split('/')[len(link.split('/'))-1]
        contest = link.split('/')[len(link.split('/'))-2]
        submissions = requests.get(f"https://codeforces.com/api/user.status?handle={handle}").json()["result"]
        for sub in submissions:
            if sub["problem"]["index"] == index and str(sub["problem"]["contestId"]) == contest and sub["verdict"] == "OK":
                #person.add(link)
                #score[person] = len(person)
                return True
    except Exception as e:
        print(f"ERROR OCCURRED\n{e.__class__.__name__}: {e}\nHandle: {handle}\nProblem URL: {link}")
    return False

def get_lb1(handle):
    if(handle not in cp1.keys()):
        return 0
    return len(cp1[handle])

def get_lb2(handle):
    if(handle not in cp2.keys()):
        return 0
    return len(cp2[handle])

def fetch_call(handle : str, category:str , link : str):
    if(category=='CP1' and handle in cp1.keys()):
        if(link in cp1[handle]):
            return True
    if(category=='CP2' and handle in cp2.keys()):
        if(link in cp2[handle]):
            return True
    if check(handle, link):
        if(category=='CP1'):
            if(handle not in cp1.keys() or type(cp1[handle])!=set()):
                cp1[handle] = set()
            cp1[handle].add(link)
        else:
            if(handle not in cp2.keys() or type(cp2[handle])!=set()):
                cp2[handle] = set()
            cp2[handle].add(link)
        return True
    return False