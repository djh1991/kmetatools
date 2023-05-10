import sys, os, re
import pickle

def taxonomydb(taxdir=""):
    """
    下载物种分类库: https://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
    读取分类库:
        t2n_d: taxid和物种名科学命名对应关系, 主要从names.dmp获取
        t2t_d: taxid物种对应的分支层级和下个层级物种, 主要从nodes.dmp获取
    从merged.dump获取旧的taxid对应的上述信息
    从t2n_d和t2t_d导出taxid的lineage关系
    """
    t2n_d = {}
    with open(os.path.join(taxdir, "names.dmp"), 'r') as f:
        for line in f:
            cols = [l.strip() for l in line.split("|")]
            if cols[0] not in t2n_d.keys():
                t2n_d[cols[0]] = ["", []]
            if cols[3] == "scientific name":
                t2n_d[cols[0]][0] = cols[1]
            else:
                t2n_d[cols[0]][1].append(cols[1])
    sys.sterr.write("loads name.dmp: %s taxonomy\n" % len(t2n_d))

    t2t_d = {}
    with open(os.path.join(taxdir, "nodes.dmp"), 'r') as f:
        for line in f:
            cols = [l.strip() for l in line.split("|")]
            t2t_d[cols[0]] = [cols[1], cols[2]]
    sys.stderr.write("loads nodes.dmp: %s taxonomy\n" % len(t2t_d))

    cn = 0
    """补充被更新的旧的taxid信息"""
    with open(os.path.join(taxdir, "merged.dmp"), 'r') as f:
        for line in f:
            cn += 1
            cols = [l.strip() for l in line.split("|")]
            old_taxid, new_taxid = cols[:2]
            t2n_d[old_taxid] = t2n_d[new_taxid]
            t2t_d[old_taxid] = t2t_d[new_taxid]
    sys.stderr.write("loads merged.dmp: %s taxonomy\n" % cn)

    lineage_pkl = os.path.join(taxdir, "lineage.pkl")
    if os.path.exists(lineage_pkl):
        with open(lineage_pkl, 'rb') as fp:
            lineage_d = pickle.load(fp)
        sys.stderr.write("loads lineages:%s\n" % len(lineage_d))
    else:
        lineage_d = taxonomy_lineage_db(t2n_d, t2t_d)
        with open(lineage_pkl, 'wb') as fp:
            pickle.dump(lineage_d, fp)

    return t2n_d, t2t_d, lineage_d

def taxonomy_lineage(taxid, t2n_d, t2t_d):
    """获取taxid对应的完整的lineage关系"""
    if taxid in ["0", "A"]:
        return [["", "", ""]]


def taxonomy_lineage_db(t2n_d, t2t_d):
    """
    如果reads比较多，会重复调用taxonomy_lineage函数查询taxid的分类
    把所有taxid直接存入字典, 能提升查询速度
    """
