
import numpy as np
from . import gtcurve
from .gtdevCommon import physicalQuantity


class transcurve():
    def __init__(self,Vgs=None,Id=None):
        self.Id = Id
        self.Vgs = Vgs
        self.vthMod = 0#0:lin.5,1: lin,2:max

    def __getattribute__(self, __name: str):
        def checkSet(keys,unit,anaFunc):
            if __name in keys:
                if not __name in object.__getattribute__(self,'__dict__'):
                    anaFunc()
                return physicalQuantity(object.__getattribute__(self,__name),unit)
            else:
                return None
        answers = []
        answers.append(checkSet(['Ion','Ioff'],'A',
                object.__getattribute__(self,"_anacurrent")))
        answers.append(checkSet(['OOR'],'dec',
                object.__getattribute__(self,"_anacurrent")))
        answers.append(checkSet(['Vth'],'V',
                object.__getattribute__(self,"getVth")))
        answers.append(checkSet(['Gm'],'S',
                object.__getattribute__(self,"_maxTrans")))
        answers.append(checkSet(['SS'],'V/dec',
                object.__getattribute__(self,"getSS")))
        for ans in answers:
            if ans:
                return ans
        return object.__getattribute__(self,__name)

    def _anacurrent(self):
        aId = abs(np.array(self.Id))
        self.Ion = np.max(aId)
        if np.min(aId)>0:
            self.Ioff=np.min(aId)
        else:
            self.Ioff=np.min(aId[aId>0])
        self.OOR = np.log10(self.Ion.num/self.Ioff.num)
        return self.Ion,self.Ioff,self.OOR
    def noBack(self):
        x,y = self.Vgs,self.Id
        if len(x)<2:
            return x,y
        tag = x[0] > x[1]
        t = len(x)
        for i in range(len(x)-1):
            if (x[i] > x[i+1])!=tag:
                t=i
                break
        return x[0:t],y[0:t]
    
    def getVth(self,mod=None):
        modMap = {
            0:0,
            "lin.5":0,
            1:1,
            "lin":1,
            2:2,
            "maxTrans":2
        }
        if mod:
            self.vthMod = modMap[mod]
        if self.vthMod == 0:
            return self._VthHLE()
        elif self.vthMod == 1:
            return self._VthLE()
        elif self.vthMod ==2:
            return self._maxTrans()
    def _maxTrans(self):
        # get threshold voltage by maximum transconductance
        Vgs,Id=self.noBack()
        import numpy as np
        _,Vgs,Id = self.limitReg(Vgs,Id,lambda y:abs(np.array(y))**0.5)
        yy=np.ediff1d(Id,to_begin=0)/np.ediff1d(Vgs,to_begin=1)
        i=np.argmax(abs(yy))
        self.Gm=yy[i]
        if self.vthMod == 2:
            self.Vth=Vgs[i]
        return self.Vth

    def _VthHLE(self):
        Vgs,Id=self.noBack()
       
        haId=abs(np.array(Id))**.5
        #reg=gtcurve.linearOfCurve(Vgs,haId)
        reg,_,_ = self.limitReg(Vgs,Id,lambda y:abs(np.array(y))**0.5)
        xdata=np.array(Vgs)[reg]
        ydata=np.array(haId)[reg]
        try:
            p = gtcurve.linearFit(xdata,ydata)
            self.Vth=p[0]/p[1]
        except:
            self.Vth=999
        return self.Vth

    def _VthLE(self):
        Vgs,Id=self.noBack()
       
        haId=abs(np.array(Id))
        #reg=gtcurve.linearOfCurve(Vgs,haId)
        reg,_,_ = self.limitReg(Vgs,Id,lambda y:abs(np.array(y)))
        xdata=np.array(Vgs)[reg]
        ydata=np.array(haId)[reg]
        try:
            p = gtcurve.linearFit(xdata,ydata)
            self.Vth=p[0]/p[1]
        except:
            self.Vth=999
        return self.Vth

    def limitReg(self, Vgs, Id, yFunc, limits=[0, 0.5e-10, 1e-10, 5e-10, 1e-9, 5e-9, 1e-8]):
        def dataAbove(x,y,limit):
            return ([a[0] for a in zip(x,y) if abs(a[1])>abs(limit)], [a[1] for a in zip(x,y) if abs(a[1])>abs(limit)])    
        lenreg = 0
        for limit in limits:
            x,y = dataAbove(Vgs,Id,limit)
            alId = yFunc(y)

            try:
                tempreg=gtcurve.linearOfCurve(x,alId,0.85)
            except:
                tempreg=[]
            if len(tempreg)>lenreg:
                reg = tempreg
                lenreg = len(tempreg)
                newX,newY = dataAbove(Vgs,Id,limit)
        return reg,newX,newY
    def getSS(self):
        Vgs,Id=self.noBack()
        reg,_,_ = self.limitReg(Vgs,Id,lambda y:np.log10(abs(np.array(y))))
        try:
            alId=np.log10(abs(np.array(Id)))
            xdata=np.array(Vgs)[reg]
            ydata=np.array(alId)[reg]
            p = gtcurve.linearFit(xdata,ydata)
            self.SS=1/abs(p[1])
        except:
            self.SS=-1
        return self.SS

