scalef=0.5
eyeShapes=['l_angry',
            'r_angry',
            'e_pinch',
            'le_up',
            're_up',
            'le_close',
            're_close']
            
faceShapes=['m_o',
            'm_m',
            'mr_smile',
            'ml_smile',
            'm_a',
            'm_ui',
            'm_li',
            'm_mr',
            'm_ml',
            'm_u',
            'm_d']

fingers=["thumb","index","middle","ring","pinky"]
joints=['jcog', 'jabdomen', 'jback', 'jchest', 'jneckBtm', 'jneck', 'jhead']
           
            
labels={'eye':'jeye',
        'head':'jhead',
        'neck':'jneck',
        'abdomen':'jabdomen',
        'cog':'jcog',
        'back':'jback',
        'chest':'jchest',
        'neckBtm':'jneckBtm',
        'jaw':'jjaw',
        'l_toeBtm':'l_toeBtm',
        'l_toe':'l_toe',
        'l_humerous':'l_humerous',
        'l_radius':'l_radius',
        'l_wrist':'l_wrist',
        'l_fibula':'l_fibula',
        'l_femur':'l_femur',
        'l_ankle':'l_ankle',
        'l_thumb':'l_thumb',
        'l_index':'l_index',
        'l_middle':'l_middle',
        'l_ring':'l_ring'}
        
yellow = (255/255, 255/255, 0/255)
bluish = (135/2255, 206/255, 235/255)
red = (255/255, 0/255, 0/255)
purple = (25/100, 7.45/100, 100/100)

rigCond={'Fingers':False,
        'Limbs':False,
        'Body':False,
        'EyeJaw':False,
}


"""
Helper Functions


"""


def eyeMC():
    x=0.5
    points=[[-x,0,-x], [-x,0,x],[x,0,x],[x,0,-x],[-x,0,-x]]    
    return points

def drawColorOverride(ctrl, color = (1,1,1)):
    cmds.setAttr(ctrl + ".overrideEnabled",1)
    cmds.setAttr(ctrl + ".overrideRGBColors",1)
    for channel, color in zip(['R', 'G', 'B'], color):
        cmds.setAttr(ctrl + ".overrideColor%s" %channel, color)

def parentList(list,up=False):
    if(up==False):
        i=0
        for i in range(0,len(list)-1):
            cmds.parent(list[i+1],list[i])
            i+=1
    if(up==True):
        i=0
        for i in range(1,len(list)):
            if(i!=0):
                cmds.parent(list[i],w=True)
            i+=1

def drawSwitch(circleName='s',rectName='r',attr='switch', move=[0,0,0],scale=[1,1,1]):
    circleName=circleName
    rectName=rectName
    cmds.circle(name=circleName)
    cmds.scale(0.2, 0.2, 0.2, circleName)
    cmds.curve(degree=1, ep=[[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[1,0,1]], name=rectName)
    cmds.scale(0.3, 0.3, 0.5, rectName)
    cmds.rotate('90deg', 0, 0, rectName)
    cmds.move(0, -0.23, 0, circleName)
    cmds.parent(circleName, rectName)
    cmds.makeIdentity(circleName,a=True)
    cmds.select(circleName)
    cmds.addAttr(shortName=attr, longName=attr, minValue=0.0, maxValue=1.0, k=True, r=True, w=True, h=False)
    revNode=circleName+'reverseNode'
    cmds.createNode('reverse', n=revNode)
    cmds.connectAttr(circleName+'.'+attr,revNode+'.input.inputX')
    cmds.setAttr(rectName+'.translateX', move[0])
    cmds.setAttr(rectName+'.translateY', move[1])
    cmds.setAttr(rectName+'.translateZ', move[2])
    cmds.makeIdentity(rectName, a=True)
    cmds.setDrivenKeyframe(circleName+'.'+attr,cd=circleName+'.translateY', dv=0.0, v=0.0)
    cmds.setDrivenKeyframe(circleName+'.'+attr,cd=circleName+'.translateY', dv=0.46, v=1.0)
    cmds.select(circleName)
    cmds.transformLimits(ety=[True,True], etx=[True,True], etz=[True,True])
    cmds.transformLimits(tx=(0,0), ty=(0, 0.46), tz=(0,0))
    cmds.select(clear=True)
    drawColorOverride(circleName, color2)
    cmds.scale(scale[0],scale[1],scale[2],rectName)

"""
Rigging The Body

"""
def rigBody(x):
    x=cmds.getAttr('jabdomen.translateX')
    y=cmds.getAttr('jabdomen.translateY')
    z=cmds.getAttr('jabdomen.translateZ')
    x1=cmds.getAttr('jcog.translateX')
    y1=cmds.getAttr('jcog.translateY')
    z1=cmds.getAttr('jcog.translateZ')
    for joint in joints:
        j=joint
        cname=joint+'_ctrl'
        cmds.circle(nr=(0,1,0),name=cname)
        cmds.scale(scalef,scalef,scalef,cname)
        cmds.parentConstraint(joint,cname,mo=False,name='del')
        cmds.delete('del')
        cmds.makeIdentity(cname,a=True)
        drawColorOverride(cname, purple)

    #cmds.joint('jcog',edit=True,oj="yzx",sao="zup",ch=True)
    for joint in joints:
        j=joint
        cname=joint+'_ctrl'
        cmds.parentConstraint(cname,joint,name=cname+'_const')
    print(joints)
    cmds.select('jcog_ctrl')
    cmds.delete('jcog_ctrl_const') 
    cmds.move(x,y,z,'jcog_ctrl.scalePivot', 'jcog_ctrl.rotatePivot',a=True)
    cmds.parentConstraint('jcog_ctrl','jcog',mo=True,name='jcog_ctrl_const')
    if(rigCond['Limbs']==True):
        for j in ["r_", "l_"]:
            cmds.parent(j+'fibula','jcog')
            cmds.parent(j+'humerous','jneckBtm')        
            for i in ["_fk","_ik"]:
                cmds.parent(j+'fibula'+i,'jcog')
                cmds.parent(j+'humerous'+i,'jneckBtm')    
    jctrls=[]
    i=0
    for j in joints:
        jctrls.append(j+'_ctrl')
        i+=1
        
    parentList(joints)
    parentList(jctrls)
    print(jctrls)
    rigCond['Body']=True
    
def deleteBodyRig(x):
    parentList(joints,up=True)
    if(rigCond['Limbs']==True):
        for i in ["r_","l_"]:
            cmds.parent(i+'fibula',w=True)
            cmds.parent(i+'humerous',w=True) 
            for j in ["_fk","_ik"]:
                cmds.parent(i+'fibula'+j,w=True)
                cmds.parent(i+'humerous'+j,w=True)
    for j in joints:
        constname=j+'_ctrl_const'
        cname=j+'_ctrl'
        if(rigCond['Limbs']==True):
            cmds.delete(constname)
            cmds.delete(cname)
    rigCond['Body']=False
"""
Rigging The Eye,Jaw and Face
"""
list=cmds.ls(selection=True)
if(list!=[]):
    globalY=cmds.getAttr('l_jeye.translateY')
def rigFace():
    list=cmds.ls(selection=True)
    print(cmds.ls(selection=True))
    cmds.createDisplayLayer(name='nst')
    cmds.group(em=True,name="annots")
    cmds.group(em=True,name="Eyectrls")
    
    def forrig(shapes, x, grp, anno):
        cmds.group(em=True,name=grp)
        i=0
        tempx=x
        for shape in shapes:
            x=x*1.25
            rectS=shape+'b'
            drawSwitch(circleName=shape,rectName=shape+'b',attr=shape+'attr',move=[0,0,0],scale=[1,1,1])
            cmds.editDisplayLayerMembers('nst',shape+'b',nr=True)
            cmds.connectAttr(shape+'.'+shape+'attr','Eyes'+'.'+shape)
            cmds.rotate(0,'180deg',0,rectS)
            cmds.makeIdentity(rectS,a=True)
            cmds.rotate(0,0,'90deg',rectS)
            j=i+1
            cmds.setAttr(rectS+'.translateY', globalY*j/5)
            yy=cmds.getAttr(shape+'b'+'.translateY')
            annot=cmds.annotate(shape,tx=shape,p=(anno,yy,0))
            cmds.parent(shape+'b',"Eyectrls")
            cmds.editDisplayLayerMembers('nst',annot)
            cmds.parent(rectS,grp)
            i=i+1
        cmds.scale(1,0.3,1,grp)
        cmds.move(x,globalY-0.5,0,grp)        
    forrig(eyeShapes,0.3,'eyeRig', 2.5)
    forrig(faceShapes,-0.15,'mouthRig', -2.5)
    cmds.setAttr("{}.displayType".format('nst'), 2) 
    for i in range(0,len(eyeShapes)+len(faceShapes)):###NNNNNNNNNNNNNNNEEEEDDD
        cmds.parent("annotation"+str(i+1),"annots")

def rigEye(x):
    cmds.curve(ep=eyeMC(),name='eyeMC',degree=1)
    cmds.mirrorJoint('l_jeye',searchReplace=["l_","r_"])
    cmds.parentConstraint('l_jeye','eyeMC',mo=False,name='del')
    cmds.delete('del')
    cmds.setAttr('eyeMC.translateZ', 0.8)
    cmds.setAttr('eyeMC.translateX', 0)
    cmds.makeIdentity('eyeMC',a=True)
    cmds.scale(scalef*2*1.25,scalef,scalef,'eyeMC')
    #for each eye
    i=0
    for eye in ["l_jeye","r_jeye"]:
        ctrl=eye+'ctrl'
        cmds.circle(name=ctrl)
        cmds.parentConstraint(eye,ctrl,mo=False,name='del')
        cmds.delete('del')
        cmds.setAttr(ctrl+'.translateZ',0.8)
        cmds.rotate('90deg',0,0,'eyeMC')
        cmds.rotate(0,'180deg',0,ctrl)
        cmds.makeIdentity(ctrl,a=True)
        cmds.scale(scalef/3,scalef/3,scalef/3, ctrl)
        cmds.makeIdentity(ctrl,a=True)
        cmds.parent(ctrl,'eyeMC')
        cmds.makeIdentity(ctrl,a=True)
        cmds.aimConstraint(ctrl,eye)
        drawColorOverride(ctrl,color2)
        drawSwitch(circleName=eye+'blink',rectName=eye+'board',attr=eye+'blinkattr', scale=[0.5*0.5,1,0.5])
        cmds.parentConstraint(eye,eye+'board',n='del')
        cmds.delete('del')
        cmds.rotate(0,'180deg',0,eye+'board')
        cmds.setAttr(eye+'board'+'.translateZ', 0.8)
        if(i==0):
            cmds.setAttr(eye+'board'+'.translateX',1)
        if(i==1):       
            cmds.setAttr(eye+'board'+'.translateX',-1)
        i=i+1
        cmds.parent(eye+'board', 'eyeMC')
    cmds.makeIdentity('eyeMC',a=True)
    cmds.parent('eyeMC','jneck_ctrl')
    rigJaw()
    for x in ['l_jeye','r_jeye']:
        cmds.parent(x,'jhead')
    #rigFace()
    rigCond['EyeJaw']=True

def rigJaw():
    points=[[0,0,1],[0,0,-1], [-1,0,0], [0,0,1]]
    cmds.curve(ep=points,name='jctrl',degree=1) 
    cmds.rotate('55deg',0,0,'jctrl') 
    cmds.scale(1,1,1.24,'jctrl') 
    cmds.select('jjaw')
    cmds.parentConstraint('jjaw','jctrl',mo=False,name='del')
    cmds.delete('del')
    cmds.rotate(0,'90deg',0,'jctrl')
    cmds.scale(0.3,0.3,0.3,'jctrl') 
    cmds.makeIdentity('jctrl',a=True)
    cmds.rotate('90deg',0,0,'jctrl')
    cmds.makeIdentity('jctrl',a=True)
    cmds.parentConstraint('jctrl', 'jjaw')
    drawColorOverride('jctrl',color2)
    cmds.parent('jctrl','jneck_ctrl')
    cmds.parent('jjaw','jhead')

def deleteRigEye(x):
    cmds.delete('eyeMC')
    cmds.delete('r_jeye')
    cmds.delete('jctrl')
    cmds.parent('l_jeye',w=True)
    cmds.delete("annots")
    cmds.delete("eyeRig")
    cmds.delete("mouthRig")
    cmds.delete("nst")
    rigCond['EyeJaw']=False

"""
Rig Limbs

"""

def rigFeet():
    x=0.1
    points=[[-x,0,-x], [-x,0,x],[x,0,x],[x,0,-x],[-x,0,-x]]    
    #cmds.mirrorJoint('l_toeBtm', searchReplace=('l_','r_'))        
    #cmds.mirrorJoint('l_toe', searchReplace=('l_','r_'))
    #for sd in ['l_','r_']:
     #   cmds.parent(sd+'toe',sd+'toeBtm')
      #  cmds.parent(sd+'toeBtm',sd+'ankle')
    #    cmds.curve(degree=1,ep=points,name=sd+'toe_ctrl')   
     #   cmds.parentConstraint(sd+'toeBtm',sd+'toe_ctrl',mo=False,name='del')    
      #  cmds.delete('del')
       # cmds.rotate('90deg','90deg',0,sd+'toe_ctrl')
   #     cmds.makeIdentity(sd+'toe_ctrl',a=True)
  #      cmds.parentConstraint(sd+'toeBtm',sd+'toe_ctrl',mo=False,name='del')    
    #    cmds.delete('del')        
     #   cmds.scale(0.3,0.5,0.8,sd+'toe_ctrl')
      #  cmds.parentConstraint(sd+'toe_ctrl',sd+'toeBtm')
    #    cmds.parent(sd+'toe_ctrl',sd+'leg_ikHandle_ctrl')
     #   drawColorOverride(sd+'toe_ctrl',color1)


def rigLimb(org,side,strJnt):
    # SETUP
    if(org=="leg"):
        arm = ["fibula", "femur", "ankle", "toeBtm", "toe"]
    if(org=="arm"):
        arm = ["humerous", "radius", "wrist"]        
    scalef = 0.2
    if(side=='l_'):
        color1 = yellow
        color2 = bluish
    else:
        color1 = red
        color2 = bluish
        
    # HELPER FUNCTIONS
    def ik_ctrl_draw():
        if(org=='leg'):
            x=0.5
            points=[[-x,0,-x], [-x,0,x],[x,0,x],[x,0,-x],[-x,0,-x]]
        if(org=='arm'):    
            points=[[3,0,0],[1,0,1],[0,0,3], 
                    [-1,0,1],[-3,0,0],[-1,0,-1],[0,0,-3],[1,0,-1],[3,0,0]]
        return points
    def pole_ctrl_draw():
        points=[[0,1,0],[1,0,1],[0,1,0],[-1,0,1],[0,1,0],[-1,0,-1],[0,1,0],[1,0,-1],    
        [-1,0,-1],[-1,0,1],[1,0,1],[1,0,-1]]
        return points
    def drawColorOverride(ctrl, color = (1,1,1)):
        cmds.setAttr(ctrl + ".overrideEnabled",1)
        cmds.setAttr(ctrl + ".overrideRGBColors",1)
        for channel, color in zip(['R', 'G', 'B'], color):
            cmds.setAttr(ctrl + ".overrideColor%s" %channel, color)
    # Renaming main 
    cmds.select(strJnt)
    cmds.joint(edit=True,oj="yzx",sao="zup",ch=True)
    cmds.select(hi=True)
    main_joints=cmds.ls(selection=True)
    print(main_joints)
	
    #FORWARD KINEMATICS
    cmds.duplicate(main_joints[0], rc = True)
    cmds.select(main_joints[0] + '1')
    cmds.select(hi=True)
    fkjoints = cmds.ls(selection=True)
    print(fkjoints)
    fkctrls = []
    i=0
    for joint in fkjoints:
        cmds.select(joint)
        jname=side+arm[i]+'_fk'
        jcname=side+arm[i]+'_fk'+'_ctrl'
        cmds.rename(jname)
        fkjoints[i] = jname
        fkctrls.append(jcname)
        cmds.select(clear=True)
        cmds.circle(nr=(0,1,0), name=jcname)
        cmds.makeIdentity(jcname, a=True)
        cmds.scale(scalef, scalef, scalef, jcname)
        cmds.parentConstraint(jname, jcname, mo=False, name='delete')
        cmds.delete('delete')
        cmds.makeIdentity(jcname, a=True)
        cmds.parentConstraint(jcname, jname, mo=True)
        drawColorOverride(jcname, color1)
        i+=1

    for j in range(0, len(fkctrls)):
        if(j<(len(fkctrls)-1)):
            cmds.parent(fkctrls[j+1], fkctrls[j])
        j=j+1
        
    print(fkjoints)
    #Inverse Kinematics
    cmds.duplicate(main_joints[0], rc = True)
    cmds.select(main_joints[0] + '1')
    cmds.select(hi=True)
    ikjoints = cmds.ls(selection=True)
    print(ikjoints)
    i=0
    for joint in ikjoints:
        cmds.select(joint)
        jname=side+arm[i]+'_ik'
        cmds.rename(jname)
        ikjoints[i] = jname
        cmds.select(clear=True)
        i=i+1

    def matchIKFK():
        for fk,ik in zip(fkjoints,ikjoints):
            for O in ["X","Y","Z"]:
                cmds.setAttr(ik+'.translate'+O,cmds.getAttr(fk+'.translate'+O))
                cmds.setAttr(ik+'.rotate'+O,cmds.getAttr(fk+'.rotate'+O))
    def printIKFK():
        for fk,ik in zip(fkjoints,ikjoints):
            for O in ["X","Y","Z"]:
                print(side+O+"Rotate"+ik+'.translate'+O+":"+str(cmds.getAttr(ik+'.translate'+O)))
                print(side+O+"Translate"+ik+'.rotate'+O+":"+str(cmds.getAttr(ik+'.rotate'+O)))



    #IK HANDLE AND IK CONTROL     
    ankle=2
    ikhandle=side+org+'_ikHandle'
    ikhandlectrl=side+org+'_ikHandle'+'_ctrl'
    cmds.ikHandle(n=ikhandle, sj=ikjoints[0], ee=ikjoints[ankle])
    cmds.curve(degree=1,ep=ik_ctrl_draw(),name=ikhandlectrl)
    cmds.scale(scalef, scalef, scalef, ikhandlectrl)
    cmds.parentConstraint(ikjoints[ankle], ikhandlectrl, mo=False, name='del')
    cmds.delete('del')

    drawColorOverride(ikhandlectrl, color1)

    #IK POLE AND IK POLE CONTROL
    pole=side+org+'_pole'
    polectrl=side+org+'_pole'+'ctrl'
    cmds.spaceLocator(name=pole)
    cmds.parentConstraint(ikjoints[1], pole, mo=False, name='del')
    cmds.delete('del')
    cmds.move(0,0,-0.5, pole, r=True)
    cmds.curve(degree=1,ep=pole_ctrl_draw(),name=polectrl)
    cmds.scale(scalef/2,scalef/2,scalef/2,polectrl)
    cmds.parentConstraint(pole,polectrl,mo=False,name='del')
    cmds.delete('del')
    cmds.rotate('90deg', 0, 0, polectrl)
    cmds.parentConstraint(polectrl,pole)
    cmds.makeIdentity(polectrl, a=True)
    drawColorOverride(polectrl, color1)

    #ApplyPOLE
    cmds.pointConstraint(ikjoints[0],ikjoints[2],polectrl,name='del')
    cmds.delete('del')
    cmds.aimConstraint(ikjoints[1],polectrl,name='del')
    cmds.delete('del')
    cmds.makeIdentity(polectrl,a=True)
    cmds.poleVectorConstraint(pole,ikhandle)
    
    #Blend IK and FK
    for jointIK, jointFK, joint in zip(ikjoints, fkjoints, main_joints):
        cmds.parentConstraint(jointIK, jointFK, joint, name=joint+'const')


    cmds.makeIdentity(ikhandlectrl, a=True)
    if(org=="leg"):    
        cmds.rotate('90deg',0,0,ikhandlectrl)
    cmds.makeIdentity(ikhandlectrl, a=True)
    
    cmds.parentConstraint(ikhandlectrl, ikhandle)
    cmds.orientConstraint(ikhandlectrl, ikjoints[ankle],mo=True)
    
    #Implement IK-FK switch
    circleName=side+org+'_switchS'
    rectName=side+org+'_switchBase'
    cmds.circle(name=circleName)
    cmds.scale(0.2, 0.2, 0.2, circleName)
    cmds.curve(degree=1, ep=[[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1],[1,0,1]], name=rectName)
    cmds.scale(0.3, 0.3, 0.5, rectName)
    cmds.rotate('90deg', 0, 0, rectName)
    cmds.move(0, -0.23, 0, circleName)
    cmds.parent(circleName, rectName)
    cmds.makeIdentity(circleName,a=True)
    cmds.select(circleName)
    cmds.addAttr(shortName='SWITCH', longName='IK_FK_SWITCH', minValue=0.0, maxValue=1.0, k=True, r=True, w=True, h=False)
    revNode=side+org+'reverseIKFK'
    cmds.createNode('reverse', n=revNode)
    cmds.connectAttr(circleName+'.IK_FK_SWITCH',revNode+'.input.inputX')
    cmds.parentConstraint(pole, rectName, n='del', sr=['x', 'y', 'z'], mo=False)
    cmds.delete('del')
    if(side=='l_'):
        cmds.move(1, 0, 0, rectName, r=True)
    if(side=='r_'):
        cmds.move(-1, 0, 0, rectName, r=True)
    cmds.makeIdentity(rectName, a=True)
    for joint in main_joints:
        cmds.connectAttr(circleName+'.IK_FK_SWITCH',joint+'const'+'.'+joint+'_fkW1')
        cmds.connectAttr(revNode+'.output.outputX',joint+'const'+'.'+joint+'_ikW0')
    cmds.setDrivenKeyframe(circleName+'.IK_FK_SWITCH',cd=circleName+'.translateY', dv=0.0, v=0.0)
    cmds.setDrivenKeyframe(circleName+'.IK_FK_SWITCH',cd=circleName+'.translateY', dv=0.46, v=1.0)
    cmds.select(circleName)
    cmds.transformLimits(ety=[True,True], etx=[True,True], etz=[True,True])
    cmds.transformLimits(tx=(0,0), ty=(0, 0.46), tz=(0,0))
    cmds.select(clear=True)
    drawColorOverride(circleName, color2)


    #SortOut All Visibility
    for ctrl in fkctrls:
        cmds.connectAttr(circleName+'.IK_FK_SWITCH', ctrl+'.visibility')

    cmds.connectAttr(circleName+'.IK_FK_SWITCH', revNode+ '.input.inputY')
    for ctrl in [ikhandlectrl, polectrl]:
        cmds.connectAttr(revNode+'.output.outputY', ctrl+'.visibility')


    #Hide Unnecessary
    cmds.hide(ikhandle)
    cmds.hide(pole)
    for i,j,k in zip(fkjoints, ikjoints, main_joints):
        cmds.hide(i)
        cmds.hide(j)
        #cmds.hide(k)
    matchIKFK()
    
    #Twist Effect
    mdn=org+side+'_mD'
    cmds.shadingNode('multiplyDivide',au=True, n=mdn)
    if(org=="leg"):
        cmds.connectAttr(ikhandle+'.rotateY',mdn+'.input1X')
        cmds.setAttr(mdn+'.operation',2)
        cmds.setAttr(mdn+'.input2X',16)
        cmds.connectAttr(mdn+'.outputX',polectrl+'.translateX')
    if(org=="arm"):
        cmds.connectAttr(ikhandle+'.rotateX',mdn+'.input1X')
        cmds.setAttr(mdn+'.operation',2)
        cmds.setAttr(mdn+'.input2X',16)
        cmds.connectAttr(mdn+'.outputX',polectrl+'.translateY')


    if(org=="leg"):
        #Roll Slider
        cName=side+"rollC"
        rName=side+"rollR"
        gName=side+"roll"+"_g"
        cmds.group(em=True,name=gName)
        drawSwitch(circleName=cName, rectName=rName, attr="froll")
        cmds.parent(rName,gName)
        cmds.scale(0.2,1,1,gName)
        if(side=="l_"):
            cmds.move(0.3,0,0,gName)
        else:
            cmds.move(-0.3,0,0,gName)
        cmds.makeIdentity(gName,a=True)
        #Twist Slider
        cName=side+"twistC"
        rName=side+"twistR"
        gName=side+"twist"+"_g"
        cmds.group(em=True,name=gName)
        drawSwitch(circleName=cName, rectName=rName, attr="ftwist")
        cmds.parent(rName,gName)
        cmds.scale(0.2,1,1,gName)
        if(side=="l_"):
            cmds.move(0.4,0,0,gName)
        else:
            cmds.move(-0.4,0,0,gName)
        cmds.makeIdentity(gName,a=True)

#Join the Fingers to the Limb
def joinF(side):
    newF=[]
    newFc=newF
    for x in fingers:
        newF.append(side+x)
    print(newF)
    for f in newF:
        cmds.parent(f,side+'wrist')
    i=0
    for x in newFc:
        newFc[i]=x+'_ctrl'
        i+=1
    for f in newFc:
        cmds.parent(f,side+'wrist')
            
            
def rigLimbs(x):
    cmds.group(em=True,name="ctrls")
    cmds.mirrorJoint("l_fibula",sr=["l_","r_"],mirrorYZ=True,mb=True)
    cmds.mirrorJoint("l_humerous",sr=["l_","r_"],mirrorYZ=True,mb=True)
    rigLimb(org="arm",side="l_",strJnt="l_humerous")
    rigLimb(org="arm",side="r_",strJnt="r_humerous")
    if(rigCond['Fingers']==True):
        joinF('l_')
        joinF('r_')
    rigLimb(org="leg",side="l_",strJnt="l_fibula")
    rigLimb(org="leg",side="r_",strJnt="r_fibula")
    rigFeet()
    def group(side):
        cmds.parent(side+"fibula"+'_fk_ctrl',"ctrls")
        cmds.parent(side+"humerous"+'_fk_ctrl',"ctrls")
        cmds.parent(side+"humerous_fk","ctrls")
        cmds.parent(side+"humerous_ik","ctrls")
        cmds.parent(side+"leg_ikHandle_ctrl","ctrls")
        cmds.parent(side+"arm_ikHandle_ctrl","ctrls")
        cmds.parent(side+"fibula_fk","ctrls")
        cmds.parent(side+"fibula_ik","ctrls")
        cmds.parent(side+"arm_pole","ctrls")
        cmds.parent(side+"leg_pole","ctrls")
        cmds.parent(side+"leg_polectrl","ctrls")
        cmds.parent(side+"arm_polectrl","ctrls")
        cmds.parent(side+"leg_switchBase","ctrls")
        cmds.parent(side+"arm_switchBase","ctrls")
        cmds.parent(side+"arm_ikHandle","ctrls")
        cmds.parent(side+"leg_ikHandle","ctrls")
    group("l_")
    group("r_")
    rigCond["Limbs"]=True
    
    
    
    
    
def deleteLimbsRig(x):
    leg = ["fibula","femur","ankle"]
    arm = ["humerous","radius","wrist"]
    for side in ["l_","r_"]:
        if(rigCond['Fingers']==True):
            for s in fingers:
                cmds.parent(side+s,w=True)
                cmds.parent(side+s+'_ctrl',w=True)
        for s in leg:
            cmds.delete(side+s+'const')
        for s in arm:
            cmds.delete(side+s+'const')
        cmds.delete(side+"fibula"+'_fk_ctrl')
        cmds.delete(side+"humerous"+'_fk_ctrl')
        cmds.delete(side+"humerous_fk")
        cmds.delete(side+"humerous_ik")
        cmds.delete(side+"leg_ikHandle_ctrl")
        cmds.delete(side+"arm_ikHandle_ctrl")
        cmds.delete(side+"leg_ikHandle")
        cmds.delete(side+"fibula_fk")
        cmds.delete(side+"fibula_ik")
        cmds.delete(side+"arm_pole")
        cmds.delete(side+"leg_pole")
        cmds.delete(side+"leg_polectrl")
        cmds.delete(side+"arm_polectrl")
        cmds.delete(side+"leg_switchBase")
        cmds.delete(side+"arm_switchBase")
    cmds.delete("r_humerous")
    cmds.delete("r_fibula")
    cmds.parent("l_toeBtm",w=True)
    cmds.parent("l_toe",w=True)    
    cmds.delete("ctrls")
    rigCond['Limbs']=False



"""
Rigging only the Fingers

"""
def rSH(s,finger):
    cmds.select(s+finger,hi=True)
    m=cmds.ls(selection=True)
    cmds.select(clear=True)
    return m

def sideOfHand(s,finger,fingers):
    fingerx=fingers
    ctrls=[]
    i=0
    for jnt in fingerx:
        jname=s+finger+str(i)
        if(i==0):
            jctrl=s+finger+"_ctrl"
        else:
            jctrl=s+finger+str(i)+"_ctrl"
        cmds.rename(jnt,jname)
        cmds.circle(nr=(0,1,0),name=jctrl)
        if(s=='l_'):
            drawColorOverride(jctrl,yellow)
        else:
            drawColorOverride(jctrl,red)
        ctrls.append(jctrl)
        cmds.scale(scalef*0.1,scalef*0.05,scalef*0.05,jctrl)
        cmds.parentConstraint(jname,jctrl,mo=False,name='del')
        cmds.delete('del')
        cmds.parentConstraint(jctrl,jname)
        i+=1
    print(ctrls)
    i=0
    parentList(ctrls)
 
         
def rigFinger(x):
    cmds.select(clear=True)
    def hand(side):
        for finger in fingers:
             cmds.joint(side+finger,edit=True,oj="yzx",sao="zup",ch=True)
             m=rSH(side,finger)
             sideOfHand(side,finger,m)
             cmds.rename(side+finger+"0",side+finger)             
             if(side=="l_"):
                 cmds.mirrorJoint("l_"+finger,sr=["l_","r_"],mirrorYZ=True,mb=True)
    hand("l_")
    hand("r_")
    rigCond['Fingers']=True

def deleteFingerRig(x):
    for m in fingers:
        cmds.delete("r_"+m)
        cmds.delete("r_"+m+"_ctrl")
        cmds.delete("l_"+m+"_ctrl")
    rigCond['Fingers']=False
"""
Main Function



"""   
   
   
                   
def rig(x):
    x=cmds.getAttr('jabdomen.translateX')
    y=cmds.getAttr('jabdomen.translateY')
    z=cmds.getAttr('jabdomen.translateZ')
    cmds.select(clear=True)
    cmds.select('jeye')
    cmds.rename('l_jeye')
    cmds.mirrorJoint(sr=["l_","r_"],mirrorYZ=True)
    cmds.parent('jjaw','jhead')
    cmds.parent('l_jeye','jhead')
    cmds.parent('r_jeye','jhead')
    cmds.parent('jhead','jneck')
    cmds.parent('jneck','jneckBtm')
    cmds.parent('jneckBtm','jchest')
    cmds.parent('jchest','jback')
    cmds.parent('jback','jabdomen')
    cmds.parent('jabdomen','jcog')
    rigFingers()
    rigBody()
    rigEye()
    rigJaw()
    for i in range(0,len(joints)-1):
        cmds.parent(joints[i+1]+'_ctrl',joints[i]+'_ctrl')
    cmds.parent('jabdomen_ctrl',w=True)
    cmds.select(clear=True)
    cmds.select('jcog_ctrl')
    cmds.delete('jcog_parentConstraint1') 
    cmds.move(x,y,z,'jcog_ctrl.scalePivot', 'jcog_ctrl.rotatePivot',a=True)
    cmds.parent('jabdomen_ctrl','jcog_ctrl')
    
    cmds.parentConstraint('jcog_ctrl','jcog',mo=True)
    for j in ["r_", "l_"]:
        cmds.parent(j+'fibula','jcog')
        cmds.parent(j+'humerous','jneckBtm')        
        for i in ["_fk","_ik"]:
            cmds.parent(j+'fibula'+i,'jcog')
            cmds.parent(j+'humerous'+i,'jneckBtm')
    rigFeet()
    cmds.deleteUI(window)


def rig(x):
    print(rigCond)

def deleteRig(x):
    print("deleteRig")



def spaces():
    cmds.iconTextStaticLabel(st='textOnly',l='')
    cmds.iconTextStaticLabel(st='textOnly',l='')
    cmds.iconTextStaticLabel(st='textOnly',l='')
    cmds.iconTextStaticLabel(st='textOnly',l='')
def space():
    cmds.iconTextStaticLabel(st='textOnly',l='')
    
    
    
windowName="Select the joints"
window=cmds.window(title=windowName,menuBar=True,widthHeight=(300,600))
labels={'eye':'l_jeye',
        'head':'jhead',
        'neck':'jneck',
        'abdomen':'jabdomen',
        'cog':'jcog',
        'back':'jback',
        'chest':'jchest',
        'neckBtm':'jneckBtm',
        'jaw':'jjaw',
        'l_toeBtm':'l_toeBtm',
        'l_toe':'l_toe',
        'l_humerous':'l_humerous',
        'l_radius':'l_radius',
        'l_wrist':'l_wrist',
        'l_fibula':'l_fibula',
        'l_femur':'l_femur',
        'l_ankle':'l_ankle',
        'l_thumb':'l_thumb',
        'l_index':'l_index',
        'l_middle':'l_middle',
        'l_ring':'l_ring',
        'l_pinky':'l_pinky'}

cmds.menu(label='Type of Rig')
cmds.radioMenuItemCollection()
cmds.menuItem( label='Human', radioButton=True )
cmds.menuItem( label='FourLegged', radioButton=False )
cmds.gridLayout(numberOfColumns=3, cellWidthHeight=(100, 40), numberOfChildren=len(labels))
for label in labels:
    cmds.button(label=label,command="cmds.rename('"+labels[label]+"')")
spaces()
space()
cmds.button(label='RIG', command=rig)
cmds.button(label='Delete Rig', command=deleteRig)
space()
cmds.button(label='Rig Finger', command=rigFinger)
cmds.button(label='Delete FingerRig', command=deleteFingerRig)
space()
cmds.button(label='Rig Limbs', command=rigLimbs)
cmds.button(label='Delete LimbsRig', command=deleteLimbsRig)
space()
cmds.button(label='Rig Body', command=rigBody)
cmds.button(label='Delete BodyRig', command=deleteBodyRig)
space()
cmds.button(label='Rig Eye&Jaw', command=rigEye)
cmds.button(label='Delete Eye&Jaw', command=deleteRigEye)
space()
cmds.button(label='Rig Face', command=rigFace)
cmds.button(label='Delete Face')
cmds.showWindow(window)



