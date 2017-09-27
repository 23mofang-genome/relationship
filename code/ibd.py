#!/usr/bin/env python
# coding:utf-8
import sys, os
def help():
    sys.stderr.write('''
    USAGE:
    /usr/local/python27/bin/python IBD.py infile1 infile2 indexifle 
    ''')

def relationshipinsample(infile1,infile2,indexfile):
    with open(infile1,'r') as oper1:
        oper1arr=[ it1.rstrip() for it1 in  oper1.readlines()]

    with open(infile2,'r') as oper2:
        oper2arr=[ it2.rstrip() for it2 in oper2.readlines()]

    with open(indexfile,'r') as snpsort:
        snpsortarr=[it2.rstrip().split('_') for it2 in snpsort.readlines()]

    chr=1
    bpos=1
    halfsnp=0
    Tol=0
    log=[]
    chrLen=[0,249250621,243199373,198022430,191154276,180915260,171115067,159138663,146364022,141213431, 135534747, 135006516, 133851895, 115169878, 107349540, 102531392, 90354753, 81195210, 78077248, 59128983, 63025520, 48129895, 51304566]

    for idx in xrange(656418):
        #lines = oper1arr[idx]
        chrom=snpsortarr[idx][0]
        chromint=int(chrom)
        pos=int(snpsortarr[idx][1])
        positionint=pos
        gt=oper1arr[idx]
        othergt=oper2arr[idx]
        if chromint != chr:
            regionSize = chrLen[chr] - bpos
            if regionSize >= 7000000 and halfsnp >= 600:
                log.append(','.join([str(chr),str(bpos),str(chrLen[chr]),str(halfsnp)]))
                Tol+=regionSize
            bpos = 1
            halfsnp = 0
            chr=chromint

        if gt=='--' or othergt=='--':
            continue

        if len(gt)==3 and len(othergt)==3:
            if gt[0]!=othergt[0] and gt[0]!=othergt[-1] and gt[-1]!=othergt[0]  and gt[-1]!=othergt[-1]:
                regionSize = positionint - bpos
                if Tol >= 50000000:
                    threshold = 700
                else:
                    threshold = (regionSize / 7000000) * 800
                if regionSize >= 7000000 and halfsnp >= threshold:
                    log.append(','.join([chrom,str(bpos),str(pos),str(halfsnp)]))
                    Tol += regionSize
                    bpos = positionint
                    halfsnp = 0
                else:
                    bpos = positionint
                    halfsnp = 0
            else:
                halfsnp += 1
        else:
            if not set(gt.split("|")) & set(othergt.split("|")):
                regionSize = positionint - bpos
                if Tol >= 50000000:
                    threshold = 700
                else:
                    threshold = (regionSize / 7000000) * 800
                if regionSize >= 7000000 and halfsnp >= threshold:
                    log.append(','.join([chrom,str(bpos),str(pos),str(halfsnp)]))
                    Tol += regionSize
                    bpos = positionint
                    halfsnp = 0
                else:
                    bpos = positionint
                    halfsnp = 0
            else:
                halfsnp += 1

    r = Tol / 2881033286.0
    if r > 0:
        name1=os.path.splitext(os.path.basename(infile1.strip()))[0]
        name2=os.path.splitext(os.path.basename(infile2.strip()))[0]
        sys.stdout.write('\t'.join([name1,name2,str(r),'|'.join(log)])+'\n')

if __name__ == '__main__':
    length = len(sys.argv)
    if len(sys.argv)!=4:
        help()
        sys.exit(-1)

    infile1=sys.argv[1]
    infile2=sys.argv[2]
    indexfile=sys.argv[3]
    try:
        relationshipinsample(infile1,infile2,indexfile)
    except Exception,e:
        sys.stderr.write(e.message)
