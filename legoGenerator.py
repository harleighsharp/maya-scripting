import maya.cmds as cmds
import random as rnd


##Create square blocks without holes (basic blocks)
def squareBlocksNoHoles():
    blockHeight = cmds.intSliderGrp('sqBlockHeight', q=True, v=True)
    blockWidth = cmds.intSliderGrp('sqBlockWidth', q=True, v=True)
    blockDepth = cmds.intSliderGrp('sqBlockDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    

    cmds.select(clear=True)
    
    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    block = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    cmds.move((cubeSizeY/2.0), moveY=True)
    bumps = createBumps(blockWidth, blockDepth, cubeSizeX, cubeSizeY, cubeSizeZ, 0.4, 0.10, 0.4)
    
    cmds.select(block)
    cmds.select(bumps, add=True)
        
    finalBlock = cmds.polyUnite(n="Block" + str(rnd.randint(1000,9999)), ch=False)
    
    applyMaterial(finalBlock, rgb)
    cmds.delete(ch=True)


##Create square blocks with holes
def squareBlocksHoles():
    blockHeight = 3
    blockWidth = 1
    blockDepth = cmds.intSliderGrp('sqHolesBlockDepth', q=True, v=True)
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)

    cmds.select(clear=True)

    cubeSizeX = blockWidth * 0.8
    cubeSizeZ = blockDepth * 0.8
    cubeSizeY = blockHeight * 0.32

    block = cmds.polyCube(h=cubeSizeY, w=cubeSizeX, d=cubeSizeZ)
    cmds.move((cubeSizeY/2.0), moveY=True)

    holedBlock = createHoles(block, blockDepth, cubeSizeX, cubeSizeY, cubeSizeZ, 0, True, 0.8)
    bumps = createBumps(blockWidth, blockDepth, cubeSizeX, cubeSizeY, cubeSizeZ, 0.4, 0.10, 0.4)
    
    cmds.select(holedBlock)
    cmds.select(bumps, add=True)
    finalBlock = cmds.polyUnite(n="Block" + str(rnd.randint(1000,9999)), ch=False)
    
    
    applyMaterial(finalBlock, rgb)
    cmds.delete(ch=True)


def technicBeamsStraight():
    blockHeight = 2
    blockWidth = 1
    blockDepth = cmds.intSliderGrp('technicStraightBeamDepth', q=True, v=True)
    
    noAxels = cmds.radioButton('noAxels',query=True, select=True )
    bothAxels = cmds.radioButton('bothAxels',query=True, select=True )
    oneAxel = cmds.radioButton('oneAxel',query=True, select=True )
    
    axels = 0
    
    if(noAxels):
        axels = 0
        
    if(oneAxel):
        axels = 1
      
    if(bothAxels):
        axels = 2
    
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    
    cmds.select(clear=True)

    beamSizeX = blockWidth * 0.8
    beamSizeZ = blockDepth * 0.8
    beamSizeY = blockHeight * 0.32

    block = cmds.polyCube(h=beamSizeY, w=beamSizeX, d=beamSizeZ)
    cmds.move((beamSizeY/2.0), moveY=True)
    
    beam = createRoundedBeams(block, beamSizeX, beamSizeY, beamSizeZ)
    #increase cube length by radius of cylinders
    beamSizeZ = beamSizeZ + 0.5
        
    indented = createBeamIndents(beam, blockDepth, beamSizeX, beamSizeY, beamSizeZ)
    
    
    finalBlock = createHoles(indented, blockDepth, beamSizeX, beamSizeY, beamSizeZ, axels, False, 0.25)
    finalBlock = cmds.rename("Block" + str(rnd.randint(1000,9999)))
    
   
    applyMaterial(finalBlock, rgb)
    cmds.delete(ch=True)

def technicBeamsAngled():
    blockHeight = 2
    blockWidth = 1
    
    
    #Length pre-bend
    block1Depth = cmds.intSliderGrp('technicAngledBeam1Depth', q=True, v=True)
    #Length post-bend
    block2Depth= cmds.intSliderGrp('technicAngledBeam2Depth', q=True, v=True)
    beamAngleChoice = cmds.optionMenuGrp('technicBeamAngle', q = True, v = True)
    
    noAxels = cmds.radioButton('noAxels',query=True, select=True )
    bothAxels = cmds.radioButton('bothAxels',query=True, select=True )
    oneAxel = cmds.radioButton('oneAxel',query=True, select=True )
    
    axels = 0
    
    if(noAxels):
        axels = 0
        
    if(oneAxel):
        axels = 1
      
    if(bothAxels):
        axels = 1
    
    if(beamAngleChoice == '53.5'):
        beamAngle = 53.5
    else:
        beamAngle = 90
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    
 
    cmds.select(clear=True)

    beamSizeX = blockWidth * 0.8
    beamSizeY = blockHeight * 0.32
    beam1SizeZ = block1Depth * 0.8
    beam2SizeZ = block2Depth * 0.8
    

    beam1 = cmds.polyCube(h=beamSizeY, w=beamSizeX, d=beam1SizeZ)
    cmds.move((beamSizeY/2.0), moveY=True)
    beam1 = createRoundedBeams(beam1, beamSizeX, beamSizeY, beam1SizeZ)
    beam1SizeZ = beam1SizeZ + 0.5
    beam1 = createBeamIndents(beam1, block1Depth, beamSizeX, beamSizeY, beam1SizeZ)
    beam1_final = createHoles(beam1, block1Depth, beamSizeX, beamSizeY, beam1SizeZ, axels, False, 0.25)
    
    
    
    beam2 = cmds.polyCube(h=beamSizeY, w=beamSizeX, d=beam2SizeZ)
    cmds.move((beamSizeY/2.0), moveY=True)
    
    if(oneAxel):
        axels = 0
    #beam2, rotated one
    beam2 = createRoundedBeams(beam2, beamSizeX, beamSizeY, beam2SizeZ)
    beam2SizeZ = beam2SizeZ + 0.5
    beam2 = createBeamIndents(beam2, block2Depth, beamSizeX, beamSizeY, beam2SizeZ)
    beam2_final = createHoles(beam2, block2Depth, beamSizeX, beamSizeY, beam2SizeZ, axels, False, 0.25)
    #to move beam 2 to end of beam1
    cmds.select(beam2_final)
    beam2Name = cmds.ls(beam2_final)[0]
   
    cmds.rotate(-180,0,0)
    cmds.makeIdentity(apply=True)
    cmds.move(0,(beamSizeY/2.0),(((beam2SizeZ/2.0)-0.25)*-1), beam2Name+".scalePivot", beam2Name+".rotatePivot", a=True)
    cmds.move(((beam2SizeZ/2.0) + (beam1SizeZ/2.0)-0.5), moveZ=True)
    
    cmds.rotate(-beamAngle,0,0, a=True)
    
    cmds.select(beam1_final)
    cmds.select(beam2_final, add=True)
    finalBlock = cmds.polyUnite(n="Block" + str(rnd.randint(1000,9999)), ch=False)
    
   
    applyMaterial(finalBlock, rgb)
    cmds.delete(ch=True)
    

def wheel():
    #dimensions 43.2 x 28
    wheelRadius = 3 * 0.8 + 0.6
    wheelWidth =  7 * 0.8
    wheelThickness = 1.0
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)    
    
    cmds.select(clear=True)
    tire = cmds.polyPipe(r=wheelRadius, h=wheelWidth, thickness=wheelThickness, sh=6, sc=2, n="Tire" + str(rnd.randint(1000,9999)))
  
    
    #extrusions and edge movements
    tireName = cmds.ls(tire)[0]
    
    cmds.select(tireName+".e[160:179]")
    cmds.select( tireName+".e[280:299]", add = True)
    
    cmds.scale(0.9, 0.9, 0.9,relative=True)
    
    cmds.select(tireName+".f[200:219]")
    cmds.select(tireName+".f[220:239]", add = True)
    cmds.scale(1, 1.8, 1,relative=True)
    
    cmds.select(clear=True)
    for face in range(200,219,2):
        cmds.select(tireName+".f["+str(face)+"]", add=True)
   
    for face in range(221,240,2):
        cmds.select(tireName+".f["+str(face)+"]", add=True)
    
    cmds.polyExtrudeFacet(lt=(0,0,0.1))
    cmds.select(clear=True)
        
    
    for face in range(140,179,2): 
        cmds.select(tireName+".f["+str(face)+"]", add=True)
    for face in range(261,300,2):
        cmds.select(tireName+".f["+str(face)+"]", add=True)
    cmds.polyExtrudeFacet(lt=(0,0,0.07))
   
    #raise flattened part to meet extrusions
    cmds.select(clear=True)
    for face in range(120,139):
        cmds.select(tireName+".f["+str(face)+"]", add=True)
    cmds.move(0, 0.07,0, relative=True)
    cmds.select(clear=True)
    for face in range(300,319):
        cmds.select(tireName+".f["+str(face)+"]", add=True)
    cmds.move(0, -0.07,0, relative=True)
    
 
    cmds.select(tire)
    cmds.move((wheelRadius), moveY=True, a=True)
    cmds.rotate(90, rotateX=True)
    
    applyMaterial(tire, rgb)
    
    
    
    hubCap = hub(wheelRadius)
    cmds.delete(ch=True)
    
   

def hub(wheelRadius):
    hubRadius = wheelRadius - 1
    hubWidth = 3 * 0.8
    hubThickness = 0
    
    rgb = cmds.colorSliderGrp('hubColor', q=True, rgbValue=True)    
    
    
    outerHub = cmds.polyCylinder(r=hubRadius, h=hubWidth)
    cmds.move((wheelRadius), moveY=True, a=True)
    cmds.rotate(90, rotateX=True)
    
    
    innerHubL = cmds.polyCylinder(r=hubRadius-0.3, h=0.6)
    cmds.move((wheelRadius), moveY=True, a=True)
    cmds.rotate(90, rotateX=True)
    cmds.move(1.2,moveZ=True, r=True)
    
    innerHubR = cmds.polyCylinder(r=hubRadius-0.3, h=0.6)
    cmds.move((wheelRadius), moveY=True, a=True)
    cmds.rotate(90, rotateX=True)
    cmds.move(-1.2,moveZ=True, r=True)
    
    cmds.select(outerHub)
    cmds.select(innerHubL, add=True)
    cmds.select(innerHubR, add=True)
    hub = cmds.polyCBoolOp(op=2, ch=False)
    cmds.select(clear=True)
    
    pairs = []
    holeArray = []
    hubHoleArray =[]
    #outer, larger radius, slight indent
    for i in range(-1,2,2):
        hole = cmds.polyCylinder(r=0.3, h=0.2, sz=1)
        cmds.rotate(90, rotateX=True)
        cmds.move((i*0.8), moveX=True, a=True)
        cmds.move(-0.9,moveZ=True)
        pairs.append(hole)
        
        hole = cmds.polyCylinder(r=0.3, h=0.2, sz=1)
        cmds.rotate(90, rotateX=True)
        cmds.move((i*0.8), moveX=True, a=True)
        cmds.move(0.9,moveZ=True)
        pairs.append(hole)
        
    for pair in pairs:
        cmds.select(pair, add=True)
    pair1 = cmds.polyUnite(ch=False)
    
    cmds.select(pair1)
    pair2 = cmds.duplicate()
    cmds.rotate(60,rotateZ=True)
    
    cmds.select(pair1)
    pair3 = cmds.duplicate()
    cmds.rotate(120,rotateZ=True)
        
    cmds.select(pair1)
    cmds.select(pair2,add=True)
    cmds.select(pair3,add=True)
    
    hubIndents = cmds.polyUnite(ch=False)
    cmds.move(wheelRadius, moveY=True)
   
    cmds.select(hub)
    cmds.select(hubIndents, add=True)
    indentedHub = cmds.polyCBoolOp(op=2)
    holePairs = []
   
    for i in range(-1,2,2):
        hole = cmds.polyCylinder(r=0.25, h=3, sz=1)
        cmds.rotate(90, rotateX=True)
        cmds.move(0,moveZ=True)
        cmds.move((i*0.8), moveX=True, a=True)
        holePairs.append(hole)
    
    cmds.select(clear=True)
    for pair in holePairs:
        cmds.select(pair, add=True)
    holePair1 = cmds.polyUnite(ch=False)
    
    cmds.select(holePair1)
    holePair2 = cmds.duplicate()
    cmds.rotate(60,rotateZ=True)
    
    cmds.select(holePair1)
    holePair3 = cmds.duplicate()
    cmds.rotate(120,rotateZ=True)
        
    cmds.select(holePair1)
    cmds.select(holePair2,add=True)
    cmds.select(holePair3,add=True)
    
    hubIndents = cmds.polyUnite(ch=False)
    cmds.move(wheelRadius, moveY=True)
   
    cmds.select(indentedHub)
    cmds.select(hubIndents, add=True)
    holedHub = cmds.polyCBoolOp(op=2)
    
    
    cyl = cmds.polyCylinder(r=0.3, h=2.2)
    cmds.move(0,moveZ=True)
    cmds.move((wheelRadius), moveY=True, a=True)
    cmds.rotate(90,rotateX=True)
    
    cmds.select(cyl)
    cmds.select(holedHub, add=True)
    hub = cmds.polyCBoolOp(op=1)
    
    
    axelHole = cmds.polyCube(h = 0.19, w=2.5, d=0.19)
    
    cmds.move(wheelRadius, moveY=True, a=True)
   
    
    holeName = cmds.ls(axelHole)[0]
    
    cmds.select(holeName+".f[0]")
    cmds.select(holeName+".f[1]", add=True)
    cmds.select(holeName+".f[2]", add=True)
    cmds.select(holeName+".f[3]", add=True)
        
    cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
    cmds.select(axelHole)
    cmds.polyBevel(sg=2, oaf=True, fn=True)
    cmds.rotate(90, rotateY=True)
    cmds.select(hub)
    cmds.select(axelHole,add=True)
    finalHub = cmds.polyCBoolOp(op=2, n="Hub" + str(rnd.randint(1000,9999)))
    
    
    applyMaterial(finalHub, rgb)
    cmds.delete(ch=True)


def axel():
    axelHeight = 1
    axelWidth = 1
    axelLength = cmds.intSliderGrp('axelLength', q=True, v=True)
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    
    axelRadius = 0.48 #0.18 base middle, then extrusions 0.15 each side, slightly smaller than
    
    axelSizeX = axelWidth * 0.8
    axelSizeY = axelHeight * 0.32
    axelSizeZ = axelLength * 0.8
    
  
    if(axelLength == 2):
        axel = cmds.polyCube(h = 0.18, w=axelSizeZ, d=0.18)
        
        cmds.move((axelRadius/2.0), moveY=True, a=True)
        axelName = cmds.ls(axel)[0]
        
        cmds.select(axelName+".f[0]")
        cmds.select(axelName+".f[1]", add=True)
        cmds.select(axelName+".f[2]", add=True)
        cmds.select(axelName+".f[3]", add=True)
            
        cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
        cmds.select(axel)
        cmds.polyBevel(sg=2, oaf=True, fn=True)
        cmds.rotate(90, rotateY=True)
        
        #booleans for grooves
        groove1 = cmds.polyPipe(r=0.25, h=0.25,thickness=0.06)
        groove2 = cmds.polyPipe(r=0.25, h=0.25,thickness=0.06)
        cmds.select(groove1)
        cmds.select(groove2,add=True)
        cmds.rotate(90,rotateX=True)
        cmds.move((axelRadius/2.0), moveY=True)
        
        cmds.select(groove1)
        cmds.move(((axelSizeZ/2.0)-0.3), moveZ=True, r=True)
        cmds.select(groove2)
        cmds.move(((-axelSizeZ/2.0)+0.3), moveZ=True, r=True)
        
        cmds.select(axel)
        cmds.select(groove1, add=True)
        cmds.select(groove2, add=True)
        
        axel = cmds.polyCBoolOp(op=2, ch=True, n="Axel" + str(rnd.randint(1000,9999)))
        
        
    if(axelLength > 2):
        axel = cmds.polyCube(h = 0.19, w=axelSizeZ, d=0.19, n="Axel" + str(rnd.randint(1000,9999)))
        
        cmds.move((axelSizeY/2.0), moveY=True, a=True)
       
        
        axelName = cmds.ls(axel)[0]
        
        cmds.select(axelName+".f[0]")
        cmds.select(axelName+".f[1]", add=True)
        cmds.select(axelName+".f[2]", add=True)
        cmds.select(axelName+".f[3]", add=True)
            
        cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
        cmds.select(axel)
        cmds.polyBevel(sg=2, oaf=True, fn=True)
        cmds.rotate(90, rotateY=True)
        
    applyMaterial(axel, rgb)
    cmds.delete(ch=True)
        
   
def connector():
    connectorLength = cmds.intSliderGrp('connectorLength', q=True, v=True)

    connectorSizeX = (1 * 0.8) - 0.1
    connectorSizeY = (1 * 0.8) - 0.1
    connectorSizeZ = (connectorLength * 0.4)
    
    rgb = cmds.colorSliderGrp('blockColour', q=True, rgbValue=True)
    
    connector = cmds.polyCylinder(r=(connectorSizeX/2.0),h=connectorSizeZ, sh=6)
    cmds.rotate(90,rotateX=True)
    
    cmds.move((connectorSizeY/2.0), moveY=True, a=True)
    connectorName = cmds.ls(connector)[0]
    
    
    cmds.select(connectorName+".e[40:99]")
    cmds.scale(0.8, 0.8, 0.8, relative=True)
    
    cmds.select(connectorName+".e[40:59]")
    cmds.move(-0.13, moveZ=True,r=True)
    cmds.select(connectorName+".e[80:99]")
    cmds.move(0.13, moveZ=True,r=True)
   
    
    axelShape = cmds.polyCube(h = 0.19, w=(connectorSizeZ+0.2), d=0.19)
    
    cmds.move((connectorSizeY/2.0), moveY=True, a=True)
    
    
    axelName = cmds.ls(axelShape)[0]
    
    cmds.select(axelName+".f[0]")
    cmds.select(axelName+".f[1]", add=True)
    cmds.select(axelName+".f[2]", add=True)
    cmds.select(axelName+".f[3]", add=True)
        
    cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
    cmds.select(axelShape)
    cmds.polyBevel(sg=2, oaf=True, fn=True)
    cmds.rotate(90, rotateY=True)
    
    
    if(connectorLength == 2):
        cmds.select(connectorName+".e[242]")
        cmds.select(connectorName+".e[246]", add=True)
        cmds.move(-0.05, moveY=True, relative=True)
        
        cmds.select(connectorName+".e[252]")
        cmds.select(connectorName+".e[256]", add=True)
        cmds.move(0.05, moveY=True, relative=True)
    
    cmds.select(connector)
    cmds.select(axelShape, add=True)
    connector = cmds.polyCBoolOp(op=2, ch=False, n="Connector" + str(rnd.randint(1000,9999)))
    
    applyMaterial(connector, rgb)
    cmds.delete(ch=True)

   
    
      
############### Repeatable functions      

# Creates bumps on top of lego blocks
def createBumps(blockWidth, blockDepth, blockSizeX, blockSizeY, blockSizeZ, offsetX, offsetY, offsetZ):
    bumpArray = []
    for i in range(blockWidth):
        for j in range(blockDepth):
            bump = cmds.polyCylinder(r=0.25, h=0.20)
            cmds.move((blockSizeY + 0.10), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeX/2.0) + 0.4), moveX=True, a=True)
            cmds.move(((j * 0.8) - (blockSizeZ/2.0) + 0.4), moveZ=True, a=True)
            bumpArray.append(bump)
            
    for bump in bumpArray:
        cmds.select(bump, add=True)
    bumps = cmds.polyUnite(ch=False)
    return bumps
    
# Creates rounded ends for beams
def createRoundedBeams(block, blockSizeX, blockSizeY, blockSizeZ):
    
    endCyl1 = cmds.polyCylinder(r=(blockSizeY/2.0), h=blockSizeX)
    cmds.rotate(90, rotateX=True)
    cmds.rotate(90, rotateY=True)
    cmds.move((blockSizeY/2.0), moveY=True)
    cmds.move((blockSizeZ/2.0), moveZ=True, a=True)
    
    endCyl2= cmds.polyCylinder(r=(blockSizeY/2.0), h=blockSizeX)
    cmds.rotate(90, rotateX=True)
    cmds.rotate(90, rotateY=True)
    cmds.move((blockSizeY/2.0), moveY=True)
    cmds.move((-blockSizeZ/2.0), moveZ=True, a=True)
    
    
    cmds.select(block)
    cmds.select(endCyl1, add=True)
    cmds.select(endCyl2, add=True)
    
    #combine cylindrical ends with rectangle using union boolean
        #joins them but removes intersecting parts
    roundedBlock = cmds.polyCBoolOp(op=1,ch=False)
    return roundedBlock
    
    
# Creates hourglass shaped indents on technic beams    
def createBeamIndents(block, blockDepth, blockSizeX, blockSizeY, blockSizeZ):
    beam = block
    indentArray = []
    for i in range(blockDepth):
        #h = 0.6 (same as outer holes), 
        #w = 0.15 (estimate for space between),
        #d = 0.35 (estimate based on image)
        indent = cmds.polyCube(h=0.6, w=0.15, d=0.35, sy=3)
        cmds.move((blockSizeX/2.0), moveX = True, a  = True)
        cmds.move((blockSizeY/2.0), moveY = True, a = True)
        cmds.move(((i  * 0.8) - (blockSizeZ/2.0)+0.65), moveZ = True)        
       
        indentName = cmds.ls(indent)[0]
        cmds.select(indentName+'.vtx[2:5]')
        cmds.move(0, 0, -0.1, r=True)
        cmds.select(indentName+'.vtx[10:13]')
        cmds.move(0, 0, 0.1, r=True)
        indentArray.append(indent)
        
        indent = cmds.polyCube(h=0.6, w=0.15, d=0.4, sy=3)
        cmds.move((-1*(blockSizeX/2.0)), moveX = True, a  = True)
        cmds.move((blockSizeY/2.0), moveY = True, a = True)
        cmds.move(((i  * 0.8) - (blockSizeZ/2.0)+0.65), moveZ = True)        
       
        indentName = cmds.ls(indent)[0]
        cmds.select(indentName+'.vtx[2:5]')
        cmds.move(0, 0, -0.1, r=True)
        cmds.select(indentName+'.vtx[10:13]')
        cmds.move(0, 0, 0.1, r=True)
        indentArray.append(indent)
        
    cmds.select(clear=True)
    
    #combine hourglass shaped indents into one polygon
    for indent in indentArray:
        cmds.select(indent, add=True)
    indents = cmds.polyUnite(ch=False)
    
    cmds.select(clear=True)
    cmds.select(beam)
    cmds.select(indents, add=True)
    finalBlock = cmds.polyCBoolOp(op=2, ch=False)
    return finalBlock


#######Punches holes in side of block
def createHoles(block, blockDepth, blockSizeX, blockSizeY, blockSizeZ, axelHoles, holeOffset, holeOffsetZ):
    beam = block
    
    #Holes are offset on reg blocks (in between bumps)
    if(holeOffset == True):
        holeArray = []
        for i in range(blockDepth-1):
            #outer, larger radius, slight indent
            hole = cmds.polyCylinder(r=0.3, h=0.1, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
            cmds.move(((blockSizeY/2.0) + 0.1), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0)+ holeOffsetZ), moveZ=True, a=True)
            cmds.move((blockSizeX/2.0), moveX = True, a = True)
            holeArray.append(hole)
            
            #same as above, other side of block
            hole = cmds.polyCylinder(r=0.3, h=0.1, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
            cmds.move(((blockSizeY/2.0) +0.1), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0)+ holeOffsetZ), moveZ=True, a=True)
            cmds.move((-1*(blockSizeX/2.0)), moveX = True, a = True)
            holeArray.append(hole)
            
            
            #smaller radius, full way through block
            hole = cmds.polyCylinder(r=0.25, h=blockSizeX, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
        
            cmds.move(((blockSizeY/2.0) + 0.1), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0) + holeOffsetZ), moveZ=True, a=True)
            holeArray.append(hole)
                
        cmds.select(beam)
        for hole in holeArray:
            cmds.select(hole, add=True)
        
        finalBlock = cmds.polyCBoolOp(op=2)
        
    #Holes on rounded beams are not offset, are flush with rounded ends
    else:
        #if no axel holes
        if(axelHoles == 0):
            start = 0
            end = 1
        if(axelHoles ==1):
            start = 1
            end = 1
        if(axelHoles ==2):
            start = 1
            end = 0
            
        holeArray = []
        for i in range(start, blockDepth+end):
            #outer, larger radius, slight indent
            hole = cmds.polyCylinder(r=0.3, h=0.1, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0)+ holeOffsetZ), moveZ=True, a=True)
            cmds.move((blockSizeX/2.0), moveX = True, a = True)
            holeArray.append(hole)
            
            #same as above, other side of block
            hole = cmds.polyCylinder(r=0.3, h=0.1, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0)+ holeOffsetZ), moveZ=True, a=True)
            cmds.move((-1*(blockSizeX/2.0)), moveX = True, a = True)
            holeArray.append(hole)
            
            #smaller radius, full way through block
            hole = cmds.polyCylinder(r=0.25, h=blockSizeX, sz=1)
            cmds.rotate(90, rotateX=True)
            cmds.rotate(90, rotateY=True)
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            cmds.move(((i * 0.8) - (blockSizeZ/2.0)+ holeOffsetZ), moveZ=True, a=True)
            holeArray.append(hole)
            
            
        if(axelHoles == 1):
            cmds.select(clear=True)
            #each part of axel shape - 0.19
            #each oart comes out 0.15 
            #total axle diameter = 0.48, axle hole diam = 0.49
            hole = cmds.polyCube(h = 0.19, w=2, d=0.19)
            
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            
            cmds.move((((-blockSizeZ)/2.0)+ holeOffsetZ), moveZ=True, a=True)
            holeName = cmds.ls(hole)[0]
            
            cmds.select(holeName+".f[0]")
            cmds.select(holeName+".f[1]", add=True)
            cmds.select(holeName+".f[2]", add=True)
            cmds.select(holeName+".f[3]", add=True)
                
            cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
            cmds.select(hole)
            cmds.polyBevel(sg=2, oaf=True, fn=True)
            holeArray.append(hole)
            
        if(axelHoles == 2):
            cmds.select(clear=True)
           
            hole = cmds.polyCube(h = 0.19, w=2, d=0.19)
            
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            
            cmds.move((((-blockSizeZ)/2.0)+ holeOffsetZ), moveZ=True, a=True)
            holeName = cmds.ls(hole)[0]
            
            cmds.select(holeName+".f[0]")
            cmds.select(holeName+".f[1]", add=True)
            cmds.select(holeName+".f[2]", add=True)
            cmds.select(holeName+".f[3]", add=True)
                
            cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
            cmds.select(hole)
            cmds.polyBevel(sg=2, oaf=True, fn=True)
            holeArray.append(hole)
            cmds.select(clear=True)
           
            hole = cmds.polyCube(h = 0.19, w=2, d=0.19)
            
            cmds.move((blockSizeY/2.0), moveY=True, a=True)
            
            cmds.move((((blockSizeZ)/2.0)- holeOffsetZ), moveZ=True, a=True)
            holeName = cmds.ls(hole)[0]
            
            cmds.select(holeName+".f[0]")
            cmds.select(holeName+".f[1]", add=True)
            cmds.select(holeName+".f[2]", add=True)
            cmds.select(holeName+".f[3]", add=True)
                
            cmds.polyExtrudeFacet(lt=(0,0,0.15), kft=False)
            cmds.select(hole)
            cmds.polyBevel(sg=2, oaf=True, fn=True)
            holeArray.append(hole)
            
             
        cmds.select(beam)
        for hole in holeArray:
            cmds.select(hole, add=True)
            
        #punch holes through rounded block 
        finalBlock = cmds.polyCBoolOp(op=2, ch=False, n="Block" + str(rnd.randint(1000,9999)))
        
    return finalBlock

def applyMaterial(object, selectedColor):
    
    colorMatte = cmds.radioButton('matte', query=True, select=True )
    colorShiny = cmds.radioButton('shiny', query=True, select=True)
    
    hubMatte = cmds.radioButton('hubMatte', query=True, select=True )
    hubShiny = cmds.radioButton('hubShiny', query=True, select=True)
    
    rgb = selectedColor
    
    if(colorMatte == True) or (hubMatte == True):
        myShader = cmds.shadingNode( 'blinn', asShader=True )
        cmds.setAttr( myShader+".color", rgb[0], rgb[1], rgb[2], type='double3')
        cmds.setAttr( myShader+".eccentricity", 0.44)
        cmds.select(object)
        cmds.hyperShade(assign = myShader)
    if(colorShiny == True) or (hubShiny == True):
        myShader = cmds.shadingNode( 'blinn', asShader=True )
        cmds.setAttr( myShader+".color", rgb[0], rgb[1], rgb[2], type='double3')
        cmds.setAttr( myShader+".eccentricity", 0.05)
        cmds.select(object)
        cmds.hyperShade(assign = myShader)


    
    
if 'myGUI' in globals():
    if cmds.window(myGUI, exists=True):
        cmds.deleteUI(myGUI, window=True)
    
myGUI = cmds.window(title="Lego Block", menuBar = True, width=455)

cmds.menu(label="Basic Options")
cmds.menuItem(label="New Scene", command=('cmds.file(new=True, force=True)'))
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'))

cmds.columnLayout()

cmds.scrollLayout(verticalScrollBarThickness=14, height=500, width=450)

cmds.frameLayout(label="Piece Colour")
cmds.columnLayout()
cmds.colorSliderGrp('blockColour', label="Colour", hsv=(10, 1, 0))

cmds.rowLayout( numberOfColumns=2, columnWidth2=(150, 80), columnAttach=[(1, 'left', 100), (2, 'left', 0)] )

cmds.radioCollection()
cmds.radioButton('matte', label='Shiny', select=True )
cmds.radioButton('shiny', label='Matte')
cmds.setParent('..')


#GUI for Square Blocks No Holes
cmds.frameLayout(collapsable=True, label="Square Blocks, No Holes")
cmds.columnLayout()

cmds.intSliderGrp('sqBlockHeight', l="Height", f=True, min=1, max=20, value=3)
cmds.intSliderGrp('sqBlockWidth', l="Width (Bumps)", f=True, min=1, max=20, value=2)
cmds.intSliderGrp('sqBlockDepth', l="Depth (Bumps)", f=True, min=1, max=20, value=8)

cmds.setParent('..')
cmds.button(label="Create Square Block", command=('squareBlocksNoHoles()'))
cmds.setParent('..')

#GUI for Square Blocks With Holes
cmds.frameLayout(collapsable=True, label="Square Blocks, With Holes")
cmds.columnLayout()

cmds.intSliderGrp('sqHolesBlockDepth', l="Depth (Bumps)", f=True, min=1, max=20, value=8)


cmds.setParent('..')
cmds.button(label="Create Square Block with Holes", command=('squareBlocksHoles()'))
cmds.setParent('..')

#GUI for Technic Beams, Straight
cmds.frameLayout(collapsable=True, label="Technic Beams, Straight")
cmds.columnLayout()

cmds.intSliderGrp('technicStraightBeamDepth', label = "Length", field = True, min = 1, max = 20, value = 2)

cmds.rowLayout( numberOfColumns=1,columnWidth1=100,columnAttach=[(1, 'left', 50)])
cmds.text( label='Axel Holes:', align='center')
cmds.setParent('..')

cmds.rowLayout( numberOfColumns=3, columnWidth3=(150, 80, 80), columnAttach=[(1, 'left', 100), (2, 'left', 0), (3, 'left', 0)] )

cmds.radioCollection()
cmds.radioButton('noAxels', label='None', select=True )
cmds.radioButton('bothAxels', label='Both ends' )
cmds.radioButton('oneAxel', label='One end' )
cmds.setParent('..')


cmds.setParent('..')
cmds.button(label = "Create Straight Technic Beam", command = 'technicBeamsStraight()')
cmds.setParent('..')


#GUI For Technic Beams, Angled
cmds.frameLayout(collapsable=True, label="Technic Beams, Angled")
cmds.columnLayout()


cmds.intSliderGrp('technicAngledBeam1Depth', l="Length (Before Bend)", f=True, min=2, max=20, value=4)
cmds.intSliderGrp('technicAngledBeam2Depth', l="Length (After Bend)", f=True, min=2, max=20, value=8)
cmds.optionMenuGrp('technicBeamAngle', l='Angle')
cmds.menuItem( label='53.5' )
cmds.menuItem( label='90' )


cmds.rowLayout( numberOfColumns=1,columnWidth1=100,columnAttach=[(1, 'left', 50)])
cmds.text( label='Axel Holes:', align='center')
cmds.setParent('..')

cmds.rowLayout( numberOfColumns=3, columnWidth3=(150, 80, 80), columnAttach=[(1, 'left', 100), (2, 'left', 0), (3, 'left', 0)] )

cmds.radioCollection()
cmds.radioButton('noAxels', label='None', select=True )
cmds.radioButton('bothAxels', label='Both ends' )
cmds.radioButton('oneAxel', label='One end' )
cmds.setParent('..')


cmds.setParent('..')
cmds.button(label = "Create Angled Technic Beam", command = 'technicBeamsAngled()')
cmds.setParent('..')


#GUI For Wheel

cmds.frameLayout( collapsable=True, label = "Wheels", width=392)
cmds.columnLayout()
cmds.colorSliderGrp('hubColor', label="Hub Color", hsv=(10, 1, 0))

cmds.rowLayout( numberOfColumns=2, columnWidth2=(150, 80), columnAttach=[(1, 'left', 100), (2, 'left', 0)] )

cmds.radioCollection()
cmds.radioButton('hubMatte', label='Shiny', select=True )
cmds.radioButton('hubShiny', label='Matte')
cmds.setParent('..')
cmds.button(label="Create Wheel", command=('wheel()'))
cmds.setParent('..')


#GUI For Axel 

cmds.frameLayout( collapsable=True, label = "Create Axel")
cmds.columnLayout()
cmds.intSliderGrp('axelLength', l="Axel Length", f=True, min=2, max=12, value=2)

cmds.setParent('..')    
cmds.button(label="Create Axel", command=('axel()'))
cmds.setParent('..')


#GUI for Connector
cmds.frameLayout( collapsable=True, label = "Create Connector")
cmds.columnLayout()
cmds.intSliderGrp('connectorLength', l="Connector Length", f=True, min=1, max=2, value=1)

cmds.setParent('..')
cmds.button(label="Create Connector", command=('connector()'))
cmds.setParent('..')



cmds.showWindow(myGUI)
