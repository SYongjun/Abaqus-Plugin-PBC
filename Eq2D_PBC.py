# -*- coding: mbcs -*-
from abaqus import *
from abaqusConstants import *
#******************************************
def create_Eq_2D(A,B,C,D,eqName,Dir_Eq,myModel):
    myModel.Equation(name = eqName, terms=((1.0,A, Dir_Eq),(-1.0,B, Dir_Eq),(-1.0,C, Dir_Eq),(1.0,D, Dir_Eq))) 
        
#******************************************
#******************************************        
def keyX(elem):
    return elem.coordinates[0]
def keyY(elem):
    return elem.coordinates[1]
def keyZ(elem):
    return elem.coordinates[2]
#******************************************
#******************************************
    
def PBC_Eq_2D(Edge_L,Edge_R,Edge_U,Edge_D,modelName):
    myModel = mdb.models[modelName]
    ass = myModel.rootAssembly
    LnodesO,RnodesO,UnodesO,DnodesO, = [],[],[],[]    
    Lnodes = Edge_L.getNodes()
    Rnodes = Edge_R.getNodes()
    Unodes = Edge_U.getNodes()
    Dnodes = Edge_D.getNodes()
    instanceName = Dnodes[0].instanceName
    for i in Lnodes:
        LnodesO.append(i)
        
    for i in Rnodes:
        RnodesO.append(i)  
        
    for i in Unodes:
        UnodesO.append(i)
        
    for i in Dnodes:
        DnodesO.append(i)
        
    LnodesO.sort(key=keyY)
    RnodesO.sort(key=keyY)
    UnodesO.sort(key=keyX)
    DnodesO.sort(key=keyX)
    LL=RnodesO[0].coordinates[0]-LnodesO[0].coordinates[0]
    HH=UnodesO[0].coordinates[1]-DnodesO[0].coordinates[1]
    for i in ass.features.keys():
        if i.startswith('RP'):
            del ass.features['%s' % (i)]
    rp1=ass.ReferencePoint(point = (1.2*RnodesO[-1].coordinates[0],0.5*(RnodesO[-1].coordinates[1]+RnodesO[0].coordinates[1]),0))
    rp2=ass.ReferencePoint(point = (0.5*(UnodesO[-1].coordinates[0]+UnodesO[0].coordinates[0]),1.2*UnodesO[-1].coordinates[1],0))
    r1 = ass.referencePoints                        
    d=len(r1)
    for i in r1.keys():
        refPoints1=(r1[i], )
        ass.Set(referencePoints=refPoints1, name='Ctrl_P'+str(d))
        d=d-1
        
#********************************************************************************   
    LD,RD,LU = [LnodesO[0].label],[RnodesO[0].label],[UnodesO[0].label]
    ass.SetFromNodeLabels(name = 'LD' , nodeLabels=((instanceName,LD),))
    ass.SetFromNodeLabels(name = 'RD' , nodeLabels=((instanceName,RD),))
    ass.SetFromNodeLabels(name = 'LU' , nodeLabels=((instanceName,LU),))
    
    for i in range(1,len(LnodesO)-1):
        con1='eqXX'+str(i)
        con2='eqXY'+str(i)
        Lnum = 'Lnode'+str(i)
        Rnum = 'Rnode'+str(i)
        ass.SetFromNodeLabels(name = Lnum , nodeLabels=((instanceName,[LnodesO[i].label]),))
        ass.SetFromNodeLabels(name = Rnum , nodeLabels=((instanceName,[RnodesO[i].label]),))
        create_Eq_2D(Rnum,Lnum,'RD','LD',con1,1,myModel)
        create_Eq_2D(Rnum,Lnum,'RD','LD',con2,2,myModel)  
    for i in range(1,len(UnodesO)):
        con1='eqYX'+str(i)
        con2='eqYY'+str(i)
        Unum = 'Unode'+str(i)
        Dnum = 'Dnode'+str(i)
        ass.SetFromNodeLabels(name = Unum , nodeLabels=((instanceName,[UnodesO[i].label]),))
        ass.SetFromNodeLabels(name = Dnum , nodeLabels=((instanceName,[DnodesO[i].label]),))
        create_Eq_2D(Unum,Dnum,'LU','LD',con1,1,myModel)
        create_Eq_2D(Unum,Dnum,'LU','LD',con2,2,myModel) 
    myModel.Equation(name='ctrl_E11',terms=((1.0,'RD',1),(-1.0,'LD', 1),(-1.0*LL,'Ctrl_P1', 1)))
    myModel.Equation(name='ctrl_E12',terms=((1.0,'RD',2),(-1.0,'LD', 2),(-1.0*LL,'Ctrl_P1', 2)))
    myModel.Equation(name='ctrl_E22',terms=((1.0,'LU',2),(-1.0,'LD', 2),(-1.0*HH,'Ctrl_P2', 2)))
    myModel.Equation(name='ctrl_E21',terms=((1.0,'LU',1),(-1.0,'LD', 1),(-1.0*HH,'Ctrl_P2', 1))) 