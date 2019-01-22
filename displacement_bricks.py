import maya.cmds as cmds
import random



brickWall = "brickWall"
cmds.polyPlane(w=10, h=5, sx=10, sy=20, n=brickWall)
cmds.move(10, moveY=True)


eCount = cmds.polyEvaluate(e=True)
cmds.select(cl=True)


for i in xrange(3,430,42):
    for j in xrange(i, i+18, 4):
        eNum = str(j)
        cmds.select(brickWall+".e["+eNum+"]", add=True)
        
for i in xrange(26,430,42):
    for j in xrange(i, i+16, 4):
        eNum = str(j)
        cmds.select(brickWall+".e["+eNum+"]", add=True)
                
cmds.delete()
cmds.select(brickWall)
cmds.scale(0.655866, 1, 1)
cmds.polyExtrudeFacet(ltz=0.14292)

fCount = cmds.polyEvaluate(f=True)


cmds.select(cl=True)
for i in xrange(0, 110,1):
    fNum = str(i)
    randNum = random.uniform(0.1,0.3)
    cmds.select(brickWall+".f["+fNum+"]")
    cmds.polyExtrudeFacet(ltz=randNum)
    




