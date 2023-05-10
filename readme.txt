一、 需要的python版本和包
    略
二、 配置文件
在metaconfig/中进行配置和一下个性化的初始化，方便调用配置中的变量值

有多种配置文件格式：
    ini:  section的键值对，无变量类型区别，参考/etc/samba/smb.conf
    json: 轻量级数据交换，javascript子集
    xml:  超文本标记，文件较大
    yaml：有标量数据形态和层次结构
    其他等
从中选择功能更全面更合适的yaml格式作配置文件格式

yaml配置文件中包含：
    相关应用软件的路径
    相关软件参数
    相关文件数据的目录地址    
    相关邮件地址
    等

三、 下机数据BaseCalling
basecalling/中：
*.donelist文件是相关项目的批次记录(已经成功执行basecalling)
需要把meta.pth加入到/mnt/turbo_meta/soft/anaconda3/lib/python3.9/site-packages/中, 即把当前目录加入python环境中,方便此目录下的模块包的导入

功能：
1. 根据下机批次名称的芯片号(ChipID),自动匹配获取实验上机信息表目录下该批次的samplesheet
2. 对samplesheet进行初步的格式内容检查, 防止中文,异常命名的样本和重复的index等错误
3. 判断下机批次的basecalling状态(未开始,执行中,出错,完成), 决定是否重新执行,并做好相关信息记录
    未开始：输出目录没有log日志，生成bcl2fastq.sh并提交任务
    执行中：输出目录有lock文件，跳过
    出错：  输出目录中的log日志中有ERROR，kill任务id(任务可能还在执行过程中一直卡住不退出), 重命名log日志(重命名日志文件不超过一定数量, 以防无限重复执行, 比如100个日志文件), 之后再生成bcl2fastq.sh并提交任务
    完成：  输出目录中有bcl2fastq.success.done文件, 把该批次下机路径记录到donefile文件中，然后跳过
4. 脚本程序lock锁定，保证任务不会重复提交执行


四、 分析步骤

思路：从basecalling下机目录开始获取样本信息, 每个分析步骤代码相互独立，同时又可以相互关联

1. 质控过滤(clean)
2. 去除宿主序列
3. 比对物种库
使用kraken比对, 使用所有的genbank物种建库

***Q1: 检测到去人源的fastq太大, 影响其他批次样本分析怎么办？
******S1: 把大的fastq放到最后导入

4. 结果统计分析
5. 整理报告
6. 数据清理于备份
7. 邮件发送
