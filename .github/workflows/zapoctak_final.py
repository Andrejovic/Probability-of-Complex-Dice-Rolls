import math
from operator import add,sub
import matplotlib.pyplot as plt

def product(*args, repeat=1):
    pools = [list(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield list(prod)


def solve(Input):
    prazdny = True
    pomocny = False
    vysledok = 0
    operator = {'+': add, '-': sub}
    option = add 
    for item in Input:
        if isinstance(item,dict):
            for index in dct.keys():
                if dct[index]!=0:
                    prazdny=False
            if not prazdny:
                pomocny = dct
            else:
                pomocny = item
        elif item in operator:
            option = operator[item]
        else:
            try:
                number = int(item)
                if not pomocny:
                    vysledok = option(vysledok, number)
                else:
                    vysledok = {}
                    for index in pomocny.keys():
                        vysledok[option(index,number)]=pomocny[index]
            except:
                print('ERROR')
        
    return vysledok


def prob_kocky(s,n,kocka):
    prob=0
    k=math.floor((s-n)/kocka)
    for suma in range(0,k+1):
        prob+=(-1)**(suma)*math.comb(n,suma)*math.comb(s-kocka*suma-1,n-1)

    return prob/(kocka**n)


def dice(pocet_kociek,pocet_stien,nasob=1):
    pocet_kociek=int(pocet_kociek)
    pocet_stien=int(pocet_stien)   
    for index in range(pocet_kociek,pocet_kociek*pocet_stien+1):
        dct[index]+=nasob*prob_kocky(index,pocet_kociek,pocet_stien)

    return dct


def magic(): #
    global pravdepodobnost,dokedy,konstanta
    if type(equation[i-1])==str:     
        pravdepodobnost=dice(equation[i-1],equation[i+1])    
    elif type(equation[i-1])==dict:
        moment=pravdepodobnost.copy()
        pravdepodobnost={}
        for variable in dct.keys():
            dct[variable]=0

        for j in moment.keys():
            if moment[j]!=0:
                pravdepodobnost=dice(j,equation[i+1],moment[j])
        dokedy+=1

    equation.pop(i-1)
    equation.pop(i-1)
    equation[i-1]=pravdepodobnost.copy()
    if equation.count('d')==0:
        konstanta=False


def counting(): #funkcia na počítanie počtu slovníkov
    pocetdict=0
    for i in range(len(equation)):
        if type(equation[i])==dict:
            pocetdict+=1
    pocetdict+=dokedy
    return pocetdict


''' CHECKLIST
- POCITANIE SAMOTNEJ KOCKY - DONE
- POCITANIE VIACNASOBNEJ KOCKY - DONE
- SCITOVANIE KOCIEK - DONE
- SCITOVANIE VIACNASOBNEJ KOCKY - DONE
- VYHODIT KONSTANTU KED JE NA VSTUPE LEN KONSTANTA - DONE?
- ODCITOVANIE KOCIEK - DONE
- STANDARTNE ROVNICE BEZ D - DONE
- ODCITOVANIE KONSTANTY - DONE
- PRICITOVANIE KONSTANTY - DONE
'''

#input vo formate kocka+-...+-kocka+-konstanta+-...+-konstanta

NUM='0123456789' #pomocny string cisel
ROZ='+-d' #pomocny string operandov 

origolist=list(input('Input a dice equation: ')) #načítanie a rozdelenie inputu do listu
index=0

#ak sa pomocou list() rozdelili cisla na cifry, zlozi ich dokopy
while origolist[index]: 
    if len(origolist)==1:
        break

    #dve za sebou hodnoty sú čísla?
    if origolist[index][0] in NUM and origolist[index+1][0] in NUM:
        origolist[index]=origolist[index]+origolist[index+1]
        origolist.pop(index+1)
        index-=1

    index+=1

    if len(origolist)<=(index+1):
        break

konstanta=True                  #temporary boolean pre existenciu konštanty
pocet=origolist.count('d')      #pocet kolko krat je vyuzity operand 'd'
rozsah=int(origolist[0])        #temporary hodnota ak sa nenachadza 'd' v rovnici
copy_help=origolist.copy()      #pomocny zoznam ktory je nezavisly od inputu a mozeme ho menit
dokedy=0                        #hodnota používaná v counting()

#výpočet rozsahu skrz odstraňovanie prvkov z kópie listu
for index in range(pocet):      
    d_index=copy_help.index('d')
    rozsah=int(copy_help[d_index-1])*int(copy_help[d_index+1])
    copy_help.pop(d_index-1)
    copy_help.pop(d_index-1)
    copy_help[d_index-1]=rozsah 

#pokračovanie ^
index=0

while len(copy_help)>1: 
    index+=1

    #práca s operátormi
    if copy_help[index]=='+' or copy_help[index]=='-':
        rozsah=int(copy_help[index-1])+int(copy_help[index+1])
        copy_help.pop(index-1)
        copy_help.pop(index-1)
        copy_help[index-1]=rozsah
        index-=2


#vytvorenie slovníku v rozsahu trochu väčšieho nech je        
dct={}                          #finálny slovník s pravdepodobnostnými hodnotami

for index in range(-rozsah,rozsah+1):
    dct[index]=0

#print(lst) #finalny DICTIONARY vysledkov
equation=origolist.copy()

#vypocitanie vsetkych kociek
i=0

while len(equation)>1 and origolist.count('d')>counting():
    if equation[i]=='d':
        magic()
        i-=2

    #pre sčitovanie a odčitovanie kociek napr. 2d2+3d3
    elif (equation[i]=='+' or equation[i]=='-') and origolist.count('d')>1:
        if type(equation[i-1])==dict and type(equation[i+1])!=dict and equation[i+2]=='d':
            i+=2

            for variable in dct.keys():
                dct[variable]=0

            magic()
            i-=4
    
    i+=1

#pokial nie je dĺžka equation po dokončení pracovania s kockami 1, ďalej spracováva equation
operators_lst=[]                #zoznam operatorov v rovnici

if len(equation)>1:        
    for variable in dct.keys():
        dct[variable]=0

    slovniky=[]                 #dvojrozmerné pole všetkých použitých slovníkov

    #prechádza equation postupne, zastaví sa vždy pri slovníkoch a operatoroch
    for index in range(len(equation)):
        if isinstance(equation[index],dict):
            slovniky.append(equation[index])
            kopia=equation[index].copy()
            equation[index].clear()

            for j in kopia.keys():
                if kopia[j]!=0:
                    equation[index][j]=kopia[j]

        elif equation[index]=='+' and (isinstance(equation[index-1],dict) == isinstance(equation[index+1],dict)):
            operators_lst.append('+')
        elif equation[index]=='-' and (isinstance(equation[index-1],dict) == isinstance(equation[index+1],dict)):
            operators_lst.append('-')

    #kombinácie všetkých slovníkov v equation
    permutations=list(product(*slovniky))
    if len(permutations[0])>1:
        for index in range(len(permutations)):
            teraz=1

            for j in range(len(permutations[index])):
                teraz*=slovniky[j][permutations[index][j]]

            for j in range(len(operators_lst)):
                if operators_lst[j]=='+':
                    permutations[index][j+1]=permutations[index][j+1]
                elif operators_lst[j]=='-':
                    permutations[index][j+1]=-permutations[index][j+1]

            #do finálneho slovníku pridá sumu z kombinácií
            dct[sum(permutations[index])]+=teraz

#pocitanie s konstantou
if len(equation)>1:
    for index in range(len(equation)):
        if not isinstance(equation[index],dict):
            try:
                if int(equation[index]):
                    dct=solve(equation)
            except:
                pass

#ak je na vstupe len konštanta, pridaj pravdepodobnost 100%
if konstanta:
    dct={}
    dct[rozsah]=1

hodnoty=[]
kluce=[]

#výpis do terminálu
for key in dct.keys():          
    if dct[key]!=0:
        hodnoty.append(dct[key]*100)
        kluce.append(key)
        print(f'{key:3}: {(dct[key]):10%}')   

#graf
fig = plt.figure()
fig.set_facecolor('azure')
plt.bar(kluce,hodnoty,color=['red'], edgecolor='black')     
plt.xlabel('HODNOTY')
plt.ylabel('PRAVDEPODOBNOST V %')
plt.grid(True, 'major','y')
plt.show()