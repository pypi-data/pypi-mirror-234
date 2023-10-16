
from . import gtcurve
from .gtdevCommon import physicalQuantity

class inverter():
    def __init__(self,vin,vout,vdd = 2):
        '''
        vin: list input voltage
        vout: list output voltage
        vdd: work voltage, 2V for default
        '''
        self.vin = vin
        self.vout = vout
        self.vdd = vdd
        
    def __getattribute__(self, __name: str):
        def checkSet(keys,unit,anaFunc):
            if __name in keys:
                if not __name in object.__getattribute__(self,'__dict__'):
                    anaFunc()
                return physicalQuantity(object.__getattribute__(self,__name),unit)
            else:
                return None
        answers = []
        answers.append(checkSet(['Vm'],'V',
                object.__getattribute__(self,"_getVm")))
        answers.append(checkSet(['NMH','NML'],'V',
                object.__getattribute__(self,"_getNoiseMargin")))
        answers.append(checkSet(['hys'],'V',
                object.__getattribute__(self,"_gethys")))
        answers.append(checkSet(['gain'],'',
                object.__getattribute__(self,"_getgain")))
        for ans in answers:
            if ans:
                return ans
        return object.__getattribute__(self,__name)

    def _getVm(self):
        x,y = gtcurve.noBack(self.vin,self.vout)
        y = gtcurve.smooth(y)
        for i in range(len(x)-1):
            a = x[i]-y[i]
            b = x[i+1] - y[i+1]
            if a*b <= 0:
                self.Vm = x[i] + (x[i+1]-x[i])*a/(a-b)
                return x[i]
    def _gethys(self):
        self.hys = gtcurve.findhys(self.vin,self.vout)
        return self.hys
    
    def _getNoiseMargin(self):
        x,y = gtcurve.noBack(self.vin,self.vout)
        y = gtcurve.smooth(y)
        nms = []
        for i in range(len(x)-2):
            d1 = (y[i+1] - y[i])/(x[i+1] - x[i])
            d2 = (y[i+2] - y[i+1])/(x[i+2] - x[i+1])
            if (d1+1) * (d2+1) <= 0:
                nms.append((x[i+1],y[i+1]))
        if len(nms) >= 2:
            hx,hy = nms[0]
            lx,ly = nms[-1]
            self.NMH = abs(hx-ly)
            self.NML = abs(lx-hy)
        else:
            self.NMH = 0
            self.NML = 0
    
    def _getgain(self):
        diff = []
        x, y = gtcurve.noBack(self.vin,self.vout)
        for i in range(len(x)-1):
            diff.append(abs((y[i]-y[i+1])/(x[i]-x[i+1])))
        self.gain = max(diff)
        return self.gain

