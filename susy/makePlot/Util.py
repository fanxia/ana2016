import math

class CombineSys(object):
    def __init__(self,cent):
        self.central_v=cent
        self.sys_v=[]

    def pushsys(self,v):
        self.sys_v.append(v)
    def sys(self):
        s=0.0
        for v in self.sys_v:
            s+=(v-self.central_v)**2
        return (s/2.0)**0.5
