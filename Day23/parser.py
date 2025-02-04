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

sets = []
for computer, linkList in links.items():
    for i, link in enumerate(linkList):
        otherLinks = linkList.copy()
        del(otherLinks[i])

        for other in otherLinks:
            if computer in links[other] and link in links[other] and 't' in (computer[0]+link[0]+other[0]):
                group = [computer, link, other]
                group.sort()
                if group not in sets:
                    sets.append(group)

print(len(sets))