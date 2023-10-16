import json

def rbuild(tr,lvl,lst):
    ix=0
    curr=tr
    while True:
        ix+=1
        if ix>=lvl:
            break
        curr=curr[-1]
    curr.append([lst[1]])
    return tr

def editctx(ctx,inp):
    inters=list(zip(ctx[:-1],ctx[1:]))
    for ix,tup in enumerate(inters):
        if inp[-1]>=tup[0][-1]:
            ctx=ctx[:ix]+[inp]
            break
        elif tup[0][-1]>inp[-1]>=tup[1][-1]:
            ctx=ctx[:ix+1]+[inp]
            break
    else:
        ctx=ctx+[inp]
    return ctx

def buildtree(lst,debgr=None):
    first=1
    ctx=[]
    tr=[]
    dbgtr=[]
    curr=[]
    lvl=0
    for tup in lst:
        sztup,txt=tup
        if first:
            prev=sztup
            ctx.append(sztup)
            first=0
        dif=sztup[-1]!=prev[-1]
        if dif:
            tr=rbuild(tr,lvl,[prev,curr])
            if debgr:
                dbgtr=rbuild(dbgtr,lvl,[prev,debgr(curr)])
            ctx=editctx(ctx,sztup)
            lvl=len(ctx)
            curr=[{str(sztup):txt}]
        else:
            curr.append({str(sztup):txt})
        prev=sztup

    if curr:
        tr=rbuild(tr,lvl,[prev,curr])
        if debgr:
            dbgtr=rbuild(dbgtr,lvl,[prev,debgr(curr)])
    
    return tr,dbgtr

def getxml(lst):
    xm=[v if v in ['<table>','</table>','<tr>','</tr>','<td>','</td>'] else f'<ln>{v}</ln>' for di in lst for k,v in di.items()]
    return xm

def rparse(tr,lst):
    for sect in tr:
        # print('\n=====start=========\n',json.dumps(sect,indent=2),'\n=======end=======\n')
        if len(sect)>2:
            lst.append('<sect><head>')
            shead=getxml(sect[0])
            lst.extend(shead)
            lst.append('</head><body>')
            rparse(sect[1:],lst)
            lst.append('</body></sect>')
        elif len(sect)==2:
            # print('\n>>>>start<<<<<<\n',json.dumps(sect,indent=2),'\n>>>>>>>end<<<<<\n')    
            lst.append('<sect><head>')
            shead=getxml(sect[0])
            lst.extend(shead)
            lst.append('</head>')
            if len(sect[1])==2:
                rparse(sect[1:2],lst)
            else:
                lst.append('<body>')
                sbody=getxml(sect[1][0])
                lst.extend(sbody)
                lst.append('</body>')
            lst.append('</sect>')
        else:
            lst.append('<sect><body>')
            sbody=getxml(sect[0])
            lst.extend(sbody)
            lst.append('</body></sect>')