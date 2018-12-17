# Simplifyng K maps using Quine Mcclusky theorme
# Author: Ujjwal Singh

def mul(x,y): # Multiply 2 minterms
    a = []
    for i in x:
        if i+"'" in y or (len(i)==2 and i[0] in y):
            return []
        else:
            a.append(i)
    for i in y:
        if i not in a:
            a.append(i)
    return a

def multiply(x,y): # Multiply 2 expressions
    a = []
    for i in x:
        for j in y:
            tmp = mul(i,j)
            a.append(tmp) if len(tmp) != 0 else None
    return a

def essentialPI(x): # Finds EPI
    a = []
    for i in x:
        if len(x[i]) == 1:
            a.append(x[i][0]) if x[i][0] not in a else None
    return a

def remove_dontcare(my_list,dc_list): # Removes don't care
    a = []
    for i in my_list:
        if int(i) not in dc_list:
            a.append(i)
    return a

def linear(x): 
    linear = []
    for i in x:
        linear.extend(x[i])
    return linear

def findVariables(x): # Finding Mean term
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list


def findminterms(a): #Merging Terms
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
    temp = []
    for i in range(pow(2,gaps)):
        temp2,ind = a[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+temp2[ind+1:].find('-')+1
            else:
                ind = temp2[ind+1:].find('-')
            temp2 = temp2[:ind]+j+temp2[ind+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp

def compare(a,b): # Minimising Expresion
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            no_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,no_index)

def removeTerms(chart,terms): # Redundancy Removed
    for i in terms:
        for j in findminterms(i):
            try:
                del chart[j]
            except KeyError:
                pass

T = [int(i) for i in input("Enter the Minterms: ").strip().split()]
dc = [int(i) for i in input("Enter the don't cares: ").strip().split()]
T.sort()
minterms = T+dc
minterms.sort()
size = len(bin(minterms[-1]))-2
groups,all_pi = {},set()

for minterm in minterms:
    try:
        groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
    except KeyError:
        groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

while True:
    tmp = groups.copy()
    groups,m,marked,should_stop = {},0,set(),True
    l = sorted(list(tmp.keys()))
    for i in range(len(l)-1):
        for j in tmp[l[i]]: 
            for k in tmp[l[i+1]]: 
                a = compare(j,k) 
                if a[0]: 
                    try:
                        groups[m].append(j[:a[1]]+'-'+j[a[1]+1:]) if j[:a[1]]+'-'+j[a[1]+1:] not in groups[m] else None # Put a '-' in the changing bit and add it to corresponding group
                    except KeyError:
                        groups[m] = [j[:a[1]]+'-'+j[a[1]+1:]] 
                    should_stop = False
                    marked.add(j) # Mark element j
                    marked.add(k) # Mark element k
        m += 1
    local_unmarked = set(linear(tmp)).difference(marked) 
    all_pi = all_pi.union(local_unmarked) # Adding Prime Implicants to global list
    if should_stop: 
        break

le = len(str(T[-1])) 
chart = {}
for i in all_pi:
    merged_minterms,y = findminterms(i),0
    for j in remove_dontcare(merged_minterms,dc):
        x = T.index(int(j))*(le+1) 
        y = x+le
        try:
            chart[j].append(i) if i not in chart[j] else None # Add minterm in chart
        except KeyError:
            chart[j] = [i]

EPI = essentialPI(chart) # Finding essential prime implicants
print("\nEssential Prime Implicants: "+', '.join(str(i) for i in EPI))
removeTerms(chart,EPI) 

if(len(chart) == 0): # If no minterms remain after removing EPI related columns
    final_result = [findVariables(i) for i in EPI] 
else: 
    P = [[findVariables(j) for j in chart[i]] for i in chart]
    while len(P)>1: 
        P[1] = multiply(P[0],P[1])
        P.pop(0)
    final_result = [min(P[0],key=len)] 
    final_result.extend(findVariables(i) for i in EPI) 
print('\n\nSolution: F = '+' + '.join(''.join(i) for i in final_result))
input("\nPlease Press Enter to Exit..")
