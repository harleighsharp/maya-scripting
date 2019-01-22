import maya.cmds as cmds
import math

if cmds.window(GUIWindow, exists=True):
    cmds.deleteUI(GUIWindow, window=True)


GUIWindow = cmds.window("My GUI Window", menuBar=True, widthHeight=(400,500))

ZV = 0.000000000000000000001

def findIntersect() : 
    selectedShapes = cmds.ls(selection=True)
    selectedCount = 0
    transformNodeList = []
    meshNodeList = []
    
    for shape in selectedShapes:
        if(cmds.objectType(shape) == 'transform'):
            transformNodeList.append(shape)
            childShape = cmds.listRelatives(shape, fullPath=True,shapes=True)
            if(cmds.objectType(childShape) == 'mesh'):
                if(selectedCount < 2):
                    meshNodeList.append(childShape)
                else:
                    print "Select 2 shapes."
                selectedCount+=1
    if(selectedCount < 2):
        print "Not enough shapes selected. Select 2 shapes."
        return False
    
    numIntersectPts = 0
    referenceObject = selectedShapes[0]
    referenceObjectMesh = meshNodeList[0]
    referenceObjectTransform = transformNodeList[0]
    
    sphereCentre = cmds.xform(referenceObject, query=True, translation=True, worldSpace=True)
    sphereFaceCount = cmds.polyEvaluate(referenceObject, face=True)
   
    sphereCentre = list([sphereCentre[0],sphereCentre[1],sphereCentre[2], 1.0])
    
    sphereMeshXNode = cmds.listRelatives(referenceObjectMesh, parent=True)
    sphereMeshXForm = cmds.xform(sphereMeshXNode, query=True, matrix=True, worldSpace=True)
    sphereLineEndPts = []
    for face in range(0, sphereFaceCount):
        vtxLst = cmds.polyInfo((referenceObjectMesh[0] + ".f[" + str(face) + "]"), faceToVertex=True)
        vtxIdx = str(vtxLst[0]).split()
        vtxA = cmds.getAttr(referenceObjectMesh[0] + ".vt[" + vtxIdx[2] + "]")
        vtxB = cmds.getAttr(referenceObjectMesh[0] + ".vt[" + vtxIdx[3] + "]")
        vtxC = cmds.getAttr(referenceObjectMesh[0] + ".vt[" + vtxIdx[4] + "]")
        
        
        vtxNewA = matrixMult(sphereMeshXForm, list(vtxA[0]))
        vtxNewB = matrixMult(sphereMeshXForm, list(vtxB[0]))
        vtxNewC = matrixMult(sphereMeshXForm, list(vtxC[0]))
        
        #since more faces then verts, some are repeated - below ensures no duplicate lines drawn
        if vtxNewA not in sphereLineEndPts:
            sphereLineEndPts.append(vtxNewA)
        if vtxNewB not in sphereLineEndPts:
            sphereLineEndPts.append(vtxNewB)
        if vtxNewC not in sphereLineEndPts:
            sphereLineEndPts.append(vtxNewC)
            
    #draw lines from sphereCentre to vertex pts
    for pt in sphereLineEndPts:
        cmds.curve(p=[(pt[0],pt[1],pt[2]),(sphereCentre[0],sphereCentre[1],sphereCentre[2])])
        
              
    cubeFaceCount = cmds.polyEvaluate(meshNodeList[1], face=True)
    cubeMesh = meshNodeList[1]
    cubeMeshXNode = cmds.listRelatives(cubeMesh, parent=True)
    cubeMeshXForm = cmds.xform(cubeMeshXNode, query=True, matrix=True, worldSpace=True) 
    
    for face in range(0, cubeFaceCount):
        vtxLst = cmds.polyInfo((cubeMesh[0] + ".f[" + str(face) + "]"), faceToVertex=True)
        vtxIdx = str(vtxLst[0]).split()
        vtxA = cmds.getAttr(cubeMesh[0] + ".vt[" + vtxIdx[2] + "]")
        vtxB = cmds.getAttr(cubeMesh[0] + ".vt[" + vtxIdx[3] + "]")
        vtxC = cmds.getAttr(cubeMesh[0] + ".vt[" + vtxIdx[4] + "]")
        vtxD = cmds.getAttr(cubeMesh[0] + ".vt[" + vtxIdx[5] + "]")
        
        
        vtxNewA = matrixMult(cubeMeshXForm, list(vtxA[0]))
        vtxNewB = matrixMult(cubeMeshXForm, list(vtxB[0]))
        vtxNewC = matrixMult(cubeMeshXForm, list(vtxC[0]))
        vtxNewD = matrixMult(cubeMeshXForm, list(vtxD[0]))
        
        planeEq = getPlaneEq(vtxNewA, vtxNewB, vtxNewC)
        for pt in sphereLineEndPts:
            
            #if pt is on either side of the plane
            scalarA = (planeEq[0]*sphereCentre[0])+(planeEq[1]*sphereCentre[1])+(planeEq[2]*sphereCentre[2])+planeEq[3]
            scalarB = (planeEq[0]*pt[0])+(planeEq[1]*pt[1])+(planeEq[2]*pt[2])+planeEq[3]
            
            if(((scalarA > 0.0) and (scalarB < 0.0)) or ((scalarA < 0.0) and (scalarB > 0.0))):
                tValue = tValueCalc(planeEq, sphereCentre, pt)
                PtI = [0.0, 0.0, 0.0]
                PtI[0] = sphereCentre[0] + (tValue * (pt[0] - sphereCentre[0]))
                PtI[1] = sphereCentre[1] + (tValue * (pt[1] - sphereCentre[1]))
                PtI[2] = sphereCentre[2] + (tValue * (pt[2] - sphereCentre[2]))
                
              
                
                vectorA = vectorFromPts(vtxNewA, vtxNewB)
                vectorB = vectorFromPts(vtxNewA, vtxNewC)
                facetArea = areaFacetCalc(vectorA, vectorB)
                
                if(pointOnFacet(vtxNewA, vtxNewB, vtxNewC, vtxNewD, facetArea, PtI) == True):
                    numIntersectPts+=1
                    cmds.polyCube(h=0.1,w=0.1,d=0.1)
                    cmds.move(PtI[0], PtI[1], PtI[2])
                    distanceIntersectToVert = distancePtToPt(PtI,pt)
                    
                    #angle between line and xz plane - vector for xz plane can be any without y coord
                    lineVector = vectorFromPts(sphereCentre, pt)
                    gridVector = [1, 0, 1]
                    angleLineGrid = angleBetweenVectors(lineVector, gridVector)
                    
                    
                    ptText = "Intersection Point [" + str(numIntersectPts) + "] " + str(round(PtI[0],2)) + ", " + str(round(PtI[1],2)) + ", " + str(round(PtI[2],2))
                    linePtText = "-- Intersecting Line: Point A: " + str(sphereCentre) + ", Point B: " + str(pt)
                    areaFacetText = "-- Area of Intersecting Facet: " + str(facetArea)
                    distanceIntersectToVertText = "-- Distance from Intersecting Point to Sphere Vertex: " + str(distanceIntersectToVert)
                    angleLineGridText = "-- Angle Between Line and Grid: " + str(angleLineGrid) + " radians"
                    
                    cmds.textScrollList('intersectionPointList', edit=True, append=[ptText])
                    cmds.textScrollList('intersectionPointList', edit=True, append=[linePtText])
                    cmds.textScrollList('intersectionPointList', edit=True, append=[areaFacetText])
                    cmds.textScrollList('intersectionPointList', edit=True, append=[distanceIntersectToVertText])
                    cmds.textScrollList('intersectionPointList', edit=True, append=[angleLineGridText])

def pointOnFacet(vertexA, vertexB, vertexC, vertexD, facetArea, intersectPt):
    
   #is the point within the area of the facet (facet made up of 4 triangles)
    vector1 = vectorFromPts(vertexA, vertexB)
    vector2 = vectorFromPts(vertexB, vertexC)
    vector3 = vectorFromPts(vertexC, vertexD)
    vector4 = vectorFromPts(vertexD, vertexA)
    vectorAintersectPt = vectorFromPts(vertexA, intersectPt)
    vectorBintersectPt = vectorFromPts(vertexB, intersectPt)
    vectorCintersectPt = vectorFromPts(vertexC, intersectPt)
    vectorDintersectPt = vectorFromPts(vertexD, intersectPt)
    
    triangle1 = areaTriangleCalc(vector1, vectorBintersectPt)
    triangle2 = areaTriangleCalc(vector2, vectorCintersectPt)
    triangle3 = areaTriangleCalc(vector3, vectorDintersectPt)
    triangle4 = areaTriangleCalc(vector4, vectorAintersectPt)

    
    sumTriAreas = (triangle1+triangle2+triangle3+triangle4)
    #rounding because there are slightly differences in decimal places
    if(round(sumTriAreas,2) == round(facetArea, 2)):
        return True
    else:
        return False
    
    
def vectorFromPts(vertexA, vertexB):
    vec = [0.0, 0.0, 0.0]
    vec[0] = vertexB[0] - vertexA[0]
    vec[1] = vertexB[1] - vertexA[1]
    vec[2] = vertexB[2] - vertexA[2]
    return vec

def getPlaneEq(vertexA, vertexB, vertexC):
    #cross product can act like normal vec
    normalVec = normalVectorCalc(vertexA, vertexB, vertexC)
    #use normal vector and one vertex on plane to find D from Ax + By + Cz + D = 0
    A = normalVec[0]
    B = normalVec[1]
    C = normalVec[2]
    planeEq = [0.0, 0.0, 0.0, 0.0]
    planeEq[0] = A
    planeEq[1] = B
    planeEq[2] = C
    planeEq[3] = (A * vertexA[0]) + (B * vertexA[1]) + (C * vertexA[2])
    planeEq[3] = -(planeEq[3])

    # Check if they are colinear
    if((abs(planeEq[0]) < ZV) and (abs(planeEq[1]) < ZV) and (abs(planeEq[2]) < ZV)):
        print("Points are colinear")
        return False
    return planeEq
    
    
def tValueCalc(planeEq, pointA, pointB):
    denominator = 0.0
    numerator = 0.0
    denominator=(planeEq[0]*(pointA[0]-pointB[0]))+(planeEq[1]*(pointA[1]-pointB[1]))+(planeEq[2]*(pointA[2]-pointB[2]))
    if(abs(denominator) < ZV):
        print "Denominator is Zero"
        return False
    numerator = (planeEq[0] * pointA[0]) + (planeEq[1] * pointA[1]) + (planeEq[2] * pointA[2]) + planeEq[3]
    return(numerator/denominator)



def normalVectorCalc(vertexA, vertexB, vertexC):
    #convert to vectors in construction order
    vectorA = vectorFromPts(vertexA, vertexB) #to get A-B
    vectorB = vectorFromPts(vertexA, vertexC) #to get A-C
    perpindicularVec = crossProductCalc(vectorA, vectorB)
    mag = magnitudeCalc(perpindicularVec)
    n = [(perpindicularVec[0] / mag),(perpindicularVec[1] / mag),(perpindicularVec[2] / mag)]
    return n
    
    
    
def dotProductCalc(vectorA, vectorB):
    dotProd = (vectorA[0]*vectorB[0])+(vectorA[1]*vectorB[1])+(vectorA[2]*vectorB[2])
    return dotProd
        
        
def crossProductCalc(vectorA, vectorB):
    crossProd = [((vectorA[1] * vectorB[2]) - (vectorA[2] * vectorB[1])), ((vectorA[2] * vectorB[0]) - (vectorA[0] * vectorB[2])), ((vectorA[0] * vectorB[1]) - (vectorA[1] * vectorB[0]))]
    return crossProd
    
    
def magnitudeCalc(vector):
    vectorXsqrd = math.pow(vector[0], 2.0)
    vectorYsqrd = math.pow(vector[1], 2.0)
    vectorZsqrd = math.pow(vector[2], 2.0)
    m = math.sqrt(vectorXsqrd+vectorYsqrd+vectorZsqrd)
    return m

def areaTriangleCalc(vectorA, vectorB):
    crossProd = crossProductCalc(vectorA, vectorB)
    magnitude = magnitudeCalc(crossProd)
    #tri is half parallellogram
    areaTri = magnitude / 2.0 
    return areaTri
    
def areaFacetCalc(vectorA, vectorB):
    #area parallellogram: ||a x b || = ||A||||B||sinTHETA
    magnitudeA = magnitudeCalc(vectorA)
    magnitudeB = magnitudeCalc(vectorB)
    prodMagnitudes = (magnitudeA*magnitudeB)
    theta = angleBetweenVectors(vectorA, vectorB)
    area = (prodMagnitudes*math.sin(theta))
    return area


def angleBetweenVectors(vectorA, vectorB):
    
    dotProd = dotProductCalc(vectorA, vectorB)
    magnitudeA = magnitudeCalc(vectorA)
    magnitudeB = magnitudeCalc(vectorB)
    prodMagnitudes = (magnitudeA*magnitudeB)
    theta = math.acos(dotProd/prodMagnitudes)
    return theta
    
    
def distancePtToPt(pointA, pointB):
    #magnitude is distance btwn pts
    vector = [pointA[0]-pointB[0],pointA[1]-pointB[1],pointA[2]-pointB[2]]
    magnitude = magnitudeCalc(vector)
    return magnitude
    
def matrixMult(Mtx, inputPt):
    outputPt = [0.0, 0.0, 0.0, 0.0]
    inputPt = [inputPt[0],inputPt[1],inputPt[2],1.0]
    outputPt[0] =(Mtx[0]*inputPt[0])+(Mtx[4]*inputPt[1])+(Mtx[8]*inputPt[2])+(Mtx[12]*inputPt[3])
    outputPt[1] =(Mtx[1]*inputPt[0])+(Mtx[5]*inputPt[1])+(Mtx[9]*inputPt[2])+(Mtx[13]*inputPt[3])
    outputPt[2] =(Mtx[2]*inputPt[0])+(Mtx[6]*inputPt[1])+(Mtx[10]*inputPt[2])+(Mtx[14]*inputPt[3])
    outputPt[3] =(Mtx[3]*inputPt[0])+(Mtx[7]*inputPt[1])+(Mtx[11]*inputPt[2])+(Mtx[15]*inputPt[3])
    return(outputPt)  


cmds.columnLayout( columnAttach=('left',5), rowSpacing=10, columnWidth=400)
cmds.button( label='Find Intersection', command='findIntersect()')
cmds.setParent('..')
cmds.paneLayout()
cmds.textScrollList('intersectionPointList', numberOfRows=10, allowMultiSelection=False, height = 300)

cmds.showWindow(GUIWindow)  