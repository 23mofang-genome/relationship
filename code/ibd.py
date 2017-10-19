#!/usr/bin/env python
# coding:utf-8
import sys, os, select, StringIO, gzip
def help():
    sys.stderr.write('''
    USAGE:
    python IBD.py ./testdata/111-1173-9987.sfs ./testdata/111-1175-1798.sfs ./snpsort.s

    Or you can alse use STDIN which separated by string "separator":
    cat ./testdata/111-1173-9987.sfs ./testdata/separator.txt ./testdata/111-1175-1798.sfs ./testdata/separator.txt ./snpsort.s ./testdata/separator.txt ./testdata/filenames.txt | python ibd.py

''')

def relationshipinsample(oper1arr, oper2arr, snpsortarr):

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
    if length == 1:
        # set a timeout 0.1s for the stdin
        rfds, _, _ = select.select([sys.stdin], [], [], 0.1)
        stringf = StringIO.StringIO(rfds[0].read())
        stringf.seek(0)
        decompressedFile = gzip.GzipFile(fileobj=stringf)
        data = decompressedFile.read()
        try:
            part_list = data.split("separator")
        except IndexError:
            help()
            sys.stderr.write("empty stdin")
            sys.exit(-1)
        if len(part_list) == 3:
            oper1arr, oper2arr = tuple([x.split() for x in part_list[:2]])
            with open('/usr/bin/snpsort.s','r') as snpsort:
                snpsortarr=[it2.rstrip().split('_') for it2 in snpsort.readlines()]
            # global
            infile1, infile2 = tuple(part_list[2].split())
        else:
            sys.stderr.write("separate error: expected 3 part, found {0}".format(len(part_list)))
            sys.exit(-1)
    elif length == 4:
        # global
        infile1=sys.argv[1]
        infile2=sys.argv[2]
        indexfile=sys.argv[3]
        with open(infile1,'r') as oper1:
            oper1arr=[ it1.rstrip() for it1 in  oper1.readlines()]

        with open(infile2,'r') as oper2:
            oper2arr=[ it2.rstrip() for it2 in oper2.readlines()]

        with open('./snpsort.s','r') as snpsort:
            snpsortarr=[it2.rstrip().split('_') for it2 in snpsort.readlines()]

    try:
        relationshipinsample(oper1arr, oper2arr, snpsortarr)
    except Exception, e:
        sys.stderr.write(e.message)
