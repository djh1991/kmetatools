import sys, os, re

def getSamplesByFqdir(fqdir, 
    pstr = [  #pstre是不同命名格式下的fastq的匹配模式, 尽量按照下面几个规则命名fastq
        "(?P<name>.*?)_(?P<lane>S\d+_L\d+)_(?P<r>R[12])",  #slot lane
        "(?P<name>.*?)_(?P<lane>S\d+)_(?P<r>R[12])",       #slot槽
        "(?P<name>.*?)_(?P<lane>L\d+)_(?P<r>R[12])",       #lane
        #"^(?P<r>S.*?)_(?P<lane>L\d+)_(?P<name>.*?)\.",  #BGISEQ
        #"^\d+_GL\d+_[AB]_S[EP]\d+D_(?P<name>.*?)_(?P<lane>L\d+)", #Genlab
    ],
    suffixs = ["fastq.gz", ".fastq", ".fq", ".fq.gz"], 
    ):
    """根据不同的fastq命名格式, 正确匹配样本名称和fastq文件之间的关系"""
    samplefqdata = {}
    ps = [re.compile(ss) for ss in pstr]
    for fqfile in sorted(os.listdir(fqdir)):
        if not any(fqfile.endswith(suffix) for suffix in suffixs):
            continue
        fqfilepath = os.path.join(fqdir, fqfile)
        pm = [p.search(fqfile) for p in ps]
        if any(pm):
            m = [x for x in pm if x][0] #取第一个能匹配上的模式
            samplename = m.group('name')
            lane = m.group('lane')
            orient = m.group('r')
            if samplename not in samplefqdata:
                samplefqdata[samplename] = {}
            if lane not in samplefqdata[samplename].keys():
                samplefqdata[samplename][lane] = {}
            samplefqdata[samplename][lane][orient] = fqfilepath
        else:
            raise Exception(f"Error: can't match samples information from fastq files({fqfile})")                        
    return samplefqdata

if __name__ == "__main__":
    inputfqdir = sys.argv[1]
    import json
    data = getSamplesByFqdir(inputfqdir)
    print(json.dumps(data, indent=4))

        
