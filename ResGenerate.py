#coding=utf-8
# 用途：自动生成 资源头文件脚本
# 用法：ResGenerate.py C:\Users\DK\Desktop\LhTestGame\Resources\scene  SceneRes.h *.png *.jpg"
# 版本：v0.2
# 更改: 2015-1-20 v0.1 创建脚本，实现自动生成资源文件功能
#		2015-1-21 v0.2 修复cmd输出乱码 增在中文编码转换(.decode('utf-8').encode('gbk'))
#		2015-1-21 v0.3 os.path.sep 添加多平台路径分隔符支持
#		2015-1-26 v0.4 fix 只处理了.png文件扩展名问题，根据传入的正则字符串处理
#       2015-2-03 v0.5 支持递归
import sys
import os
import glob
import time

#获取脚本文件的当前路径

def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]

    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径

    if os.path.isdir(path):
        return path

    elif os.path.isfile(path):
        return os.path.dirname(path)
    
#打印结果
print "当前路径脚本：".decode('utf-8').encode('gbk'),cur_file_dir()

if (len(sys.argv)<3):
    print "参数个数错误 必须输入三个参数以上 参数（包括三个） ".decode('utf-8').encode('gbk')
    print "用法：ResGenerate.py [-r（可选项 是否递归）] [path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "或者：python ResGenerate.py -r [path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "例如：[python(可选项)] ResGenerate.py -r C:\Users\DK\Desktop\LhTestGame\Resources\scene  SceneRes.h *.png *.jpg".decode('utf-8').encode('gbk')
    sys.exit(1)

arg_index=2	
path=sys.argv[1]
name=sys.argv[2]
matches=[]
recursive=False
if (sys.argv[1]=='-r'):
    print "递归调用"
    path=sys.argv[2]
    name=sys.argv[3]
    arg_index=3
    recursive=True

 

index=0
for element in sys.argv:
    if(index>arg_index):
        matches.append(element)
    index+=1

if os.path.exists(path):
    print "path=".decode('utf-8').encode('gbk'),path,"路径存在".decode('utf-8').encode('gbk')
    print ".....脚本执行中.....".decode('utf-8').encode('gbk')
else:
    print "path=".decode('utf-8').encode('gbk'),path,"路径不存在".decode('utf-8').encode('gbk')
    print "用法：ResGenerate.py [-r（可选项 是否递归）][path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "或者：python ResGenerate.py -r [path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "例如：[python(可选项)] ResGenerate.py -r C:\Users\DK\Desktop\LhTestGame\Resources\scene  SceneRes.h *.png *.jpg".decode('utf-8').encode('gbk')
    sys.exit(1)
    
if (len(matches)>0):
    print "存在正则匹配参数 matches=".decode('utf-8').encode('gbk'),matches
else:
    print "不存在正则匹配参数 matches=".decode('utf-8').encode('gbk'),matches
    print "用法：ResGenerate.py [-r（可选项 是否递归）] [path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "或者：python ResGenerate.py -r [path] [name] [matches ...]".decode('utf-8').encode('gbk')
    print "例如：[python(可选项)] ResGenerate.py -r C:\Users\DK\Desktop\LhTestGame\Resources\scene  SceneRes.h *.png *.jpg".decode('utf-8').encode('gbk')
    sys.exit(1)
        

	
out=path+"\\"+name
definstr="_"+name.replace('.h','').upper()+"_H_"
# 写入文件头
file_object = open(out, 'w') 
file_object.write("/*\n * Create By:  本文件由ResGenerate.py自动生成\n * Create on:  "+time.strftime('%Y-%m-%d',time.localtime(time.time()))
+"\n * Author	:  D.K.\n * Blog		:  darklost.me\n */\n\n\n");
file_object.write("#ifndef  "+definstr+"\n#define  "+definstr+"\n\n\n\n\n") 

def deal_filename(filename,matches):
        outLine="static const char * g_"
        fileSplitList=filename.split("Resources"+os.path.sep )
        fileEndName=fileSplitList[-1]
        g_name=os.path.basename(fileEndName)
        outLine+=g_name.replace(matches.replace('/*',''),' ')
        outLine+='= "'
        outLine+=fileEndName.replace('\\','/')
        outLine+='";\n\n'
        return outLine

def get_match_file(path,matches):
        list_file=[]
        if recursive:
            for root , dirs , files in os.walk(path):
                for filename in files:
                    fileFullName=os.path.join(root,filename)
                    print "file=".decode('utf-8').encode('gbk')+fileFullName
                    if(fileFullName.endswith(matches.replace('/*',''))):
                        outLine=deal_filename(fileFullName,matches)
                        list_file.append(outLine)
                        print "outLine=".decode('utf-8').encode('gbk')+outLine.replace('\n','')
                    print '\n'
        else:
            for filename in glob.glob(path+matches):
                print "file=".decode('utf-8').encode('gbk')+filename
                outLine=deal_filename(filename,matches)
                list_file.append(outLine)
                print "outLine=".decode('utf-8').encode('gbk')+outLine.replace('\n','')
                print '\n'
        return list_file
    

# 文件列表
list_file=[]
print "Test=", matches[0].replace('*','')
# 遍历所有正则匹配文件
for match in matches:
    print "....开始匹配文件类型：".decode('utf-8').encode('gbk')+match
    list_file.extend(get_match_file(path, "/"+match))
    print "....结束匹配文件类型：".decode('utf-8').encode('gbk')+match+"\n"

# file_object = open(out, 'w+') 
file_object.writelines(list_file)
file_object.write("\n\n\n#endif //"+definstr)
file_object.close( )
print "总计资源数量".decode('utf-8').encode('gbk'),len(list_file)
print ".....脚本执行完毕.....".decode('utf-8').encode('gbk')

    

    


