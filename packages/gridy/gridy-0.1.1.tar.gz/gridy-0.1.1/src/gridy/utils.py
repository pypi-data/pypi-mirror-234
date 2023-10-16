from pathlib import Path
import io

def get_fpath(strpth):
    return Path(strpth)

def fpath_from_lst(lst,psx=False,both=False):
    pth=Path(*lst)
    pxp=pth.as_posix()
    if both:
        return pth,pxp
    elif psx:
        return pxp
    return pth

def makedr(pth):
    Path(pth).mkdir(parents=True,exist_ok=True)

def abslute(pth,psx=False):
    abspth=get_fpath(pth).resolve()
    if psx:
        abspth=posixp(abspth)
    return abspth

def posixp(pth):
    return Path(pth).as_posix()

def lJustPgNo(pgNo,nop):
    return str(pgNo).zfill(len(str(nop)))

def get_bio(byts=b'',fnm="temp.txt",buff=False):
    fobj=io.BytesIO(byts)
    if fnm:
        fobj.name=fnm
    fobj.seek(0)
    if buff:
        return io.BufferedReader(fobj)
    return fobj

def get_sfx(fpth):
    return get_fpath(fpth).suffix

def get_stem(fpth):
    return get_fpath(fpth).stem

def get_fname(fpth):
    return get_fpath(fpth).name