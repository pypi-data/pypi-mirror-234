import cv2
import os
import numpy as np
import copy
# from bin import pdfminer_testing as pdfmin
from collections import defaultdict
from collections import OrderedDict
from itertools import groupby
from . import utils
from . import constants as cns
from . import pdfExtractionUtils as pdfutil
import lxml.html
import re
from datetime import datetime
import math
import traceback

def getLSgmt(edges,minLsLen,type='H'):
    def iterativeMethod(edges,minLsLen,type):
        lstVLines=[]
        for idxListCell,listCell in enumerate(edges):
            if not any(listCell):
                #lstVlines.append([])
                continue
            lstLineSeg=[]
            start=0
            end=0
            for cellIdx,cellVal in enumerate(listCell):
                if cellVal and not start:
                    start=cellIdx
                if cellVal:
                    end=cellIdx
                if not cellVal and start:
                    if end-start>=minLsLen:
                        if type=='H':
                            lstLineSeg.append((start,idxListCell,end,idxListCell))
                        elif type=='V':
                            lstLineSeg.append((idxListCell,start,idxListCell,end))
                    start=0
                    end=0
            if lstLineSeg:
                lstVLines.append(lstLineSeg)
        return lstVLines
    
    def regexMethod(edges,minLsLen,type):
        def func(arr,static,minLsLen,type):
            lstLsStr=re.findall('(?:\d+(?:,|$))+',','.join([str(ix) if elm else 'False' for ix,elm in enumerate(arr)]))
            lstLs=[]
            for lsStr in lstLsStr:
                lsInt=list(map(int,re.sub(',$','',lsStr).split(',')))
                lsLow=lsInt[0]
                lsUp=lsInt[-1]
                if lsUp-lsLow<minLsLen:
                    continue
                if type=='H':
                    lstLs.append((lsLow,static,lsUp,static))
                elif type=='V':
                    lstLs.append((static,lsLow,static,lsUp))
            if lstLs:
                return lstLs
            
        # edgesFlt=copy.deepcopy(edges[np.apply_along_axis(any,1,edges)])

        return list(filter(None,[func(edges[ix],ix,minLsLen,type) for ix in range(edges.shape[0])]))

    res=iterativeMethod(edges,minLsLen,type)

    return res
    # return regexMethod(edges,minLsLen,type)

def captureInteractions(lstHLines,lstVLines):
    lstIntersections=[]
    for lstHLine in lstHLines:
        for hLSeg in lstHLine:
            xRange=(hLSeg[0],hLSeg[2])
            yStatic=hLSeg[1]
            for lstVLine in lstVLines:
                for vLSeg in lstVLine:
                    isXInRange,isYInRange=False,False
                    yRange=(vLSeg[1],vLSeg[3])
                    xStatic=vLSeg[0]
                    if xRange[0]<=xStatic<=xRange[1]:
                        isXInRange=True
                    if yRange[0]<=yStatic<=yRange[1]:
                        isYInRange=True
                    if isXInRange and isYInRange:
                        lstIntersections.append((xStatic,yStatic))
    return list(set(lstIntersections))
        
def getBBox(lstIntersections,lstHLines,lstVLines):
    diHLines={lst[0][1]:lst for lst in lstHLines}
    diVLines={lst[0][0]:lst for lst in lstVLines}
    lstIntersections=sorted(lstIntersections,key=lambda tup: (tup[1],tup[0]))
    diBbox={}
    for idx,pt in enumerate(lstIntersections[0:-1]):
        pt_right=sorted([p for p in lstIntersections if p[1]==pt[1] and p[0]>pt[0]],key=lambda tup: tup[0])
        pt_btm=sorted([p for p in lstIntersections if p[0]==pt[0] and p[1]>pt[1]],key=lambda tup: tup[0])
        if not pt_right or not pt_btm:
            continue
        for idx1,pt1 in enumerate(lstIntersections[idx+1:]):
            if pt1[0]==pt[0] or pt1[1]==pt[1]:
                continue
            if (pt1[0],pt[1]) in pt_right and (pt[0],pt1[1]) in pt_btm:
                pt1ToPtLsUp=(pt1[0],pt[1],pt1[0],pt1[1])
                pt1ToPtLsLeft=(pt[0],pt1[1],pt1[0],pt1[1])

                ptToPt1LsBtm=(pt[0],pt[1],pt[0],pt1[1])
                ptToPt1LsRight=(pt[0],pt[1],pt1[0],pt[1])

                if pt not in diBbox:
                    if not (
                        any([vLs for vLs in diVLines[pt1[0]] if 
                                 vLs[1]<=pt1ToPtLsUp[1]<pt1ToPtLsUp[3]<=vLs[3]]
                                 ) and 
                        any([hLs for hLs in diHLines[pt1[1]] if 
                                 hLs[0]<=pt1ToPtLsLeft[0]<pt1ToPtLsLeft[2]<=hLs[2]]
                                 )
                            ):
                        continue

                    if not (
                        any([vLs for vLs in diVLines[pt[0]] if 
                                 vLs[1]<=ptToPt1LsBtm[1]<ptToPt1LsBtm[3]<=vLs[3]]
                                 ) and 
                        any([hLs for hLs in diHLines[pt[1]] if 
                                 hLs[0]<=ptToPt1LsRight[0]<ptToPt1LsRight[2]<=hLs[2]]
                                 )
                            ):
                        continue
                    diBbox[pt]=pt1
    return diBbox
    


def debugLS(img,lstHLines,lstVLines,imgFNm,outDir=cns.debugTblPath,
            outFNm=cns.debugLsFNm,outFExt=cns.tblDebugExt):
    if not cns.debugTblImg:
        return
    img=copy.deepcopy(img)
    outPth,outPthPsx=utils.fpath_from_lst([outDir,imgFNm,f"{outFNm}.{outFExt}"],both=True)
    utils.makedr(outPth.parent)
    try:
        for lstHLine in lstHLines:
            for lSeg in lstHLine:
                cv2.line(img,(lSeg[0],lSeg[1]),(lSeg[2],lSeg[3]),(0,255,0),1)
        for lstVLine in lstVLines:
            for lSeg in lstVLine:
                cv2.line(img,(lSeg[0],lSeg[1]),(lSeg[2],lSeg[3]),(0,255,0),1)
    except:
        print('temp')
    cv2.imwrite(outPthPsx,img)

def convrtBbxtoLn(bbx):
    return ((bbx[0],bbx[1],bbx[2],bbx[1]), (bbx[0],bbx[3],bbx[2],bbx[3]),(bbx[0],bbx[1],bbx[0],bbx[3]),(bbx[2],bbx[1],bbx[2],bbx[3]))


def debugBboxAsRect(bbx,img,imgFNm):
    tupLn=convrtBbxtoLn(bbx)
    lstHLines=[[tupLn[0],tupLn[1]]]
    lstVLines=[[tupLn[2],tupLn[3]]]
    debugLS(img,lstHLines,lstVLines,imgFNm)


def debugPoints(img,lstPts,imgFNm,outDir=cns.debugTblPath,outFNm=cns.debugIsectPtsFNm,
                outFExt=cns.tblDebugExt,text=True):
    img=copy.deepcopy(img)
    if not cns.debugTblImg:
        return
    outPth,outPthPsx=utils.fpath_from_lst([outDir,imgFNm,f"{outFNm}.{outFExt}"],both=True)
    utils.makedr(outPth.parent)
    for pt in lstPts:
        if text:
            cv2.putText(img,"Pt{}".format(pt),pt,cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
        else:
            cv2.putText(img,".",pt,cv2.FONT_HERSHEY_SIMPLEX,0.07,(0,0,255),1)
        cv2.imwrite(outPthPsx,img)

def debugBbox(img,diBBox,imgFNm,outDir=cns.debugTblPath,outFNm=cns.debugPtsFNm,
                outFExt=cns.tblDebugExt,text=True,iter=False):
    if not cns.debugTblImg:
        return
    img=copy.deepcopy(img)
    outPth,outPthPsx=utils.fpath_from_lst([outDir,imgFNm,f"{outFNm}.{outFExt}"],both=True)
    utils.makedr(outPth.parent)
    for ul,lr in diBBox.items():
        if text:
            cv2.putText(img,"UL{}".format(str(ul)),ul,cv2.FONT_HERSHEY_SIMPLEX,0.3,(0,0,255),1)
            cv2.putText(img,"LR{}".format(str(lr)),lr,cv2.FONT_HERSHEY_SIMPLEX,0.3,(255,0,0),1)
            if iter:
                cv2.imwrite(outPthPsx,img)
        else:
            cv2.putText(img,".",ul,cv2.FONT_HERSHEY_SIMPLEX,0.07,(0,0,255),1)
            cv2.putText(img,".",lr,cv2.FONT_HERSHEY_SIMPLEX,0.07,(255,0,0),1)
    if not iter:
        cv2.imwrite(outPthPsx,img)

def debugImage(img,imgFNm,outDir=cns.debugTblPath,outFNm=cns.debugImgFNm,outFExt=cns.tblDebugExt):
    if not cns.debugTblImg:
        return
    img=copy.deepcopy(img)
    outPth,outPthPsx=utils.fpath_from_lst([outDir,imgFNm,f"{outFNm}.{outFExt}"],both=True)
    utils.makedr(outPth.parent)
    cv2.imwrite(outPthPsx,img)

def imgBboxToPdfBboxMult(diBBox,maxY):
    diPdfBbox={}
    for ul,lr in diBBox.items():
        k=ul+lr
        diPdfBbox[k]=pdfutil.imgBboxToPdfBbox(ul,lr,maxY)
        return diPdfBbox
    
def getTextInsideBboxMult(lstPdfBbox,diTags):
    diBboxText={}
    for pdfBbox in lstPdfBbox:
        diBboxText[pdfBbox]=pdfutil.getTextInsideBbox(diTags,pdfBbox)
    return diBboxText

def auto_canny(image,sigma=0.33):
    # compute the median of the single channel pixel intensities
    v=np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower=int(max(0,(1.0-sigma)*v))
    upper=int(min(255,(1.0+sigma)*v))
    edged=cv2.Canny(image,lower,upper)

    #return the edged image
    return edged

def findAllTbls(img,diTagsPg,edges,imgDir,imgFNm,minLsLen,tblBbox=None):
    def intraConnectLines(lstLines,ixLow,ixUp,tol=cns.tblTol,intraClsLen=cns.intraCLsLen):
        diLs={}
        for lnIx,ln in enumerate(lstLines): # loops over all lines
            flag=True
            lsIx=0
            while (flag):
                '''sorts line by the low index. i.e. for hLs(1,4,10,4) ixLow would be 0 and ixUp would be 2'''
                lnSort=sorted((ln),key=lambda tup: (tup[ixLow],(tup[ixUp]-tup[ixLow])))
                lstTmp=[]
                for ix,ls in list(enumerate(lnSort))[lsIx:-1]:
                    ls1=lnSort[ix+1] # takes two successive ls (line segment)
                    lsLen,ls1Len=ls[ixUp]+1-ls[ixLow],ls1[ixUp]+1-ls1[ixLow]
                    # check if the distance between them is less than
                    if lsLen>intraClsLen and ls1Len>intraClsLen and (0<ls1[ixLow]-ls[ixUp]<tol or ls[ixLow]<=ls1[ixLow]<=ls[ixUp]):
                        lstTmp.append(ls)
                    else:
                        lstTmp.append(ls)
                        lsLow=min([ls[ixLow] for ls in lstTmp])
                        lsUp=max([ls[ixUp] for ls in lstTmp])
                        lsStatic=lstTmp[0][ixLow+1]
                        if ixLow==0:
                            keyTup=(lsLow,lsStatic,lsUp,lsStatic)
                        else:
                            keyTup=(lsStatic,lsLow,lsStatic,lsUp)
                        diLs[keyTup]=lstTmp
                        lstTmp=[]
                        lsIx=ix+1
                        break
                else:
                    lstTmp.append(lnSort[-1])
                    lsLow=min([ls[ixLow] for ls in lstTmp])
                    lsUp=max([ls[ixUp] for ls in lstTmp])
                    lsStatic=lstTmp[0][ixLow+1]
                    if ixLow==0:
                        keyTup=(lsLow,lsStatic,lsUp,lsStatic)
                    else:
                        keyTup=(lsStatic,lsLow,lsStatic,lsUp)
                    diLs[keyTup]=lstTmp
                    flag=False
        return diLs

    def reshpMrgdLs(lstMrgdLs,ixLow,ixSrt):
        lstLines=[]
        steps=sorted(list(set([ls[ixLow] for ls in lstMrgdLs])))
        for ix,step in enumerate(steps):
            lstStep=[]
            for mrgdLs in lstMrgdLs:
                if mrgdLs[ixLow]==step:
                    lstStep.append(mrgdLs)
            lstLines.append(sorted(lstStep,key=lambda tup: tup[ixSrt]))
        return lstLines
    
    def completeBbox(hLs,vLs,tol):
        xStatic=vLs[0] # x value is static for any vLs
        yStatic=hLs[1] # y value is static for any hLs
        xDif,xDifAbs=hLs[0]-xStatic, abs(hLs[0]-xStatic) # dif and absolute dif between hls lower-x value and xStatic
        xDif2,xDifAbs2=xStatic-hLs[2],abs(xStatic-hLs[2]) # dif and absolute dif between hls lower-x value and xStatic
        yDif,yDifAbs=vLs[1]-yStatic, abs(vLs[1]-yStatic) # dif and absolute dif between vls lower-y value and xStatic
        yDif2,yDifAbs2=yStatic-vLs[3],abs(yStatic-vLs[3]) # dif and absolute dif between vls lower-y value and xStatic

        if ((0<=xDif<=tol and 0<=yDif<=tol) or (0<=xDifAbs<=tol and 0<=yDifAbs<=tol)):
            '''if both xDif and yDif are within tolerance or both xDifAbs and yDifAbs are within tolerance'''
            if not (0<=xDif<=tol and 0<=yDif<=tol):
                '''if both xDifAbs and yDifAbs are within tolerance, take lower-x of hls and yStatic'''
                pt_x,pt_y=hLs[0],yStatic
            else:
                '''if both xDif and yDif are within tolerance, take xStatic and yStatic'''
                pt_x,pt_y=xStatic,yStatic
            return (pt_x,pt_y,hLs[2],vLs[3])
        
        
        elif ((0<=xDif2<=tol and 0<=yDif<=tol) or (0<=xDifAbs2<=tol and 0<=yDifAbs<=tol)):
            '''if both xDif2 and yDif are within tolerance or both xDifAbs2 and yDifAbs are within tolerance'''
            if not (0<=xDif2<=tol and 0<=yDif<=tol):
                '''if both xDifAbs2 and yDifAbs are within tolerance, take upper-x of hls and yStatic'''
                pt_x,pt_y=hLs[2],yStatic
            else:
                '''if both xDif2 and yDif are within tolerance, take xStatic and yStatic'''
                pt_x,pt_y=xStatic,yStatic
            return (hLs[0],pt_y,pt_x,vLs[3])
        
        elif ((0<=xDif2<=tol and 0<=yDif2<=tol) or (0<=xDifAbs2<=tol and 0<=yDifAbs2<=tol)):
            '''if both xDif2 and yDif2 are within tolerance or both xDifAbs2 and yDifAbs2 are within tolerance'''
            if not (0<=xDif2<=tol and 0<=yDif2<=tol):
                '''if both xDifAbs2 and yDifAbs2 are within tolerance, take upper-x of hls and yStatic'''
                pt_x,pt_y=hLs[2],yStatic
            else:
                '''if both xDif2 and yDif2 are within tolerance, take xStatic and yStatic'''
                pt_x,pt_y=xStatic,yStatic
            return (hLs[0],vLs[1],pt_x,pt_y)
        
        elif ((0<=xDif<=tol and 0<=yDif2<=tol) or (0<=xDifAbs<=tol and 0<=yDifAbs2<=tol)):
            '''if both xDif and yDif2 are within tolerance or both xDifAbs and yDifAbs2 are within tolerance'''
            if not (0<=xDif<=tol and 0<=yDif2<=tol):
                '''if both xDifAbs and yDifAbs2 are within tolerance, take lower-x of hls and yStatic'''
                pt_x,pt_y=hLs[0],yStatic
            else:
                '''if both xDif and yDif2 are within tolerance, take xStatic and yStatic'''
                pt_x,pt_y=xStatic,yStatic
            return (pt_x,vLs[1],hLs[2],pt_y)
    
    def overlappingBbox(bbx1,bbx2):
        overlap=False
        if (bbx1==bbx2):
            # both bbx1 and bbx2 are equal
            overlap=True
        elif (bbx2[0]<=bbx1[0]<bbx1[2]<=bbx2[2]) and (bbx2[1]<=bbx1[1]<bbx1[3]<=bbx2[3]):
            # bbx1 is contained in bbx2
            overlap=True
        elif (bbx1[0]<=bbx2[0]<bbx2[2]<=bbx1[2]) and (bbx1[1]<=bbx2[1]<bbx2[3]<=bbx1[3]):
            # bbx2 is contained in bbx1
            overlap=True
        elif (bbx2[1]<=bbx1[1]<bbx2[3] or bbx2[1]<bbx1[3]<=bbx2[3]) and (bbx1[0]<=bbx2[0]<bbx1[2] or bbx1[0]<bbx2[2]<=bbx1[2]):
            overlap=True
        return overlap
    
    def distinctTables(lst):
        lstDistinct=[]
        ignore=[]
        for ix,tup in enumerate(lst):
            if tup in ignore:
                continue
            for ix1,tup1 in enumerate(lst):
                if ix==ix1:
                    continue
                if ((tup1[0]<=tup[0]<=tup1[2] or tup1[0]<=tup[2]<=tup1[2]) and
                    (tup1[1]<=tup[1]<=tup1[3] or tup1[1]<=tup[3]<=tup1[3])):
                    if (tup[2]-tup[0])*(tup[3]-tup[1])<(tup1[2]-tup1[0])*(tup1[3]-tup1[1]):
                        break
                    elif (tup[2]-tup[0])*(tup[3]-tup[1]) == (tup1[2]-tup1[0])*(tup1[3]-tup1[1]):
                        ignore.append(tup1)
            else:
                lstDistinct.append(tup)
        return lstDistinct
    
    def isovrlap(lstMainBbox,candbbx):
        for bbx in lstMainBbox:
            bbxint=tuple(map(int,bbx))
            xbbx=set(range(bbxint[0],bbxint[2]+1))
            ybbx=set(range(bbxint[1],bbxint[3]+1))

            candint=tuple(map(int,candbbx))
            xcand=set(range(candint[0],candint[2]+1))
            ycand=set(range(candint[1],candint[3]+1))

            if xbbx.intersection(xcand) and ybbx.intersection(ycand):
                return True
            
        return False

    def findTblMainBbox(lstHLines,lstVLines,tol=cns.tblTol):
        '''this function detects all tables on a page'''
        lstMainBbox=[]
        hLsCovered=[]
        lstCompletedMainBox=[]
        flag=True
        while (flag):
            brk=False
            for hLs in lstHLines:
                '''loops over all hls from topleft to lower right
                and tries to locate leftmost vls with respect to
                any particular hls. If it finds one then it determines if there
                exists corresponding bottommost hls and rightmost vls and if found then
                together these four ls (two hls and two vls) define a particular table'''
                if hLs in hLsCovered or any([bbx[0]<=hLs[0]<=bbx[2] and bbx[1]<=hLs[1]<=bbx[3] for bbx in lstMainBbox]):
                    '''continues if an hls is already exhausted (could not become a part of a table) or a part of already identified table'''
                    if cns.debugTblMainBbox:
                        print('hLs {} is either captured or exhausted'.format(hLs))
                    continue
                lenLstVLines=len(lstVLines)
                for ix,vLs in enumerate(lstVLines):
                    if all([not(tup[0]<=hLs[0]<hLs[2]<=tup[2] and tup[1]<=vLs[1]<vLs[3]<=tup[3]) for tup in lstCompletedMainBox]):
                        completedBbox=completeBbox(hLs,vLs,tol)
                        if (
                            completedBbox and (completedBbox[2]-completedBbox[0]>=cns.minTblOutBorder and completedBbox[3]-completedBbox[1]>=cns.minTblOutBorder)
                            and not any([overlappingBbox(completedBbox,tup) for tup in lstCompletedMainBox])
                        ):
                            ovrlap=isovrlap(lstCompletedMainBox+lstMainBbox,completedBbox)
                            if not ovrlap:
                                lstCompletedMainBox.append(completedBbox)

                    if (
                        not(vLs[0]+tol>=hLs[0] and vLs[1]>=hLs[1]-tol) 
                        or any([ bbx[0]<=vLs[0]<=bbx[2] and bbx[1]<=vLs[1]<=bbx[3] for bbx in lstMainBbox])
                    ):
                        '''continues if a vls is not within the tolerance of the hls under
                        consideration or if vls is a part of already identified table'''
                        if cns.debugTblMainBbox:
                            print('vLs {} is either captured or exhausted'.format(vLs))
                        continue
                    xStatic=vLs[0] # x value is static for any vLs
                    yStatic=hLs[1] # y value is static for any hLs
                    xDif,xDifAbs=hLs[0]-xStatic, abs(hLs[0]-xStatic) # dif and absolute dif between hls lower-x value and xStatic
                    yDif,yDifAbs=vLs[0]-yStatic, abs(vLs[0]-yStatic) # dif and absolute dif between vls lower-y value and yStatic


                    if ((0<=xDif<=tol and 0<=yDif<=tol) or (0<=xDifAbs<=tol and 0<=yDifAbs<=tol)):
                        if (0<=xDif<=tol):
                            pt1_x=xStatic
                        elif (0<=xDifAbs<=tol):
                            pt1_x=hLs[0]
                        if (0<=yDif<=tol):
                            pt1_y=yStatic
                        elif (0<=yDifAbs<=tol):
                            pt1_y=vLs[0]
                        
                        '''point1_x and point1_y are determined. Now point2_x and point2_y should be determined'''

                        '''temporary list of rightmost vertical ls based on within tolerance signed diff'''
                        tmpX1=[ls for ls in sorted(lstVLines,key=lambda tup:(-tup[0],tup[1])) if
                            0<=ls[0]-hLs[2]<=tol and 0<=ls[1]-yStatic<=tol]
                        '''temporary list of rightmost vertical ls based on within tolerance absolute diff'''
                        tmpX2=[ls for ls in sorted(lstVLines,key=lambda tup:(-tup[0],tup[1])) if
                            0<=abs(ls[0]-hLs[2])<=tol and 0<=abs(ls[1]-yStatic)<=tol]
                        
                        '''temporary list of rightmost vertical ls based on within tolerance signed diff'''
                        tmpY1=[ls for ls in sorted(lstHLines,key=lambda tup:(-tup[1],tup[0])) if
                            0<=ls[0]-xStatic<=tol and 0<=ls[1]-vLs[3]<=tol]
                        '''temporary list of rightmost vertical ls based on within tolerance absolute diff'''
                        tmpY2=[ls for ls in sorted(lstHLines,key=lambda tup:(-tup[1],tup[0])) if
                            0<=abs(ls[0]-xStatic)<=tol and 0<=abs(ls[1]-vLs[3])<=tol]
                        
                        pt2_x,pt2_y=None,None

                        if tmpX1:
                            pt2_x=tmpX1[0][0]
                        elif tmpX2:
                            pt2_x=hLs[2]
                        if tmpY1:
                            pt2_y=tmpY1[0][1]
                        elif tmpY2:
                            pt2_y=vLs[3]
                        
                        if not (pt2_x and pt2_y):
                            '''continue if both pt2_x and pt2_y are not determined'''
                            if cns.debugTblMainBbox:
                                print('continuing for vLs {} ix {} remaining {}'.format(vLs,ix,lenLstVLines-ix))
                            continue
                        if pt2_x-pt1_x>=cns.minTblOutBorder and pt2_y-pt1_y>=cns.minTblOutBorder:
                            '''if pt2_x and pt2_y are determined and the identified table border is 
                            above the threshold then accept that table and break from all for-loops and 
                            continue to the next iteration of while-loop'''
                            candbbx=(pt1_x,pt1_y,pt2_x,pt2_y) #candidate bbox
                            
                            ovrlap=isovrlap(lstMainBbox+lstCompletedMainBox,candbbx)
                            if not ovrlap:
                                lstMainBbox.append(candbbx)
                            brk=True
                            if cns.debugTblMainBbox:
                                print('breaking for hLs {}, vLs {}, ix {}, remaining {}'.format(hLs,vLs,ix,lenLstVLines-ix))
                            break
                hLsCovered.append(hLs) # collect those hls which are not part of any table
                if brk:
                    break
            if not brk:
                flag=False
        if lstCompletedMainBox==lstMainBbox:
            lstMainBbox=lstMainBbox
        else:
            lstMainBbox=distinctTables(list(set(lstCompletedMainBox+lstMainBbox)))
        
        return lstMainBbox

    
    def filt(lstLines,ixStatic,minLsLen,returnMrgBkt=False,customFilt=False):
        filtLstLines=[]
        if ixStatic==0:
            l,u=1,3
        else:
            l,u=0,2
        lstMrgBucket=[]
        mrgBucket=[]
        mrgLenBucket=[]
        for ix,ln in enumerate(lstLines):
            lnSpan=(ln[0][l],ln[-1][u])
            lnLen=lnSpan[1]-lnSpan[0]
            if 0<lnSpan[1]-lnSpan[0]<minLsLen:
                continue
            staticCrnt=ln[0][ixStatic]
            if ix<len(lstLines)-1:
                lnNxt=lstLines[ix+1]
                staticNxt=lnNxt[0][ixStatic]
                lnNxtSpan=(lnNxt[0][l],lnNxt[-1][u])
                if lnNxtSpan[1]-lnNxtSpan[0]>=cns.intraCLsLen and 0< (staticNxt-staticCrnt)<cns.filtTol:
                    if cns.customFilt or customFilt:
                        mrgBucket.append((ln,lnLen))
                    else:
                        if all([lnLen>=tup[1] for tup in mrgBucket]):
                            mrgBucket=[(ln,lnLen)]
                    continue
            if cns.customFilt or customFilt:
                mrgBucket.append((ln,lnLen))
            else:
                if all([lnLen>=tup[1] for tup in mrgBucket]):
                    mrgBucket=[(ln,lnLen)]
            lstMrgBucket.append(mrgBucket)
            filtLstLines,mrgBucket=processBucket([tup[0] for tup in mrgBucket],ixStatic,l,u,filtLstLines)
        if returnMrgBkt:
            return filtLstLines,lstMrgBucket
        return filtLstLines
    
    def filterLn(lstHLines,lstVLines,minLsLen):
        filtLstHLines=filt(lstHLines,1,minLsLen)
        filtLstVLines=filt(lstVLines,0,minLsLen)
        return filtLstHLines,filtLstVLines
    
    def removeJunkFrmBbox(lstHLines,lstVLines,diBbox):
        deleteHLines=[]
        deleteVLines=[]
        for k,v in diBbox.items():
            for ix,vLn in enumerate(lstVLines):
                if k[0]<=vLn[0][0]<=v[0] and k[1]<=vLn[0][1]<vLn[0][3]<v[1] and vLn[0][1]!=k[1]:
                    deleteVLines.append((ix,0))

                if k[0]<=vLn[-1][0]<=v[0] and k[1]<=vLn[-1][1]<vLn[-1][3]<v[1] and vLn[-1][1]!=k[1]:
                    deleteVLines.append((ix,-1))
            
            for ix,hLn in enumerate(lstHLines):
                if k[0]<=hLn[0][0]<hLn[0][2]<=v[0] and k[1]<=hLn[0][1]<=v[1] and hLn[0][2]!=v[0]:
                    deleteHLines.append((ix,0))

                if k[0]<=hLn[-1][0]<hLn[-1][2]<=v[0] and k[1]<=hLn[-1][1]<=v[1] and hLn[-1][2]!=v[0]:
                    deleteHLines.append((ix,-1))

        for tup in deleteHLines:
            ixLn,ixLs=tup
            if len(lstHLines[ixLn])>0:
                lstHLines[ixLn].pop(ixLs)
        for tup in deleteVLines:
            ixLn,ixLs=tup
            if len(lstVLines[ixLn])>0:
                lstVLines[ixLn].pop(ixLs)
        filtLstHLines=[ln for ln in lstHLines if ln]
        filtLstVLines=[ln for ln in lstVLines if ln]
        return filtLstHLines,filtLstVLines
    
    def getOuterBbox(lstLines):
        prntBbox=(lstLines[0][0][0],lstLines[0][0][1],lstLines[-1][0][2],lstLines[-1][0][3])
        return prntBbox
    
    def getOpenEndedOuterBbox(diBbox,yTop,yBtm,xLft,xRht,img,imgFNm):
        # if not diBbox and cns.tblWithoutLn:
        #     diBbox[(xLft,yTop)]=(xRht,yBtm)

        lstBbox=sorted([k+v for k,v in zip(diBbox.keys(),diBbox.values())],key=lambda tup:(tup[1],tup[0]))
        prntBbox=(lstBbox[0][0],lstBbox[0][1],lstBbox[-1][2],lstBbox[-1][3])
        # debugBbox(img,{(prntBbox[0],prntBbox[1]):(prntBbox[2],prntBbox[3])},imgFNm)
        lftCol={(xLft,k[1]):(k[0],v[1]) for k,v in diBbox.items() if k[0]==prntBbox[0]}
        rhtCol={(v[0],k[1]):(xRht,v[1]) for k,v in diBbox.items() if v[0]==prntBbox[2]}
        topRow={(k[0],yTop):(v[0],k[1]) for k,v in diBbox.items() if k[1]==prntBbox[1]}
        btmRow={(k[0],v[1]):(v[0],yBtm) for k,v in diBbox.items() if v[1]==prntBbox[3]}
        mrgAll={}

        for di in [lftCol,rhtCol,topRow,btmRow]:
            mrgAll.update(di)

        # update the 4 corner bboxes

        cornerBboxes={
            (xLft,yTop):(prntBbox[0],prntBbox[1]),
            (prntBbox[2],yTop):(xRht,prntBbox[1]),
            (xLft,prntBbox[3]):(prntBbox[0],yBtm),
            (prntBbox[2],prntBbox[3]):(xRht,yBtm)
            }
        
        mrgAll.update({k:v for k,v in cornerBboxes.items() if k not in mrgAll})
        return prntBbox,mrgAll
                

    def completeLines(outerBbox,interCHLines,interCVLines):
        interCHLinesComp=[[(min(outerBbox[0],ln[0][0]),ln[0][1],max(outerBbox[2],ln[0][2]),ln[0][3])] for ln in interCHLines]
        interCVLinesComp=[[(ln[0][0],min(outerBbox[1],ln[0][1]),ln[0][2],max(outerBbox[3],ln[0][3]))] for ln in interCVLines]
        return interCHLinesComp,interCVLinesComp
    
    def convertBbxToLn(bbx):
        return (
            (bbx[0],bbx[1],bbx[2],bbx[1]),
            (bbx[0],bbx[3],bbx[2],bbx[3]),
            (bbx[0],bbx[1],bbx[0],bbx[3]),
            (bbx[2],bbx[1],bbx[2],bbx[3]),
            )

    def adjoinOuterBbx(lstMainBbox,diHLs,diVLs):
        for bbx in lstMainBbox:
            lstLn=convertBbxToLn(bbx)
            topLn=lstLn[0]
            btmLn=lstLn[1]
            lftLn=lstLn[2]
            rhtLn=lstLn[3]
            diHLs[topLn]=[topLn]
            diHLs[btmLn]=[btmLn]
            diVLs[lftLn]=[lftLn]
            diVLs[rhtLn]=[rhtLn]
        return diHLs,diVLs
    
    def findExtension(ls,lstMrgBkt,ixStatic,ixLow,ixUp):
        if not lstMrgBkt:
            return None
        firstCandidates=lstMrgBkt[1]
        lastCandidates=lstMrgBkt[-2]
        first=any([lstMrgBkt[0][-1][0][0][ixStatic]<ls[ixLow]<candLs[ixStatic]<=ls[ixUp]+cns.tblTol for candLs in firstCandidates[0][0]])
        last=any([ls[ixLow]-cns.tblTol<=candLs[ixStatic]<ls[ixUp]<lstMrgBkt[-1][0][0][0][ixStatic] for candLs in lastCandidates[-1][0]])

        if first and last:
            return 3
        return 1 if first else 2 if last else None


    def extendLines(bbx,tupLines,minLsLen):
        diHLines=tupLines[0]
        diVLines=tupLines[1]
        diHLinesNew={}
        lstHLines=reshpMrgdLs(diHLines.keys(),1,0)
        lstVLines=reshpMrgdLs(diVLines.keys(),0,1)
        interCVLines,interCHLines=interConnectLines(lstVLines,lstHLines)
        for hLs,lstHLs in list(diHLines.items()):
            newHLs=hLs
            ixStatic=1
            staticVal=hLs[ixStatic]
            subsetVLn=[vLn for vLn in interCVLines if any(vLs[1]<=staticVal<=vLs[3] for vLs in vLn)]
            filtLstVLines,lstMrgBkt=filt(subsetVLn,0,minLsLen,returnMrgBkt=True,customFilt=True)
            extend=findExtension(hLs,lstMrgBkt,0,0,2)
            if extend==1:
                newHLs=(bbx[0],newHLs[1],newHLs[2],newHLs[3])
            elif extend==2:
                newHLs=(newHLs[0],newHLs[1],bbx[2],newHLs[3])
            elif extend==3:
                newHLs=(bbx[0],newHLs[1],bbx[2],newHLs[3])
            diHLinesNew[newHLs]=lstHLs

        diVLinesNew={}
        for vLs,lstVLs in list(diVLines.items()):
            newVLs=vLs
            ixStatic=0
            staticVal=vLs[ixStatic]
            subsetHLn=[hLn for hLn in interCHLines if any(hLs[0]<=staticVal<=hLs[2] for hLs in hLn)]
            filtLstHLines,lstMrgBkt=filt(subsetHLn,0,minLsLen,returnMrgBkt=True,customFilt=True)
            extend=findExtension(vLs,lstMrgBkt,1,1,3)
            if extend==1:
                newVLs=(newVLs[0],bbx[1],newVLs[2],newVLs[3])
            elif extend==2:
                newVLs=(newVLs[0],newVLs[1],newVLs[2],bbx[3])
            elif extend==3:
                newVLs=(newVLs[0],bbx[1],newVLs[2],bbx[3])
            diVLinesNew[newVLs]=lstVLs
        
        return (diHLinesNew,diVLinesNew)

    def getExtendedMainBbox(lstMainBbox,lstHLines,lstVLines,minLsLen):

        def extendMainBbox(mainBbox,lstMrgdBktHLines,lstMrgdBktVLines):
            tmpH=[tup[0] for hLnBkt in lstMrgdBktHLines for tup in hLnBkt]
            tmpV=[tup[0] for vLnBkt in lstMrgdBktVLines for tup in vLnBkt]

            xLft=min([mainBbox[0]]+[hLn[0][0] for hLn in tmpH if (mainBbox[0]<=hLn[0][0]<hLn[0][2]<=mainBbox[2] or hLn[0][0]<=mainBbox[0]<=hLn[0][2] or hLn[0][0]<=mainBbox[2]<=hLn[0][2])])
            xRht=max([mainBbox[2]]+[hLn[-1][2] for hLn in tmpH if (mainBbox[0]<=hLn[-1][0]<hLn[-1][2]<=mainBbox[2] or hLn[-1][0]<=mainBbox[0]<=hLn[-1][2] or hLn[-1][0]<=mainBbox[2]<=hLn[-1][2])])
            yTop=min([mainBbox[1]]+[vLn[0][1] for vLn in tmpV if (mainBbox[1]<=vLn[0][1]<vLn[0][3]<=mainBbox[3] or vLn[0][1]<=mainBbox[1]<=vLn[0][3] or vLn[0][1]<=mainBbox[3]<=vLn[0][3])])
            yBtm=max([mainBbox[3]]+[vLn[-1][3] for vLn in tmpV if (mainBbox[1]<=vLn[-1][1]<vLn[-1][3]<=mainBbox[3] or vLn[-1][1]<=mainBbox[1]<=vLn[-1][3] or vLn[-1][1]<=mainBbox[3]<=vLn[-1][3])])
            return (xLft,yTop,xRht,yBtm)
        
        lstExtendedMainBbox=[]
        for mainBbox in lstMainBbox:
            filtLstHLines,lstMrgBktHLines=filt(reshpMrgdLs(lstHLines,1,0),1,minLsLen,returnMrgBkt=True,customFilt=True)
            filtLstVLines,lstMrgBktVLines=filt(reshpMrgdLs(lstVLines,0,1),0,minLsLen,returnMrgBkt=True,customFilt=True)
            lstMrgBktHLinesSubset=[mrgBkt for mrgBkt in lstMrgBktHLines if all([mainBbox[1]<=tup[0][0][1]<=mainBbox[3] for tup in mrgBkt])]
            lstMrgBktVLinesSubset=[mrgBkt for mrgBkt in lstMrgBktVLines if all([mainBbox[0]<=tup[0][0][0]<=mainBbox[2] for tup in mrgBkt])]
            extendMainBbox=extendMainBbox(mainBbox,lstMrgBktHLinesSubset,lstMrgBktVLinesSubset)

        return lstExtendedMainBbox
    

    def interConnectLines(lstVLines,lstHLines,tol=cns.tblTol):
        lstVLinesCp=[[list(ls) for ls in ln] for ln in copy.deepcopy(lstVLines)]
        lstHLinesCp=[[list(ls) for ls in ln] for ln in copy.deepcopy(lstHLines)]
        flag=True
        while (flag):
            brk=False
            for hLnIx,hLn in enumerate(copy.deepcopy(lstHLinesCp)):
                for hLsIx,hLs in enumerate(hLn):
                    for vLnIx,vLn in enumerate(copy.deepcopy(lstVLinesCp)):
                        for vLsIx,vLs in enumerate(vLn):
                            xStatic=vLs[0]
                            yStatic=hLs[1]
                            if vLs[3]<yStatic:
                                dif=yStatic-vLs[3]
                                if dif<=tol:
                                    lstVLinesCp[vLnIx][vLsIx][3]+=dif

                            elif yStatic<vLs[1]:
                                dif=vLs[1]-yStatic
                                if dif<=tol:
                                    lstVLinesCp[vLnIx][vLsIx][1]-=dif

                            if hLs[2]<xStatic:
                                dif=xStatic-hLs[2]
                                if dif<=tol:
                                    lstHLinesCp[hLnIx][hLsIx][2]+=dif
                                    brk=True
                                    break

                            elif xStatic<hLs[0]:
                                dif=hLs[0]-xStatic
                                if dif<=tol:
                                    lstHLinesCp[hLnIx][hLsIx][0]-=dif
                                    brk=True
                                    break

                        if brk:
                            break
                    if brk:
                        break
                if brk:
                    break
            if not brk:
                flag=False

        lstVLines=[[tuple(ls) for ls in ln] for ln in copy.deepcopy(lstVLinesCp)]
        lstHLines=[[tuple(ls) for ls in ln] for ln in copy.deepcopy(lstHLinesCp)]
        return lstVLines,lstHLines
    

    def getDiPdfBbxErase(diTagsPg,pdfBbx):
        diPdfBbxErase={}

        for bbx,tup in diTagsPg:
            if (
                (tup[0] in cns.eraseTags) and
                (bbx[0]>pdfBbx[0] and bbx[1]>pdfBbx[1] and bbx[2]<pdfBbx[2] and bbx[3]<pdfBbx[3])
            ):
                if tup[0]=='text':
                    if tup[1].xpath('normalize-space(.)').strip():
                        diPdfBbxErase[bbx]=tup[0]
                else:
                    diPdfBbxErase[bbx]=tup[0]
        return diPdfBbxErase
    

    def eraseCellElm(imgDir,imgFNm,lstMainBbox,diTagsPg,edges):
        diBbox={(bbx[0],bbx[1]):(bbx[2],bbx[3]) for bbx in lstMainBbox}
        imgShp=edges.shape
        diPdfBbox=pdfutil.imgBboxToPdfBboxMult(diBbox,imgShp[0]) # converting Img-Bbox to Pdf-Bbox
        imgBbx,pdfBbx=list(diPdfBbox.items())[0]

        cpEdges=copy.deepcopy(edges) # creates a copy of edges
        diPdfBbxErase=getDiPdfBbxErase(diTagsPg,pdfBbx) # collects bboxes of all tags to be erased
        '''converts collect bboxes to corresponding image bboxes'''
        lstImgBbxErase=[pdfutil.translateBbox(list(pdfBbx),imgShp[0]) for pdfBbx in diPdfBbxErase.keys()]
        if cns.debugCrop:
            '''crops them and saves to disk for debugging purpose'''
            pdfutil.cropMultiBoxes(imgFNm+'.png',diPdfBbxErase.items(), inpDir=imgDir,
                                   outDir=cns.tblCropPath.format(imgFNm))
        
        for imgBbxErase in lstImgBbxErase:
            '''loops over bboxes and erases all content within them'''
            pt1_x=imgBbxErase[0]-cns.eraseTol
            pt1_y=imgBbxErase[1]-cns.eraseTol
            pt2_x=imgBbxErase[2]+cns.eraseTol
            pt2_y=imgBbxErase[3]+cns.eraseTol

            '''erase operation by means of setting pixel=0 for 0<pixel<=255'''
            cpEdges[pt1_y:pt2_y,pt1_x:pt2_x]=0
        return cpEdges
    
    def getDiLines(lstMainBbox,diHLs,diVLs):
        diHLines={}
        diVLines={}
        for bbx in lstMainBbox:
            for mrgdHLs,lstHLs in diHLs.items():
                if (
                    ((bbx[0]<=mrgdHLs[0]<mrgdHLs[2]<=bbx[2]) or
                    (mrgdHLs[0]<bbx[0]<mrgdHLs[2]) or
                    (mrgdHLs[0]<bbx[2]<mrgdHLs[2]))
                    and
                    (bbx[1]<=mrgdHLs[1]<=bbx[3])
                ):
                    newMrgdHLs=mrgdHLs
                    if(mrgdHLs[0]<bbx[0]<mrgdHLs[2]):
                        newMrgdHLs=(bbx[0],newMrgdHLs[1],newMrgdHLs[2],newMrgdHLs[3])
                    if(mrgdHLs[0]<bbx[0]<mrgdHLs[2]):
                        newMrgdHLs=(newMrgdHLs[0],newMrgdHLs[1],bbx[2],newMrgdHLs[3])
                    diHLines.setdefault(bbx,{}).update({newMrgdHLs:lstHLs})

            for mrgdVLs,lstVLs in diVLs.items():
                if (
                    (bbx[0]<=mrgdVLs[0]<=bbx[2])
                    and
                    ((bbx[1]<=mrgdVLs[1]<mrgdVLs[3]<=bbx[3]) or
                    (mrgdVLs[1]<bbx[1]<mrgdVLs[3]) or
                    (mrgdVLs[1]<bbx[3]<mrgdVLs[3]))
                    
                    
                ):
                    newMrgdVLs=mrgdVLs
                    if(mrgdVLs[1]<bbx[1]<mrgdVLs[3]):
                        newMrgdVLs=(newMrgdVLs[0],bbx[1],newMrgdVLs[2],newMrgdVLs[3])
                    if(mrgdVLs[1]<bbx[3]<mrgdVLs[3]):
                        newMrgdVLs=(newMrgdVLs[0],newMrgdVLs[1],newMrgdVLs[2],bbx[3])
                    diVLines.setdefault(bbx,{}).update({newMrgdVLs:lstVLs})

        diLines={}
        for bbx in lstMainBbox:
            if cns.tblWithoutLn:
                if not diHLines.get(bbx):
                    diHLines[bbx]={
                        (bbx[0],bbx[1],bbx[2],bbx[1]):[(bbx[0],bbx[1],bbx[2],bbx[1])],
                        (bbx[0],bbx[3],bbx[2],bbx[3]):[(bbx[0],bbx[3],bbx[2],bbx[3])]
                        }

                if not diVLines.get(bbx):
                    diVLines[bbx]={
                        (bbx[0],bbx[1],bbx[0],bbx[3]):[(bbx[0],bbx[1],bbx[0],bbx[3])],
                        (bbx[2],bbx[1],bbx[2],bbx[3]):[(bbx[2],bbx[1],bbx[2],bbx[3])]
                        }
            diLines[bbx]=(diHLines[bbx],diVLines[bbx])
        return diLines
    
    def removeJunkLsNew(diBbox,lstHLines,lstVLines):
        lstHLinesNew,lstVLinesNew=[],[]
        for ln in lstHLines:
            lnNew=[]
            for ls in ln:
                if all([not((ul[0]<ls[0]<ls[2]<=lr[0] or ul[0]<=ls[0]<ls[2]<lr[0]) and ul[1]<ls[1]<lr[1]) for ul,lr in diBbox.items()]):
                    lnNew.append(ls)
            if lnNew:
                lstHLinesNew.append(lnNew)
        for ln in lstVLines:
            lnNew=[]
            for ls in ln:
                if all([not(ul[0]<ls[0]<lr[0] and (ul[1]<ls[1]<ls[3]<=lr[1] or ul[1]<=ls[1]<ls[3]<lr[1])) for ul,lr in diBbox.items()]):
                    lnNew.append(ls)
            if lnNew:
                lstVLinesNew.append(lnNew)
        return lstHLinesNew,lstVLinesNew
    
    def removeJunkBbxNew(lstHLines,lstVLines,img,imgFNm):
        lstIntersections=captureInteractions(lstHLines,lstVLines)
        debugPoints(img,lstIntersections,imgFNm,text=False)
        diBbox=getBBox(lstIntersections,lstHLines,lstVLines)
        # debugBbox(img,diBbox,imgFNm,text=False,iter=True)
        debugBbox(img,diBbox,imgFNm)
        lstHLines,lstVLines=removeJunkLsNew(diBbox,lstHLines,lstVLines)
        return lstHLines,lstVLines
    
    def getLinesSbst(lstLines,tblBbox,ixStatic):
        if ixStatic==0:
            l,u=1,3
        else:
            l,u=0,2
        
        lstLinesSbst=[]
        for ln in lstLines:
            lnNew=[]
            for ls in ln:
                if tblBbox[ixStatic]<=ls[ixStatic]<=tblBbox[ixStatic+2]:
                    if tblBbox[1]<=ls[1]<ls[u]<=tblBbox[u]:
                        lnNew.append(ls)

                    elif ls[1]<=tblBbox[1]<tblBbox[u]<=ls[u]:
                        newLs=list(copy.deepcopy(tblBbox))
                        newLs[ixStatic],newLs[ixStatic+2]=ls[ixStatic],ls[ixStatic]
                        lnNew.append(tuple(newLs))
                    elif tblBbox[l]<=ls[l]<=tblBbox[u]:
                        newLs=list(copy.deepcopy(ls))
                        newLs[u]=tblBbox[u]
                        lnNew.append(tuple(newLs))
                    elif tblBbox[l]<=ls[u]<=tblBbox[u]:
                        newLs=list(copy.deepcopy(ls))
                        newLs[l]=tblBbox[l]
                        lnNew.append(tuple(newLs))
            if lnNew:
                lstLinesSbst.append(lnNew)
        return lstLinesSbst
    
    def allignTblBbox(lstHLines,lstVLines):
        minX=min([ls[0] for ln in lstHLines for ls in ln])
        maxX=max([ls[2] for ln in lstHLines for ls in ln])
        minY=min([ls[1] for ln in lstVLines for ls in ln])
        maxY=max([ls[3] for ln in lstVLines for ls in ln])
        return (minX,minY,maxX,maxY)
    
    def checkOverlap(tup,tup1,ixStatic,overlapTol):
        if ixStatic==0:
            l,u=1,3
        else:
            l,u=0,2
        
        return (
            (tup[l]<=tup[l]<tup1[u]<=tup[u] or tup1[l]<=tup[l]<tup[u]<=tup1[u])
            or
            ((tup1[l]-overlapTol<=tup[l]<tup[u]<=tup1[u]+overlapTol) or 
             (tup[l]-overlapTol<=tup1[l]<tup1[u]<=tup[u]+overlapTol) or 
             (tup1[l]-overlapTol<=tup[l]<=tup1[u]+overlapTol) or 
             (tup1[l]-overlapTol<=tup[u]<=tup1[u]+overlapTol))
        )

    def mergeClusters(lstLs,ixStatic,l,u):
        diScattered={}
        diUnited={}

        for ls in lstLs:
            for ls1 in lstLs:
                if checkOverlap(ls,ls1,ixStatic,cns.tblTol):
                    diScattered.setdefault(ls,[]).append(ls1)

        for ls,scattered in diScattered.items():
            lstStatic=[ls[ixStatic] for ls in scattered]
            staticVal=math.ceil((min(lstStatic)+max(lstStatic))/2)
            lstL=[ls[l] for ls in scattered]
            lstU=[ls[u] for ls in scattered]
            lsNew=list(copy.deepcopy(ls))
            lsNew[l],lsNew[u]=min(lstL),max(lstU)
            lsNew[ixStatic],lsNew[ixStatic+2]=staticVal,staticVal
            diUnited[ls]=tuple(lsNew)
        return diUnited

    def mergeClustersWrap(lstLs,ixStatic,l,u):
        diUnited=mergeClusters(lstLs,ixStatic,l,u)
        diUnited=mergeClusters(list(diUnited.values()),ixStatic,l,u)
        return diUnited
    
    def shiftToLastLnNew(lstLs,ixStatic,l,u):
        diUnited=mergeClustersWrap(lstLs,ixStatic,l,u)
        if ixStatic==0:
            lstMrgdLn=reshpMrgdLs(list(set(diUnited.values())),0,1)
        elif ixStatic==1:
            lstMrgdLn=reshpMrgdLs(list(set(diUnited.values())),1,0)
        return lstMrgdLn
            
    def processMrgBucket(mrgBucket,ixStatic,ixLow,ixUp):
        mrgBucketFlat=[ls for ln in mrgBucket for ls in ln]
        shifted=shiftToLastLnNew(mrgBucketFlat,ixStatic,ixLow,ixUp)
        return shifted
    
    def processBucket(mrgBucket,ixStatic,ixLow,ixUp,filtLstLines):
        mrgdLn=processMrgBucket(mrgBucket,ixStatic,ixLow,ixUp)
        filtLstLines.extend(mrgdLn)
        mrgBucket=[]
        return filtLstLines,mrgBucket

    def handleIsectOfChrAndClBrdr(lstLines,ixStatic,img,imgFNm):
        if ixStatic==0:
            l,u=1,3
        else:
            l,u=0,2
        ixStaticTol=2
        lstLinesFlat=[tup for lst in lstLines for tup in lst]
        cellBorders=[tup for tup in lstLinesFlat if (tup[u]-tup[l]) > cns.minCellBorderLen]
        lstLinesFlatSbst=[tup for tup in lstLinesFlat if any([0<=tup[ixStatic]-clBrdr[ixStatic]<=ixStaticTol for clBrdr in cellBorders])]
        if ixStatic==0:
            debugLS(img,[[ls] for ls in lstLinesFlatSbst],[],imgFNm)
        else:
            debugLS(img,[],[[ls] for ls in lstLinesFlatSbst],imgFNm)

        for clBrdr in cellBorders:
            lstLinesFlatSbst=[tup for tup in lstLinesFlat if 0<=tup[ixStatic]-clBrdr[ixStatic]<=ixStaticTol]
            diUnited=mergeClustersWrap(lstLinesFlatSbst,ixStatic,l,u)
            for tup in lstLinesFlatSbst:
                lstLinesFlat.remove(tup)
            
            lstLinesFlat.extend(diUnited.values())
        lstLinesFlat=[tup for tup in lstLinesFlat if ((tup[u]-tup[l])>=cns.intraCLsLen)]
        return lstLinesFlat


    def getMrgdLn(lstHLines,lstVLines,tblBbox):
        st=datetime.now()
        tblBboxNew=[]
        if tblBbox:
            lstHLines=getLinesSbst(lstHLines,tblBbox,1)
            lstVLines=getLinesSbst(lstVLines,tblBbox,0)
            tblBboxNew=allignTblBbox(lstHLines,lstVLines)
        pdfutil.debugTimeTaken(st,datetime.now(),'getLsSgmt')
        debugLS(img,lstHLines,lstVLines,imgFNm)
        lstHLines=reshpMrgdLs(handleIsectOfChrAndClBrdr(lstHLines,1,img,imgFNm),1,0)
        lstVLines=reshpMrgdLs(handleIsectOfChrAndClBrdr(lstVLines,0,img,imgFNm),0,1)

        debugLS(img,lstHLines,lstVLines,imgFNm)
        st=datetime.now()
        diHLs=intraConnectLines(lstHLines,0,2)
        diVLs=intraConnectLines(lstVLines,1,3)
        pdfutil.debugTimeTaken(st,datetime.now(),'intraConnect')
        diHLs={k:v for k,v in diHLs.items() if k[2]-k[0]>=cns.mrgdHLsLen}
        diVLs={k:v for k,v in diVLs.items() if k[3]-k[1]>=cns.mrgdHLsLen}

        debugLS(img,[diHLs.keys()],[diVLs.keys()],imgFNm)
        return diHLs,diVLs,tblBboxNew
    
    def allignWithTblMainBBox(lstHLines,lstVLines):
        topLn=lstHLines[0]
        btmLn=lstHLines[-1]
        lftLn=lstVLines[0]
        rhtLn=lstVLines[-1]

        if topLn[0][0]<lftLn[0][0]:
            lftLn=[(topLn[0][0],lftLn[0][1],topLn[0][0],lftLn[0][3])]
        if topLn[0][2]>rhtLn[0][0]:
            rhtLn=[(topLn[0][2],rhtLn[0][1],topLn[0][2],rhtLn[0][3])]
        if topLn[0][0]<btmLn[0][0]:
            btmLn=[(topLn[0][0],btmLn[0][1],btmLn[0][2],btmLn[0][3])]
        if topLn[0][2]>btmLn[0][2]:
            btmLn=[(btmLn[0][0],btmLn[0][1],topLn[0][2],btmLn[0][3])]
        if lftLn[0][3]>btmLn[0][1]:
            btmLn=[(btmLn[0][0],lftLn[0][3],btmLn[0][2],lftLn[0][3])]
                    
        lstHLines[0]=topLn
        lstHLines[-1]=btmLn
        lstVLines[0]=lftLn
        lstVLines[-1]=rhtLn

        return lstHLines,lstVLines
    
    if cns.isPdfTbl:
        '''if pdf is editable then a few native elements like textbox,
        image,figure can be removed safely from the corresponding image file.
        This will give performane boost to the process since otherwise all line
        segments (tiny ones too) have to be processed and removed separately'''

        debugImage(edges,imgFNm,outFNm=cns.debugLsBefEraseFNm)
        '''identifies and removes tags from edges file'''
        edges=eraseCellElm(imgDir,imgFNm,[(0,0,edges.shape[1],edges.shape[0])],diTagsPg,edges)
        debugImage(edges,imgFNm,outFNm=cns.debugLsAftEraseFNm)

    lstHLines=getLSgmt(edges,minLsLen,'H')
    lstVLines=getLSgmt(edges.transpose(),minLsLen,'V')
    origTblBbox=copy.deepcopy(tblBbox)

    if tblBbox:
        diHLs,diVLs={},{}
        newTblBbox=[]
        for bbx in tblBbox:
            diHLsBbx,diVLsBbx,tblBboxNew=getMrgdLn(copy.deepcopy(lstHLines),copy.deepcopy(lstVLines),bbx)
            diHLs.update(diHLsBbx)
            diVLs.update(diVLsBbx)
            newTblBbox.append(tblBboxNew)
        tblBbox=newTblBbox
    else:
        '''find, intraconnect and merge line segments'''
        diHLs,diVLs,_=getMrgdLn(copy.deepcopy(lstHLines),copy.deepcopy(lstVLines),tblBbox)

    debugLS(img,[diHLs.keys()],[diVLs.keys()],imgFNm)

    st=datetime.now()
    '''determines the outer bounding boxes of all tables present of a page'''
    lstMainBbox=tblBbox if tblBbox else findTblMainBbox(diHLs.keys(),diVLs.keys())

    print('^^^lstMainBbox^^^',lstMainBbox)
    if origTblBbox:
        mapOrigNewBbox=dict(zip(lstMainBbox,origTblBbox))

    for bbx in lstMainBbox:
        debugBboxAsRect(bbx,img,imgFNm)
    if cns.extendMainBbox:
        lstMainBbox=getExtendedMainBbox(lstMainBbox,diHLs.keys(),diVLs.keys(),minLsLen)
        for bbx in lstMainBbox:
            debugBboxAsRect(bbx,img,imgFNm)
    diHLs,diVLs=adjoinOuterBbx(lstMainBbox,diHLs,diVLs)
    pdfutil.debugTimeTaken(st,datetime.now(),'findTblMainBbox')

    '''reshape lstMainBbox for writing to file'''
    diMainBbox={(tup[0],tup[1]):(tup[2],tup[3]) for tup in lstMainBbox}
    debugBbox(img,diMainBbox,imgFNm)
    '''assigns line segments to their corresponding table'''
    diLines=getDiLines(lstMainBbox,diHLs,diVLs)

    for bbx,tupLines in list(diLines.items()):
        if cns.extendTable:
            tupLines=extendLines(bbx,tupLines,minLsLen)
        diHLsTbl,diVLsTbl=tupLines[0],tupLines[1]
        debugLS(img,[diHLsTbl.keys()],[diVLsTbl.keys()],imgFNm)
        lstHLines=reshpMrgdLs(diHLsTbl.keys(),1,0)
        lstVLines=reshpMrgdLs(diVLsTbl.keys(),0,1)
        debugLS(img,lstHLines,lstVLines,imgFNm)
        filtLstHLines,filtLstVLines=filterLn(lstHLines,lstVLines,minLsLen)
        debugLS(img,filtLstHLines,filtLstVLines,imgFNm)
        '''connect every pair of one horizontal lsgmt and one verical lsgmt 
        if their corner points are within tolerance limit with respect to each other'''
        interCVLines,interCHLines=interConnectLines(filtLstVLines,filtLstHLines)
        debugLS(img,interCHLines,interCVLines,imgFNm)
        st=datetime.now()

        '''discards lines which are away from each other by less than the
        tolerance. This is mainly done to avoid double edges for the same line'''
        filtLstHLines,filtLstVLines=filterLn(interCHLines,interCVLines,minLsLen)
        debugLS(img,filtLstHLines,filtLstVLines,imgFNm)

        filtLstHLines,filtLstVLines=allignWithTblMainBBox(filtLstHLines,filtLstVLines)
        debugLS(img,filtLstHLines,filtLstVLines,imgFNm)

        interCVLines,interCHLines=interConnectLines(filtLstVLines,filtLstHLines)
        interCHLines,interCVLines=removeJunkBbxNew(interCHLines,interCVLines,img,imgFNm)
        debugLS(img,interCHLines,interCVLines,imgFNm)
        # outerBbox=getOuterBbox(interCHLines)
        interCHLinesComp,interCVLinesComp=completeLines(bbx,interCHLines,interCVLines)
        debugLS(img,interCHLinesComp,interCVLinesComp,imgFNm)
        diLines[bbx]=(interCHLines,interCVLines,interCHLinesComp,interCVLinesComp)

    if origTblBbox:
        diLinesNew={mapOrigNewBbox[k]:v for k,v in diLines.items()}
    else:
        diLinesNew=diLines

    return diLinesNew

    


    



def bboxesToTable(di,diComp):

    def partitioning(di,diComp):
        diNew={}
        for ulComp,lrComp in diComp.items():
            for ul,lr in di.items():
                if ul[0]<=ulComp[0]<lrComp[0]<=lr[0] and ul[1]<=ulComp[1]<lrComp[1]<=lr[1]:
                    diNew[ulComp+lrComp]=ul+lr
        return diNew

    def finalShape(diNew):
        rows=[]
        for y in sorted(list(set([k[1] for k in diNew.keys()]))):
            row=[]
            for c,p in sorted(diNew.items(),key=lambda tup: (tup[0][1],tup[0][0])):
                if c[1]==y:
                    row.append(p)
            rows.append(row)
        return rows
    
    diNew=partitioning(di,diComp)
    return finalShape(diNew)

def htmlTable(lol,pgNo):
    diBboxGrp={}
    for row in lol:
        tDi={}
        for bbox in row:
            tDi.setdefault(bbox,[]).append(bbox)
        for k,v in tDi.items():
            diBboxGrp.setdefault(k,[]).append(v)

    diSpanInfo={}
    for k,v in diBboxGrp.items():
        colSpan=len(v[0])
        rowSpan=len(v)
        diSpanInfo.setdefault(k,{})['cSpan']=colSpan
        diSpanInfo.setdefault(k,{})['rSpan']=rowSpan
    
    srtLstBbx=sorted(diBboxGrp.keys(),key=lambda tup: (tup[1],tup[0]))
    grpd=groupby(srtLstBbx,lambda tup: tup[1])
    theadCSpan=len(lol[0]) if lol else 1
    tblString='''<table border="1"><thead><tr><th colspan="{0}">Page: {1}</th></tr></thead><tbody>'''.format(theadCSpan,pgNo)
    for _,g in grpd:
        trString='''<tr style="height: 15.0pt;">'''
        for elm in g:
            tdString=r'''<td rowspan="{0}" colspan="{1}">{{{2}}}</td>'''
            rSpan=diSpanInfo[elm]['rSpan']
            cSpan=diSpanInfo[elm]['cSpan']
            tdString=tdString.format(rSpan,cSpan,elm)
            trString+=tdString
        trString+='''</tr>'''
        tblString+=trString
    tblString+='''</tbody></table>'''
    return tblString,diSpanInfo
        
def extractTable(fNm,pgNo,pagesInFile,diTagsPg,tblBbox=None,imgBytes=None):
    '''the main wrapper for extraction of table from on single pdf page'''

    '''determining minimum line segment length based on whether the image is taken from an editable pdf or not.
    If image is of editable pdf then all the textlines can be parsed and minLSLen can be set to a bare minimum like 5 pixels
    otherwise it should be set higher (30 or above) depending on the table'''

    if cns.isPdfTbl:
        minLsLen=cns.pdfTblMinLsLen
    else:
        minLsLen=cns.tblMinLsLen
    justPgNo=utils.lJustPgNo(pgNo,pagesInFile) # Left justifying page number (i.e. 1 to 01 or 1 to 001 depending on the total number of pages)
    justPgNo=pgNo # Left justifying page number (i.e. 1 to 01 or 1 to 001 depending on the total number of pages)
    imgFNmNoExt='{0}-{1}'.format('p',justPgNo)
    imgDir=str(utils.fpath_from_lst([cns.imageDir,fNm]))
    imgPath=str(utils.fpath_from_lst([imgDir,f"{imgFNmNoExt}.png"]))
    # imgFNm=imgFNmNoExt+'.png'
    # imgDir=cns.imageDir+fNm+'/'
    # imgPath=imgDir+imgFNm # complete image path
    if imgBytes:
        nparr=np.fromstring(imgBytes,np.uint8)
        img=cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    else:
        img=cv2.imread(imgPath) #reading image in numpy array using opencv
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #grayscale image
    if cns.microEdges:
        edges=cv2.Canny(gray,10,100,apertureSize=3)
    else:
        if cns.triageEdges:
            edges=cv2.Canny(gray,50,150,apertureSize=3)
        else:
            edges=auto_canny(gray) #Canny edge detection # added for document_comparison project

    imgPth=utils.fpath_from_lst([utils.get_fname(imgDir),imgFNmNoExt],psx=True)
    debugImage(edges,imgPth,outDir=cns.debugTblPath,outFNm=cns.debugEdgesFNm) # writing edges image to file
    debugImage(gray,imgPth,outDir=cns.debugTblPath,outFNm=cns.debugGrayFNm) # writing grayscale image to file

    '''detect all tables on a page and assign the corresponding hLs 
    (horizontal line segment) and vLs (vertical line segment) to each of them'''
    diTbls=findAllTbls(img,diTagsPg,edges,imgDir,imgPth,minLsLen,tblBbox)

    diTblsNew={}
    lstHLinesAllTbls=[]
    lstVLinesAllTbls=[]
    '''capture all cells of table and converting corresponding
    bounding boxes to final table'''
    for tbl,tupLines in diTbls.items():
        lstHLines,lstVLines=tupLines[0],tupLines[1] # collecting horizontal and vertical lines
        lstHLinesAllTbls.extend(lstHLines)
        lstVLinesAllTbls.extend(lstVLines)
        lstHLinesComp,lstVLinesComp=tupLines[2],tupLines[3] #collecting horizontal and vertical lines 
        # lstHLinesComp=[[(lst[0][0],lst[0][1],515,lst[0][3])] for lst in lstHLinesComp]
        # debugLS(img,lstHLines,lstVLines,imgPth)
        imgShp=edges.shape
        lstIntersections=captureInteractions(lstHLines,lstVLines) # capture intersection points of every pair of horizontal and vertical lines
        lstIntersectionsComp=captureInteractions(lstHLinesComp,lstVLinesComp) # capture intersection points of every pair of horizontal and vertical lines
        debugPoints(img,lstIntersections,imgPth)
        
        diBbox=getBBox(lstIntersections,lstHLines,lstVLines) # capture bounding box using intersection points and lines
        diBboxComp=getBBox(lstIntersectionsComp,lstHLinesComp,lstVLinesComp)

        debugBbox(img,diBbox,imgPth)
        debugBbox(img,diBboxComp,imgPth)
        # lol=bboxesToTableOld(diBbox) # list of lists where each sublist represents one row of a table
        lol=bboxesToTable(diBbox,diBboxComp) # list of lists where each sublist represents one row of a table
        print('pg {}'.format(pgNo),lol)
        htmTbl,diSpanInfo=htmlTable(lol,pgNo) # converts lol to html table
        diTblsNew[tbl]={'diBbox':diBbox,'lol':lol,'htmTbl':htmTbl,'diSpanInfo':diSpanInfo,'imgShp':imgShp}
    debugLS(img,lstHLinesAllTbls,lstVLinesAllTbls,imgPth)
    return diTblsNew

