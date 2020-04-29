import json

cnt=0

class echStudent():
    def __init__(self,s,num):
        global cnt
        self.name=s
        self.no=num
        cnt+=1
        self.count=cnt
        self.mark=0

    def __lt__(self,y):
        if self.no!=y.no:
            return self.no<y.no
        else:
            return self.name<y.name

    def __str__(self):
        return str(self.no)+"号 - "+self.name


class echTest():
    def __init__(self,s,_stus):
        self.stus=[]
        self.name=s
        for s in _stus:
            self.stus.append(echStudent(s.name,s.no))

    def change(self,n,m):
        for s in self.stus:
            if s.name==n:
                s.mark=m
                break

    def sort(self,mode):
        if mode==1:
            self.stus=sorted(self.stus,key=lambda x: -x.mark)
        if mode==2:
            self.stus=sorted(self.stus)

    def __str__(self):
        s="Test name:"+self.name
        for st in self.stus:
            s+="\n -"+st.name+":"+str(st.mark)+"分"
        return s


class echClass():

    def __init__(self,s):
        self.name=s
        self.stus=[]
        self.tests=[]

    def __str__(self):
        s=""
        s+="Class name:"+self.name+"\n"
        s+="Students:\n"
        for st in self.stus:
            s+=" -"+st.name+"\n"
        s+="Tests:\n"
        for i in range(len(self.tests)):
            s+=self.tests[i].__str__()+"\n"
        return s

    def add_stu(self,stu_name,stu_no):
        self.stus.append(echStudent(stu_name,stu_no))
        self.stus.sort()

    def del_stu(self,_stu):
        x=echStudent("",-1)
        if isinstance(_stu,int):
            for stu in self.stus:
                if stu.no==_stu:
                    x=stu
                    break
        elif isinstance(_stu,str):
            for stu in self.stus:
                if stu.name==_stu:
                    x=stu
                    break
        self.stus.remove(x)

    def add_test(self,test_name):
        if isinstance(test_name,str):
            self.tests.append(echTest(test_name,self.stus))
        elif isinstance(test_name,echTest):
            self.tests.append(test_name)

    def del_test(self,test_name):
        x=echTest("",[])
        if isinstance(test_name,str):
            for test in self.tests:
                if(test.name==test_name):
                    x=test
                    break
            self.tests.remove(x)
        elif isinstance(test_name,int):
            x=self.tests[test_name]
            self.tests.remove(x)


class echSaver():

    def __init__(self,f):
        self._c={}
        self.file=f
    
    def save(self,c):
        res={}
        for name,clas in c.items():
            res[name]={"STUS":[],"TESTS":[]}
            for stu in clas.stus:
                res[name]["STUS"].append({"NAME":stu.name,"NO":stu.no})
            for test in clas.tests:
                t={"NAME":test.name,"MARK":[]}
                for stu in test.stus:
                    t["MARK"].append({"NO":stu.no,"NAME":stu.name,"MARK":stu.mark})
                res[name]["TESTS"].append(t)
        fwrite=open(self.file,"w")
        json.dump(res,fwrite,indent=4)

    def load(self):
        fread=open(self.file,"r")
        s=json.load(fread)
        res={}
        for name,clas in s.items():
            res[name]=echClass(name)
            for stu in clas["STUS"]:
                res[name].add_stu(stu["NAME"],stu["NO"])
            for test in clas["TESTS"]:
                t=echTest(test["NAME"],[])
                for stu in test["MARK"]:
                    s=echStudent(stu["NAME"],stu["NO"])
                    s.mark=stu["MARK"]
                    t.stus.append(s)
                res[name].tests.append(t)
        return res