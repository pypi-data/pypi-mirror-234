from . import utils
import os
# os.chdir('UI')
pdf2htmlExePath=r'..\pdf2htmlEX-win32-0.14.6-upx-with-poppler-data\pdf2htmlEX.exe'
inpPath='tests/input'
outPath='tests/output'
skipConv=True
diSel={
    'tagsWithNoChildren':"..//page[@id='{0}']//*[@bbox and not(*)]",
    'imgTxtLn2':".//page[@id='{0}']//*[local-name()='textline' or local-name()='figure']",
    'pgChildrenTags':".//page[@id='{0}']/*",
    'rect':".//page[@id='{0}']//rect",
    'fig':".//page[@id='{0}']//figure",
    'textline':".//page[@id='{0}']//textline",
    'curve':".//page[@id='{0}']//curve",
    'line':".//page[@id='{0}']//line",
    'textbox':".//page[@id='{0}']//textbox",
    'textpg':".//text",
    'fig-curve-rect':".//page[@id='{0}']//*[self::curve or self::figure or self::rect]",
    }
imageDir=f'{outPath}/images'
pdfDir=inpPath
tmpDir=f'{outPath}/tmp'
pdfToImgToolPath=r"pdfbox/pdfbox-app-2.0.25.jar"

debugTable=False
createState=False
useState=False
isPdfTbl=True
tblTol=5
icTol=15
pdfTblMinLsLen=tblTol+1
tblMinLsLen=1
intraCLsLen=15
mrgdHLsLen=15
mrgdVLsLen=15
filtTol=5
eraseTol=tblTol-2
tblFltTol=tblTol-2
minTblOutBorder=50
minCellBorderLen=30
tblDebugExt='.png'
debugTblPath=f'{tmpDir}/table'
debugLsFNm='mylines'
debugPtsFNm='myPts'
debugIsectPtsFNm='myIsectPts'
debugLsBefEraseFNm='befEraseTags'
debugLsAftEraseFNm='aftEraseTags'
debugEdgesFNm='edges'
debugGrayFNm='gray'
debugImgFNm='temp_image'
debugLsAftJunkEraseFNm='aftEraseJunk'
eraseTags=['text']
tblCropPath=tmpDir+'table/crops/{}/'
debugCropLog=False
debugCrop=False
debugTblMainBbox=False
debugTblEraseJunk=False
debugTblImg=True
debugDiTbl=True
combineDbgImg=False
debugTime=False
debubTblTime=True
combineDf=True
customFilt=True
tblWithoutLn=False
extendTable=False
extendMainBbox=False
microEdges=False
combineTbls=False
tblApiPort='8088'
triageEdges=True
mongoConHost='localhost'
mongoConPort=27017