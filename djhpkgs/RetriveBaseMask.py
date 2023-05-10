import re, os, sys

def RetriveBaseMask(runinfoxml):
    """
    从下机RunInfo.xml文件中获取每次Cycle循环碱基长度
    RunInfo.xml中:
        IsIndexedRead=Y是接头碱基循环长度
        IsIndexedRead=N是测序片段循环长度
    """
    from xml.dom.minidom import parse
    import xml.dom.minidom
    DOMTree = xml.dom.minidom.parse(runinfoxml)
    collection = DOMTree.documentElement
    RM = collection.getElementsByTagName("Reads")[0]
    basemask = []
    for rm in RM.getElementsByTagName("Read"):
        NumCycles = rm.getAttribute("NumCycles")
        IsIndexedRead = rm.getAttribute("IsIndexedRead")
        if IsIndexedRead == "N":
            #basecalling需要去除末端碱基, 尤其是双色荧光测序，末端碱基无法区分C/G，必须去除
            basemask.append("y%sn"%(int(NumCycles)-1))
        else:
            basemask.append("I%s"%NumCycles)
    return ",".join(basemask)

if __name__ == "__main__":
    input_runinfo = sys.argv[1]
    print(RetriveBaseMask(input_runinfo))
