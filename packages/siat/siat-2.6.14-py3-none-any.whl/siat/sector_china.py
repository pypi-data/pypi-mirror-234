# -*- coding: utf-8 -*-
"""
本模块功能：中国行业板块市场分析
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年10月20日
最新修订日期：2020年10月21日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
版权所有：王德宏
用途限制：仅限研究与教学使用，不可商用！商用需要额外授权。
特别声明：作者不对使用本工具进行证券投资导致的任何损益负责！
"""

#==============================================================================
#关闭所有警告
import warnings; warnings.filterwarnings('ignore')
from siat.common import *
from siat.translate import *
from siat.bond_base import *
from siat.stock import *
from siat.risk_adjusted_return import *
from siat.financials_china2 import *
#==============================================================================

if __name__=='__main__':
    indicator="新浪行业"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"

def sector_list_china(indicator="新浪行业"):
    """
    功能：行业分类列表
    indicator="新浪行业","启明星行业","概念","地域","行业"
    来源网址：http://finance.sina.com.cn/stock/sl/#qmxindustry_1
    """
    #检查选项是否支持
    indicatorlist=["新浪行业","概念","地域","行业","启明星行业"]
    if indicator not in indicatorlist:
        print("#Error(sector_list_china): unsupported sectoring method",indicator)
        print("Supported sectoring methods:",indicatorlist)
        return None
    
    import akshare as ak
    try:
        df = ak.stock_sector_spot(indicator=indicator)
        
        #去掉空格，否则匹配容易失败
        df['板块']=df['板块'].apply(lambda x: x.strip())   
        df['label']=df['label'].apply(lambda x: x.strip())
        
    except:
        print("  #Error(sector_list_china): data source tentatively unavailable for",indicator)
        print("  Possible reason: data source is self-updating.")
        print("  Solution: have a breath of fresh air and try later.")
        return None
    
    sectorlist=list(df['板块'])
    #按照拼音排序
    sectorlist=list(set(list(sectorlist)))
    sectorlist=sort_pinyin(sectorlist)
    #解决拼音相同带来的bug：陕西省 vs 山西省
    if '陕西省' in sectorlist:
        pos=sectorlist.index('陕西省')
        if sectorlist[pos+1] == '陕西省':
            sectorlist[pos] = '山西省'
    if '山西省' in sectorlist:
        pos=sectorlist.index('山西省')
        if sectorlist[pos+1] == '山西省':
            sectorlist[pos+1] = '陕西省'
    listnum=len(sectorlist)
    
    if indicator != "行业":
        method=indicator
    else:
        method="证监会门类/大类"
    print("\n===== 中国股票市场的行业/板块:",listnum,"\b个（按"+method+"划分） =====\n")

    if indicator in ["新浪行业","启明星行业","概念"]:
        #板块名字长度
        maxlen=0
        for s in sectorlist:        
            l=strlen(s)
            if l > maxlen: maxlen=l
        #每行打印板块名字个数
        rownum=int(80/(maxlen+2))
        
        for d in sectorlist:
            if strlen(d) < maxlen:
                dd=d+" "*(maxlen-strlen(d))
            else:
                dd=d
            print(dd,end='  ')
            pos=sectorlist.index(d)+1
            if (pos % rownum ==0) or (pos==listnum): print(' ')    

    #if indicator in ["地域","行业"]:
    if indicator in ["地域"]:    
        linemaxlen=60
        linelen=0
        for d in sectorlist:
            dlen=strlen(d)
            pos=sectorlist.index(d)+1
            #超过行长
            if (linelen+dlen) > linemaxlen:
                print(' '); linelen=0
            #是否最后一项
            if pos < listnum:
                print(d,end=', ')
            else:
                print(d+"。"); break
            linelen=linelen+dlen

    #证监会行业划分
    if indicator in ["行业"]:   
        df['csrc_type']=df['label'].apply(lambda x: x[8:9])
        csrc_type_list=list(set(list(df['csrc_type'])))
        csrc_type_list.sort()
        
        for t in csrc_type_list:
            dft=df[df['csrc_type']==t]
            sectorlist=list(dft['板块'])
            listnum=len(sectorlist)
            
            linemaxlen=80
            linelen=0
            print(t,end=': ')
            for d in sectorlist:
                dlen=strlen(d)
                pos=sectorlist.index(d)+1
                #超过行长
                if (linelen+dlen) > linemaxlen:
                    print(' '); linelen=0
                #是否最后一项
                if pos < listnum:
                    print(d,end=', ')
                else:
                    #print(d+"。"); break
                    print(d+" "); break
                linelen=linelen+dlen
            
            
    import datetime
    today = datetime.date.today()
    print("\n*** 信息来源：新浪财经,",today) 
    
    return df


#==============================================================================
if __name__=='__main__':
    sector_name="房地产"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"
    
    sector_name="煤炭"
    sector_code_china(sector_name)

def sector_code_china(sector_name):
    """
    功能：查找行业、板块名称对应的板块代码
    """
    import akshare as ak
    print("\n===== 查询行业/板块代码 =====")
    
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_code=''; found=0
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        
        #去掉空格，否则匹配容易失败
        dfi['板块']=dfi['板块'].apply(lambda x: x.strip())  
        dfi['label']=dfi['label'].apply(lambda x: x.strip())
        
        try:
            sector_code=list(dfi[dfi['板块']==sector_name]['label'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['板块']==sector_name]
            
            if found > 0: print(" ")
            if indicator == "行业": indicator = "证监会行业"
            print("行业/板块名称："+sector_name)
            print("行业/板块代码："+sector_code,end='')
            print(", "+indicator+"分类")
            found=found+1
        except:
            # 无意义，仅为调试
            x=1
            continue
    
    #未找到板块代码
    if found==0:
        print("  #Error(sector_code_china): unsupported sector name",sector_name)
        return 
    
    return 

if __name__=='__main__':
    sector_name="房地产"
    df=sector_code_china(sector_name)
    df=sector_code_china("医药生物")
    df=sector_code_china("资本市场服务")
    
#==============================================================================
if __name__=='__main__':
    comp="xxx"
    comp="涨跌幅"
    comp="成交量"
    comp="平均价格"
    comp="公司家数"
    
    indicator="+++"
    indicator="新浪行业"
    indicator="启明星行业"
    indicator="地域"
    indicator="行业"
    num=10

def sector_rank_china(comp="涨跌幅",indicator="新浪行业",num=10):
    """
    功能：按照比较指标降序排列
    comp="涨跌幅",平均价格，公司家数
    indicator="新浪行业","启明星行业","概念","地域","行业"
    num：为正数时列出最高的前几名，为负数时列出最后几名
    
    注意：公司家数字段最大值为100，是bug？
    """
    #检查选项是否支持
    #complist=["涨跌幅","成交量","平均价格","公司家数"]
    complist=["涨跌幅","平均价格","公司家数"]
    if comp not in complist:
        print("#Error(sector_rank_china): unsupported measurement",comp)
        print("Supported measurements:",complist)
        return None
    
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    if indicator not in indicatorlist:
        print("#Error(sector_list_china): unsupported sectoring method",indicator)
        print("Supported sectoring method:",indicatorlist)
        return None
    
    import akshare as ak
    try:
        df = ak.stock_sector_spot(indicator=indicator)  
        
        #去掉空格，否则匹配容易失败
        df['板块']=df['板块'].apply(lambda x: x.strip())   
        df['label']=df['label'].apply(lambda x: x.strip())
        
    except:
        print("#Error(sector_rank_china): data source tentatively unavailable for",indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return None
    
    df.dropna(inplace=True)
    #出现列名重名，强制修改列名
    df.columns=['label','板块','公司家数','平均价格','涨跌额','涨跌幅', \
                '总成交量(手)','总成交额(万元)','个股代码','个股涨跌幅','个股股价', \
                '个股涨跌额','个股名称']
    df['均价']=round(df['平均价格'].astype('float'),2)
    df['涨跌幅%']=round(df['涨跌幅'].astype('float'),2)
    #平均成交量:万手
    df['平均成交量']=(df['总成交量(手)'].astype('float')/df['公司家数'].astype('float')/10000)
    df['平均成交量']=round(df['平均成交量'],2)
    #平均成交额：亿元
    df['平均成交额']=(df['总成交额(万元)'].astype('float')/df['公司家数'].astype('float'))/10000
    df['平均成交额']=round(df['平均成交额'],2)
    stkcd=lambda x: x[2:]
    df['个股代码']=df['个股代码'].apply(stkcd)
    try:
        df['个股涨跌幅%']=round(df['个股涨跌幅'].astype('float'),2)
    except:
        pass
    try:
        df['个股股价']=round(df['个股股价'].astype('float'),2)
    except:
        pass
    try:
        df['公司家数']=df['公司家数'].astype('int')
    except:
        pass
    df2=df[['板块','涨跌幅%','平均成交量','平均成交额','均价', \
            '公司家数','label','个股名称','个股代码','个股涨跌幅','个股股价']].copy()
    df2=df2.rename(columns={'个股名称':'代表个股','label':'板块代码'})
    
    #删除无效的记录
    df2=df2.drop(df2[df2['均价'] == 0.0].index)
    
    if comp == "涨跌幅":
        df3=df2[['板块','涨跌幅%','均价','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['涨跌幅%'],ascending=False,inplace=True)
    """
    if comp == "成交量":
        df3=df2[['板块','平均成交量','涨跌幅%','均价','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['平均成交量'],ascending=False,inplace=True)
    """
    if comp == "平均价格":
        df3=df2[['板块','均价','涨跌幅%','公司家数','板块代码','代表个股']]
        df3.sort_values(by=['均价'],ascending=False,inplace=True)
    if comp == "公司家数":
        df3=df2[['板块','公司家数','均价','涨跌幅%','板块代码','代表个股']]
        df3.sort_values(by=['公司家数'],ascending=False,inplace=True)
    df3.reset_index(drop=True,inplace=True)
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    if indicator == "行业":
        indtag="证监会行业"
    else:
        indtag=indicator
    
    #处理空记录
    if len(df3) == 0:
        print("#Error(sector_rank_china):data source tentatively unavailable for",comp,indicator)
        print("Possible reason: data source is self-updating.")
        print("Solution: have a breath of fresh air and try later.")
        return
    
    df3.index=df3.index + 1
    print("\n===== 中国股票市场：板块"+comp+"排行榜（按照"+indtag+"分类） =====")
    if num > 0:
        print(df3.head(num))
    else:
        print(df3.tail(-num))
    
    import datetime
    today = datetime.date.today()
    footnote1="*注：代表个股是指板块中涨幅最高或跌幅最低的股票"
    print(footnote1)
    print(" 板块数:",len(df),"\b, 数据来源：新浪财经,",today,"\b（信息为上个交易日）") 

    return df3

#==============================================================================
if __name__=='__main__':
    sector="new_dlhy"
    sector="xyz"
        
    num=10

def sector_detail_china(sector="new_dlhy",comp="涨跌幅",num=10):
    """
    功能：按照板块内部股票的比较指标降序排列
    sector：板块代码
    num：为正数时列出最高的前几名，为负数时列出最后几名
    """
    debug=False

    #检查选项是否支持
    complist=["涨跌幅","换手率","收盘价","市盈率","市净率","总市值","流通市值"]
    if comp not in complist:
        print("  #Error(sector_detail_china): unsupported measurement",comp)
        print("  Supported measurements:",complist)
        return None
    
    #检查板块代码是否存在
    import akshare as ak
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_name=''
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        
        #去掉字符串中的空格，否则匹配容易失败
        dfi['板块']=dfi['板块'].apply(lambda x: x.strip()) 
        dfi['label']=dfi['label'].apply(lambda x: x.strip())
        
        if debug: print("i=",i)
        try:
            sector_name=list(dfi[dfi['label']==sector]['板块'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['label']==sector]
            break
        except:
            continue
    #未找到板块代码
    if sector_name == '':
        print("  #Error(sector_detail_china): unsupported sector code",sector)
        return
    
    #板块成份股
    try:
        df = ak.stock_sector_detail(sector=sector)
    except:
        print("  #Error(sector_rank_china): data source tentatively unavailable for",sector)
        print("  Possible reason: data source is self-updating.")
        print("  Solution: have a breath of fresh air and try later.")
        return None
    
    df.dropna(inplace=True)
    df['个股代码']=df['code']
    df['个股名称']=df['name']
    df['涨跌幅%']=round(df['changepercent'].astype('float'),2)
    df['收盘价']=round(df['settlement'].astype('float'),2)
    #成交量:万手
    df['成交量']=round(df['volume'].astype('float')/10000,2)
    #成交额：亿元
    df['成交额']=round(df['amount'].astype('float')/10000,2)
    df['市盈率']=round(df['per'].astype('float'),2)
    df['市净率']=round(df['pb'].astype('float'),2)
    #总市值：亿元
    df['总市值']=round(df['mktcap'].astype('float')/10000,2)
    #流通市值：亿元
    df['流通市值']=round(df['nmc'].astype('float')/10000,2)
    df['换手率%']=round(df['turnoverratio'].astype('float'),2)
    
    #删除无效的记录
    df=df.drop(df[df['收盘价'] == 0].index)
    df=df.drop(df[df['流通市值'] == 0].index)
    df=df.drop(df[df['总市值'] == 0].index)
    df=df.drop(df[df['市盈率'] == 0].index)
    
    df2=df[[ '个股代码','个股名称','涨跌幅%','收盘价','成交量','成交额', \
            '市盈率','市净率','换手率%','总市值','流通市值']].copy()
    
    if comp == "涨跌幅":
        df3=df2[['个股名称','个股代码','涨跌幅%','换手率%','收盘价','市盈率','市净率','流通市值']]
        df3.sort_values(by=['涨跌幅%'],ascending=False,inplace=True)
    if comp == "换手率":
        df3=df2[['个股名称','个股代码','换手率%','涨跌幅%','收盘价','市盈率','市净率','流通市值']]
        df3.sort_values(by=['换手率%'],ascending=False,inplace=True)
    if comp == "收盘价":
        df3=df2[['个股名称','个股代码','收盘价','换手率%','涨跌幅%','市盈率','市净率','流通市值']]
        df3.sort_values(by=['收盘价'],ascending=False,inplace=True)
    if comp == "市盈率":
        df3=df2[['个股名称','个股代码','市盈率','市净率','收盘价','换手率%','涨跌幅%','流通市值']]
        df3.sort_values(by=['市盈率'],ascending=False,inplace=True)
    if comp == "市净率":
        df3=df2[['个股名称','个股代码','市净率','市盈率','收盘价','换手率%','涨跌幅%','流通市值']]
        df3.sort_values(by=['市净率'],ascending=False,inplace=True)
    if comp == "流通市值":
        df3=df2[['个股名称','个股代码','流通市值','总市值','市净率','市盈率','收盘价','换手率%','涨跌幅%']]
        df3.sort_values(by=['流通市值'],ascending=False,inplace=True)
    if comp == "总市值":
        df3=df2[['个股名称','个股代码','总市值','流通市值','市净率','市盈率','收盘价','换手率%','涨跌幅%']]
        df3.sort_values(by=['总市值'],ascending=False,inplace=True)  
        
    df3.reset_index(drop=True,inplace=True)
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    df3.index=df3.index + 1
    print("\n=== 中国股票市场："+sector_name+"板块，成份股排行榜（按照"+comp+"） ===\n")
    if num > 0:
        print(df3.head(num))
    else:
        print(df3.tail(-num))
    
    import datetime
    today = datetime.date.today()
    footnote1="\n 注：市值的单位是亿元人民币, "
    print(footnote1+"板块内成份股个数:",len(df))
    print(" 数据来源：新浪财经,",today,"\b（信息为上个交易日）") 

    return df2

#==============================================================================
if __name__=='__main__':
    ticker='600021.SS'
    ticker='000661.SZ'
    ticker='999999.SS'
    sector="new_dlhy"
    sector="yysw"
    sector="xyz"

def sector_position_china(ticker,sector="new_dlhy"):
    """
    功能：查找一只股票在板块内的百分数位置
    ticker：股票代码
    sector：板块代码
    """
    ticker1=ticker[:6]
    
    import akshare as ak
    import numpy as np
    import pandas as pd    
    
    #检查板块代码是否存在
    indicatorlist=["新浪行业","概念","地域","启明星行业","行业"]
    sector_name=''
    for i in indicatorlist:
        dfi=ak.stock_sector_spot(indicator=i)
        
        #去掉空格，否则匹配容易失败
        dfi['板块']=dfi['板块'].apply(lambda x: x.strip())   
        dfi['label']=dfi['label'].apply(lambda x: x.strip())
        
        try:
            sector_name=list(dfi[dfi['label']==sector]['板块'])[0]
            #记录找到的板块分类
            indicator=i
            #记录找到的板块概述
            dff=dfi[dfi['label']==sector]
            break
        except:
            continue
    #未找到板块代码
    if sector_name == '':
        print("  #Error(sector_position_china): unsupported sector code",sector)
        return None
    
    #板块成份股
    try:
        #启明星行业分类没有成份股明细
        df = ak.stock_sector_detail(sector=sector)
    except:
        print("  #Error(sector_position_china): sector detail not available for",sector,'by',indicator)
        print("  Possible reason: data source is self-updating.")
        print("  Solution: have a breath of fresh air and try later.")
        return None

    #清洗原始数据: #可能同时含有数值和字符串，强制转换成数值
    df['changepercent']=round(df['changepercent'].astype('float'),2)
    df['turnoverratio']=round(df['turnoverratio'].astype('float'),2)
    df['settlement']=round(df['settlement'].astype('float'),2)
    df['per']=round(df['per'].astype('float'),2)
    df['pb']=round(df['pb'].astype('float'),2)
    df['nmc']=round(df['nmc'].astype('int')/10000,2)
    df['mktcap']=round(df['mktcap'].astype('int')/10000,2)
    
    #检查股票代码是否存在
    sdf=df[df['code']==ticker1]
    if len(sdf) == 0:
        print("  #Error(sector_position_china): retrieving",ticker,"failed in sector",sector,sector_name)
        print("  Try later if network responses slowly.")
        return None       
    sname=list(sdf['name'])[0]
    
    #确定比较范围
    complist=['changepercent','turnoverratio','settlement','per','pb','nmc','mktcap']
    compnames=['涨跌幅%','换手率%','收盘价(元)','市盈率','市净率','流通市值(亿元)','总市值(亿元)']
    compdf=pd.DataFrame(columns=['指标名称','指标数值','板块百分位数%','板块中位数','板块最小值','板块最大值'])
    for c in complist:
        v=list(sdf[c])[0]
        vlist=list(set(list(df[c])))
        vlist.sort()
        vmin=round(min(vlist),2)
        vmax=round(max(vlist),2)
        vmedian=round(np.median(vlist),2)
        
        pos=vlist.index(v)
        pct=round((pos+1)/len(vlist)*100,2)
        
        s=pd.Series({'指标名称':compnames[complist.index(c)], \
                     '指标数值':v,'板块百分位数%':pct,'板块中位数':vmedian, \
                    '板块最小值':vmin,'板块最大值':vmax})
        try:
            compdf=compdf.append(s,ignore_index=True)
        except:
            compdf=compdf._append(s,ignore_index=True)
        
    compdf.reset_index(drop=True,inplace=True)     

    print("\n======= 股票在所属行业/板块的位置分析 =======")
    print("股票: "+sname+" ("+ticker+")")
    print("所属行业/板块："+sector_name+" ("+sector+", "+indicator+"分类)")
    print("")
    
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    print(compdf.to_string(index=False))
    
    import datetime
    today = datetime.date.today()
    print('') #空一行
    print("注：板块内成份股个数:",len(df),"\b, 数据来源：新浪财经,",today,"\b(信息为上个交易日)")

    return df,compdf    
    

#==============================================================================

def invest_concept_china(num=10):
    """
    废弃！
    功能：汇总投资概念股票名单，排行
    来源网址：http://finance.sina.com.cn/stock/sl/#qmxindustry_1
    """
    print("\nWarning: This function might cause your IP address banned by data source!")
    print("Searching stocks with investment concepts in China, it may take long time ...")
    
    #找出投资概念列表
    import akshare as ak
    cdf = ak.stock_sector_spot(indicator="概念")
    
    #去掉空格，否则匹配容易失败
    cdf['板块']=cdf['板块'].apply(lambda x: x.strip())
    cdf['label']=cdf['label'].apply(lambda x: x.strip())    
    
    cdf.sort_values(by=['label'],ascending=True,inplace=True)
    clist=list(cdf['label'])
    cnames=list(cdf['板块'])
    cnum=len(clist)
    
    import pandas as pd
    totaldf=pd.DataFrame()
    import time
    i=0
    #新浪财经有反爬虫，这个循环做不下去
    for c in clist:
        print("...Searching for conceptual sector",c,cnames[clist.index(c)],end='')
        try:
            sdf = ak.stock_sector_detail(c)
            sdf['板块']=cnames(clist.index(c))
            totaldf=pd.concat([totaldf,sdf],ignore_index=True)
            print(', found.')
        except:
            print(', failed:-(')
            #continue
                    #等待一会儿，避免被禁访问
        time.sleep(10)
        i=i+1
        if i % 20 == 0:
            print(int(i/cnum*100),'\b%',end=' ')
    print("...Searching completed.")
    
    if len(totaldf) == 0:
        print("#Error(sector_rank_china): data source tentatively banned your access:-(")
        print("Solutions:1) try an hour later, or 2) switch to another IP address.")
        return None
    
    #分组统计
    totaldfrank = totaldf.groupby('name')['板块','code'].count()
    totaldfrank.sort_values(by=['板块','code'],ascending=[False,True],inplace=True)
    totaldfrank['name']=totaldfrank.index
    totaldfrank.reset_index(drop=True,inplace=True)

    #更新每只股票持有的概念列表
    for i in totaldfrank.index:
        tdfsub=totaldf[totaldf['name']==totaldfrank.loc[i,"name"]]
        sectors=str(list(tdfsub['板块'])) 
        # 逐行修改列值
        totaldfrank.loc[i,"sectors"] = sectors

    #合成
    totaldf2=totaldf.drop('板块',axix=1)
    totaldf2.drop_duplicates(subset=['code'],keep='first',inplace=True)
    finaldf = pd.merge(totaldfrank,totaldf2,how='inner',on='name')
    
    return finaldf
    
    
#==============================================================================
#==============================================================================
#申万行业分类：https://www.swhyresearch.com/institute_sw/allIndex/analysisIndex
#==============================================================================
#==============================================================================
def industry_sw_list():
    """
    功能：输出申万指数代码df。
    输入：
    输出：df
    """
    import pandas as pd
    industry=pd.DataFrame([
        
        #市场表征指数F，一级行业I，二级行业T，风格策略S
        ['F','801001','申万50'],['F','801002','申万中小'],['F','801003','申万Ａ指'],
        ['F','801005','申万创业'],['F','801250','申万制造'],['F','801260','申万消费'],
        ['F','801270','申万投资'],['F','801280','申万服务'],['F','801300','申万300指数'],
        ['I','801010','农林牧渔'],['I','801030','基础化工'],['I','801040','钢铁'],
        ['I','801050','有色金属'],['I','801080','电子'],['I','801110','家用电器'],
        ['I','801120','食品饮料'],['I','801130','纺织服饰'],['I','801140','轻工制造'],
        ['I','801150','医药生物'],['I','801160','公用事业'],['I','801170','交通运输'],
        ['I','801180','房地产'],['I','801200','商贸零售'],['I','801210','社会服务'],
        ['I','801230','综合'],['I','801710','建筑材料'],['I','801720','建筑装饰'],
        ['I','801730','电力设备'],['I','801740','国防军工'],['I','801750','计算机'],
        ['I','801760','传媒'],['I','801770','通信'],['I','801780','银行'],
        ['I','801790','非银金融'],['I','801880','汽车'],['I','801890','机械设备'],
        ['I','801950','煤炭'],['I','801960','石油石化'],['I','801970','环保'],
        ['I','801980','美容护理'],['T','801012','农产品加工'],['T','801014','饲料'],
        ['T','801015','渔业'],['T','801016','种植业'],['T','801017','养殖业'],
        ['T','801018','动物保健Ⅱ'],['T','801032','化学纤维'],['T','801033','化学原料'],
        ['T','801034','化学制品'],['T','801036','塑料'],['T','801037','橡胶'],
        ['T','801038','农化制品'],['T','801039','非金属材料Ⅱ'],['T','801043','冶钢原料'],
        ['T','801044','普钢'],['T','801045','特钢Ⅱ'],['T','801051','金属新材料'],
        ['T','801053','贵金属'],['T','801054','小金属'],['T','801055','工业金属'],
        ['T','801056','能源金属'],['T','801072','通用设备'],['T','801074','专用设备'],
        ['T','801076','轨交设备Ⅱ'],['T','801077','工程机械'],['T','801078','自动化设备'],
        ['T','801081','半导体'],['T','801082','其他电子Ⅱ'],['T','801083','元件'],
        ['T','801084','光学光电子'],['T','801085','消费电子'],['T','801086','电子化学品Ⅱ'],
        ['T','801092','汽车服务'],['T','801093','汽车零部件'],['T','801095','乘用车'],
        ['T','801096','商用车'],['T','801101','计算机设备'],['T','801102','通信设备'],
        ['T','801103','IT服务Ⅱ'],['T','801104','软件开发'],['T','801111','白色家电'],
        ['T','801112','黑色家电'],['T','801113','小家电'],['T','801114','厨卫电器'],
        ['T','801115','照明设备Ⅱ'],['T','801116','家电零部件Ⅱ'],['T','801124','食品加工'],
        ['T','801125','白酒Ⅱ'],['T','801126','非白酒'],['T','801127','饮料乳品'],
        ['T','801128','休闲食品'],['T','801129','调味发酵品Ⅱ'],['T','801131','纺织制造'],
        ['T','801132','服装家纺'],['T','801133','饰品'],['T','801141','包装印刷'],
        ['T','801142','家居用品'],['T','801143','造纸'],['T','801145','文娱用品'],
        ['T','801151','化学制药'],['T','801152','生物制品'],['T','801153','医疗器械'],
        ['T','801154','医药商业'],['T','801155','中药Ⅱ'],['T','801156','医疗服务'],
        ['T','801161','电力'],['T','801163','燃气Ⅱ'],['T','801178','物流'],
        ['T','801179','铁路公路'],['T','801181','房地产开发'],['T','801183','房地产服务'],
        ['T','801191','多元金融'],['T','801193','证券Ⅱ'],['T','801194','保险Ⅱ'],
        ['T','801202','贸易Ⅱ'],['T','801203','一般零售'],['T','801204','专业连锁Ⅱ'],
        ['T','801206','互联网电商'],['T','801218','专业服务'],['T','801219','酒店餐饮'],
        ['T','801223','通信服务'],['T','801231','综合Ⅱ'],['T','801711','水泥'],
        ['T','801712','玻璃玻纤'],['T','801713','装修建材'],['T','801721','房屋建设Ⅱ'],
        ['T','801722','装修装饰Ⅱ'],['T','801723','基础建设'],['T','801724','专业工程'],
        ['T','801726','工程咨询服务Ⅱ'],['T','801731','电机Ⅱ'],['T','801733','其他电源设备Ⅱ'],
        ['T','801735','光伏设备'],['T','801736','风电设备'],['T','801737','电池'],
        ['T','801738','电网设备'],['T','801741','航天装备Ⅱ'],['T','801742','航空装备Ⅱ'],
        ['T','801743','地面兵装Ⅱ'],['T','801744','航海装备Ⅱ'],['T','801745','军工电子Ⅱ'],
        ['T','801764','游戏Ⅱ'],['T','801765','广告营销'],['T','801766','影视院线'],
        ['T','801767','数字媒体'],['T','801769','出版'],['T','801782','国有大型银行Ⅱ'],
        ['T','801783','股份制银行Ⅱ'],['T','801784','城商行Ⅱ'],['T','801785','农商行Ⅱ'],
        ['T','801881','摩托车及其他'],['T','801951','煤炭开采'],['T','801952','焦炭Ⅱ'],
        ['T','801962','油服工程'],['T','801963','炼化及贸易'],['T','801971','环境治理'],
        ['T','801972','环保设备Ⅱ'],['T','801981','个护用品'],['T','801982','化妆品'],
        ['T','801991','航空机场'],['T','801992','航运港口'],['T','801993','旅游及景区'],
        ['T','801994','教育'],['T','801995','电视广播Ⅱ'],['S','801811','大盘指数'],
        ['S','801812','中盘指数'],['S','801813','小盘指数'],['S','801821','高市盈率指数'],
        ['S','801822','中市盈率指数'],['S','801823','低市盈率指数'],['S','801831','高市净率指数'],
        ['S','801832','中市净率指数'],['S','801833','低市净率指数'],['S','801841','高价股指数'],
        ['S','801842','中价股指数'],['S','801843','低价股指数'],['S','801851','亏损股指数'],
        ['S','801852','微利股指数'],['S','801853','绩优股指数'],['S','801863','新股指数'],
        ['3','850111','种子'],['3','850113','其他种植业'],['3','850122','水产养殖'],
        ['3','850142','畜禽饲料'],['3','850151','果蔬加工'],['3','850152','粮油加工'],
        ['3','850154','其他农产品加工'],['3','850172','生猪养殖'],['3','850173','肉鸡养殖'],
        ['3','850181','动物保健Ⅲ'],['3','850322','氯碱'],['3','850323','无机盐'],
        ['3','850324','其他化学原料'],['3','850325','煤化工'],['3','850326','钛白粉'],
        ['3','850335','涂料油墨'],['3','850337','民爆制品'],['3','850338','纺织化学制品'],
        ['3','850339','其他化学制品'],['3','850382','氟化工'],['3','850372','聚氨酯'],
        ['3','850135','食品及饲料添加剂'],['3','850136','有机硅'],['3','850341','涤纶'],
        ['3','850343','粘胶'],['3','850351','其他塑料制品'],['3','850353','改性塑料'],
        ['3','850354','合成树脂'],['3','850355','膜材料'],['3','850362','其他橡胶制品'],
        ['3','850363','炭黑'],['3','850331','氮肥'],['3','850332','磷肥及磷化工'],
        ['3','850333','农药'],['3','850381','复合肥'],['3','850523','非金属材料Ⅲ'],
        ['3','850442','板材'],['3','850521','其他金属新材料'],['3','850522','磁性材料'],
        ['3','850551','铝'],['3','850552','铜'],['3','850553','铅锌'],
        ['3','850531','黄金'],['3','850544','其他小金属'],['3','850812','分立器件'],
        ['3','850813','半导体材料'],['3','850814','数字芯片设计'],['3','850815','模拟芯片设计'],
        ['3','850817','集成电路封测'],['3','850818','半导体设备'],['3','850822','印制电路板'],
        ['3','850823','被动元件'],['3','850831','面板'],['3','850832','LED'],
        ['3','850833','光学元件'],['3','850841','其他电子Ⅲ'],['3','850853','品牌消费电子'],
        ['3','850854','消费电子零部件及组装'],['3','850861','电子化学品Ⅲ'],['3','850922','车身附件及饰件'],
        ['3','850923','底盘与发动机系统'],['3','850924','轮胎轮毂'],['3','850925','其他汽车零部件'],
        ['3','850926','汽车电子电气系统'],['3','850232','汽车经销商'],['3','850233','汽车综合服务'],
        ['3','858811','其他运输设备'],['3','858812','摩托车'],['3','850952','综合乘用车'],
        ['3','850912','商用载货车'],['3','850913','商用载客车'],['3','851112','空调'],
        ['3','851116','冰洗'],['3','851122','其他黑色家电'],['3','851131','厨房小家电'],
        ['3','851141','厨房电器'],['3','851151','照明设备Ⅲ'],['3','851161','家电零部件Ⅲ'],
        ['3','851241','肉制品'],['3','851246','预加工食品'],['3','851247','保健品'],
        ['3','851251','白酒Ⅲ'],['3','851232','啤酒'],['3','851233','其他酒类'],
        ['3','851271','软饮料'],['3','851243','乳品'],['3','851281','零食'],
        ['3','851282','烘焙食品'],['3','851242','调味发酵品Ⅲ'],['3','851312','棉纺'],
        ['3','851314','印染'],['3','851315','辅料'],['3','851316','其他纺织'],
        ['3','851325','鞋帽及其他'],['3','851326','家纺'],['3','851329','非运动服装'],
        ['3','851331','钟表珠宝'],['3','851412','大宗用纸'],['3','851413','特种纸'],
        ['3','851422','印刷'],['3','851423','金属包装'],['3','851424','塑料包装'],
        ['3','851425','纸包装'],['3','851436','瓷砖地板'],['3','851437','成品家居'],
        ['3','851438','定制家居'],['3','851439','卫浴制品'],['3','851491','其他家居用品'],
        ['3','851452','娱乐用品'],['3','851511','原料药'],['3','851512','化学制剂'],
        ['3','851521','中药Ⅲ'],['3','851522','血液制品'],['3','851523','疫苗'],
        ['3','851524','其他生物制品'],['3','851542','医药流通'],['3','851543','线下药店'],
        ['3','851532','医疗设备'],['3','851533','医疗耗材'],['3','851534','体外诊断'],
        ['3','851563','医疗研发外包'],['3','851564','医院'],['3','851611','火力发电'],
        ['3','851612','水力发电'],['3','851614','热力服务'],['3','851616','光伏发电'],
        ['3','851617','风力发电'],['3','851610','电能综合服务'],['3','851631','燃气Ⅲ'],
        ['3','851782','原材料供应链服务'],['3','851783','中间产品及消费品供应链服务'],['3','851784','快递'],
        ['3','851785','跨境物流'],['3','851786','仓储物流'],['3','851787','公路货运'],
        ['3','851731','高速公路'],['3','851721','公交'],['3','851771','铁路运输'],
        ['3','851741','航空运输'],['3','851761','航运'],['3','851711','港口'],
        ['3','851811','住宅开发'],['3','851812','商业地产'],['3','851813','产业地产'],
        ['3','851831','物业管理'],['3','852021','贸易Ⅲ'],['3','852031','百货'],
        ['3','852032','超市'],['3','852033','多业态零售'],['3','852034','商业物业经营'],
        ['3','852041','专业连锁Ⅲ'],['3','852062','跨境电商'],['3','852063','电商服务'],
        ['3','852182','检测服务'],['3','852183','会展服务'],['3','852121','酒店'],
        ['3','852111','人工景区'],['3','852112','自然景区'],['3','852131','旅游综合'],
        ['3','859852','培训教育'],['3','857821','国有大型银行Ⅲ'],['3','857831','股份制银行Ⅲ'],
        ['3','857841','城商行Ⅲ'],['3','857851','农商行Ⅲ'],['3','851931','证券Ⅲ'],
        ['3','851941','保险Ⅲ'],['3','851922','金融控股'],['3','851927','资产管理'],
        ['3','852311','综合Ⅲ'],['3','857111','水泥制造'],['3','857112','水泥制品'],
        ['3','857121','玻璃制造'],['3','857122','玻纤制造'],['3','850615','耐火材料'],
        ['3','850616','管材'],['3','850614','其他建材'],['3','850623','房屋建设Ⅲ'],
        ['3','857221','装修装饰Ⅲ'],['3','857236','基建市政工程'],['3','857251','园林工程'],
        ['3','857241','钢结构'],['3','857242','化学工程'],['3','857243','国际工程'],
        ['3','857244','其他专业工程'],['3','857261','工程咨询服务Ⅲ'],['3','850741','电机Ⅲ'],
        ['3','857334','火电设备'],['3','857336','其他电源设备Ⅲ'],['3','857352','光伏电池组件'],
        ['3','857354','光伏辅材'],['3','857355','光伏加工设备'],['3','857362','风电零部件'],
        ['3','857371','锂电池'],['3','857372','电池化学品'],['3','857373','锂电专用设备'],
        ['3','857375','蓄电池及其他电池'],['3','857381','输变电设备'],['3','857382','配电设备'],
        ['3','857321','电网自动化设备'],['3','857323','电工仪器仪表'],['3','857344','线缆部件及其他'],
        ['3','850711','机床工具'],['3','850713','磨具磨料'],['3','850715','制冷空调设备'],
        ['3','850716','其他通用设备'],['3','850731','仪器仪表'],['3','850751','金属制品'],
        ['3','850725','能源及重型设备'],['3','850728','楼宇设备'],['3','850721','纺织服装设备'],
        ['3','850726','印刷包装机械'],['3','850727','其他专用设备'],['3','850936','轨交设备Ⅲ'],
        ['3','850771','工程机械整机'],['3','850772','工程机械器件'],['3','850781','机器人'],
        ['3','850782','工控设备'],['3','850783','激光设备'],['3','850784','其他自动化设备'],
        ['3','857411','航天装备Ⅲ'],['3','857421','航空装备Ⅲ'],['3','857431','地面兵装Ⅲ'],
        ['3','850935','航海装备Ⅲ'],['3','857451','军工电子Ⅲ'],['3','850702','安防设备'],
        ['3','850703','其他计算机设备'],['3','852226','IT服务Ⅲ'],['3','851041','垂直应用软件'],
        ['3','851042','横向通用软件'],['3','857641','游戏Ⅲ'],['3','857651','营销代理'],
        ['3','857661','影视动漫制作'],['3','857674','门户网站'],['3','857691','教育出版'],
        ['3','857692','大众出版'],['3','859951','电视广播Ⅲ'],['3','852213','通信工程及服务'],
        ['3','852214','通信应用增值服务'],['3','851024','通信网络设备及器件'],['3','851025','通信线缆及配套'],
        ['3','851026','通信终端及配件'],['3','851027','其他通信设备'],['3','859511','动力煤'],
        ['3','859512','焦煤'],['3','859521','焦炭Ⅲ'],['3','859621','油田服务'],
        ['3','859622','油气及炼化工程'],['3','859631','炼油化工'],['3','859632','油品石化贸易'],
        ['3','859633','其他石化'],['3','859711','大气治理'],['3','859712','水务及水治理'],
        ['3','859713','固废治理'],['3','859714','综合环境治理'],['3','859721','环保设备Ⅲ'],
        ['3','859811','生活用纸'],['3','859821','化妆品制造及其他'],['3','859822','品牌化妆品'],
        
        #手工添加：可能重复
        ], columns=['type','code','name'])

    return industry
#==============================================================================
def industry_sw_list_all():
    """
    功能：输出申万指数所有代码df。
    输入：
    输出：df，包括市场表征指数F，一级行业指数I，二级行业T，风格指数S，三级行业3
    """
    import pandas as pd
    import akshare as ak
    
    symboltypes=["市场表征", "一级行业", "二级行业", "风格指数"] 
    indextypecodes=['F','I','T','S']
    industry=pd.DataFrame()
    for s in symboltypes:
        dft = ak.index_realtime_sw(symbol=s)
        
        pos=symboltypes.index(s)
        dft['指数类别代码']=indextypecodes[pos]
        dft['指数类别名称']=s
        
        if len(industry)==0:
            industry=dft
        else:
            industry=pd.concat([industry,dft],ignore_index=True)
    
    industry2=industry[['指数类别代码','指数代码','指数名称']]    
    industry2.columns=['type','code','name']   
    
    #获取申万一级行业指数代码和名称
    #df1=ak.sw_index_first_info()
    
    #获取申万二级行业指数代码和名称
    #df2 = ak.sw_index_second_info()
    
    #获取申万三级行业指数代码和名称
    df3 = ak.sw_index_third_info()
    df3['type']='3'
    df3['code']=df3['行业代码'].apply(lambda x:x[:6])
    df3['name']=df3['行业名称']
    industry3=df3[['type','code','name']]
    
    industry_all=pd.concat([industry2,industry3],ignore_index=True)
    # 删除完全重复的行
    industry_all.drop_duplicates(inplace=True)

    
    return industry_all

if __name__=='__main__':
    idf=industry_sw_list()
    idf=industry_sw_list_all()

#==============================================================================
if __name__=='__main__':
    idf=industry_sw_list_all()
    
    industry_sw_list_print(idf,numberPerLine=3)
    
def industry_sw_list_print(idf,numberPerLine=3):
    """
    功能：打印df定义形式，每3个一行，需要定期更新，并复制到函数industry_sw_list()
    """

    #遍历
    counter=0
    for index,row in idf.iterrows():
        #print(row['type'],row['code'],row['name'])
        print('[\''+row['type']+'\',\''+row['code']+'\',\''+row['name']+'\']',end=',')
        counter=counter+1
        if counter % numberPerLine ==0:
            print()

    return

#==============================================================================
if __name__=='__main__':
    itype='I'
    numberPerLine=5
    colalign='left'
    
    print_industry_sw(itype='I',numberPerLine=5,colalign='right')

def print_industry_sw(itype='I',numberPerLine=5,colalign='left'):
    """
    按照类别打印申万行业列表，名称(代码)，每行5个
    """
    df=industry_sw_list()
    df1=df[df['type']==itype]
    df1['name_code']=df1.apply(lambda x: x['name']+'('+x['code']+')',axis=1)
    
    symboltypes=["市场表征", "一级行业", "二级行业", "三级行业", "风格指数"] 
    indextypecodes=['F','I','T','3','S']
    pos=indextypecodes.index(itype)
    iname=symboltypes[pos]
    
    ilist=list(df1['name_code'])
    print("\n*** 申万行业分类："+iname+"，共计"+str(len(ilist))+'个行业(板块)')
    
    if itype=='3':
        numberPerLine=4
    
    printInLine_md(ilist,numberPerLine=numberPerLine,colalign=colalign)
    
    return

#==============================================================================
if __name__=='__main__':
    iname='食品饮料'
    iname='银行'
    iname='汽车'
    numberPerLine=5
    colalign='right'
    
    print_industry_component_sw(iname,numberPerLine=5,colalign='right')

def print_industry_component_sw(iname,numberPerLine=5,colalign='left'):
    """
    打印申万行业的成分股，名称(代码)
    """
    
    icode=industry_sw_code(iname)
    
    clist,cdf=industry_stock_sw(icode,top=1000)    

    #cdf['icode']=cdf['证券代码'].apply(lambda x: x+'.SS' if x[:1] in ['6'] else (x+'.SZ' if x[:1] in ['0','3'] else x+'.BJ' ))
    cdf['icode']=cdf['证券代码']
    
    # 删除'证券名称'为None的行
    cdf=cdf.mask(cdf.eq('None')).dropna()
    cdf['name_code']=cdf.apply(lambda x: x['证券名称']+'('+x['icode']+')',axis=1)
    
    ilist=list(cdf['name_code'])
    import datetime as dt; stoday=dt.date.today()    
    print("\n*** "+iname+'行业(板块)包括的股票：共计'+str(len(ilist))+'只，'+str(stoday)+"统计")
    
    printInLine_md(ilist,numberPerLine=numberPerLine,colalign=colalign)
    
    return

#==============================================================================
if __name__=='__main__':
    icode='850831'
    numberPerLine=5
    colalign='right'
    
    print_industry_component_sw2(icode,numberPerLine=5,colalign='right')

def print_industry_component_sw2(icode,numberPerLine=5,colalign='left'):
    """
    打印申万行业的成分股，名称(代码)
    输入：申万行业代码，一二三级均可
    """
    iname=industry_sw_name(icode)
    
    clist,cdf=industry_stock_sw(icode,top=1000)    

    #cdf['icode']=cdf['证券代码'].apply(lambda x: x+'.SS' if x[:1] in ['6'] else (x+'.SZ' if x[:1] in ['0','3'] else x+'.BJ' ))
    cdf['icode']=cdf['证券代码']
    
    # 删除'证券名称'为None的行
    cdf=cdf.mask(cdf.eq('None')).dropna()
    cdf['name_code']=cdf.apply(lambda x: x['证券名称']+'('+x['icode']+')',axis=1)
    
    ilist=list(cdf['name_code'])
    import datetime as dt; stoday=dt.date.today()    
    print("\n*** "+iname+'行业(板块)包括的股票：共计'+str(len(ilist))+'只，'+str(stoday)+"统计")
    
    printInLine_md(ilist,numberPerLine=numberPerLine,colalign=colalign)
    
    return
    
#==============================================================================
def industry_sw_name(icode):
    """
    功能：将申万指数代码转换为指数名称。
    输入：指数代码
    输出：指数名称
    """
    industry=industry_sw_list()

    try:
        iname=industry[industry['code']==icode]['name'].values[0]
    except:
        #未查到
        if not icode.isdigit():
            print("  #Warning(industry_sw_name): industry name not found for",icode)
        iname=icode
   
    return iname

if __name__=='__main__':
    icode='801862'
    industry_sw_name(icode)

#==============================================================================
def industry_sw_code(iname):
    """
    功能：将申万指数名称转换为指数代码。
    输入：指数名称
    输出：指数代码
    """
    industry=industry_sw_list()

    try:
        icode=industry[industry['name']==iname]['code'].values[0]
    except:
        #未查到
        #print("  #Warning(industry_sw_code): industry name not found",iname)
        return None
   
    return icode

if __name__=='__main__':
    iname='申万创业'
    industry_sw_code(iname)

#==============================================================================
def industry_sw_codes(inamelist):
    """
    功能：将申万指数名称/列表转换为指数代码列表。
    输入：指数名称/列表
    输出：指数代码列表
    """
    industry=industry_sw_list()

    icodelist=[]
    if isinstance(inamelist,str):
        icode=industry_sw_code(inamelist)
        if not (icode is None):
            icodelist=[icode]
        else:
            if inamelist.isdigit():
                return inamelist
            else:
                print("  #Warning(industries_sw_code): industry code not found for",inamelist)
                return None

    if isinstance(inamelist,list):
        if len(inamelist) == 0:
            print("  #Warning(industries_sw_code): no industry code found in for",inamelist)
            return None
        
        for i in inamelist:
            icode=industry_sw_code(i)
            if not (icode is None):
                icodelist=icodelist+[icode]
            else:
                if i.isdigit():
                    icodelist=icodelist+[i]
                else:
                    print("  #Warning(industries_sw_code): industry code not found",i)
                    return None
   
    return icodelist

if __name__=='__main__':
    inamelist='申万创业'
    industry_sw_codes(inamelist)
    
    inamelist=['申万创业','申万投资','申万制造','申万消费']
    industry_sw_codes(inamelist)
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='I'
    graph=True
    axisamp=0.8
    
def industry_ranking_sw(start,end,measure='Exp Ret%', \
                                itype='I',period="day", \
                                graph=True,axisamp=0.8):
    """
    完整版，全流程
    功能：模板，遍历某类申万指数，计算某项业绩指标，汇集排序
    itype: F表征指数，I行业指数，S风格指数
    period="day"; choice of {"day", "week", "month"}
    绘图：柱状图，可选
    """
    #检查日期的合理性
    result,start1,end1=check_period(start,end)
    
    #检查itype的合理性
    
    #获得指数代码
    idf=industry_sw_list()
    idf1=idf[idf['type']==itype]
    ilist=list(idf1['code'])

    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame(columns=['date','ticker','start','end','item','value'])

    print("\nSearching industry prices, it may take great time, please wait ...")
    for i in ilist:
        
        print("  Processing industry",i,"\b, please wait ...")
        #抓取指数价格，选取期间范围
        dft = ak.index_hist_sw(symbol=i,period="day")
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        #dft1=dft[(dft.index>=start1) & (dft.index<=end1)]
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]

        #计算指标
        dft3=all_calculate(dft2,i,start,end)
        dft4=dft3.tail(1)
        
        #记录
        idate=dft4.index.values[0]
        idate=pd.to_datetime(idate)
        iend=idate.strftime('%Y-%m-%d')
        try:
            ivalue=round(dft4[measure].values[0],2)
            s=pd.Series({'date':idate,'ticker':i,'start':start,'end':iend,'item':measure,'value':ivalue})
            try:
                df=df.append(s,ignore_index=True)
            except:
                df=df._append(s,ignore_index=True)
        except:
            print("  #Error(industry_ranking_sw): measure not supported",measure)
            return None
        
    df.sort_values(by='value',ascending=True,inplace=True)
    df['name']=df['ticker'].apply(lambda x: industry_sw_name(x))
    df.set_index('name',inplace=True)
    colname='value'
    titletxt="行业板块分析：业绩排名"
    import datetime; today=datetime.date.today()
    footnote0=ectranslate(measure)+' ==>\n'
    footnote1='申万行业分类，观察期：'+start+'至'+iend+'\n'
    footnote2="数据来源: 申万宏源, "+str(today)
    footnote=footnote0+footnote1+footnote2
    
    plot_barh(df,colname,titletxt,footnote,axisamp=axisamp) 
    #plot_barh2(df,colname,titletxt,footnote)

    return df
    
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='I'
    graph=True
    axisamp=0.8
    
    df=industry_ranking_sw(start,end,measure='Exp Ret%',axisamp=0.8)
    
#==============================================================================
def industry_ranking_sw2(industrylist,start,end,measure='Exp Ret%', \
                         period="day", \
                         graph=True,axisamp=0.8):
    """
    完整版，全流程
    功能：模板，遍历某些指定的申万指数，计算某项业绩指标，汇集排序
    特点：不限类别，自由指定申万指数；指定行业指定指标横截面对比
    period="day"; choice of {"day", "week", "month"}
    绘图：柱状图，可选
    """
    #检查日期的合理性
    result,start1,end1=check_period(start,end)
    
    #检查itype的合理性
    
    #获得指数代码
    ilist=industrylist

    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame(columns=['date','ticker','start','end','item','value'])

    print("\nSearching industry prices, it may take great time, please wait ...")
    for i in ilist:
        
        print("  Processing industry",i,"\b, please wait ...")
        #抓取指数价格，选取期间范围
        try:
            dft = ak.index_hist_sw(symbol=i,period="day")
        except:
            print("  #Warning(industry_ranking_sw2): industry not found for",i)
            continue
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        #dft1=dft[(dft.index>=start1) & (dft.index<=end1)]
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]

        #计算指标
        dft3=all_calculate(dft2,i,start,end)
        dft4=dft3.tail(1)
        
        #记录
        idate=dft4.index.values[0]
        idate=pd.to_datetime(idate)
        iend=idate.strftime('%Y-%m-%d')
        try:
            ivalue=round(dft4[measure].values[0],2)
            s=pd.Series({'date':idate,'ticker':i,'start':start,'end':iend,'item':measure,'value':ivalue})
            try:
                df=df.append(s,ignore_index=True)
            except:
                df=df._append(s,ignore_index=True)
        except:
            print("  #Error(industry_ranking_sw): measure not supported",measure)
            return None
        
    df.sort_values(by='value',ascending=True,inplace=True)
    df['name']=df['ticker'].apply(lambda x: industry_sw_name(x))
    df.set_index('name',inplace=True)
    
    df.dropna(inplace=True)
    
    colname='value'
    titletxt="行业板块分析：业绩排名"
    import datetime; today=datetime.date.today()
    footnote0=ectranslate(measure)+' ==>\n'
    footnote1='申万行业分类，观察期：'+start+'至'+iend+'\n'
    footnote2="数据来源: 申万宏源, "+str(today)
    footnote=footnote0+footnote1+footnote2
    
    plot_barh(df,colname,titletxt,footnote,axisamp=axisamp) 
    #plot_barh2(df,colname,titletxt,footnote)

    return df
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    itype='F'
    period="day"
    industry_list='all'    
    
def get_industry_sw(itype='I',period="day",industry_list='all'):
    """
    功能：遍历某类申万指数，下载数据
    itype: F表征指数，I行业指数，S风格指数
    period="day"; choice of {"day", "week", "month"}
    industry_list: 允许选择部分行业
    """
    
    #检查itype的合理性
    typelist=['F','I','T','3','S','A']
    if not (itype in typelist):
        print("  #Error(get_industry_sw): unsupported industry category",itype)
        print("  Supported industry category",typelist)
        print("  F: Featured, I-Industry, S-Styled, A-All (more time))")
        return None
    
    #获得指数代码
    if industry_list=='all':
        idf=industry_sw_list()
        
        if itype == 'A':
            ilist=list(idf['code'])
        else:
            idf1=idf[idf['type']==itype]
            ilist=list(idf1['code'])
    else:
        ilist=industry_list
        
    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame()

    print("Searching industry information, please wait ...")
    num=len(ilist)
    if num <= 10:
        steps=5
    else:
        steps=10
        
    total=len(ilist)
    for i in ilist:
        
        #print("  Retrieving information for industry",i)
        
        #抓取指数价格
        try:
            dft = ak.index_hist_sw(symbol=i,period="day")
        except:
            print("  #Warning(get_industry_sw): unsupported industry",i)
            continue
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]
        try:
            df=df.append(dft2)
        except:
            df=df._append(dft2)
        
        current=ilist.index(i)
        print_progress_percent(current,total,steps=steps,leading_blanks=2)
    
    #num=list(set(list(df['ticker'])))
    print("  Successfully retrieved",len(df),"records in",len(ilist),"industries")
    #print("  Successfully retrieved",len(df),"records in",num,"industries")
    return df

    
if __name__=='__main__':
    df=get_industry_sw('F')

#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    measure='Exp Ret%'
    period="day"
    industry_list=['850831','801785','801737','801194','801784','801783','801782']    
    
def get_industry_sw2(industry_list,period="day"):
    """
    功能：遍历指定的申万指数列表，下载数据
    period="day"; choice of {"day", "week", "month"}
    """
    
    #循环获取指标
    import pandas as pd
    import akshare as ak
    import datetime
    df=pd.DataFrame()

    print("Searching industry information, please wait ...")
    ilist=industry_list
    num=len(ilist)
    if num <= 10:
        steps=5
    else:
        steps=10
        
    total=len(ilist)
    for i in ilist:
        
        #print("  Retrieving information for industry",i)
        
        #抓取指数价格
        try:
            dft = ak.index_hist_sw(symbol=i,period="day")
        except:
            print("  #Warning(get_industry_sw): unsupported industry",i)
            continue
        
        dft['ticker']=dft['代码']
        dft['date']=dft['日期'].apply(lambda x: pd.to_datetime(x))
        dft.set_index('date',inplace=True)
        dft['Open']=dft['开盘']
        dft['High']=dft['最高']
        dft['Low']=dft['最低']
        dft['Close']=dft['收盘']
        dft['Adj Close']=dft['收盘']
        dft['Volume']=dft['成交量']
        dft['Amount']=dft['成交额']
        
        dft.sort_index(ascending=True,inplace=True)
        dft2=dft[['ticker','Open','High','Low','Close','Adj Close','Volume','Amount']]
        try:
            df=df.append(dft2)
        except:
            df=df._append(dft2)
        
        current=ilist.index(i)
        print_progress_percent(current,total,steps=steps,leading_blanks=2)
    
    #num=list(set(list(df['ticker'])))
    print("  Successfully retrieved",len(df),"records in",len(ilist),"industries")
    #print("  Successfully retrieved",len(df),"records in",num,"industries")
    return df

#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    
def calc_industry_sw(df,start,end):
    """
    功能：遍历某类申万指数，计算某项业绩指标，汇集排序
    df: 来自于get_industry_sw
    输出：最新时刻数据idf，全部时间序列数据idfall
    """
    #检查日期的合理性
    result,start1,end1=check_period(start,end)
    if not result:
        print("  #Error(calc_industry_sw): invalid date period",start,end)
        return None
    
    #获得指数代码
    ilist=list(set(list(df['ticker'])))
    ilist.sort()

    #循环获取指标
    import pandas as pd
    import datetime
    idf=pd.DataFrame()
    idfall=pd.DataFrame()

    print("Calculating industry performance, please wait ...")
    num=len(ilist)
    if num <= 10:
        steps=5
    else:
        steps=10
        
    total=len(ilist)
    for i in ilist:
        
        #print("  Processing industry",i)
        
        #抓取指数价格
        dft = df[df['ticker']==i]
        dft.sort_index(ascending=True,inplace=True)
        dft2=dft

        #计算指标
        dft3=all_calculate(dft2,i,start,end)
        dft3['start']=start

        #截取绘图区间
        dft3a=dft3[(dft3.index >= start1) & (dft3.index <= end1)]
        
        dft4=dft3a.tail(1)
        try:
            idf=idf.append(dft4)
            idfall=idfall.append(dft3a)
        except:
            idf=idf._append(dft4)
            idfall=idfall._append(dft3a)

        current=ilist.index(i)
        print_progress_percent(current,total,steps=steps,leading_blanks=2) 
    
    print("  Successfully processed",len(ilist),"industries")
    return idf,idfall
    
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    idf,idfall=calc_industry_sw(df,start,end)
    
#==============================================================================
#==============================================================================
if __name__=='__main__':
    measure='Exp Ret%'
    industries=[]
    graph=True
    axisamp=0.8
    px=False
    maxitems=32
    printout=False
    
    industries=['801770','801720','医药生物']
    
def rank_industry_sw(idf,measure='Exp Ret%',industries=[], \
                     graph=True,axisamp=0.8,px=False,maxitems=32, \
                         printout=False):
    """
    功能：遍历某类申万指数的某项业绩指标，汇集排序
    绘图：水平柱状图
    graph=True：是否绘图，一幅图最多绘制maxitems个项目
    axisamp=0.9：调节水平柱子伸缩比例，数值越大越收缩，数值越小越放大，有时也需要负的数值
    px=False：默认不使用plotly express
    printout=False：是否打印结果清单
    """
    import pandas as pd
    import datetime as dt
    
    idf['Date']= pd.to_datetime(idf.index) 
    idf['end'] = idf['Date'].dt.strftime('%Y-%m-%d')    
    
    #获得指标数据
    try:
        gdf=idf[['ticker',measure,'start','end']]
        num1=len(gdf)
    except:
        print("  #Error(rank_industry_sw): unsupported measurement",measure)
        return None

    gdf.dropna(inplace=True)
    num2=len(gdf)
    if num2==0:
        print("  #Error(rank_industry_sw): no data found for",measure)
        return None

    if num2 < num1:
        print("  #Warning(rank_industry_sw):",num1-num2,"industries removed as no enough data found for",measure)
        
    gdf[measure]=gdf[measure].apply(lambda x: round(x,1))
    istart=gdf['start'].values[0]
    idate=gdf.index.values[0]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    gdf['name']=gdf['ticker'].apply(lambda x: industry_sw_name(x))
    gdf.set_index('name',inplace=True)
    gdf.sort_values(by=measure,ascending=True,inplace=True)
    
    if len(industries) > 0:
        gdf1a=gdf[gdf.index.isin(industries)]
        gdf1b=gdf[gdf.ticker.isin(industries)]
        gdf1=pd.concat([gdf1a,gdf1b])
        gdf1.sort_values(by=measure,ascending=True,inplace=True)
    else:
        gdf1=gdf
    
    if printout or graph:
        titletxt="行业板块分析：最新业绩排名"
        import datetime; today=datetime.date.today()
        footnote0=ectranslate(measure)+' -->\n\n'
        footnote1='申万行业分类，'+iend+'快照'
        footnote2='观察期：'+istart+'至'+iend+'，'
        footnote3="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote0+footnote1+'\n'+footnote2+footnote3
    
    if printout or (len(gdf1) > maxitems):
        gdf2=gdf1.sort_values(by=measure,ascending=False)
        gdf2.reset_index(inplace=True)
        gdf2.index=gdf2.index+1
        gdf2.columns=['行业名称','行业代码',ectranslate(measure),'开始日期','结束日期']
        
        print("***",titletxt,'\n')
        alignlist=['center']+['left']*(len(list(gdf2))-1)
        print(gdf2.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
        

    if graph:
        if (len(gdf1) <= maxitems):
            colname=measure
            if not px:
                footnote=footnote0+footnote1+'\n'+footnote2+footnote3
                plot_barh(gdf1,colname,titletxt,footnote,axisamp=axisamp)
            else: #使用plotly_express
                titletxt="行业板块业绩排名："+ectranslate(measure)
                footnote=footnote1+'。'+footnote2+footnote3
                plot_barh2(gdf1,colname,titletxt,footnote)
        else:
            print("\n  #Sorry, there are too much items to be illustrated")
            print("  Solution: select some of them and use the industries=[] option")
            
    return gdf
    
if __name__=='__main__':
    measure='Exp Ret%'
    axisamp=0.8
    
    gdf=analyze_industry_sw(idf,measure='Exp Ret%',axisamp=0.8)
    gdf=analyze_industry_sw(idf,measure='Exp Ret Volatility%',axisamp=1.6)
    gdf=analyze_industry_sw(idf,measure='Exp Ret LPSD%',axisamp=1.7)
    gdf=analyze_industry_sw(idf,measure='Annual Ret Volatility%',axisamp=1.3)
    gdf=analyze_industry_sw(idf,measure='Annual Ret%',axisamp=1.0)
    gdf=analyze_industry_sw(idf,measure='Quarterly Ret%',axisamp=0.3)
    gdf=analyze_industry_sw(idf,measure='Monthly Ret%',axisamp=0.6)
    
#==============================================================================
if __name__=='__main__':
    industry_list=['801050','801080']
    measure='Exp Ret%'
    start='2020-11-1'
    end='2022-10-31'
    itype='I'
    period="day"
    graph=True

def compare_mindustry_sw(industry_list,measure,start,end, \
                         itype='I',period="day",graph=True,printout=False,sortby='tpw_mean'):
    """
    功能：比较多个行业industry_list某个指标measure在时间段start/end的时间序列趋势
    industry_list: 至少有两项，若太多了则生成的曲线过于密集
    特点：完整过程
    """ 
    """
    #检查行业代码的个数不少于两个
    if len(industry_list) < 2:
        print("  #Warning(compare_mindustry_sw): need at least 2 indistries to compare")
        return None
    """
    #检查行业代码是否在范围内
    ilist_all=list(industry_sw_list()['code'])
    for i in industry_list:
        if not (i in ilist_all):
            print("  #Warning(compare_mindustry_sw): unsupported industry",i)
            return None
    
    
    #检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(compare_mindustry_sw): invalid date period",start,end)
        return None
    
    
    #获取数据
    ddf=get_industry_sw(itype=itype,period=period,industry_list=industry_list)
    
    #计算指标
    _,idf=calc_industry_sw(ddf,start,end)
    
    #转换数据表结构为横排并列，适应绘图要求
    ilist=list(set(list(idf['ticker'])))
    import pandas as pd
    dfs=pd.DataFrame()
    notfoundlist=[]
    for i in ilist:
        
        dft=idf[idf['ticker']==i]
        istart=idf['start'].values[0]
        
        try:
            dft1=pd.DataFrame(dft[measure])
        except:
            print("  #Error(compare_mindustry_sw) unsupported measurement",measure)
            return None
        dft1.dropna(inplace=True)
        if len(dft1)==0:
            notfoundlist=notfoundlist+[i]
            continue
        
        dft1.rename(columns={measure:industry_sw_name(i)},inplace=True)
        if len(dfs)==0:
            dfs=dft1
        else:
            dfs=pd.merge(dfs,dft1,how='outer',left_index=True,right_index=True)
    
    if len(notfoundlist) > 0:
        print("  #Warning(compare_mindustry_sw): industry measure not found",notfoundlist)
        
    #绘制多条曲线
    idate=dfs.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    #截取绘图区间
    result,istartpd,iendpd=check_period(istart,iend)
    dfs1=dfs[(dfs.index >= istartpd) & (dfs.index <= iendpd)]
    
    y_label=measure
    title_txt="行业板块分析：市场业绩趋势与评价"
    import datetime; today = datetime.date.today()
    if graph:
        colname=measure
        
        import datetime; today=datetime.date.today()
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        draw_lines(dfs1,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)

    if printout:
        df2=dfs1
        dfcols=list(df2)
        for c in dfcols:
            ccn=codetranslate(c)+'('+c+')'
            df2.rename(columns={c:ccn},inplace=True)
        
        if sortby=='tpw_mean':
            sortby_txt='按推荐标记+近期优先加权平均值降序排列'
        elif sortby=='min':
            sortby_txt='按推荐标记+最小值降序排列'
        elif sortby=='mean':
            sortby_txt='按推荐标记+平均值降序排列'
        elif sortby=='median':
            sortby_txt='按推荐标记+中位数值降序排列'
        else:
            pass
        
        title_txt='*** '+title_txt+'：'+y_label+'，'+sortby_txt
        additional_note="*** 注：列表仅显示有星号标记或特定数量的证券。"
        footnote='比较期间：'+start+'至'+end
        ds=descriptive_statistics(df2,title_txt,additional_note+footnote,decimals=4, \
                               sortby=sortby,recommend_only=False)
    
    return dfs
    
if __name__=='__main__':
    mdf=compare_mindustry_sw(industry_list,measure,start,end)

#==============================================================================
if __name__=='__main__':
    industry_list=['801050','801080']
    measure='Exp Ret%'
    start='2023-1-1'
    end='2023-4-11'
    period="day"
    graph=True
    printout=False
    sortby='tpw_mean'

def compare_mindustry_sw2(industry_list,measure,start,end, \
                         period="day",graph=True,printout=False,sortby='tpw_mean'):
    """
    功能：比较多个行业industry_list某个指标measure在时间段start/end的时间序列趋势
    industry_list: 至少有两项，若太多了则生成的曲线过于密集
    特点：完整过程，无需规定申万行业类别；多个行业，单一指标
    """ 
    """
    #检查行业代码的个数不少于两个
    if len(industry_list) < 2:
        print("  #Warning(compare_mindustry_sw): need at least 2 indistries to compare")
        return None
    """
    #检查行业代码是否在范围内
    ilist_all=list(industry_sw_list()['code'])
    for i in industry_list:
        if not (i in ilist_all):
            if not i.isdigit():
                print("  #Warning(compare_mindustry_sw): unsupported industry",i)
                return None
    
    #检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(compare_mindustry_sw): invalid date period",start,end)
        return None
    
    #获取数据
    ddf=get_industry_sw2(industry_list=industry_list,period=period)
    
    #计算指标
    _,idf=calc_industry_sw(ddf,start,end)
    
    #转换数据表结构为横排并列，适应绘图要求
    ilist=list(set(list(idf['ticker'])))
    import pandas as pd
    dfs=pd.DataFrame()
    notfoundlist=[]
    for i in ilist:
        
        dft=idf[idf['ticker']==i]
        istart=idf['start'].values[0]
        
        try:
            dft1=pd.DataFrame(dft[measure])
        except:
            print("  #Error(compare_mindustry_sw) unsupported measurement",measure)
            return None
        dft1.dropna(inplace=True)
        if len(dft1)==0:
            notfoundlist=notfoundlist+[i]
            continue
        
        dft1.rename(columns={measure:industry_sw_name(i)},inplace=True)
        if len(dfs)==0:
            dfs=dft1
        else:
            dfs=pd.merge(dfs,dft1,how='outer',left_index=True,right_index=True)
    
    if len(notfoundlist) > 0:
        print("  #Warning(compare_mindustry_sw): industry measure not found for",notfoundlist)
        
    #绘制多条曲线
    idate=dfs.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    #截取绘图区间
    result,istartpd,iendpd=check_period(istart,iend)
    dfs1=dfs[(dfs.index >= istartpd) & (dfs.index <= iendpd)]
    
    y_label=measure
    title_txt="行业(板块)分析：市场业绩趋势与评价"
    import datetime; today = datetime.date.today()
    if graph:
        colname=measure
        title_txt="行业(板块)分析：市场业绩趋势"
        import datetime; today=datetime.date.today()
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        draw_lines(dfs1,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label='', \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)

    if printout:
        df2=dfs1
        dfcols=list(df2)
        for c in dfcols:
            cname=codetranslate(c)
            if cname == c:
                ccn=c
            else:
                ccn=cname+'('+c+')'
                df2.rename(columns={c:ccn},inplace=True)
        
        if sortby=='tpw_mean':
            sortby_txt='按推荐标记+近期优先加权平均值降序排列'
        elif sortby=='min':
            sortby_txt='按推荐标记+最小值降序排列'
        elif sortby=='mean':
            sortby_txt='按推荐标记+平均值降序排列'
        elif sortby=='median':
            sortby_txt='按推荐标记+中位数值降序排列'
        else:
            pass
        
        title_txt='*** '+title_txt+'：'+y_label+'，'+sortby_txt
        additional_note="*** 注：列表仅显示有星号标记或特定数量的证券。"
        footnote='比较期间：'+start+'至'+end
        ds=descriptive_statistics(df2,title_txt,additional_note+footnote,decimals=4, \
                               sortby=sortby,recommend_only=False)
    
    return dfs
    
if __name__=='__main__':
    mdf=compare_mindustry_sw2(industry_list,measure,start,end)

#==============================================================================
if __name__=='__main__':
    industry_list=['801050','801080']
    measure='Exp Ret%'
    start='2020-11-1'
    end='2022-10-31'
    itype='I'
    period="day"
    graph=True

def compare_industry_sw(idfall,industry_list,measure,graph=True):
    """
    功能：比较多个行业industry_list某个指标measure在时间段start/end的时间序列趋势
    industry_list: 至少有两项，若太多了则生成的曲线过于密集
    特点：需要依赖其他前序支持
    #获取数据
    ddf=get_industry_sw(itype=itype,period=period,industry_list=industry_list)
    
    #计算指标
    idf=calc_industry_sw(ddf,start,end,latest=False)
    
    """    
    """
    #检查行业代码的个数不少于两个
    if len(industry_list) < 2:
        print("  #Warning(compare_industry_sw): need at least 2 indistries to compare")
        return None
    """
    #检查行业代码是否在范围内
    ilist_all=list(industry_sw_list()['code'])
    for i in industry_list:
        if not (i in ilist_all):
            if not i.isdigit():
                print("  #Warning(compare_mindustry_sw): unsupported or no such industry",i)
                return None
    
    #转换数据表结构为横排并列，适应绘图要求
    import pandas as pd
    dfs=pd.DataFrame()
    notfoundlist=[]
    for i in industry_list:
        
        try:
            dft=idfall[idfall['ticker']==i]
        except:
            print("  #Error(compare_mindustry_sw) unsupported or no such industry",i)
            return None
        
        if not (len(dft)==0):
            istart=dft['start'].values[0]
        else:
            print("  #Error(compare_mindustry_sw) unsupported or no such industry",i)
            return None

        try:
            dft1=pd.DataFrame(dft[measure])
        except:
            print("  #Error(compare_mindustry_sw) unsupported measurement",measure)
            return None
        dft1.dropna(inplace=True)
        if len(dft1)==0:
            notfoundlist=notfoundlist+[i]
            #print("  #Warning(compare_mindustry_sw): no data found for industry",i,"on",measure)
            continue
        
        dft1.rename(columns={measure:industry_sw_name(i)},inplace=True)
        if len(dfs)==0:
            dfs=dft1
        else:
            dfs=pd.merge(dfs,dft1,how='outer',left_index=True,right_index=True)
    
    if len(notfoundlist)>0:
        print("  #Warning(compare_mindustry_sw):",measure,"data not found for industries",notfoundlist)
    
    #绘制多条曲线
    idate=dfs.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')
    
    #截取数据区间
    result,istartpd,iendpd=check_period(istart,iend)
    dfs1=dfs[(dfs.index >= istartpd) & (dfs.index <= iendpd)]
    
    if graph:
        y_label=measure
        colname=measure
        title_txt="行业板块分析：市场业绩趋势"
        
        import datetime; today=datetime.date.today()
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        if 'Ret%' in measure:
            axhline_label='收益零线'
        else:
            axhline_label=''

        draw_lines(dfs1,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label=axhline_label, \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)

    return dfs1
    
if __name__=='__main__':
    mdf=compare_industry_sw(idfall,industry_list,measure)

#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    idf,idfall=calc_industry_sw(df,start,end)
    base_return='Annual Ret%'
    graph=True

def compare_industry_sw_sharpe(idfall,industries,base_return='Annual Ret%',graph=True):
    """
    功能：比较申万行业的夏普比率
    idfall: 由calc_industry_sw函数获得
    industries: 仅限idfall中的行业
    
    缺陷：未考虑无风险利率
    """
    
    #获得年度收益率TTM
    aret=compare_industry_sw(idfall,industries,measure=base_return,graph=False)
    if aret is None:
        return None
    
    #获得年度收益率波动率TTM
    pos=base_return.index('%')
    base_risk=base_return[:pos]+' Volatility%'
    aretrisk=compare_industry_sw(idfall,industries,measure=base_risk,graph=False)
    
    #合成
    industrylist=list(aret)  
    atmp=pd.merge(aret,aretrisk,how='inner',left_index=True,right_index=True)
    for i in industrylist:
        atmp[i]=atmp[i+'_x']/atmp[i+'_y']
        
    sdf=atmp[industrylist]
    if graph:
        y_label='夏普比率（基于'+ectranslate(base_return)+'）'
        title_txt="行业板块分析：市场发展趋势"
        
        istart=sdf.index[0].strftime('%Y-%m-%d')
        iend=sdf.index[-1].strftime('%Y-%m-%d')
        footnote1='\n申万行业分类，观察期：'+istart+'至'+iend+'\n'
        import datetime; today=datetime.date.today()
        #footnote2="数据来源: 申万宏源, "+str(today)+'统计（未计入无风险利率）'
        footnote2="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote1+footnote2

        if 'Ret%' in base_return:
            axhline_label='收益零线'
        else:
            axhline_label=''

        draw_lines(sdf,y_label,x_label=footnote, \
                   axhline_value=0,axhline_label=axhline_label, \
                   title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)
    
    return sdf

if __name__=='__main__':
    industries=['801005', '801270', '801250', '801260']
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Annual Ret%')
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Quarterly Ret%')
    
    sdf=compare_industry_sw_sharpe(idfall,industries,base_return='Exp Ret%')
    
#==============================================================================
if __name__=='__main__':
    start='2018-1-1'
    end='2022-10-31'
    df=get_industry_sw('F')
    idf,idfall=calc_industry_sw(df,start,end)
    base_return='Exp Ret%'
    graph=True
    
    df=rank_industry_sw_sharpe(idfall,base_return='Exp Ret%',axisamp=0.8)

def rank_industry_sw_sharpe(idfall,base_return='Exp Ret%',graph=True,axisamp=0.8,px=False):
    """
    功能：比较申万行业最近的夏普比率，绘制水平柱状图
    idfall: 由calc_industry_sw函数获得
    
    缺陷：未考虑无风险利率
    """

    allindustries=list(set(list(idfall['ticker'])))
    df=compare_industry_sw_sharpe(idfall,allindustries,base_return=base_return,graph=False)
    dftail1=df.tail(1)
    dftail2=dftail1.T
    col=list(dftail2)[0]
    
    dftail3=dftail2.sort_values(by=col,ascending=True)
    dftail3[col]=dftail3[col].apply(lambda x: round(x,2))
        
    istart=idfall['start'].values[0]
    idate=idfall.index.values[-1]
    idate=pd.to_datetime(idate)
    iend=idate.strftime('%Y-%m-%d')

    if graph:
        colname=col
        titletxt="行业板块分析：最新业绩排名"
        import datetime; today=datetime.date.today()
        footnote0='夏普比率(基于'+ectranslate(base_return)+') -->\n\n'
        footnote1='申万行业分类，'+iend+'快照'
        footnote2='观察期：'+istart+'至'+iend+'，'
        footnote3="数据来源: 申万宏源, "+str(today)+'统计'
        footnote=footnote0+footnote1+'\n'+footnote2+footnote3
        if not px:
            footnote=footnote0+footnote1+'\n'+footnote2+footnote3
            plot_barh(dftail3,colname,titletxt,footnote,axisamp=axisamp)
        else: #使用plotly_express
            titletxt="行业板块业绩排名：夏普比率(基于"+ectranslate(base_return)+')'
            footnote=footnote1+'。'+footnote2+footnote3
            plot_barh2(dftail3,colname,titletxt,footnote)

    return dftail3

    
#==============================================================================
if __name__=='__main__':
    industry='850831'
    top=5

def industry_stock_sw(industry='801270',top=5,printout=False):
    """
    功能：获取申万行业指数的成分股
    排序：按照权重从大到小，重仓优先
    """
    # 检查行业代码的合理性
    inddf=industry_sw_list()
    ilist=list(inddf['code'])
    if not (industry in ilist):
        if not industry.isdigit():
            print("  #Warning(industry_stock_sw): industry code not found for",industry)
            return None
    
    import akshare as ak
    try:
        cdf = ak.index_component_sw(industry)
    except:
        print("  #Warning(industry_stock_sw): fetching index component failed or code not found",industry)
        return None

    # 删除'证券名称'为None的行
    cdf=cdf.mask(cdf.eq('None')).dropna()

    #排名
    cdf.sort_values(by='最新权重',ascending=False,inplace=True)    
    cdf.reset_index(drop=True,inplace=True)
    cdf['序号']=cdf.index+1
    
    if top > 0:
        cdf1=cdf.head(top)
    else:
        cdf1=cdf.tail(-top)
    cdf1['最新权重']=cdf1['最新权重'].apply(lambda x: round(x,2))
    cdf1['证券代码']=cdf1['证券代码'].apply(lambda x: x+'.SS' if x[:1] in ['6'] else (x+'.SZ' if x[:1] in ['0','3'] else x+'.BJ' ))
        
    clist=list(cdf1['证券代码'])
    """
    clist1=[]
    for c in clist:
        first=c[:1]
        if first == '6':
            clist1=clist1+[c+'.SS']
        else:
            clist1=clist1+[c+'.SZ']
    """
    if printout:
        title_txt="申万行业指数成分股排名与权重："+industry_sw_name(industry)+'指数('+industry+')'
        import datetime as dt; today=str(dt.date.today())
        footnote="*** 数据来源：sina/EM，"+str(today)
        df_directprint(cdf1,title_txt,footnote)        
    
    #return clist1,cdf1
    return clist,cdf1
    
if __name__=='__main__':
    clist,cdf=industry_stock_sw(industry='801005',top=10)
    clist,cdf=industry_stock_sw(industry='850831',top=-10)
#==============================================================================
if __name__ =="__main__":
    
    # 新冠疫情三年
    start='2023-1-1'; end='2023-4-10'
    itype='T'
    
    idf,idfall=get_industry_info_sw(start,end,itype='I')

def get_industry_info_sw(start,end,itype='I'):
    """
    功能：获得申万行业历史数据
    start: 开始日期
    end: 结束日期
    
    返回：idf, idfall，供进一步分析使用。
    """
    
    # 检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(get_industry_info_sw): invalid date period from",start,'to',end)
        return None,None
    
    print("This may need great great time depending on network/computer speed, take a break ...")
    print("\n*** Step 1:")
    # 获取行业历史数据，本步骤所需时间较长
    df=get_industry_sw(itype=itype)
    
    print("\n*** Step 2:")
    # 计算基础数据，本步骤所需时间较长
    idf,idfall=calc_industry_sw(df,start,end)
    
    return idf,idfall    

#==============================================================================
if __name__ =="__main__":
    
    # 新冠疫情三年
    industry_list=['850831','801785','801737','801194','801784','801783','801782']
    start='2023-1-1'; end='2023-4-3'

def get_industry_info_sw2(industry_list,start,end):
    """
    功能：获得申万行业历史数据
    start: 开始日期
    end: 结束日期
    特点：指定行业，可以混合各种指数
    
    返回：idf, idfall，供进一步分析使用。
    """
    
    # 检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(get_industry_info_sw2): invalid date period from",start,'to',end)
        return None,None
    
    print("This may need great time depending on network/computer speed, take a break ...")
    print("\n*** Step 1:")
    # 获取行业历史数据，本步骤所需时间较长
    df=get_industry_sw2(industry_list)
    
    print("\n*** Step 2:")
    # 计算基础数据，本步骤所需时间较长
    idf,idfall=calc_industry_sw(df,start,end)
    
    return idf,idfall    

#==============================================================================
if __name__ =="__main__":
    start='2022-1-1'
    end='2022-12-20'
    tickers=['600600.SS','600132.SS','000729.SZ','002461.SZ','600573.SS']
    measures=['Exp Ret%']    
    market_index='000001.SS'
    window=252
    colalign='right'
    
    rs=rank_msecurity_performance(tickers,start,end,measures=['Exp Ret%'])

def rank_msecurity_performance(tickers,start,end, \
                            measures=['Exp Ret%'], \
                            market_index='000001.SS',window=252,colalign='right'):
    """
    功能：列示多只股票多个指标的对比，从高到低
    
    """
    print("Searching for multiple security information, please wait ......") 
    #屏蔽函数内print信息输出的类
    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout

    rar_list=['treynor','sharpe','sortino','alpha']
    rar_list_e=['Treynor Ratio','Sharpe Ratio','Sortino Ratio','Jensen alpha']
    rar_list_c=['特雷诺比率','夏普比率','索替诺比率','阿尔法值']

    import pandas as pd
    df=pd.DataFrame()
    allmeasures=measures+rar_list
    for m in allmeasures:
        # 显示进度条
        print_progress_percent2(m,allmeasures,steps=len(allmeasures),leading_blanks=4)
        
        if not (m in rar_list):
            with HiddenPrints():
                dft=compare_msecurity(tickers,measure=m,start=start,end=end,graph=False)
            
            #修改列明为股票名称(股票代码)格式，以便与compare_mrar的结果一致
            dft_new_cols=[]
            for t in tickers:
                c=codetranslate(t)+'('+t+')'
                dft_new_cols=dft_new_cols+[c]
            dft.columns=dft_new_cols
            
            dft['指标']=ectranslate(m)
        else:
            with HiddenPrints():
                dft=compare_mrar(tickers,rar_name=m,start=start,end=end, \
                             market_index=market_index,window=window,graph=False)
            mpos=rar_list.index(m)
            mname=rar_list_c[mpos]
            dft['指标']=mname
        
            del dft['time_weight']
            del dft['relative_weight']
        
        dft1=dft.tail(1)
        cols1=list(dft1)
        cols1.remove('指标')
        for c in cols1:
            dft1[c]=dft1[c].apply(lambda x: round(float(x),4))
            
        if len(df) == 0:
            df=dft1
        else:
            df=pd.concat([df,dft1])
            
    df.set_index('指标',inplace=True)
    df1=df.T
    cols=list(df1)
    
    # 横向指标求和，作为排序依据
    #df1['value']=df1.loc[:,cols].apply(lambda x: x.sum(),axis=1)
    df1.sort_values('夏普比率',ascending=False,inplace=True)
    #del df1['value']
    
    df1.reset_index(inplace=True)
    df1.rename(columns={'index':'股票'},inplace=True)
    
    alignlist=['left']+[colalign]*(len(allmeasures)-1)
    
    print("\n*** 股票多重指标比较：按夏普比率降序排列\n")
    print(df1.to_markdown(index=False,tablefmt='plain',colalign=alignlist))
    
    print("\n*** 观察期：",start,'至',end,'\b，表中数据为',end+'快照')
    print("    表中的夏普比率/索替诺比率/阿尔法值均为TTM滚动值")
    import datetime; today=datetime.date.today()
    print("    数据来源：新浪财经/东方财富，"+str(today)+'统计')
    
    return df1
#==============================================================================
#==============================================================================
if __name__=='__main__':
    tickers=['801160','801120','801170','801710','801890','801040','801130','801180','801720','801970']
    start='2022-1-1'
    end='2023-3-22'
    info_type='Close'
    
    df=get_industry_sw('I')
    df=industry_correlation_sw(df,tickers,start,end,info_type='Close')

def cm2inch(x,y):
    return x/2.54,y/2.54

def industry_correlation_sw(df,tickers,start,end, \
                            info_type='Close',corr_size=6,star_size=5):
    """
    功能：股票/指数收盘价之间的相关性
    info_type='Close': 默认Close, 还可为Open/High/Low/Volume
    """
    # 检查行业个数
    if not isinstance(tickers,list) or len(tickers) < 2:
        print("  #Error(industry_correlation_sw): number of industries too few",tickers)
        return None
    
    # 检查信息类型
    info_types=['Close','Open','High','Low','Volume']
    info_types_cn=['收盘价','开盘价','最高价','最低价','成交量']
    if not(info_type in info_types):
        print("  #Error(industry_correlation_sw): invalid information type",info_type)
        print("  Supported information type:",info_types)
        return None
    pos=info_types.index(info_type)
    info_type_cn=info_types_cn[pos]
    
    # 检查日期
    result,startdt,enddt=check_period(start,end)
    if not result: 
        print("  #Error(industry_correlation_sw): invalid period",start,end)
        return None
    
    # 合成行业行情信息
    print("  Consolidating industry performance, please wait ...")
    import pandas as pd
    
    """
    tickercodes=industry_sw_codes(tickers)
    if tickercodes is None:
        tickercodes=tickers
    """
    
    dfs=None
    for ind in tickers:
        dft=df[df['ticker']==ind]
        if dft is None: 
            print("  #Warning(industry_correlation_sw): unknown industry code",ind)
            continue
    
        dft2=dft[(dft.index >= startdt) & (dft.index <= enddt)]
        dft3=pd.DataFrame(dft2[info_type])
        dft3.rename(columns={info_type:industry_sw_name(ind)},inplace=True)
        
        if dfs is None:
            dfs=dft3
        else:
            dfs=pd.merge(dfs,dft3,how='inner',left_index=True,right_index=True)
    dfs.dropna(axis=0,inplace=True)

    df_coor = dfs.corr()

    print("  Preparing cross-industry correlations, please wait ...")
    # here put the import lib
    import seaborn as sns
    sns.set(font='SimHei')  # 解决Seaborn中文显示问题

    fig = plt.figure(figsize=(cm2inch(12,8)))
    ax1 = plt.gca()
    
    #构造mask，去除重复数据显示
    import numpy as np
    mask = np.zeros_like(df_coor)
    mask[np.triu_indices_from(mask)] = True
    mask2 = mask
    mask = (np.flipud(mask)-1)*(-1)
    mask = np.rot90(mask,k = -1)
    
    im1 = sns.heatmap(df_coor,annot=True,cmap="YlGnBu"
                        , mask=mask#构造mask，去除重复数据显示
                        ,vmax=1,vmin=-1
                        , fmt='.2f',ax = ax1,annot_kws={"size":corr_size})
    
    ax1.tick_params(axis = 'both', length=0)
    
    #计算相关性显著性并显示
    from scipy.stats import pearsonr
    rlist = []
    plist = []
    for i in dfs.columns.values:
        for j in dfs.columns.values:
            r,p = pearsonr(dfs[i],dfs[j])
            try:
                rlist.append(r)
                plist.append(p)
            except:
                rlist._append(r)
                plist._append(p)
    
    rarr = np.asarray(rlist).reshape(len(dfs.columns.values),len(dfs.columns.values))
    parr = np.asarray(plist).reshape(len(dfs.columns.values),len(dfs.columns.values))
    xlist = ax1.get_xticks()
    ylist = ax1.get_yticks()
    
    widthx = 0
    widthy = -0.15
    
    # 星号的大小
    font_dict={'size':star_size}
    
    for m in ax1.get_xticks():
        for n in ax1.get_yticks():
            pv = (parr[int(m),int(n)])
            rv = (rarr[int(m),int(n)])
            if mask2[int(m),int(n)]<1.:
                #if abs(rv) > 0.5:
                if rv > 0.3:
                    if  pv< 0.05 and pv>= 0.01:
                        ax1.text(n+widthx,m+widthy,'*',ha = 'center',color = 'white',fontdict=font_dict)
                    if  pv< 0.01 and pv>= 0.001:
                        ax1.text(n+widthx,m+widthy,'**',ha = 'center',color = 'white',fontdict=font_dict)
                    if  pv< 0.001:
                        #print([int(m),int(n)])
                        ax1.text(n+widthx,m+widthy,'***',ha = 'center',color = 'white',fontdict=font_dict)
                else: 
                    if  pv< 0.05 and pv>= 0.01:
                        ax1.text(n+widthx,m+widthy,'*',ha = 'center',color = 'k',fontdict=font_dict)
                    elif  pv< 0.01 and pv>= 0.001:
                        ax1.text(n+widthx,m+widthy,'**',ha = 'center',color = 'k',fontdict=font_dict)
                    elif  pv< 0.001:
                        ax1.text(n+widthx,m+widthy,'***',ha = 'center',color = 'k',fontdict=font_dict)
    
    plt.title("行业板块"+info_type_cn+"之间的相关性")
    plt.tick_params(labelsize=corr_size)
    
    footnote1="\n显著性数值：***非常显著(<0.001)，**很显著(<0.01)，*显著(<0.05)，其余为不显著"
    footnote2="\n系数绝对值：>=0.8极强相关，0.6-0.8强相关，0.4-0.6相关，0.2-0.4弱相关，否则为极弱(不)相关"

    footnote3="\n观察期间: "+start+'至'+end
    import datetime as dt; stoday=dt.date.today()    
    footnote4="；来源：Sina/EM，"+str(stoday)+"；基于申万行业分类"
    
    fontxlabel={'size':corr_size}
    plt.xlabel(footnote1+footnote2+footnote3+footnote4,fontxlabel)
    plt.show()
    
    return df_coor

#==============================================================================
#==============================================================================
if __name__=='__main__':
    industries=['煤炭','医药生物','801750']
    top=10
    printout=True

def mixed_industry_stocks(industries=['煤炭','医药生物'],top=10,printout=True):
    """
    功能：将不同行业指数(industries)中的前top个(按指数内权重降序)成分股合成为字典，等权重
    """
    
    # 将行业列表转换为行业代码列表
    industries1=[]
    for i in industries:
        if i.isdigit():
            industries1=industries1+[i]
        else:
            industries1=industries1+[industry_sw_code(i)]
            
    # 抓取行业内成分股。合并
    import pandas as pd
    df=pd.DataFrame()
    for i in industries1:
        _,dft=industry_stock_sw(industry=i,top=top,printout=False)
        dft['行业代码']=i
        dft['行业名称']=industry_sw_name(i)
        
        if len(df)==0:
            df=dft
        else:
            df=pd.concat([df,dft])
            
    # 去掉重复的股票（假设可能有一只股票被计入多个指数）
    df.drop_duplicates(subset=['证券代码'], keep='first', inplace=True)
    df['初始权重']=round(1.0 / len(df),4)
    df.reset_index(drop=True,inplace=True)
    df['序号']=df.index+1
    
    df_print=df[['序号','证券名称','证券代码','初始权重','行业名称','行业代码']]
    
    if printout:
        alignlist=['center']+['center']*(len(list(df_print))-1)
        
        if len(industries) > 1:
            print("\n*** 混合行业投资组合的成分股：初始等权重\n")
        else:
            print("\n*** 单一行业投资组合的成分股：初始等权重\n")
            
        print(df_print.to_markdown(index=False,tablefmt='plain',colalign=alignlist))
        import datetime; today=datetime.date.today()
        print("\n*** 数据来源：申万宏源，统计日期："+str(today))
    
    # 生成成分股字典
    stock_dict=df.set_index(['证券代码'])['初始权重'].to_dict()

    return stock_dict    
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================



#==============================================================================

    