import sys, re, os
import pandas as pd

def checkSampleSheet(samplesheet, batch=""):
    """
    检查samplesheet格式是否正确，主要包括:
        1. 是否存在该samplesheet文件
        2. 是否是csv格式(excel二进制格式会报错)
        3. 样本/barcode是否重复
        4. 是否有中文(非ascii码值都会报错)
        5. 样本名是否有异常字符等
    """
    if not samplesheet or not os.path.exists(samplesheet):
        raise ValueError(f"未检索上传对应批次({batch})的samplesheet")
    sheetcsv = os.path.basename(samplesheet)
    info = {}
    with open(samplesheet, 'r', encoding="utf-8") as f:
        for ln, line in enumerate(f):
            """配中文, bcl2fastq不识别包含中文的samplesheet"""
            zhm = re.search("[\u4e00-\u9fa5]+", line)
            if zhm:
                raise ValueError('%s第%s行包含中文字符"%s"\n'%(sheetcsv, ln+1, zhm.group()))
            cols = [l.strip() for l in line.split(",")]
            m = re.match("\[(.*?)\]$", cols[0])
            if m:
                tag = m.groups()[0]
                info[tag] = []
            else:
                if cols[0] != "":
                    info[tag].append(cols)

    outcol = info["Data"][0]   #Data表头
    outdata = info["Data"][1:] #Data内容
    if len(outdata) == 0:
        raise ValueError(f"{sheetcsv}中未有任何样本记录")
    df = pd.DataFrame(outdata, columns=outcol)
    record_num = df.shape[0]
    
    """检查样本命名异常(包含异常字符)"""
    samples = list(df["Sample_ID"])
    err_samples = []
    for sp in samples:
        m = re.search("^[0-9a-zA-Z-]+$", sp)
        if not m:
            err_samples.append(sp)
    if err_samples:
        raise ValueError("%s中样本名(%s)包含不规范字符"%(sheetcsv, ",".join(err_samples)))
    
    """检查是否有重复样本"""
    from collections import Counter
    multi_samples = []
    for k, v in Counter(samples).items():
        if v > 1:
            multi_samples.append(k)
    if multi_samples:
        raise ValueError("%s中样本名(%s)重复"%(sheetcsv, ",".join(multi_samples)))
    
    """检查barcode index是否重复"""
    index_pairs = list(map(lambda x,y: x+"-"+y, df["index"], df["index2"]))
    multi_index = []
    for k, v in Counter(index_pairs).items():
        if v > 1:
            multi_index.append(k)
    if multi_index:
        raise ValueError("%s中barcode index pairs(%s)重复"%(sheetcsv, ",".join(multi_index)))

    return df

if __name__ == "__main__":
    input_sheetcsv = sys.argv[1]
    data = checkSampleSheet(input_sheetcsv)
    print(data)
