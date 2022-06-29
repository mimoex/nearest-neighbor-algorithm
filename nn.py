#coding:utf-8
import time
import random
import networkx as nx
import matplotlib.pyplot as plt

#都市間距離を計算
def distance(pa,pb):
    return ((pa[0]-pb[0])**2+(pa[1]-pb[1])**2)**0.5

def graph_of_tour(tour):
    Gt=nx.Graph()
    for i in range(len(tour)):
        ci=tour[i]
        if i==len(tour)-1:
            ci=tour[0]
        else:
            cj=tour[i+1]
        Gt.add_edge(ci,cj,weight=distance(C[ci],C[cj]))
    return Gt

def tsp_solve(C,timelimit=500):
    G=nx.Graph()

    for v in C:
        G.add_node(v)
    for i,ci in enumerate(C):
        for j,cj in enumerate(C):
            if i<j:
                G.add_edge(ci,cj,weight=distance(C[ci],C[cj]))
    # 最近傍法
    v=0
    min_d,min_u=100000000,None

    for u in G[v]:
        print(u,G[v][u]["weight"])
        if min_d>G[v][u]["weight"]:
            min_d=G[v][u]["weight"]
            min_u=u
    print(min_d,min_u)

    tour=[0]
    visited={0:True}

    while len(tour)<len(C):
        v=tour[-1]
        
        min_d,min_u=100000000,None
        for u in G[v]:
            if min_d>G[v][u]["weight"] and u not in visited:
                min_d=G[v][u]["weight"]
                min_u=u
        visited[min_u]=True
        tour.append(min_u)

    print(tour)
    ##ここまで最近傍法

    # 2-swap
    def better_solution(sol):
        n=len(sol)
        print(sol)
        for i in range(n):
            for length in range(2,n):
                if i+length-1 > n-1:
                    break
                print("reverse path from",i,"length",length)
                path=sol[i:i+length]
                #path.reverse()
                print(sol[:i],"<",path,">",sol[i+length:])
                print("del:",sol[i-1],sol[i])
                print("del:",sol[i+length-1],sol[(i+length)%n])
                print("add:",sol[i-1],sol[i+length-1])
                print("add:",sol[i],sol[(i+length)%n])
                diff=-distance(C[sol[i-1]],C[sol[i]])-distance(C[sol[i+length-1]],C[sol[(i+length)%n]])\
                    +distance(C[sol[i-1]],C[sol[i+length-1]])\
                    +distance(C[sol[i]],C[sol[(i+length)%n]])
                print(diff)
                if diff<-0.0000001:
                    path.reverse()
                    bsol=sol[:i]+path+sol[i+length:]
                    return bsol

        return None

    print("local opt:",tour)
    starttime=time.time()

    sol=tour
    while time.time() - starttime<timelimit:
        tour = [i for i in C]
        bsol=better_solution(sol)
        if bsol==None:
            tour=sol
        else:
            sol=bsol
    return tour


C={}
n=30    #ノード数
R=10000 #座標の最大値


for i in range(n):
    x=random.randint(0,R)
    y=random.randint(0,R)
    C[i]=(x,y)
    
print(C)

#最近傍法の処理
tour=tsp_solve(C,10)


#結果をグラフに表示
Gt=graph_of_tour(tour)

print("size of tour:",Gt.size(weight="weight"))
print("feasibility:",nx.is_k_edge_connected(Gt,2))


plt.figure(figsize=(6,6))

nx.draw_networkx(Gt,pos=C,node_color="yellow",node_size=200,with_labels=True,edge_color="k",width=1)
plt.show()