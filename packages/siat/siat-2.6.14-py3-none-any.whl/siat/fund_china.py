# -*- coding: utf-8 -*-
"""
本模块功能：中国基金市场案例分析
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2020年10月17日
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
from siat.grafix import *
from siat.bond_base import *
#==============================================================================
if __name__=='__main__':
    fund='000592.SS'
    quarter1='2022Q4'
    quarter2='2023Q1'
    
    df=fund_stock_holding_compare_china(fund,quarter1,quarter2,top=10)

#比较两个季度之间的基金持仓变化
def fund_stock_holding_compare_china(fund,quarter1,quarter2,top=10):
    """
    功能：基金fund在两个季度quarter1和quarter2的持仓股票对比（股数和金额），前top名股票
    参数：
    fund,str,基金代码;
    quarter1,str,靠前的季度, 格式为 'YYYYQ1',例如: '2021Q2';
    quarter2,str,靠后的季度, 格式为 'YYYYQ1',例如: '2021Q2';
    """
    print("Searching fund stock holding info, it may take time, please wait ...\n")
    
    import akshare as ak
    import pandas as pd    
    
    code=fund[:6]
    s1=quarter1.upper()
    s2=quarter2.upper()
    years=[s1[0:4],s2[0:4]]

    s1_share = s1+'持股数'
    s2_share = s2+'持股数'
    s1_value = s1+'持仓市值'
    s2_value = s2+'持仓市值'
    s1_ratio = s1+'持仓比例'
    s2_ratio = s2+'持仓比例'

    """
    try:
        data = ak.fund_portfolio_hold_em(symbol=fund,date=years[0])
    except:
        print("  #Error(fund_stock_holding_compare_china): stock fund",fund,"not found or wrong year",years[0])
        return
    if len(data)==0:
        print("  #Error(fund_stock_holding_compare_china): stock fund",fund,"not found or wrong year",years[0])
        return      
    """
    
    data=pd.DataFrame()
    for yr in years:
        try:
            df_tmp = ak.fund_portfolio_hold_em(symbol=code,date=yr)
        except:
            print("  #Error(fund_stock_holding_compare_china): wrong year",yr)
            break

        if len(df_tmp)==0:
            print("  #Error(fund_stock_holding_compare_china): stock fund",fund,"not found or wrong year",years[0])
            break
        
        if len(data)==0:
            data=df_tmp
        else:
            try:
                data = data.append(df_tmp)
            except:
                data = data._append(df_tmp)
            
    data.drop_duplicates(keep='first', inplace=True)

    data['季度']=data['季度'].apply(lambda x:x[:6])
    data['季度'] = data['季度'].str.replace('年','Q')
    data['占净值比例'] = pd.to_numeric(data['占净值比例'])

    df1 =data[data['季度']==s1]
    if len(df1)==0:
        print("  #Error(fund_stock_holding_compare_china): no data available for",s1)
        return        
    
    df1 = df1[['股票代码', '股票名称','持股数','持仓市值','占净值比例']]
    df1 = df1.rename(columns={'持股数':s1_share,'持仓市值':s1_value,'占净值比例':s1_ratio})
    df2 =data[data['季度']==s2]
    if len(df2)==0:
        print("  #Error(fund_stock_holding_compare_china): no data available for",s2)
        return 
    
    df2 = df2[['股票代码', '股票名称','持股数','持仓市值','占净值比例']]
    df2 = df2.rename(columns={'持股数':s2_share,'持仓市值':s2_value,'占净值比例':s2_ratio})

    df_merge = pd.merge(df1,df2,on='股票代码',how='outer')

# Q2 和 Q4，即半年度和年度报告，是需要披露全部持仓的
# 合并后，在dataframe 中 NaN 的数据应为 0

    if s1.endswith('Q2') or s1.endswith('Q4'):
        df_merge[s1_share] = df_merge[s1_share].fillna(0)
        df_merge[s1_value] = df_merge[s1_value].fillna(0)
        df_merge[s1_ratio] = df_merge[s1_ratio].fillna(0)

    if s2.endswith('Q2') or s2.endswith('Q4'):
        df_merge[s2_share] = df_merge[s2_share].fillna(0)
        df_merge[s2_value] = df_merge[s2_value].fillna(0)
        df_merge[s2_ratio] = df_merge[s2_ratio].fillna(0)

    df_merge.fillna(0,inplace=True)    

    df_merge['持股数变化'] = df_merge[s2_share] - df_merge[s1_share]
    df_merge = df_merge.sort_values(s2_value,ascending=False)
    
    df_merge['股票名称'] = df_merge['股票名称_y']
    df_merge.loc[df_merge['股票名称'].isna(),'股票名称'] = df_merge.loc[df_merge['股票名称'].isna(),'股票名称_x']
    df_merge = df_merge[['股票代码', '股票名称', s1_share,s1_value, s1_ratio,s2_share,s2_value,s2_ratio, '持股数变化']]
    
    df_merge.reset_index(drop=True,inplace=True)
    if top>0:
        df=df_merge.head(top)
    else:
        df=df_merge.head(-top)
    """
    #持股数和持仓比例取整数
    df.fillna(0)
    try:
        df[s1_share]=df[s1_share].astype('int')
    except: pass
    try:
        df[s2_share]=df[s2_share].astype('int')
    except: pass
    try:
        df[s1_value]=df[s1_value].astype('int')
    except: pass
    try:
        df[s2_value]=df[s2_value].astype('int')
    except: pass
    df['持股数变化'] = df[s2_share] - df[s1_share]
    """
    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    #获取基金名称
    """
    #names = ak.fund_em_fund_name()
    names = ak.fund_name_em()
    namedf=names[names['基金代码']==code]
    if len(namedf)==0:
        name=fund
    else:
        name=namedf['基金简称'].values[0]
    """
    name=get_fund_name_china2(fund)
    
    order='前'
    if top <0: 
        order='后'
        top=-top
        
    # 替换空值
    df.fillna('---')
    
    print("===== 中国基金持仓股票分析："+name+'，'+s1+"对比"+s2,"(按后者持仓比例高低排列，"+order+str(top)+"名股票) =====\n")
    print(df.to_string(index=False))
    import datetime; today = datetime.date.today()
    print("\n*** 注：持股数为万股，持仓市值为万元，持仓比例为占基金资产净值比例%，包括A股与非A股")
    print("    数据来源：天天基金/东方财富, 期间持仓股票总计"+str(len(df_merge))+"只,",today)      
    
    return df_merge

#==============================================================================

if __name__=='__main__':
    fund='000592.SS'
    year_num=2
    
    df=fund_stock_holding_rank_china(fund,year_num=2)
    
# 获取单只基金的十大股票名称信息
def fund_stock_holding_rank_china(fund,year_num=2):
    """
    比较股票型基金fund近year_num年持仓的前10大股票排名变化
    """
    print("Searching fund stock holding info, it may take time, please wait ...\n")
    code=fund[:6]
    
    import akshare as ak
    import pandas as pd

    import datetime; today = datetime.date.today()
    year_0_num=int(str(today)[0:4])
    years=[]
    for yr in range(0,year_num):
        yri=str(year_0_num - yr)
        years=years+[yri]
    years.sort(reverse=False)    
    """
    #抓取第一年的信息
    data = ak.fund_portfolio_hold_em(symbol=fund,date=years[0])
    if len(data)==0:
        print("  #Error(fund_stock_holding_rank_china): stock fund",fund,"not found")
        return          
    """
    data=pd.DataFrame()
    try:
        for yr in years:
            df_tmp = ak.fund_portfolio_hold_em(symbol=code,date=yr)
            try:
                data = data.append(df_tmp)
            except:
                data = data._append(df_tmp)
    except:
        years_1=[]
        for yr in years:
            yr_1=str(int(yr)-1)
            years_1=years_1+[yr_1]
            
        for yr in years_1:
            df_tmp = ak.fund_portfolio_hold_em(symbol=code,date=yr)
            try:
                data = data.append(df_tmp)
            except:
                data = data._append(df_tmp)
            
    data.drop_duplicates(keep='first', inplace=True)

    # data['季度']=data['季度'].apply(lambda x:x[:8])
    data['季度']=data['季度'].apply(lambda x:x[:6])
    data['季度'] = data['季度'].str.replace('年','Q')
    #data['占净值比例'] = pd.to_numeric(data['占净值比例'])
    #data.fillna(0,inplace=True)
    #data=data.replace('',0)
    data['占净值比例'] = pd.to_numeric(data['占净值比例'])
    
    # 序号中，有些是字符串，并且包含字符 “*”，需要替换，最后转换为数字
    data['序号'] = data['序号'].astype(str)
    data['序号'] = data['序号'].str.replace('\*','',regex=True)
    data['序号'] = pd.to_numeric(data['序号'])
    
    data = data.sort_values(['季度','持仓市值'],ascending=[True,False])
    #data.drop_duplicates(keep='first',inplace=True)
    
    yqlist=list(set(list(data['季度'])))
    yqlist.sort(reverse=False)
    import pandas as pd
    data2=pd.DataFrame()
    
    for yq in yqlist:
        dft=data[data['季度']==yq]
        dft.sort_values(by='占净值比例',ascending=False,inplace=True)
        dft.reset_index(drop=True,inplace=True)
        dft['序号']=dft.index + 1
        dft2=dft.head(10)
        
        if len(data2)==0:
            data2=dft2
        else:
            try:
                data2=data2.append(dft2)
            except:
                data2=data2._append(dft2)
    
    # 合成信息
    data2['持股状况']=data2.apply(lambda x: x['股票名称']+'('+str(x['占净值比例'])+'，'+str(x['持股数'])+')',axis=1)
    
    df = data2.set_index(['序号','季度']).stack().unstack([1,2]).head(10)
    
    #df = df.loc[:,(slice(None), '股票名称')] # 只选取 股票名称
    df = df.loc[:,(slice(None), '持股状况')] # 只选取 持股状况
    
    df = df.droplevel(None,axis=1)
    df.columns.name=None
    df.reset_index(inplace=True)
    """
    df['基金代码']=code
    cols = df.columns.tolist()
    cols = cols[:1] + cols[-1:] + cols[1:-1] # 将基金代码列名放前面
    df = df[cols]
    """
    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    #获取基金名称
    """
    #names = ak.fund_em_fund_name()
    names = ak.fund_name_em()
    namedf=names[names['基金代码']==fund]
    if len(namedf)==0:
        name=fund
    else:
        name=namedf['基金简称'].values[0]
    """
    name=get_fund_name_china2(fund)
    
    print("=== 基金持仓股票排行分析："+name+"，按照占净值比例高低排列 ===\n")
    
    alignlist=['center']+['left']*(len(list(df))-1)
    print(df.to_markdown(index=False,tablefmt='plain',colalign=alignlist))
    #print(df.to_string(index=False))
    
    import datetime; today = datetime.date.today()
    print("\n*** 注：包括A股与非A股。持股结构：股票简称(占净值比例%，持股数万股),",today)          
    #print("\n*** 注：包括A股与非A股。数据来源：天天基金/东方财富,",today)
    
    return df,data

#==============================================================================
if __name__=='__main__':
    fund='180801'
    top=10

def reits_jsl_china(fund='',top=10):
    """
    功能：REITs基金信息概述和列表
    目前不能正常工作，因为集思录数据源现在需要会员登陆才能显示和下载信息
    """
    import akshare as ak
    try:
        df1 = ak.reits_info_jsl()
        df2 = ak.reits_realtime_em()
    except:
        print("  #Error(reits_jsl_china): sorry, data source currently unavailable")
        return None
    
    #合成基金类型信息
    import pandas as pd
    df = pd.merge(df1,df2,on = ['代码'],how='left')    
    df.rename(columns={'涨幅':'涨幅%','成交额_x':'成交额(万元)','折价率':'折价率%','规模':'规模(亿元)','剩余年限':'剩余年限(年)','涨跌幅':'涨跌幅%'}, inplace=True)
    num=len(df)
    
    df.sort_values(by=['昨收'],ascending=False,inplace=True)
    df.reset_index(drop=True,inplace=True)
    import datetime
    today = datetime.date.today()
    
    dfa=df[df['代码']==fund]
    # 未找到
    if len(dfa)==0:
        if top > 0:
            dfa=df.head(top)
        else:
            dfa=df.tail(-top)
        dfb=dfa[['代码','名称','昨收','规模(亿元)','到期日']]
        
        #设置打印对齐
        pd.set_option('display.max_columns', 1000)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 1000)
        pd.set_option('display.unicode.ambiguous_as_wide', True)
        pd.set_option('display.unicode.east_asian_width', True)
        
        order='前'
        if top <0: 
            order='后'
            top=-top
        print("\n===== 中国REITs基金列表(按最新价高低排列，"+order+str(top)+"名) =====\n")
        print(dfb)

        print("*** 数据来源：东方财富/集思录, 总计"+str(num)+"只REITs基金,",today)         
        return dfb

    #单列一只基金的具体信息
    collist=['代码','简称','名称','全称','项目类型','基金公司','规模(亿元)','到期日','剩余年限(年)','净值','净值日期','现价','涨幅%','开盘价','最高价','最低价','昨收','成交额(万元)']
    maxcollen=0
    for i in collist:
        ilen=hzlen(i)
        if maxcollen < ilen:
            maxcollen=ilen
            
    dfb=dfa[collist]
    print("\n===== 中国REITs基金详情(代码"+fund+") =====\n")
    for i in collist:
        print(i,' '*(maxcollen-hzlen(i))+'：',dfb[i].values[0])

    print("*** 数据来源：东方财富/集思录,",today)         
    return dfb  

#==============================================================================
if __name__=='__main__':
    top=10
    
    df=reits_list_china(top=10)

def reits_list_china(top=20):
    """
    功能：REITs基金信息概述和列表
    目前不能正常工作，因为数据源集思录现在需要会员登陆才能显示信息
    """
    import akshare as ak
    try:
        df2 = ak.reits_realtime_em()
    except:
        print("  #Error(reits_profile_china): akshare does not work properly now")
        return None
    
    #df2.sort_values(by=['昨收'],ascending=False,inplace=True)
    df2.sort_values(by=['最新价'],ascending=False,inplace=True)
    df2.reset_index(drop=True,inplace=True)
    df2['序号']=df2.index + 1
    num=len(df2)
    
    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
        
    if top > 0:
        order='前'
        dfb=df2.head(top)
    else: 
        order='后'
        top=-top
        dfb=df2.tail(top)
    
    dfb.fillna("---",inplace=True)
    dfb['成交额']=dfb['成交额'].apply(lambda x: int(x))
    
    print("\n===== 中国REITs基金列表(按最新价高低排列，"+order+str(top)+"名) =====\n")
    """
    print(dfb.to_string(index=False))
    """
    #print('')   #在标题与表格之间空一行
    alignlist=['right','center','left']+['right']*9
    try:   
        print(dfb.to_markdown(index=False,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        print_df=dfb.to_markdown(index=False,tablefmt='plain',colalign=alignlist)
        print_df2=print_df.encode("utf-8",errors="strict")
        print(print_df2)       
        
    import datetime
    today = datetime.date.today()
    print("\n*** 数据来源：东方财富, 总计"+str(num)+"只REITs基金,",today)         
    
    return df2

#==============================================================================

if __name__=='__main__':
    fund_type='全部类型'
    fund_type='债券型'
    printout=True

def pof_list_china(fund_type='全部类型',printout=True):
    """
    功能：抓取公募基金列表，按照基金类型列表，按照基金名称拼音排序
    """
    print("Searching for publicly offering fund (POF) information in China ...")
    import akshare as ak
    
    #基金基本信息：基金代码，基金简称，基金类型
    #df = ak.fund_em_fund_name()
    df = ak.fund_name_em()
    
    df.sort_values(by=['拼音全称'],na_position='first',inplace=True)
    df.drop_duplicates(subset=['基金代码','基金类型'], keep='first',inplace=True)    
    
    #获取基金类型列表，并去掉重复项
    typelist=list(set(list(df['基金类型'])))
    #判断类型是否支持
    matchtype=False
    for t in typelist+['全部类型']:
        if fund_type in t:
            matchtype=True
            break
        
    if not matchtype:
        print("  #Error(fund_list_china): unsupported fund type:",fund_type)
        print("  Supported fund_type:",typelist+['全部类型'])
        return None

    #摘取选定的基金类型
    if fund_type != '全部类型':
        #df2=df[df['基金类型']==fund_type]
        df2=df[df['基金类型'].apply(lambda x: fund_type in x)]
    else:
        df2=df
    df3=df2[['基金简称','基金代码','基金类型']]
    df3.reset_index(drop=True,inplace=True) 
    
    #打印种类数量信息    
    if printout:
        num=len(df3)
        if fund_type != '全部类型':
            print(texttranslate("共找到")+str(num)+texttranslate("支基金, 类型为")+fund_type)
            return df3
        
        print("\n",texttranslate("======= 中国公募基金种类概况 ======="))
        print(texttranslate("公募基金总数："),"{:,}".format(num))
        print(texttranslate("其中包括："))
       
        maxlen=0
        for t in typelist:
            tlen=hzlen(t)
            if tlen > maxlen: maxlen=tlen
        maxlen=maxlen+1
        
        #排序
        dfg=pd.DataFrame(df.groupby("基金类型").size())
        dfg.sort_values(by=[0], ascending=False, inplace=True)
        typelist2=list(dfg.index)
        try:
            typelist2.remove('')
        except:
            pass
        
        for t in typelist2:
            n=len(df[df['基金类型']==t])
            """
            tlen=strlen(t)
            prefix=' '*4+t+' '*(maxlen-tlen)+':'
            print(prefix,"{:,}".format(n),"\b,",round(n/num*100,2),'\b%')
            """
            print('{t:<{len}}\t'.format(t=t,len=maxlen-len(t.encode('GBK'))+len(t)+2),str(n).rjust(6,' '),"\t",(str(round(n/num*100,2))+'%').rjust(6,' '))

        import datetime
        today = datetime.date.today()
        print(texttranslate("数据来源：东方财富/天天基金,"),today)
        
    return df3

if __name__=='__main__':
    df=pof_list_china()

#==============================================================================
if __name__=='__main__':
    info_type='单位净值'
    fund_type='股票型'

def oef_rank_china(info_type='单位净值',fund_type='全部类型',rank=10):
    """
    功能：中国开放式基金排名，单位净值，累计净值，手续费
    """
    typelist=['单位净值','累计净值','手续费','增长率']
    if info_type not in typelist:
        print("  #Error(oef_rank_china): unsupported info type",info_type)
        print("  Supported info type:",typelist)
        return None
    
    print("Searching for open-ended fund (OEF) information in China ...")
    import akshare as ak   
    
    #获取开放式基金实时信息
    df1 = ak.fund_open_fund_daily_em()
    collist=list(df1)
    nvname1=collist[2]
    nvdate=nvname1[:10]
    nvname2=collist[3]
    #修改列名
    df1.rename(columns={nvname1:'单位净值',nvname2:'累计净值'}, inplace=True) 
    #df1a=df1.drop(df1[df1['单位净值']==''].index)
    #df1b=df1a.drop(df1a[df1a['累计净值']==''].index)
    df1c=df1[['基金代码','基金简称','单位净值','累计净值','日增长率','申购状态','赎回状态','手续费']]
    
    
    #获取所有公募基金类型信息
    #df2 = ak.fund_em_fund_name()
    df2 = ak.fund_name_em()
    
    df2a=df2[['基金代码','基金类型']]
    
    #合成基金类型信息
    import pandas as pd
    import numpy as np
    df3 = pd.merge(df1c,df2a,on = ['基金代码'],how='left')
    
    df3.fillna(0,inplace=True)
    df3=df3.replace('',0)
    df3['单位净值']=df3['单位净值'].astype('float')
    df3['累计净值']=df3['累计净值'].astype('float')
    df3['日增长率']=df3['日增长率'].astype('float')
    
    """
    df=df3[(df3['基金类型'] is not np.nan) and (df3['基金类型'] != 0)]
    """
    # 避免该字段出现非字符串类型引起后续出错
    df3['基金类型']=df3['基金类型'].astype(str)
    df=df3
    
    #过滤基金类型
    if fund_type != '全部类型':
        fundtypelist=list(set(list(df['基金类型'])))
        """
        while np.nan in fundtypelist:
            fundtypelist.remove(np.nan)
        while 0 in fundtypelist:
            fundtypelist.remove(0)            
        """    
        found=False
        for ft in fundtypelist:
            if ft==0: continue
            if fund_type in ft: 
                found=True
                break
        if not found:
            print("  #Error(oef_rank_china): unsupported fund type",fund_type)
            print("  Supported fund type:",fundtypelist)
            return None
        fund_filter=lambda x: fund_type in x
        df.dropna(inplace=True)
        df['基金类型s']=df['基金类型'].apply(fund_filter)
        
        if fund_type == 'QDII':
            df['基金类型s']=df.apply(lambda x: False if '不含' in x['基金类型'] else x['基金类型s'],axis=1)
        
        df=df[df['基金类型s']==True]    
    
    if info_type == '单位净值':
        df['单位净值']=df['单位净值'].apply(lambda x: round(x,2))
        df.sort_values(by=['单位净值'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','基金类型','单位净值','申购状态','赎回状态']]
        print(texttranslate("\n===== 中国开放式基金排名：单位净值 ====="))
    
    if info_type == '累计净值':
        df['累计净值']=df['累计净值'].apply(lambda x: round(x,2))
        df.sort_values(by=['累计净值'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','基金类型','累计净值','申购状态','赎回状态']]
        print(texttranslate("\n===== 中国开放式基金排名：累计净值 ====="))      
    
    if info_type == '手续费':
        df.sort_values(by=['手续费'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','基金类型','手续费','申购状态','赎回状态']]
        print(texttranslate("\n===== 中国开放式基金排名：手续费 ====="))          
    
    if info_type == '增长率':
        df.sort_values(by=['日增长率'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','基金类型','日增长率','申购状态','赎回状态']]
        print(texttranslate("\n===== 中国开放式基金排名：增长率% ====="))          
    
    df=df.replace(0,'--')
    
    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    dfprint.dropna(inplace=True)
    dfprint.reset_index(drop=True,inplace=True)
    dfprint.index=dfprint.index + 1
    
    if rank >= 0:
        dfprint10=dfprint.head(rank)
    else:
        dfprint10=dfprint.tail(-rank)
    #print(dfprint10.to_string(index=False))
    """
    print(dfprint10)
    """
    """
    alignlist=['left','left']+['center']*(len(list(amac_sum_df.head(10)))-3)+['right']
    """
    print('')   #在标题与表格之间空一行
    alignlist=['right','left','center','center','right','center','center']
    try:   
        print(dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        print_df=dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist)
        print_df2=print_df.encode("utf-8",errors="strict")
        print(print_df2)    
    
    print('\n'+texttranslate("共找到披露净值信息的开放式基金数量:"),len(dfprint),'\b，',end='')
    print(texttranslate("基金类型:"),fund_type)
    
    print(texttranslate("净值日期:"),nvdate,'\b. ',end='')
    import datetime
    today = datetime.date.today()
    print(texttranslate("数据来源：东方财富/天天基金,"),today)        
    
    return df

if __name__=='__main__':
     df=oef_rank_china(info_type='单位净值')
     df=oef_rank_china(info_type='累计净值')
     df=oef_rank_china(info_type='手续费')

#==============================================================================
if __name__=='__main__':
    fund_code='000009'
    fund_code='0000XX'
    fund_name,fund_type=get_oef_name_china(fund_code)
    
def get_oef_name_china(fund_code):
    """
    功能：获得基金的名称和类型
    """
    
    import akshare as ak 
    try:
        names=ak.fund_name_em() 
    except:
        return fund_code,'未知类型'
    
    dft=names[names['基金代码']==fund_code]
    if len(dft) != 0:
        fund_name=dft['基金简称'].values[0]
        fund_type=dft['基金类型'].values[0]
    else:
        return fund_code,'未知类型'
    
    return fund_name,fund_type

#==============================================================================
if __name__=='__main__':
    fund='050111.SS'
    fund='000592.SS'
    fromdate='2020-9-1'
    todate='2021-9-1'
    trend_type='净值'
    power=0
    twinx=False
    zeroline=False

def oef_trend_china(fund,fromdate,todate,trend_type='净值', \
                    power=0,twinx=False,loc1='upper left',loc2='lower left'):
    """
    功能：开放式基金业绩趋势，单位净值，累计净值，近三个月收益率，同类排名，总排名
    """
    #检查走势类型
    trendlist=["净值","收益率","排名"]
    if trend_type not in trendlist:
        print("  #Error(oef_trend_china): unsupported trend type:",trend_type)
        print("  Supported trend types:",trendlist)
        return None
    
    #检查日期
    result,start,end=check_period(fromdate,todate)
    if not result:
        print("  #Error(oef_trend_china): invalid date period:",fromdate,todate)
        return None
    """
    #转换日期格式
    import datetime
    startdate=datetime.datetime.strftime(start,"%Y-%m-%d")
    enddate=str(datetime.datetime.strftime(end,"%Y-%m-%d"))
    """
    print("Searching for open-ended fund (OEF) trend info in China ...")
    import akshare as ak   

    #开放式基金-历史数据
    import datetime; today = datetime.date.today()
    source=texttranslate("数据来源：东方财富/天天基金")

    fund1=fund[:6]
    fund_name,_=get_oef_name_china(fund1)

    #绘制单位/累计净值对比图
    if trend_type == '净值':
        df1 = ak.fund_open_fund_info_em(fund=fund1, indicator="单位净值走势")
        df1.rename(columns={'净值日期':'date','单位净值':'单位净值'}, inplace=True)
        df1['日期']=df1['date']
        df1.set_index(['date'],inplace=True) 
        
        df2 = ak.fund_open_fund_info_em(fund=fund1, indicator="累计净值走势")
        df2.rename(columns={'净值日期':'date','累计净值':'累计净值'}, inplace=True)
        df2.set_index(['date'],inplace=True)       
        
        #合并
        import pandas as pd
        df = pd.merge(df1,df2,left_index=True,right_index=True,how='inner')
        dfp=df[(df['日期'] >= start)]
        dfp=dfp[(dfp['日期'] <= end)]
        if len(dfp) == 0:
            print("  #Error(oef_trend_china): no info found for",fund,"in the period:",fromdate,todate)
            return
        
        #绘制双线图
        ticker1=fund1; colname1='单位净值';label1=texttranslate('单位净值')
        ticker2=fund1; colname2='累计净值';label2=texttranslate('累计净值')
        #ylabeltxt='人民币元'
        ylabeltxt=texttranslate('净值')
        
        titletxt=texttranslate("开放式基金的净值趋势：")+fund_name
        
        #footnote=source+', '+str(today)
        footnote='注意：图中为基金市场交易价格，存在溢价或折价，可能与基金公司公布的净值存在差异\n'+source+', '+str(today)
        
        plot_line2(dfp,ticker1,colname1,label1, \
               dfp,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote,power=power,twinx=twinx, \
                   loc1=loc1,loc2=loc2)
        return df
    
    #绘制累计收益率单线图
    if trend_type == '收益率':
        df = ak.fund_open_fund_info_em(fund=fund1, indicator="累计收益率走势")
        df.rename(columns={'净值日期':'date','累计收益率':'累计收益率'}, inplace=True)
        df['日期']=df['date']
        df.set_index(['date'],inplace=True) 
        dfp=df[(df['日期'] >= start)]
        dfp=dfp[(dfp['日期'] <= end)]  
        if len(dfp) == 0:
            print("  #Error(oef_trend_china): no info found for",fund,"in the period:",fromdate,todate)
            return        
    
        colname='累计收益率'; collabel=texttranslate('累计收益率%')
        ylabeltxt=texttranslate('收益率%')
        titletxt=texttranslate("开放式基金的累计收益率趋势：")+fund_name
        footnote=source+', '+str(today)
        plot_line(dfp,colname,collabel,ylabeltxt,titletxt,footnote,power=power,loc=loc1)    
        return df
    
    #绘制同类排名图：近三个月收益率
    if trend_type == '排名':
        df1 = ak.fund_open_fund_info_em(fund=fund1, indicator="同类排名走势")
        df1.rename(columns={'报告日期':'date','同类型排名-每日近三月排名':'同类排名','总排名-每日近三月排名':'总排名'}, inplace=True)
        df1['日期']=df1['date']
        df1['总排名']=df1['总排名'].astype('int64')
        df1.set_index(['date'],inplace=True) 
        
        df2 = ak.fund_open_fund_info_em(fund=fund1, indicator="同类排名百分比")
        df2.rename(columns={'报告日期':'date','同类型排名-每日近3月收益排名百分比':'同类排名百分比'}, inplace=True)
        df2.set_index(['date'],inplace=True)       
        
        #合并
        import pandas as pd
        df = pd.merge(df1,df2,left_index=True,right_index=True,how='inner')
        dfp=df[(df['日期'] >= start)]
        dfp=dfp[(dfp['日期'] <= end)]
        if len(dfp) == 0:
            print("  #Error(oef_trend_china): no info found for",fund,"in the period:",fromdate,todate)
            return        

        #绘制双线图：同类排名，总排名
        ylabeltxt=''
        titletxt=texttranslate("开放式基金的近三个月收益率排名趋势：")+fund_name
        
        footnote=source+', '+str(today)        
        
        ticker1=fund1; colname1='同类排名';label1=texttranslate('同类排名')
        """
        ticker2=fund1; colname2='同类排名百分比';label2=texttranslate('同类排名百分比')
        dfp1=pd.DataFrame(dfp[colname1])
        dfp2=pd.DataFrame(dfp[colname2])
        plot_line2(dfp1,ticker1,colname1,label1, \
               dfp2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote,power=power,twinx=True)
        """
        #    
        ticker2=fund1; colname2='总排名';label2=texttranslate('开放式基金总排名')  
        dfp1=pd.DataFrame(dfp[colname1])
        dfp2=pd.DataFrame(dfp[colname2])        
        plot_line2(dfp1,ticker1,colname1,label1, \
               dfp2,ticker2,colname2,label2, \
               ylabeltxt,titletxt,footnote,power=power,twinx=twinx, \
                   loc1=loc1,loc2=loc2)            
        
        return df
    
#==============================================================================
if __name__=='__main__':
    pass

def mmf_rank_china(rank=10):
    """
    功能：中国货币型基金排名，7日年化收益率%
    """
    
    print("Searching for money market fund (OEF) information in China ...")
    import akshare as ak   
    
    #获取货币型基金实时信息
    df = ak.fund_money_fund_daily_em()
    collist=list(df)
    nvname=collist[6]
    nvdate=nvname[:10]
    #修改列名
    df.rename(columns={nvname:'7日年化%'}, inplace=True) 
    #dfa=df.drop(df[df['7日年化%']==''].index)
    dfb=df[['基金代码','基金简称','7日年化%','成立日期','基金经理','手续费']]
    
    dfb.sort_values(by=['7日年化%'],ascending=False,inplace=True)
    dfprint=dfb[['基金简称','基金代码','7日年化%','基金经理','手续费']]
    print(texttranslate("\n======= 中国货币型基金排名：7日年化收益率 ======="))
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    dfprint.dropna(inplace=True)
    dfprint.reset_index(drop=True,inplace=True)
    dfprint.index=dfprint.index + 1
    
    if rank >=0:
        dfprint10=dfprint.head(rank)
    else:
        dfprint10=dfprint.tail(-rank)
    #print(dfprint10.to_string(index=False))
    """
    print(dfprint10)
    """
    print('')   #在标题与表格之间空一行
    alignlist=['right','left','center','center','center','right']
    try:   
        print(dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        print_df=dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist)
        print_df2=print_df.encode("utf-8",errors="strict")
        print(print_df2)       
    
    print('')   #在表格与脚注之间空一行
    print(texttranslate("共找到披露收益率信息的货币型基金数量:"),len(dfprint))
    
    print(texttranslate("收益率日期:"),nvdate,'\b. ',end='')    
    import datetime
    today = datetime.date.today()
    print(texttranslate("数据来源：东方财富/天天基金,"),today)        
    
    return df

if __name__=='__main__':
     df=mmf_rank_china()

#==============================================================================
if __name__=='__main__':
    fund='320019.SS'
    fromdate='2020-1-1'
    todate='2020-10-16'
    power=0

def mmf_trend_china(fund,fromdate,todate,power=0):
    """
    功能：货币型基金业绩趋势，7日年化收益率
    """
    
    #检查日期
    result,start,end=check_period(fromdate,todate)
    if not result:
        print("  #Error(mmf_trend_china): invalid date period:",fromdate,todate)
        return None
    import datetime
    startdate=datetime.datetime.strftime(start,"%Y-%m-%d")
    enddate=str(datetime.datetime.strftime(end,"%Y-%m-%d"))
    
    print("Searching for money market fund (MMF) trend info in China ...")
    import akshare as ak   

    #基金历史数据
    import datetime; today = datetime.date.today()
    source=texttranslate("数据来源：东方财富/天天基金")

    
    #绘制收益率单线图
    fund1=fund[:6]
    df = ak.fund_money_fund_info_em(fund1)
    df.sort_values(by=['净值日期'],ascending=True,inplace=True)
    df['7日年化%']=df['7日年化收益率'].astype("float")
    
    import pandas as pd
    df['date']=pd.to_datetime(df['净值日期'])
    df.set_index(['date'],inplace=True) 
    
    dfp = df[(df.index >= startdate)]
    dfp = dfp[(dfp.index <= enddate)]    
    if len(dfp) == 0:
        print("  #Error(mmf_trend_china): no info found for",fund,"in the period:",fromdate,todate)
        return    
    
    colname='7日年化%'; collabel=texttranslate('7日年化%')
    ylabeltxt=''
    titletxt=texttranslate("货币型基金的7日年化收益率趋势：")+get_fund_name_china2(fund)
    footnote=source+', '+str(today)
    plot_line(dfp,colname,collabel,ylabeltxt,titletxt,footnote,power=power)    
    
    return df
    
#==============================================================================
if __name__=='__main__':
    info_type='单位净值'
    fund_type='全部类型'
    fund_type='增长率'
    rank=10

def etf_rank_china(info_type='单位净值',fund_type='全部类型',rank=10):
    """
    功能：中国ETF基金排名，单位净值，累计净值，手续费
    """
    typelist=['单位净值','累计净值','市价','增长率']
    if info_type not in typelist:
        print("  #Error(etf_rank_china): unsupported info type",info_type)
        print("  Supported info type:",typelist)
        return None
    
    print("Searching for exchange traded fund (ETF) information in China ...")
    import akshare as ak   
    
    #获取ETF基金实时信息
    df1 = ak.fund_etf_fund_daily_em()
    #删除全部为空值'---'的列
    df1t=df1.T
    df1t['idx']=df1t.index
    df1t.drop_duplicates(subset=['idx'],keep='last',inplace=True)
    df2=df1t.T
    #删除空值'---'的列
    
    #提取净值日期
    collist=list(df2)
    nvname1=collist[3]
    nvdate=nvname1[:10]
    nvname2=collist[4]
    #修改列名
    df3=df2.rename(columns={nvname1:'单位净值',nvname2:'累计净值'}) 
    df=df3[['基金简称','基金代码','类型','单位净值','累计净值','增长率','市价']]
    
    # 过滤idx行
    df=df[df.index != 'idx']
    
    #过滤基金类型
    if fund_type != '全部类型':
        fundtypelist=list(set(list(df['类型'])))
        found=False
        for ft in fundtypelist:
            if fund_type in ft: 
                found=True
                break
        if not found:
            print("  #Error(etf_rank_china): unsupported fund type",fund_type)
            print("  Supported fund type:",fundtypelist)
            return None
        fund_filter=lambda x: fund_type in x
        df['基金类型s']=df['类型'].apply(fund_filter)
        
        if fund_type == 'QDII':
            df['基金类型s']=df.apply(lambda x: False if '不含' in x['类型'] else x['基金类型s'],axis=1)
        
        df=df[df['基金类型s']==True]  
    
    #df=df.replace('---',0)
    if info_type == '单位净值':
        df=df.replace('---',0)
        df['单位净值']=df['单位净值'].astype(float)
        df.sort_values(by=['单位净值'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','类型','单位净值','市价']]
        print(texttranslate("\n===== 中国ETF基金排名：单位净值 ====="))
    
    if info_type == '累计净值':
        df=df.replace('---',0)
        df['累计净值']=df['累计净值'].astype(float)
        df.sort_values(by=['累计净值'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','类型','累计净值','单位净值']]
        print(texttranslate("\n===== 中国ETF基金排名：累计净值 ====="))        
    
    if info_type == '市价':
        df=df.replace('---',0)
        df['市价']=df['市价'].astype(float)
        df.sort_values(by=['市价'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','类型','市价','单位净值']]
        print(texttranslate("\n===== 中国ETF基金排名：市价 ====="))          
    
    if info_type == '增长率':
        df['增长率']=df['增长率'].astype(str)
        df.sort_values(by=['增长率'],ascending=False,inplace=True)
        dfprint=df[['基金简称','基金代码','类型','增长率','市价','单位净值']]
        print(texttranslate("\n===== 中国ETF基金排名：增长率 ====="))   
        
    #设置打印对齐
    import pandas as pd
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    dfprint.dropna(inplace=True)
    dfprint.reset_index(drop=True,inplace=True)
    dfprint.index=dfprint.index + 1
    
    if rank >=0:
        dfprint10=dfprint.head(rank)
    else:
        dfprint10=dfprint.tail(-rank)
    #print(dfprint10.to_string(index=False))
    """
    print(dfprint10)
    """
    print('')   #在标题与表格之间空一行
    alignlist=['right','left','center','center','right','right']
    try:   
        print(dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        print_df=dfprint10.to_markdown(index=True,tablefmt='plain',colalign=alignlist)
        print_df2=print_df.encode("utf-8",errors="strict")
        print(print_df2)       
    
    print('')   #空一行
    print(texttranslate("共找到披露净值信息的ETF基金数量:"),len(dfprint),'\b. ',end='')
    print(texttranslate("基金类型:"),fund_type)
    
    print(texttranslate("净值日期:"),nvdate,'\b. ',end='')
    import datetime
    today = datetime.date.today()
    print(texttranslate("数据来源：东方财富/天天基金,"),today)        
    
    return df

if __name__=='__main__':
     df=etf_rank_china(info_type='单位净值',fund_type='全部类型')
     df=etf_rank_china(info_type='累计净值')
     df=etf_rank_china(info_type='市价')

#==============================================================================
if __name__=='__main__':
    fund='159922.SS'
    fromdate='2020-1-1'
    todate='2020-10-16'

def etf_trend_china(fund,fromdate,todate,loc1='best',loc2='best',twinx=False,graph=True):
    """
    功能：ETF基金业绩趋势，单位净值，累计净值
    """
    #检查日期
    result,start,end=check_period(fromdate,todate)
    if not result:
        print("  #Error(oef_trend_china): invalid date period:",fromdate,todate)
        return None
    #转换日期格式
    import datetime
    startdate=str(datetime.datetime.strftime(start,"%Y-%m-%d"))
    enddate=str(datetime.datetime.strftime(end,"%Y-%m-%d"))

    print("Searching for exchange traded fund (ETF) trend info in China ...")
    import akshare as ak   

    import datetime; today = datetime.date.today()
    source=texttranslate("数据来源：东方财富/天天基金")

    
    #获取基金数据
    fund1=fund[:6]
    df = etf_hist_df = ak.fund_etf_fund_info_em(fund1)
    import pandas as pd
    df['date']=pd.to_datetime(df['净值日期'])
    df.set_index(['date'],inplace=True) 
    df['单位净值']=df['单位净值'].astype("float")
    df['累计净值']=df['累计净值'].astype("float")
        
    dfp=df[(df['净值日期'] >= start)]
    dfp=dfp[(dfp['净值日期'] <= end)]
    if len(dfp) == 0:
        print("  #Error(etf_trend_china): no info found for",fund,"in the period:",fromdate,todate)
        return    
        
    #绘制双线图
    if graph:
        ticker1=fund1; colname1='单位净值';label1=texttranslate('单位净值')
        ticker2=fund1; colname2='累计净值';label2=texttranslate('累计净值')
        ylabeltxt=texttranslate('人民币元')
        titletxt=texttranslate("ETF基金的净值趋势：")+get_fund_name_china2(fund)
        footnote=source+', '+str(today)
        
        plot_line2(dfp,ticker1,colname1,label1, \
                   dfp,ticker2,colname2,label2, \
                   ylabeltxt,titletxt,footnote, twinx=twinx, \
                       loc1=loc1,loc2=loc2)
    
    return dfp
    
if __name__=='__main__':
    df=etf_trend_china('510580','2019-1-1','2020-9-30')
    
#==============================================================================

def fund_summary_china():
    """
    功能：中国基金投资机构概况
    爬虫来源地址：https://zhuanlan.zhihu.com/p/97487003
    """
    print("Searching for fund investment institutions in China ...")
    import akshare as ak

    #会员机构综合查询：
    #机构类型：'商业银行','支付结算机构','证券公司资管子公司','会计师事务所',
    #'保险公司子公司','独立服务机构','证券投资咨询机构','证券公司私募基金子公司',
    #'私募基金管理人','公募基金管理公司','地方自律组织','境外机构','期货公司',
    #'独立第三方销售机构','律师事务所','证券公司','其他机构','公募基金管理公司子公司',
    #'期货公司资管子公司','保险公司'
    try:
        amac_df = ak.amac_member_info()
    except:
        print("  #Error(): data source tentatively inaccessible, try later")
        return None
    
    """    
    typelist=['公募基金管理公司','公募基金管理公司子公司','私募基金管理人', \
                '期货公司','期货公司资管子公司','证券公司', \
                '证券公司私募基金子公司','证券公司资管子公司','境外机构']
    """
    typelist=list(set(list(amac_df["机构类型"])))
    """
    maxlen=0
    for t in typelist:
        #tlen=strlen(t)
        tlen=hzlen(t)
        if tlen > maxlen: maxlen=tlen
    maxlen=maxlen+1
    """
    
    import pandas as pd
    pd.set_option('display.max_columns',1000)   # 设置最大显示列数的多少
    pd.set_option('display.width',1000)         # 设置宽度,就是说不换行,比较好看数据
    pd.set_option('display.max_rows',500)       # 设置行数的多少
    pd.set_option('display.colheader_justify','left')
      
    print(texttranslate("\n===== 中国基金投资机构概况 ====="))
    print(texttranslate("机构（会员）数量："),end='')
    num=len(list(set(list(amac_df["机构（会员）名称"]))))
    print("{:,}".format(num))
        
    print(texttranslate("其中包括："))
    amac_sum_df=pd.DataFrame(columns=['机构类型','数量','占比%'])
    for t in typelist:
        df_sub=amac_df[amac_df['机构类型']==t]
        n=len(list(set(list(df_sub['机构（会员）名称']))))
        pct=round(n/num*100,2)
        
        s=pd.Series({'机构类型':t,'数量':n,'占比%':pct})
        try:
            amac_sum_df=amac_sum_df.append(s,ignore_index=True)
        except:
            amac_sum_df=amac_sum_df._append(s,ignore_index=True)        
        """
        tlen=hzlen(t)
        prefix=' '*4+t+'.'*(maxlen-tlen)+':'
        print(prefix,"{:,}".format(n),"\b,",round(n/num*100,2),'\b%')     
        """
        #print('{t:<{len}}\t'.format(t=t,len=maxlen-len(t.encode('GBK'))+len(t)),"{:,}".format(n),"\b,",round(n/num*100,2),'\b%')
        #print('{t:<{len}}\t'.format(t=t,len=maxlen-len(t.encode('GBK'))+len(t)),str(n).rjust(6,' '),"\t",(str(round(n/num*100,2))+'%').rjust(6,' '))
    
    amac_sum_df.sort_values(by=['数量'],ascending=False,inplace=True)
    amac_sum_df.reset_index(drop=True,inplace=True)        
    amac_sum_df.index=amac_sum_df.index + 1   
    """
    from IPython.display import display
    display(amac_sum_df.head(10))
    """
    """
    pandas2prettytable(amac_sum_df.head(10),titletxt='',firstColSpecial=True,leftColAlign='l',otherColAlign='c',tabborder=False)
    """
    alignlist=['left','left']+['center']*(len(list(amac_sum_df.head(10)))-3)+['right']
    try:   
        print(amac_sum_df.head(10).to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    except:
        #解决汉字编码gbk出错问题
        print_df=amac_sum_df.head(10).to_markdown(index=True,tablefmt='plain',colalign=alignlist)
        print_df2=print_df.encode("utf-8",errors="strict")
        print(print_df2)
    
    import datetime; today = datetime.date.today()
    source=texttranslate("\n数据来源：中国证券投资基金业协会")
    footnote=source+', '+str(today)  
    print(footnote)
    
    """    
    print(texttranslate("\n===== 中国基金投资机构会员代表概况 ====="))
    print(texttranslate("会员代表人数："),end='')
    num=len(list(set(list(amac_df["会员代表"]))))
    print("{:,}".format(num))        
        
    print(texttranslate("其中工作在："))
    amac_mbr_df=pd.DataFrame(columns=['机构类型','数量','占比%'])
    for t in typelist:
        df_sub=amac_df[amac_df['机构类型']==t]
        n=len(list(set(list(df_sub['会员代表']))))
        pct=round(n/num*100,2)
        
        s=pd.Series({'机构类型':t,'数量':n,'占比%':pct})
        try:
            amac_mbr_df=amac_sum_df.append(s,ignore_index=True)
        except:
            amac_mbr_df=amac_mbr_df._append(s,ignore_index=True)        

    amac_mbr_df.sort_values(by=['数量'],ascending=False,inplace=True)
    amac_mbr_df.reset_index(drop=True,inplace=True)        
    amac_mbr_df.index=amac_mbr_df.index + 1  

    pandas2prettytable(amac_mbr_df.head(10),titletxt='',firstColSpecial=True,leftColAlign='l',otherColAlign='c',tabborder=False)
    print(footnote)        
    """
    
    return amac_df


#==============================================================================
if __name__=='__main__':
    location='全国'
    df=pef_manager_china(location='全国')

def pef_manager_china(location='全国'):
    """
    功能：中国私募基金管理人地域分布概况
    爬虫来源地址：https://zhuanlan.zhihu.com/p/97487003
    """
    
    print("Searching for private equity fund (PEF) managers info in China ...")
    import akshare as ak
    import pandas as pd

    #私募基金管理人综合查询
    manager_df = ak.amac_manager_info()
    num=len(list(manager_df["法定代表人/执行事务合伙人(委派代表)姓名"]))
    
    #注册地检查
    if location != '全国':
        typelist=sort_pinyin(list(set(list(manager_df['注册地']))))
        typelist.remove('')
        if location not in typelist:
            print("  #Error(pef_manager_china): failed to find registration place-"+location)
            print("  Supported registration place：",typelist+['全国'])
            return

    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)

    import datetime; today = datetime.date.today()
    source=texttranslate("数据来源：中国证券投资基金业协会")
    footnote=source+', '+str(today)          
    
    if location != '全国':
        manager_df=manager_df[manager_df['注册地']==location]
        print(texttranslate("\n===== 中国私募基金管理人角色分布 ====="))
        print(texttranslate("地域：")+location)
        print(texttranslate("法定代表人/执行合伙人数量："),end='')
        num1=len(list(manager_df["法定代表人/执行事务合伙人(委派代表)姓名"]))
        print("{:,}".format(num1),texttranslate('\b, 占比全国'),round(num1/num*100.0,2),'\b%')
        
        print(texttranslate("其中, 角色分布："))
        #instlist=list(set(list(manager_df['机构类型'])))
        instlist=['私募股权、创业投资基金管理人','私募证券投资基金管理人','私募资产配置类管理人','其他私募投资基金管理人']
        mtype=pd.DataFrame(columns=['管理人类型','人数','占比%'])
        for t in instlist:
            df_sub=manager_df[manager_df['机构类型']==t]
            n=len(list(df_sub['法定代表人/执行事务合伙人(委派代表)姓名']))
            pct=round(n/num1*100,2)
            s=pd.Series({'管理人类型':t,'人数':n,'占比%':pct})
            try:
                mtype=mtype.append(s,ignore_index=True)
            except:
                mtype=mtype._append(s,ignore_index=True)
        mtype.sort_values(by=['人数'],ascending=False,inplace=True)
        mtype.reset_index(drop=True,inplace=True)        
        mtype.index=mtype.index + 1
        
        print(mtype)
        print(footnote)
        return manager_df
    
    print(texttranslate("\n===== 中国私募基金管理人地域分布概况 ====="))
    print(texttranslate("法定代表人/执行合伙人数量："),end='')
    num=len(list(manager_df["法定代表人/执行事务合伙人(委派代表)姓名"]))
    print("{:,}".format(num))  
        
    typelist=sort_pinyin(list(set(list(manager_df['注册地']))))
    typelist.remove('')
        
    print(texttranslate("其中分布在："))
    location=pd.DataFrame(columns=['注册地','人数','占比%'])
    for t in typelist:
        df_sub=manager_df[manager_df['注册地']==t]
        n=len(list(df_sub['法定代表人/执行事务合伙人(委派代表)姓名']))
        pct=round(n/num*100,2)
        s=pd.Series({'注册地':t,'人数':n,'占比%':pct})
        try:
            location=location.append(s,ignore_index=True)
        except:
            location=location._append(s,ignore_index=True)
    location.sort_values(by=['人数'],ascending=False,inplace=True)
        
    location.reset_index(drop=True,inplace=True)
    location.index=location.index + 1
    
    location10=location.head(10)
    pctsum=round(location10['占比%'].sum(),2)
    
    print(location10)
    print(texttranslate("上述地区总计占比:"),pctsum,'\b%')
    print(footnote)             
    
    """
    print("\n===== 中国私募基金管理人角色分布 =====")
    print("地域："+location)
    print("法定代表人/执行合伙人数量：",end='')
    num1=len(list(manager_df["法定代表人/执行事务合伙人(委派代表)姓名"]))
    print("{:,}".format(num1),'\b, 占比全国',round(num1/num*100.0,2),'\b%')
        
    print("其中, 角色分布：")
    #instlist=list(set(list(manager_df['机构类型'])))
    instlist=['私募股权、创业投资基金管理人','私募证券投资基金管理人','私募资产配置类管理人','其他私募投资基金管理人']
    mtype=pd.DataFrame(columns=['管理人类型','人数','占比%'])
    for t in instlist:
        df_sub=manager_df[manager_df['机构类型']==t]
        n=len(list(df_sub['法定代表人/执行事务合伙人(委派代表)姓名']))
        pct=round(n/num1*100,2)
        s=pd.Series({'管理人类型':t,'人数':n,'占比%':pct})
        mtype=mtype.append(s,ignore_index=True) 
    mtype.sort_values(by=['人数'],ascending=False,inplace=True)
    mtype.reset_index(drop=True,inplace=True)        
        
    print(mtype)
    print(footnote)
    """
    
    return manager_df


#==============================================================================
if __name__=='__main__':
    start_page=1
    end_page=10
    step_pages=5
    DEBUG=True
    
    df,failedpages=get_pef_product_china_pages(start_page,end_page,step_pages)

def get_pef_product_china_pages(start_page,end_page,step_pages,DEBUG=True):   
    """
    功能：获取中国私募基金产品运营方式和状态信息，指定页数范围和页数跨度
    返回：获取的数据，失败的页数范围列表。
    """
    DEBUG=DEBUG
    if DEBUG:
        print("  Starting to retrieve pef info from",start_page,"to",end_page,"by every",step_pages,"pages ...")
    
    import akshare as ak
    import pandas as pd
    
    df=pd.DataFrame()
    pg=start_page
    failedpages=[]
    while pg <= end_page:
        pg_end=pg+step_pages-1
        try:
            if DEBUG:
                print("    Getting pef info from page",pg,"to",pg_end)
            dft = ak.amac_fund_info(start_page=str(pg),end_page=str(pg_end))
            
            if len(df)==0:
                df=dft
            else:
                #df=df.append(dft)
                df=pd.concat([df,dft],ignore_index=True)
        except:
            if DEBUG:
                print("  Warning: failed to get pef pages from",pg,'to',pg_end)
            failedpages=failedpages+[[pg,pg_end]]
        
        pg=pg_end + 1
    
    if DEBUG:
        print('\n',end='')
        print("  Successfully retrieved pef info",len(df),"records, with failed page range",len(failedpages),'pairs')

    return df,failedpages

#==============================================================================
if __name__=='__main__':
    max_pages=2000
    step_page_list=[100,10,1]
    DEBUG=True

def get_pef_product_china(max_pages=2000,step_page_list=[200,10,1],DEBUG=True):   
    """
    功能：获取中国私募基金产品运营方式和状态信息，耗时较长
    注意：由于获取过程极易失败，因此分割为三个阶段进行下载，然后合成。
    """
    print("  Searching pef info repeatedly, may need several hours, please wait ...")
    import pandas as pd
    
    # 第1步：页数跨度最大
    per_step=1
    step_pages=step_page_list[per_step-1]
    df1,failedpages1=get_pef_product_china_pages(start_page=1,end_page=max_pages,step_pages=step_pages,DEBUG=DEBUG)
    
    # 第2步：页数跨度第二大
    per_step=2
    df2=df1.copy(deep=True)
    failedpages2=[]
    
    if len(failedpages1) > 0:
        
        step_pages=step_page_list[per_step-1]
        
        for fp in failedpages1:
            start_page=fp[0]
            end_page=fp[1]
            
            dft,failedpagest=get_pef_product_china_pages(start_page=start_page,end_page=end_page,step_pages=step_pages,DEBUG=DEBUG)
            if len(dft) > 0:
                #df1=df1.append(dft)
                df2=pd.concat([df2,dft],ignore_index=True)
                
            if len(failedpagest) > 0:
                failedpages2=failedpages2+failedpagest
    
    # 第3步：页数跨度小
    per_step=3
    df3=df2.copy(deep=True)
    failedpages3=[]
    
    if len(failedpages2) > 0:
        
        step_pages=step_page_list[per_step-1]
        
        for fp in failedpages2:
            start_page=fp[0]
            end_page=fp[1]
            
            dft,failedpagest=get_pef_product_china_pages(start_page=start_page,end_page=end_page,step_pages=step_pages,DEBUG=DEBUG)
            if len(dft) > 0:
                #df1=df1.append(dft)
                df3=pd.concat([df3,dft],ignore_index=True)
                
            if len(failedpagest) > 0:
                failedpages3=failedpages3+failedpagest

    if DEBUG:
        print("  Finally retrieved pef info",len(df3),"records, with failed pages",failedpages3)
    
    return df3


#==============================================================================


def pef_product_china(DEBUG=False):
    
    """
    功能：中国私募基金管理人的产品管理概况
    爬虫来源地址：https://zhuanlan.zhihu.com/p/97487003
    """
    print("Searching for private equity fund (PEF) info in China, it may take hours ...")
    import akshare as ak
    import pandas as pd

    #私募基金管理人基金产品
    product_df = get_pef_product_china(max_pages=2200,step_page_list=[200,10,1],DEBUG=False)
    
    print(texttranslate("\n== 中国私募基金管理人的产品与运营概况 =="))
    print(texttranslate("产品数量："),end='')
    num=len(list(product_df["基金名称"]))
    print("{:,}".format(num))  
        
    #管理类型
    print(texttranslate("产品的运营方式分布："))
    #typelist=list(set(list(product_df['私募基金管理人类型'])))
    typelist=['受托管理','顾问管理','自我管理']
    for t in typelist:
            df_sub=product_df[product_df['私募基金管理人类型']==t]
            n=len(list(set(list(df_sub['基金名称']))))
            prefix=' '*4+t+':'
            print(prefix,"{:,}".format(n),"\b,",round(n/num*100,2),'\b%')     
        
    #运行状态
    print(texttranslate("产品的运营状态分布："))
    """
    typelist=list(set(list(product_df['运行状态'])))
    typelist=['状态不明' if i =='' else i for i in typelist]
    """
    typelist=['正在运作','提前清算','正常清算','延期清算','投顾协议已终止','']
    maxlen=0
    for t in typelist:
            tlen=strlen(t)
            if tlen > maxlen: maxlen=tlen
    maxlen=maxlen+1 
        
    for t in typelist:
            df_sub=product_df[product_df['运行状态']==t]
            n=len(list(set(list(df_sub['基金名称']))))
            if t =='': t='状态不明'
            tlen=strlen(t)
            prefix=' '*4+t+' '*(maxlen-tlen)+':'
            print(prefix,"{:,}".format(n),"\b,",round(n/num*100,2),'\b%')      

    import datetime; today = datetime.date.today()
    source=texttranslate("数据来源：中国证券投资基金业协会")
    footnote=source+', '+str(today)       
    print(footnote)
        
    #推出产品数量排行
    print(texttranslate("\n===== 中国推出产品数量最多的私募基金管理人 ====="))
    subttl=pd.DataFrame(product_df.groupby(by=['私募基金管理人名称'])['基金名称'].count())
    subttl.rename(columns={'基金名称':'产品数量'}, inplace=True)
    subttl['占比‰']=round(subttl['产品数量']/num*1000.0,2)
    subttl.sort_values(by=['产品数量'],ascending=False,inplace=True)
    subttl.reset_index(inplace=True)
    
    subttl.index=subttl.index + 1
    subttl10=subttl.head(10)
        
    #设置打印对齐
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    print(subttl10)
    
    pctsum=round(subttl10['占比‰'].sum(),2)    
    print(texttranslate("上述产品总计占比:"),pctsum,'\b‰')     
    print(footnote)
        
    print(texttranslate("\n===== 中国私募基金管理人的产品托管概况 ====="))
    #托管产品数量排行
    tnum=len(list(set(list(product_df['托管人名称']))))
    print(texttranslate("托管机构数量:"),"{:,}".format(tnum))
    
    subttl=pd.DataFrame(product_df.groupby(by=['托管人名称'])['基金名称'].count())
    subttl.rename(columns={'基金名称':'产品数量'}, inplace=True)
    subttl.sort_values(by=['产品数量'],ascending=False,inplace=True)
    subttl.reset_index(inplace=True)
        
    subttl=subttl[subttl['托管人名称']!='']
    #subttl.drop(subttl.index[0], inplace=True)       # 删除第1行
    subttl.reset_index(drop=True,inplace=True)
    subttl['占比%']=round(subttl['产品数量']/num*100.0,2)
    
    subttl.index=subttl.index + 1
    subttl10=subttl.head(10)
        
    pctsum=round(subttl10['占比%'].sum(),2)
    print(subttl10)
    print(texttranslate("上述金融机构托管产品总计占比:"),pctsum,'\b%')
    print(footnote)     
        
    return product_df   


#==============================================================================
#==============================================================================
if __name__=='__main__':
    fund_list=['510050.SS','510210.SS']
    start='2022-1-1'
    end='2022-10-31'
    ftype='单位净值'
    loc1='best'
    loc2='best'
    graph=True    

def compare_metf_china(fund_list,start,end,ftype='单位净值',graph=True):
    """
    功能：比较多只交易所基金的单位净值或累计净值，仅限中国内地
    """
    
    #检查日期期间的合理性
    result,startpd,endpd=check_period(start,end)
    if not result:
        print("  #Error(compare_metf): invalid date period",start,end)
        return None
    
    #检查净值类型
    typelist=['单位净值','累计净值']
    if not (ftype in typelist):
        print("  #Error(compare_metf): invalid fund value type",ftype)
        print("  Supported fund value type:",typelist)
        return None

    import os, sys
    class HiddenPrints:
        def __enter__(self):
            self._original_stdout = sys.stdout
            sys.stdout = open(os.devnull, 'w')

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.stdout.close()
            sys.stdout = self._original_stdout
    
    #循环获取基金净值
    import pandas as pd
    fdf=pd.DataFrame()
    print("Searching for ETF fund information, please wait ...")
    for f in fund_list:
        
        f6=f[:6]
        try:
            with HiddenPrints():
                dft=etf_trend_china(f6,start,end,graph=False)
        except:
            print("  #Error(compare_metf): ETF fund not found for",f)
            return None
        
        dft2=pd.DataFrame(dft[ftype])
        dft2.rename(columns={ftype:get_fund_name_china2(f)}, inplace=True)
        if len(fdf)==0:
            fdf=dft2
        else:
            fdf=pd.merge(fdf,dft2,how='outer',left_index=True,right_index=True)
            
    #绘图
    y_label=ftype
    import datetime; today = datetime.date.today()
    
    lang=check_language()
    if lang == 'English':
        x_label="Source: eastmoney/tiantian funds, "+str(today)
        title_txt="Compare Multiple ETF Fund Performance"
    else:
        x_label="数据来源: 东方财富/天天基金，"+str(today)
        title_txt="比较多只ETF基金的净值指标"

    draw_lines(fdf,y_label,x_label,axhline_value=0,axhline_label='',title_txt=title_txt, \
                   data_label=False,resample_freq='H',smooth=True)
        
    return fdf
    
if __name__=='__main__':
    fund_list=['510050.SS','510210.SS','510880.SS','510180.SS']
    fdf=compare_metf_china(fund_list,start,end,ftype='单位净值',graph=True)
    
#==============================================================================
#==============================================================================
#==============================================================================
#以下信息专注于中国内地基金信息，来源于akshare，尚未利用
#==============================================================================
def fund_info_china0():
    
    #证券公司集合资管产品
    cam_df = ak.amac_securities_info()
    
    #证券公司直投基金：
    #中国证券投资基金业协会-信息公示-私募基金管理人公示-基金产品公示-证券公司直投基金
    sdif_df = ak.amac_aoin_info()
    
    #证券公司私募投资基金
    speif_df = ak.amac_fund_sub_info()
    
    #证券公司私募基金子公司管理人信息
    spesub_manager_df = ak.amac_member_sub_info()
    
    #基金公司及子公司集合资管产品
    #中国证券投资基金业协会-信息公示-私募基金管理人公示-基金产品公示-基金公司及子公司集合资管产品
    sscam_df = ak.amac_fund_account_info()
    
    #期货公司集合资管产品
    #中国证券投资基金业协会-信息公示-私募基金管理人公示-基金产品公示-期货公司集合资管产品
    fccam_df = ak.amac_futures_info()
    
    #==========================================================================
    #以下为公募数据：
    
    #基金净值估算数据，当前获取在交易日的所有基金的净值估算数据
    #爬虫来源：https://zhuanlan.zhihu.com/p/140478554?from_voters_page=true
    #信息内容：基金代码，基金类型，单位净值，基金名称
    fnve_df = ak.fund_value_estimation_em()
    
    #挑选QDII产品
    fnve_list=list(set(list(fnve_df['基金类型'])))
    qdii=lambda x: True if 'QDII' in x else False
    fnve_df['is_QDII']=fnve_df['基金类型'].apply(qdii)
    fnve_qdii_df=fnve_df[fnve_df['is_QDII']==True]
    
    #基金持股：获取个股的基金持股数据
    #爬虫来源：https://my.oschina.net/akshare/blog/4428824
    #持股的基金类型：symbol="基金持仓"; choice of {"基金持仓", "QFII持仓", "社保持仓", "券商持仓", "保险持仓", "信托持仓"}
    #返回：单次返回指定 symbol 和 date 的所有历史数据
    df = ak.stock_report_fund_hold(symbol="基金持仓", date="20200630")
    
    ###Fama-French三因子回归A股实证（附源码）
    #代码来源：https://mp.weixin.qq.com/s?__biz=MzU5NDY0NDM2NA==&mid=2247486057&idx=1&sn=0fb3f8558da4e55789ce340c03b648cc&chksm=fe7f568ac908df9c22bae8b52207633984ec91ef7b2728eea8c6a75089b8f2db284e3d611775&scene=21#wechat_redirect

    ###Carhart四因子模型A股实证（附源码）
    #代码来源：https://my.oschina.net/akshare/blog/4340998
    
    #==========================================================================
    ###其他公募基金实时/历史行情
    #爬虫来源：https://cloud.tencent.com/developer/article/1624480
    
    ###########XXX理财型基金-实时数据
    #基金代码，基金简称，当前交易日-7日年化收益率，封闭期，申购状态
    wmf_df = ak.fund_financial_fund_daily_em()
    #理财型基金-历史数据
    #净值日期，7日年化收益率，申购状态，赎回状态
    wmf_hist_df = ak.fund_financial_fund_info_em(fund="000134")
    
    ###########分级基金(结构化基金)-实时数据
    #基金代码，基金简称，单位净值，累计净值，市价，折价率，手续费
    gsf_df = ak.fund_graded_fund_daily_em()
    #分级基金-历史数据
    #净值日期，7日年化收益率，申购状态，赎回状态
    gsf_hist_df = ak.fund_graded_fund_info_em(fund="150232")
    
    ###抓取沪深股市所有指数关联的公募基金列表（含ETF、增强、分级等）
    #代码来源：https://blog.csdn.net/leeleilei/article/details/106124894
    
    ###pyecharts绘制可伸缩蜡烛图
    #代码地址：https://segmentfault.com/a/1190000021999451?utm_source=sf-related
    
#==============================================================================
if __name__=='__main__':
    etflist=choose_etf_china(etf_type='股票型',startpos=0,endpos=10,printout=True)

def choose_etf_china(etf_type='股票型',startpos=0,endpos=10,printout=True):
    """
    功能：从数据库中挑选中国ETF基金
    输入：
    startpos=0,endpos=10：同型ETF列表的起始终止位置，同型ETF内部按照基金简称顺序排列
    输出：基金代码列表
    """    
    
    # 检查ETF类型
    etf_types=['股票型','债券型','商品型','货币型','QDII','全部']
    etf_type1=etf_type.upper()
    if not (etf_type1 in etf_types):
        print("  #Error(choose_etf_china): unsupported ETF type:",etf_type)
        print("  Supported ETF types:",etf_types)
        return None
    
    # 搜索处理ETF类型
    import akshare as ak
    names = ak.fund_name_em()

    names['ETF']=names['基金简称'].apply(lambda x: 1 if 'ETF' in x else 0)
    names_etf=names[names['ETF']==1]
    
    if etf_type != '全部':
        ftypea=['QDII','债券型-中短债','债券型-可转债','债券型-长债','商品（不含QDII）','指数型-股票','货币型']
        ftypes=['QDII','债券型','债券型','债券型','商品型','股票型','货币型']
        names_etf['基金分类']=names_etf['基金类型'].apply(lambda x:ftypes[ftypea.index(x)])
        names_etf2=names_etf[names_etf['基金分类']==etf_type]
    else:
        names_etf2=names_etf
        
    names_etf2.sort_values(by=['基金分类','基金代码'],ascending=[True,True],inplace=True)
    etfcols=['基金代码','基金简称','基金分类','基金类型']
    names_etf2=names_etf2[etfcols]
    
    names_etf3=names_etf2[startpos:endpos]
    if len(names_etf3)==0:
        print("  #Error(choose_etf_china): no records of ETF selected")
        print("  Parameter startpos",startpos,'should be smaller than endpos',endpos)
        return None
    
    names_etf4=names_etf3[etfcols]    
    names_etf4.reset_index(drop=True,inplace=True)
    names_etf4.index=names_etf4.index+1
    
    print("\n")
    alignlist=['right','center','left']+['center']*(len(list(names_etf4))-2)
    print(names_etf4.to_markdown(index=True,tablefmt='plain',colalign=alignlist))
    print("\n*** ETF基金("+etf_type+")总数:",len(names_etf2),"\b。",end='')
    
    import datetime; today = datetime.date.today().strftime("%Y-%m-%d")
    footnote=texttranslate("数据来源：新浪财经，")+today
    print(footnote)

    
    return list(names_etf4['基金代码']),names_etf2

#==============================================================================
#==============================================================================
if __name__=='__main__':
    fund='sh510170'
    fund='sh000311'
    
    info=fund_info_china('sh510170')
    info=fund_info_china('510170.SS')
    
    fund='510170.SS'

def fund_info_china(fund):
    """
    功能：查询中国基金代码和类型
    注意：实际仅需6位数字代码
    
    数据来源：东方财富，天天基金网
    """
    print("Searching for fund info, it may take a long time, please wait ...")
    
    # 代码中提取6位数字
    fund1=fund.upper()
    exchlist=['SH','SZ','.SS','.SZ']
    for exch in exchlist:
        fund1=fund1.replace(exch,'')
    
    import pandas as pd
    import akshare as ak
    
    # 检查基金是否存在
    try:
        names = ak.fund_name_em()
        namedf=names[names['基金代码']==fund1]
        
        if len(namedf) >= 1:
            df1=namedf[['基金代码','基金简称','基金类型']]
            fname=namedf['基金简称'].values[0]
            ftype=namedf['基金类型'].values[0]
        else:
            print("  #Warning(fund_info_china): info not found for fund",fund)
            return None
    except:
            print("  #Warning(fund_info_china): info source inaccessible for now, try later")
            return None
    
    # 基金评级
    df6=pd.DataFrame()
    titletxt6="***** 基金概况与评级"
    footnote6="注：评级机构为上海证券、招商证券和济安金信，数字表示星星个数，在同类基金中通常越高越好"
    try:
        dft6 = ak.fund_rating_all()
        dft6t=dft6[dft6['代码']==fund1]
        dft6t.fillna('---',inplace=True)
        fmanager=dft6t['基金经理'].values[0]
        
        if len(dft6t) >= 1:
            df6=dft6t
            printInMarkdown(df6,titletxt=titletxt6,footnote=footnote6)
    except:
        pass
    
    # 指数型基金信息
    df2=pd.DataFrame()
    titletxt2="***** 指数型基金的相关信息"
    footnote2="注：单位净值元，日/今年来/今年来的增长率及手续费为百分比"
    try:
        dft2 = ak.fund_info_index_em(symbol="全部", indicator="全部")
        dft2.sort_values('基金代码',inplace=True)
        dft2t=dft2[dft2['基金代码']==fund1]
        
        if len(dft2t) >= 1:
            df2=dft2t[['基金代码','单位净值','日期','日增长率','今年来','今年来','手续费']]
            printInMarkdown(df2,titletxt=titletxt2,footnote=footnote2)
    except:
        pass
    
    # 基金持仓：股票
    titletxt3="***** 基金持仓情况：股票"
    footnote3="注：占净值比例为百分比，持股数为万股，(持仓)市值为万元"
    df3=pd.DataFrame()
    import datetime; today = datetime.date.today()
    thisYear=str(today)[:4]
    try:
        dft3 = ak.fund_portfolio_hold_em(symbol=fund1,date=thisYear)
        dft3.sort_values(by=['季度','占净值比例'],ascending=[False,False],inplace=True)
        
        if len(dft3) >= 1:
            df3=dft3
            df3['持仓类型']='股票'
            printInMarkdown(df3,titletxt=titletxt3,footnote=footnote3)
    except:
        pass
    
    # 基金持仓：债券
    titletxt4="***** 基金持仓情况：债券"
    df4=pd.DataFrame()
    try:
        dft4 = ak.fund_portfolio_bond_hold_em(symbol=fund1,date=thisYear)
        dft4.sort_values(by=['季度','占净值比例'],ascending=[False,False],inplace=True)
        
        if len(dft4) >= 1:
            df4=dft4
            df4['持仓类型']='债券'
            printInMarkdown(df4,titletxt=titletxt4)
    except:
        print("\n #Warning(fund_info_china): unable to retrieve bond holding info for",fund,"@",thisYear)

    
    # 基金持仓：行业配置
    titletxt5="***** 基金的行业配置情况"
    footnote5="注：占净值比例为百分比，市值为万元"
    df5=pd.DataFrame()
    try:
        dft5 = ak.fund_portfolio_industry_allocation_em(symbol=fund1,date=thisYear)
        dft5.sort_values(by=['截止时间','占净值比例'],ascending=[False,False],inplace=True)
        
        if len(dft5) >= 1:
            df5=dft5
            df5['持仓类型']='行业配置'   
            printInMarkdown(df5,titletxt=titletxt5,footnote=footnote5)
    except:
        pass
    
    # 基金经理
    titletxt7="***** 基金经理的相关情况"
    source="数据来源：东方财富/天天基金"
    footnote7="注：从业时间为天数，现任基金资产总规模为该基金经理管辖所有基金的总规模(亿元)，最佳回报为历史业绩(百分比)\n"+source+"，"+str(today)
    
    df7=pd.DataFrame()
    try:
        dft7 = ak.fund_manager(adjust='0')
        dft7t=dft7[dft7['姓名']==fmanager]
        
        if len(dft7t) >= 1:
            current=dft7t['现任基金'].values[0]
            df7=dft7t[['姓名','所属公司','累计从业时间','现任基金资产总规模','现任基金最佳回报']]
            
            printInMarkdown(df7,titletxt=titletxt7)
            print(' ')
            print("基金经理当前兼任情况：")
            num=print_long_text(current)
            print(' ')
            print(footnote7)
    except:
        print("\n #Warning(fund_info_china): unable to retrieve job info for",fmanager)
    
    return 

#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================
#==============================================================================



























