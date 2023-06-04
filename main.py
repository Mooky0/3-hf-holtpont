import sys

## Néha akarunk kiíratni néha nem. A debugvar global bool-al ezt lehet állítani.
def debug(s : str):
    if debugvar:print(s) 


class Graph():
    def __init__(self):
        self.graph = {}
        self.vertecies = []
 
    def addEdge(self, u, v):
        if (u in self.graph.keys()):
            self.graph[u].append(v)
        else:
            self.graph[u] = [v]
    
    def delete_task(self, task):
        try:
            del self.graph[task.name]
        except(KeyError):
            pass
        to_del = []
        for k, v in self.graph.items():
            try:
                if task.name in v and len(v) > 1:
                    v.remove(task.name)
                elif task.name in v:
                    to_del.append(k)
            except(ValueError):
                pass

        try:
            for i in to_del:
                del self.graph[i]
                first = wait[i].pop(0)
                #g.removeEdge(first, i)
                self.removeEdge(first, i)
                g.addEdge(i, first) ## first in line
                fifo[first].move += 1
        except(KeyError, IndexError):
            pass
        for i in to_del:
            pass


    def __str__(self) -> str:
        return self.graph.__str__()

    ## assuming it exists
    def removeEdge(self, u, v):
        try:
            if len(self.graph[u]) > 1:
                self.graph[u].remove(v)
            else:
                del self.graph[u]
        except(ValueError):
            pass

    def isCyclicUtil(self, v, visited, recStack):
 
        visited[v] = True
        recStack[v] = True

        for neighbour in self.graph[v]:
            try:
                if visited[neighbour] == False:
                    if self.isCyclicUtil(neighbour, visited, recStack) == True:
                        return True
                elif recStack[neighbour] == True:
                    return True
            except(KeyError):
                continue
 
        recStack[v] = False
        return False
 
    def not_reserved(self, s : str) -> bool:
        for keys in self.graph.keys():
            if (s in keys):
                return False
        return True

    def isCyclic(self):
        visited = {}
        recStack = {}
        for i in self.graph.keys():
            visited[i] = False
            recStack[i] = False
        for node in self.graph.keys():
            if visited[node] == False:
                if self.isCyclicUtil(node, visited, recStack) == True:
                    return True
        return False
    


class Task():
    def __init__(self, _name:str, _moves:list) -> None:
        self.name = _name
        self.moves = _moves.copy()
        self.move = 0
        self.alive = True

    def __str__(self) -> str:
        return self.name + ": " + self.moves.__str__()
    
    def is_waiting(self, g : Graph):
        return self.name in g.graph.keys()

    def step(self, g : Graph):
        global answear
        if (self.is_waiting(g)):
            return
        else:
            try:
                m = self.moves[self.move]
            except (IndexError):
                exit_task(self)
                return
            if(m[0] == '+'):
                if (g.not_reserved(m[1:])):
                    g.addEdge(m[1:], self.name) # szabad szóval lefoglaljuk
                    debug("new " + m[1:] +" for " + self.name)
                else:
                    g.addEdge(self.name, m[1:]) ## várakoztatjuk
                    if g.isCyclic(): ## holtpont lenne visszautasítjuk
                        g.removeEdge(self.name, m[1:])
                        answear += (self.name + "," + str(self.move+1) + "," + m[1:] + '\n')
                        self.move += 1
                        return
                    else:
                        try:    
                            wait[m[1:]].append(self.name)
                            return
                        except:
                            wait[m[1:]] = [self.name]
                            return


            elif (m[0] == '-'):
                try:
                    g.removeEdge(m[1:], self.name)
                    try:
                        first = wait[m[1:]].pop(0)
                    except(KeyError, IndexError):
                        return
                    g.removeEdge(first, m[1:])
                    g.addEdge(m[1:], first) ## first in line
                    fifo[first].move += 1
                    debug("del " + m[1:] +" from " + self.name)
                except(ValueError):
                    pass
                except(KeyError):
                    debug("!del " + m[1:] +" from " + self.name)
                    
            self.move += 1
 


class FIFO:
    
    def __init__(self, *args : Task) -> None:
        self.tasks : list(Task) = []
        self.idx : int = 0
        for i in args:
            self.tasks.append(i)

    # def skip(self):
    #     self.idx += 1
    #     if (self.idx > len(self.tasks) -1):
    #         self.idx = 0

    # def next(self) -> Task:
    #     ret = self.tasks[self.idx]
    #     self.idx += 1
    #     if (self.idx > len(self.tasks) -1):
    #         self.idx = 0
    #     return ret
    
    ## return the first element of the list (next in the FIFO)
    def pop(self) -> Task:
        tmp : Task = self.tasks[0]
        self.tasks.pop(0)
        return tmp
    
    ## ads at the end oh the list (FIFO)
    def push(self, task : Task):
        self.tasks.append(task)

    def delete(self, task : Task):
        self.tasks.remove(task)

    def step(self, g : Graph):
        for i in self.tasks:
            i.step(g)

    def size(self) -> int:
        return len(self.tasks)
    
    def all_used(self) -> bool:
        for i in self.tasks:
            if i.lock == 0 and i.used == False:
                return False
        return True    

    def lookup(self, _name : int):
        for i in self.tasks:
            if (i.name == _name):
                return i
        return None
    
    def __getitem__(self, key):
        for i in self.tasks:
            if (i.name == key):
                return i
        return None
    
    def __str__(self) -> str:
        ret: str = ""
        for i in self.tasks:
            ret += i.__str__() + '\n'
        return ret
    
    ## puts an already existing task at the end of the Fifo
    def put_back(self, task : Task):
        self.tasks.remove(task)
        self.tasks.append(task)

def exit_task(task : Task):
    ##fifo.delete(task=task)
    if task.alive == False:
        return
    g.delete_task(task)
    task.alive = False
    return

def main(input_str : str):
    global debugvar
    global fifo
    global g
    global wait
    global answear
    answear = ''
    debugvar = False
    wait = {}
    fifo = FIFO()
    g = Graph()
    for i in input_str.split('\n'):
        ##print(line)
        line = list(map(str.strip, i.split(',')))
        task : Task = Task(line[0], line[1:])
        fifo.push(task)
        # try:
        #     line = input()
        # except(EOFError):
        #     break

    ##print(fifo)
    global clock
    clock = 0
    for i in range(30):
        fifo.step(g)
        clock += 1

    debug(g)
    return answear
    

if '__main__' == __name__:
    local = False
    if (not local):
        input_str = sys.stdin.read()
        answear = main(input_str)
        print(answear[:-1])
    else:
        pass