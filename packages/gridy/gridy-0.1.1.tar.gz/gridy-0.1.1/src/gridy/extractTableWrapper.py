from . import pdfExtractionUtils as pdfutil
import cv2
import lxml.html
from . import constants as cns
from . import extractTable1 as tblExt1
import pandas as pd
import re
from . import utils
import copy
from datetime import datetime
import os
from multiprocessing import Pool
import math
import numpy as np
import glob
import io

utils.makedr(cns.inpPath)
utils.makedr(cns.outPath)
utils.makedr(cns.imageDir)
utils.makedr(cns.tmpDir)
utils.makedr(cns.debugTblPath)

def combineTblsAcrosPg(diTbl,pages,stTxtLnBbx=None,endTxtLnBbx=None,ix=0):
    lstYMx=[lstTbls[0][1]['imgShp'][0] for pg,lstTbls in diTbl.items() if lstTbls]
    if not lstYMx:
        return [],[]
    else:
        yMx=lstYMx[0]
    stTxtLnBbx=pdfutil.translateBbox(list(stTxtLnBbx),yMx) if stTxtLnBbx else stTxtLnBbx
    endTxtLnBbx=pdfutil.translateBbox(list(endTxtLnBbx),yMx) if endTxtLnBbx else endTxtLnBbx
    
    firstPg=pages[0]
    if stTxtLnBbx:
        firstPgTbl=[(bbx,tbl) for bbx,tbl in diTbl[firstPg] if bbx[0]>=stTxtLnBbx[0]-1 and bbx[1]>=stTxtLnBbx[1]]
        if not firstPgTbl:
            firstPg=pages[1]
            firstPgTbl=diTbl[firstPg][ix]
        else:
            firstPgTbl=firstPgTbl[ix]
    else:
        firstPgTbl=diTbl[firstPg][-1] if diTbl[firstPg] else {}
    endPg=pages[-1]
    if endTxtLnBbx:
        endPgTbl=[(bbx,tbl) for bbx,tbl in diTbl[endPg] if bbx[0]<=endTxtLnBbx[0]]
        if not endPgTbl:
            endPg=pages[-2]
            endPgTbl=diTbl[endPg][ix]
        else:
            endPgTbl=endPgTbl[ix]
    else:
        endPgTbl=diTbl[endPg][0] if diTbl[endPg] else {}

    othPgTbl=[pgTbls[ix] if pgTbls else {} for pg,pgTbls in diTbl.items() if pg in list(range(firstPg+1,endPg))]
    if len(pages)>1:
        tblsNeeded=[firstPgTbl]+othPgTbl+[endPgTbl]
    else:
        tblsNeeded=[firstPgTbl]
    return map(list,zip(*[tup for tup in zip(range(firstPg,endPg+1),tblsNeeded) if tup[1]]))

def getDfPerTbl(pg,tblInfoTbl,diTagsPg):
    diBbox,lol,htmTbl,diSpanInfo,imgShp=tblInfoTbl['diBbox'],tblInfoTbl['lol'],tblInfoTbl['htmTbl'],tblInfoTbl['diSpanInfo'],tblInfoTbl['imgShp']
    diPdfBbox=pdfutil.imgBboxToPdfBboxMult(diBbox,imgShp[0])
    if cns.debugTable:
        bbxXml=pdfutil.getXmlInsideBboxMult(diPdfBbox,diTagsPg,text=True)
        # print('bbxXml',bbxXml)
        bbxXmlStr={bbx:"".join(lstTg) for bbx,lstTg in bbxXml.items()}
        header=[bbxXmlStr[bbx] for bbx in lol[0]]
    else:
        bbxXml=pdfutil.getXmlInsideBboxMult(diPdfBbox,diTagsPg)
        # bbxXmlStr={bbx:"".join(
        #     [lxml.html.tostring(tg).decode('utf-8') for tg in lstTg])
        #     for bbx,lstTg in bbxXml.items()}
        
        bbxXmlStr={bbx:"".join(
            [tg.decode('utf-8') if isinstance(tg,bytes) else lxml.html.tostring(tg).decode('utf-8') for tg in lstTg])
            for bbx,lstTg in bbxXml.items()}
        
        header=[pdfutil.getTagText(bbxXmlStr[bbx]) for bbx in lol[0]]

    htmlTbl=htmTbl.format(**{str(k):v for k,v in bbxXmlStr.items()})
    lstData=[[str({'id':{'pg':pg,'prntBbox':(bbx,diSpanInfo[bbx]['rSpan'],diSpanInfo[bbx]['cSpan'])},'data':bbxXmlStr[bbx]}) 
              for ix,bbx in enumerate(l)] for l in lol[1:]]
    df=pd.DataFrame(lstData,columns=header)
    return (htmlTbl,df)


def getDfPerPg(pg,tblsNeededPg,diTagsPg):
    tblsPg=[]
    for tblInfoTbl in tblsNeededPg:
        bbxTup=()
        if isinstance(tblInfoTbl,tuple):
            imgBbx=tblInfoTbl[0]
            maxY=tblInfoTbl[1]['imgShp'][0]
            ul=(imgBbx[0],imgBbx[1])
            lr=(imgBbx[2],imgBbx[3])
            pdfBbx=pdfutil.imgBboxToPdfBbox(ul,lr,maxY)
            bbxTup=(imgBbx,pdfBbx)
            tblInfoTbl=tblInfoTbl[1]
        tupFormats=getDfPerTbl(pg,tblInfoTbl,diTagsPg)
        tblsPg.append(tupFormats+bbxTup)
    return tblsPg

def getDf(diTagsF,tblsNeeded):
    diTbl={}
    for pg,tblInfoPg in tblsNeeded.items():
        print('creating df for page: {}'.format(pg))
        diTagsPg=dict(diTagsF[pg])
        diTbl[pg]=getDfPerPg(pg,tblInfoPg,diTagsPg)
    print('*****df creation done*****')
    return diTbl


def combineImages(fNm,pages):
    pattern=cns.tmpDir+'/'+'combined*.png'
    fileList=glob.glob(pattern)
    for filePath in fileList:
        os.remove(filePath)
    ranges=[pages[x:x+30] for x in range(0,len(pages),30)]
    for ixRng,rng in enumerate(ranges):
        uniqShapes=set((cv2.imread('{}table/{}-{}/mylines.png'.format(cns.tmpDir,fNm,pg)).shape for pg in rng))
        ySizeMax=max([shp[0] for shp in uniqShapes])
        xSizeMax=max([shp[1] for shp in uniqShapes])
        imCombined=None
        for ix,im in enumerate((cv2.imread('{}table/{}-{}/mylines.png'.format(cns.tmpDir,fNm,pg)) for pg in rng)):
            xDiff=xSizeMax-im.shape[1]
            yDiff=ySizeMax-im.shape[0]
            if xDiff==0:
                im1=im
            else:
                xDiffArr=np.full((im.shape[0],xDiff,3),255)
                im1=np.hstack((im,xDiffArr))
            if yDiff==0:
                im2=im
            else:
                yDiffArr=np.full((yDiff,xSizeMax,3),255)
                im2=np.vstack((im1,yDiffArr))
            if imCombined is None:
                imCombined=im2
            else:
                imCombined=np.append(imCombined,im2,axis=0)

        OutPath=cns.tmpDir+'/'+'combined{}.png'.format(ixRng)
        cv2.imwrite(OutPath,imCombined)

def extractTableMultiple(fNm,diXml,pgRng=(),pgLst=[],stTxtLnBbx=None,endTxtLnBbx=None,ix=0,imgBytes=None):
    diTags=pdfutil.parseMultiple(diXml,selKey='tagsWithNoChildren',text=False)
    pagesInFile=len(diTags[fNm].keys())
    diTagsF=diTags[fNm]
    pages=range(pgRng[0],pgRng[1]+1) if pgRng else pgLst if pgLst else diTagsF.keys()
    diTbl={}

    for pg in pages:
        diTagsPg=diTagsF[pg]
        diTblsPg=tblExt1.extractTable(fNm,pg,pagesInFile,diTagsPg,imgBytes=imgBytes)
        diTbl[pg]=sorted(diTblsPg.items(),key=lambda tup: (tup[0][1],tup[0][0]))
    print('####table extraction done####')

    if cns.combineDbgImg:
        combineImages(fNm,list(pages))
    diAllTblInfo={pg:[tup[1] for tup in lstTbl] for pg,lstTbl in diTbl.items()}
    diAllTbl=getDf(diTagsF,diAllTblInfo)
    debugDiTbl(diAllTbl,outFNm='allTbls')
    if cns.combineTbls:
        pagesNew,tblsNeeded=combineTblsAcrosPg(diTbl,list(pages),stTxtLnBbx=stTxtLnBbx,endTxtLnBbx=endTxtLnBbx,ix=ix)
        diTblsNeeded={tup[0]:[tup[1]] for tup in zip(pagesNew,tblsNeeded)}
        diTbl=getDf(diTagsF,diTblsNeeded)
    else:
        diTbl=getDf(diTagsF,diTbl)
    return diTbl

def debugDiTbl(diTbl,outFNm='diTbl'):
    if not cns.debugDiTbl:
        return
    fpth=utils.fpath_from_lst([cns.tmpDir,f"{outFNm}.html"])
    htm="<html><body>"+"<br><br>".join([tup[0] for pg,lstTup in diTbl.items() for tup in lstTup])+"</body></html>"
    
    with open(fpth,'w',encoding="utf-8",errors="backslashreplace") as fp:
        fp.write(htm)

def debugDf(diTbl,fullTbl):
    fullTbl=fullTbl.fillna('')
    lstRows=[]
    lol=[]
    for ix,rowTup in list(enumerate(fullTbl.iterrows())):
        row=rowTup[1]
        rowNew={colNm:pdfutil.getTagText(eval(colVal)['data']) if eval(colVal)['data'] else eval(colVal)['data'] for colNm,colVal in row.items(0)}
        lol.append(list(rowNew.values()))
        lstRows.append(rowNew)
    df=pd.DataFrame(lstRows)
    tblString='''<table border="1"><tbody><thead>{}</thead>'''.format("<td>"+"</td><td>".join(df.columns)+"</td>")
    for row in lol:
        trString=r'''<tr style="height: 15.0pt;">'''
        for elm in row:
            tdString=r'''<td>{}</td>'''
            tdStrig=tdString.format(elm)
            trString+=tdString
        trString+='''</tr>'''
        tblString+=trString
    tblString+='''</tbody></table>'''

    fpth=utils.fpath_from_lst([cns.tmpDir,f"fnlTbl.html"])
    with open(fpth,'wb') as fp:
        fp.write(tblString.encode('utf-8'))
    return tblString,df

def extractTableFromLoc(fNm,diXml,diPages):
    diTags=pdfutil.parseMultiple(diXml,selKey='tagsWithNoChildren',text=False)
    pagesInFile=len(diTags[fNm].keys())
    diTagsF=diTags[fNm]
    diTbl={}
    for pg,lstLoc in diPages.items():
        diTagsPg=diTagsF[pg]
        diTblsPg=tblExt1.extractTable(fNm,pg,pagesInFile,diTagsPg,tblBbox=lstLoc)
        diTbl[pg]=[(tbl,diTblsPg[tbl]) for tbl in lstLoc]
    diAllTblInfo={pg:[tup[1] for tup in lstTbl] for pg,lstTbl in diTbl.items()}
    diAllTbl=getDf(diTagsF,diAllTblInfo)
    debugDiTbl(diAllTbl,outFNm='allTbls')
    return diAllTbl

def extractTableMultipleMultiProc(fNm,diXml,pgRng=(),pgLst=[],stTxtLnBbx=None,endTxtLnBbx=None,ix=0):
    diTags=pdfutil.parseMultiple(diXml,selKey='pgChildrenTags',text=False)
    pagesInFile=len(diTags[fNm].keys())
    diTagsF=diTags[fNm]
    pages=range(pgRng[0],pgRng[1]+1) if pgRng else pgLst if pgLst else diTagsF.keys()
    diTbl={}
    tasks=[]
    for pg in pages:
        diTagsPg=diTagsF[pg]
        tasks.append((fNm,pg,pagesInFile,{}))
    pool=Pool(processes=8)
    results=pool.starmap(tblExt1.extractTable,tasks)
    for pg,res in zip(pages,results):
        diTbl[pg]=sorted(res.items(0,key=lambda tup: (tup[0][1],tup[0][0])))
    pagesNew,tblsNeeded=combineTblsAcrosPg(diTbl,list(pages),stTxtLnBbx=stTxtLnBbx,endTxtLnBbx=endTxtLnBbx,ix=ix)
    diTbl=getDf(pagesNew,diTagsF,tblsNeeded)
    return diTbl

def frmTxtToTxtLn(lstTxtTg):
    di={}
    for txtTg in lstTxtTg:
        di.setdefault(txtTg[0][1],[]).append(txtTg[1][1])
    return [tup[1] for tup in sorted(di.items(),key=lambda tup: tup[0],reverse=True)]

def combineDfs(diTbl):
    def joinContinuedRows(fullTbl):
        refFntSz='10.524'
        refFntCls='UHCSans-Bold'
        newRows=[]
        ixSlice=0
        flag=True
        newRow=pd.Series()
        while(flag):
            for ix, rowTup in list(enumerate(fullTbl.iterrows()))[ixSlice:]:
                row=rowTup[1]
                if not eval(row[0])['data']:
                    newRow={
                        colNm:str({'id':eval(colVal)['id'],'data':eval(colVal)['data']+eval(row[colNm])['data']}) for
                        colNm,colVal in newRow.items()} if ix!=0 else row
                    continue
                xmlTr=lxml.html.fromstring(eval(row[0])['data'])
                lstTxtTg=pdfutil.parseTree(xmlTr,selKey='textPg')
                lstTxtLn=frmTxtToTxtLn(lstTxtTg)

                lstTxtLn=[txtLn for txtLn in lstTxtLn if re.sub('\n+','',''.join([tg.xpath('normalize-space(.)') for tg in txtLn]))!='']
                if not lstTxtLn:
                    newRow={
                        colNm:str({'id':eval(colVal)['id'],'data':eval(colVal)['data']+eval(row[colNm])['data']}) for
                        colNm,colVal in newRow.items()}
                    continue
                firstTxtLn=lstTxtLn[0]
                lstFntSz=list(set([tg.xpath('string(./@size)') for tg in firstTxtLn]))
                lstFntCls=list(set([tg.xpath('string(./@font)') for tg in firstTxtLn]))
                # if not (len(lstFntCls)==1 and lstFntCls[0]==refFntCls and len(lstFntSz)==1 and lstFntSz[0]==refFntSz):
                if not (len(lstFntCls)==1 and lstFntCls[0]==refFntCls and len(lstFntSz)==1):
                    if (isinstance(newRow,dict)):
                        newRow=pd.Series(newRow)
                    if newRow.empty:
                        newRow=row
                        continue
                    newRow={colNm:str({'id':eval(colVal)['id'],'data':eval(colVal)['data']+eval(row[colNm])['data']}) for colNm,colVal in newRow.items()}
                # elif (len(lstFntCls)==1 and lstFntCls[0]==refFntCls and len(lstFntSz)==1 and lstFntSz[0]==refFntSz):
                elif (len(lstFntCls)==1 and lstFntCls[0]==refFntCls and len(lstFntSz)==1):
                    if (isinstance(newRow,dict)):
                        newRow=pd.Series(newRow)
                    if not newRow.empty:
                        newRows.append(newRow)
                    newRow=row
                    ixSlice=ix+1
                    break
            else:
                newRows.append(pd.Series(newRow))
                flag=False
        dfNew=pd.DataFrame(newRows)
        return dfNew

    fullTbl=pd.concat([tup[1] for pg,lstTbl in diTbl.items() for tup in lstTbl])
    nCols=len(fullTbl.columns)
    if len(set(fullTbl.columns))<nCols:
        newCols=[''.join(map(str,tup)) for tup in zip(['col']*nCols,range(nCols))]
        fullTbl.columns=newCols
    fullTbl=joinContinuedRows(fullTbl)
    return fullTbl


def findAllTables(fNm,diOut=None,pdfDir=None):
    lstFiles=[fNm]
    if not diOut:
        diOut=pdfutil.convertMultiple(lstFiles)
    fpth=utils.fpath_from_lst([cns.tmpDir,f"{fNm}.xml"])
    with open(fpth,'wb') as fp:
        fp.write(diOut[fNm]+b'</pages>')
    numPages=len(lxml.html.fromstring(diOut[fNm]).xpath('//page'))
    st=datetime.now()
    pdfutil.pdfToImgPDFBox(fNm,1,numPages,pdfDir=pdfDir)
    print('Time Taken in Image Conversion:',(datetime.now()-st).seconds)
    st=datetime.now()
    diTbl=extractTableMultiple(fNm,diOut)
    print('Time Taken in Table Extraction:',(datetime.now()-st).seconds)
    debugDiTbl(diTbl,outFNm='diTbl_'+fNm)
    return diTbl
    
def findAllTablesNew(fNm,diOut=None,pdfDir=None,imgBytes=None):
    lstFiles=[fNm]
    if not diOut:
        diOut=pdfutil.convertMultiple(lstFiles)
    st=datetime.now()
    print('Time Taken in Image Conversion:',(datetime.now()-st).seconds)
    st=datetime.now()
    diTbl=extractTableMultiple(fNm,diOut,imgBytes=imgBytes)
    print('Time Taken in Table Extraction:',(datetime.now()-st).seconds)
    debugDiTbl(diTbl,outFNm='diTbl_'+fNm)
    return diTbl

def parseXmlMultApi(diOut,funcInp):
    diTags=pdfutil.parseMultiple(diOut,selKey=funcInp['selKey'],text=funcInp['text'])
    diTagsNew={}
    for fNm,diPg in diTags.items():
        for pgNm,lstTags in diPg.items():
            for tgTup in lstTags:
                bbx=tgTup[0]
                tgInfo=tgTup[1]
                tgTyp,tgObj=tgInfo[0],tgInfo[1]
                tgObjStr=lxml.html.tostring(tgObj)
                diTagsNew.setdefault(fNm,{}).setdefault(pgNm,[]).append((bbx,(tgTyp,tgObjStr)))
    return diTagsNew



def triggr(bytsorfp,fnm):
    if isinstance(bytsorfp,(io.BufferedReader,io.BytesIO)):
        br=io.BufferedReader(bytsorfp)
        outPth=utils.fpath_from_lst([cns.inpPath,fnm])
        with open(outPth,'wb') as fp:
            fp.write(br.read())
    fstem=utils.get_stem(fnm)
    lstFiles=[fstem]

    diOut=pdfutil.convertMultiple(lstFiles)
    fpth=utils.fpath_from_lst([cns.tmpDir,f"{fstem}.xml"])
    with open(fpth,'wb') as fp:
        fp.write(diOut[fstem]+b'</pages>')
    numPages=len(lxml.html.fromstring(diOut[fstem]).xpath('//page'))
    pdfutil.pdfToImgPDFBox(fstem,1,numPages)
    # pdfutil.pdfToImg(fstem,1,numPages)
    st=datetime.now()
    diTbl=extractTableMultiple(fstem,diOut)
    debugDiTbl(diTbl)
    pdfutil.debugTimeTaken(st,datetime.now(),'Table Extraction',debug=True)
    
if __name__=='__main__':
    # temp()
    # exit()
    
    fNm='pdfwithtbl'
    pageNo=1
    lstFiles=[fNm]
    diOut=pdfutil.convertMultiple(lstFiles)
    fpth=utils.fpath_from_lst([cns.tmpDir,f"{fNm}.xml"])
    with open(fpth,'wb') as fp:
        fp.write(diOut[fNm]+b'</pages>')
    numPages=len(lxml.html.fromstring(diOut[fNm]).xpath('//page'))
    pdfutil.pdfToImgPDFBox(fNm,1,numPages)
    # pdfutil.pdfToImg(fNm,1,numPages)
    st=datetime.now()
    diTbl=extractTableMultiple(fNm,diOut)
    # diTbl=extractTableMultipleMultiProc(fNm,diOut,pgRng=(1,52))
    # diTbl=extractTableMultiple(fNm,diOut,pgRng=(77,129))
    # diPages={1:[(40,293,1240,497)]}
    # diTbl=extractTableFromLoc(fNm,diOut,diPages)
    # diPagesPdfBbx={1:[(24.5,181.8,564.224,236.8),(24.5,142.9,570.34,170.4)]}
    # diPagesPdfBbx={1:[(264.384,546.382,573.988,575.818)]}
    # diPagesImgBbx={}
    # imgMaxY=1650
    # for pg,lstPdfBbx in diPagesPdfBbx.items():
    #     diPagesImgBbx[pg]=[pdfutil.translateBbox(list(pdfBbx),imgMaxY) for pdfBbx in lstPdfBbx]
    # diTbl=extractTableFromLoc(fNm,diOut,diPagesImgBbx)

    # print(diTbl)
    debugDiTbl(diTbl)
    pdfutil.debugTimeTaken(st,datetime.now(),'Table Extraction',debug=True)
    exit(0)
    if cns.combineDf:
        fnlTbl=combineDfs(diTbl)
        dfHtm,dfTxt=debugDf(diTbl,fnlTbl)
    pdfutil.debugTimeTaken(st,datetime.now(),'Table Extraction',debug=True)
    exit(0)
    diTags=pdfutil.parseMultiple(diOut,selKey='figure',text=False)# {'f1':{1:[((ulx,uly,lrx,lry):rect),((1,2,3,4):rect)]}}
    justPgNo=utils.lJustPgNo(pageNo)
    diTagsPg=dict(diTags[fNm][pageNo])
    pgBbox=diTagsPg.keys()
    imgFNm='{0}-{1}.png'.format(fNm,justPgNo)
    diBbox={imgFNm:pgBbox}
    pdfutil.cropMultiFiles(diBbox)
    img=cv2.imread(r'{0}{1}'.format(cns.imageDir,imgFNm))

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgShp=gray.shape
    sampleImgBboxs={(130,268):(580,373),(580,268):(880,373),(880,268):(1180,373)}
    diPdfBbox=pdfutil.imgBboxToPdfBboxMult(sampleImgBboxs,imgShp[0])
    textInsideBbox=pdfutil.getXmlInsideBboxMult(diPdfBbox.value(),diTagsPg)
    print(textInsideBbox)

