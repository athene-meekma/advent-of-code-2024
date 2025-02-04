import pprint

test = 0
if test:
    fn = 'test.txt'
else:
    fn = 'input.txt'

links = {}
with open(fn, 'r') as f:
    for line in f:
        comps = line.strip().split('-')
        if not comps[0] in links:
            links[comps[0]] = []
        links[comps[0]].append(comps[1])

        if not comps[1] in links:
            links[comps[1]] = []
        links[comps[1]].append(comps[0])

def getConnected(processed, linkList):
    for link in linkList:
        if all(x in links[link] for x in processed):
            processed.append(link)

    return processed

maxSet = None
for computer, linkList in links.items():
    for i, link in enumerate(linkList):
        otherLinks = linkList.copy()
        del(otherLinks[i])

        set = getConnected([computer, link], otherLinks)
        if maxSet == None or len(set) > len(maxSet):
            maxSet = set

maxSet.sort()
print(','.join(maxSet))