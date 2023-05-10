import sys
import re, os
import glob

def getSheetbyBatch(batch, sheetdir, stag="meta"):
    """
    通过目录批次名称, 获取上机的芯片号chipid, 用芯片号到到对应的samplesheet
    批次目录和samplesheet命名格式、日期都可能不一致, 只有芯片号chipid肯定是对应一致的
    stag是筛选完chipid的csv后, 再用stag字符筛选, 因为一个芯片号可能对应多个不同项目后缀的samplesheet
    """
    batchname = os.path.basename(batch)
    m = re.match("\d+_[A-Z0-9]+_\d+_([A-Z0-9]+)", batchname)
    if m:
        chipid = m.groups()[0]
        chipid = chipid[1:] #芯片号是批次名最后的字符
    else:
        chipid = batchname #没有匹配到chipid, 就用bathname.csv查找samplesheet
    #print(os.path.join(sheetdir, "*%s*.csv"%chipid))
    sheetcsv = glob.glob(os.path.join(sheetdir, "*%s*.csv"%chipid))
    #是否追加不同项目的samplesheet的过滤, 需要考虑不同子公司，不同项目的命名格式
    if stag:
        sheetcsv = [csv for csv in sheetcsv if re.search(stag, os.path.basename(csv), re.I)]
    if len(sheetcsv) == 0:
        return []
    elif len(sheetcsv) == 1:
        return sheetcsv[0]
    else:
        """如果还是有多个samplesheet, 取第一个csv"""
        bcsv = [os.path.basename(csv) for csv in sheetcsv]
        sys.stderr.write("Warnning: 存在多个芯片号相同的批次(默认取第一个), 请核查：%s" % bcsv)
        return sheetcsv[0]

if __name__ == "__main__":

    batch = sys.argv[1]
    sheetdir = sys.argv[2]
    stag = sys.argv[3]

    print(getSheetbyBatch(batch, sheetdir, stag=stag))
    

