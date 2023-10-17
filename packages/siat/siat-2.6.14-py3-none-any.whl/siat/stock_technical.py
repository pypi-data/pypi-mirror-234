# -*- coding: utf-8 -*-
"""
本模块功能：股票技术分析 technical analysis
所属工具包：证券投资分析工具SIAT 
SIAT：Security Investment Analysis Tool
创建日期：2023年1月27日
最新修订日期：2023年1月27日
作者：王德宏 (WANG Dehong, Peter)
作者单位：北京外国语大学国际商学院
作者邮件：wdehong2000@163.com
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
from siat.security_prices import *
from siat.stock import *
#==============================================================================
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize']=(12.8,7.2)
plt.rcParams['figure.dpi']=300
plt.rcParams['font.size'] = 13
plt.rcParams['xtick.labelsize']=11 #横轴字体大小
plt.rcParams['ytick.labelsize']=11 #纵轴字体大小

title_txt_size=16
ylabel_txt_size=14
xlabel_txt_size=14
legend_txt_size=14

import mplfinance as mpf

#处理绘图汉字乱码问题
import sys; czxt=sys.platform
if czxt in ['win32','win64']:
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    mpfrc={'font.family': 'SimHei'}

if czxt in ['darwin']: #MacOSX
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family': 'Heiti TC'}

if czxt in ['linux']: #website Jupyter
    plt.rcParams['font.family']= ['Heiti TC']
    mpfrc={'font.family':'Heiti TC'}

# 解决保存图像时'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 

#==============================================================================
#==============================================================================
#==============================================================================

if __name__ =="__main__":
    ticker='AAPL'
    start='2022-12-1'
    end='2023-1-26'
    ahead_days=30*2
    start1=date_adjust(start,adjust=-ahead_days)
    
    df=get_price(ticker,start1,end)
    
    RSI_days=14
    
    OBV_days=5
    
    MA_days=[5,20]
    
    MACD_fastperiod=12
    MACD_slowperiod=26
    MACD_signalperiod=9
    
    KDJ_fastk_period=5
    KDJ_slowk_period=3
    KDJ_slowk_matype=0
    KDJ_slowd_period=3
    KDJ_slowd_matype=0
    
    VOL_fastperiod=5
    VOL_slowperiod=10
    
    PSY_days=12
    
    ARBR_days=26
    
    CR_days=16
    CRMA_list=[5,10,20]
    
    EMV_days=14
    EMV_madays=9
    
    BULL_days=20
    BULL_nbdevup=2
    BULL_nbdevdn=2
    BULL_matype=0
    
    TRIX_days=12
    TRIX_madays=20
    
    DMA_fastperiod=10
    DMA_slowperiod=50
    DMA_madays=10
    
    BIAS_list=[6,12,24]
    
    CCI_days=14
    
    WR_list=[10,6]
    
    ROC_days=12
    ROC_madays=6
    
    DMI_DIdays=14
    DMI_ADXdays=6
    
def calc_technical(df,start,end, \
                   RSI_days=14, \
                   OBV_days=5, \
                   MA_days=[5,20], \
                   MACD_fastperiod=12,MACD_slowperiod=26,MACD_signalperiod=9, \
                   KDJ_fastk_period=9,KDJ_slowk_period=5,KDJ_slowk_matype=1, \
                   KDJ_slowd_period=5,KDJ_slowd_matype=1, \
                   VOL_fastperiod=5,VOL_slowperiod=10, \
                   PSY_days=12, \
                   ARBR_days=26, \
                   EMV_days=14,EMV_madays=9, \
                   BULL_days=20,BULL_nbdevup=2,BULL_nbdevdn=2,BULL_matype=0, \
                   TRIX_days=12,TRIX_madays=20, \
                   BIAS_list=[6,12,24], \
                   CCI_days=14, \
                   WR_list=[10,6], \
                   ROC_days=12,ROC_madays=6, \
                   DMI_DIdays=14,DMI_ADXdays=6):
    """
    功能：计算股票的技术分析指标
    输入：df，四种股价Open/Close/High/Low，成交量Volume
    输出：df
    支持的指标：
    RSI、OBV、MACD、 KDJ、 SAR、  VOL、 PSY、 ARBR、 CR、 EMV、 
    BOLL、 TRIX、 DMA、 BIAS、 CCI、 W%R、 ROC、 DMI
    """
    
    # 导入需要的包
    import talib    
    
    #=========== RSI，相对强弱指标Relative Strength Index
    """
    计算公式：RSI有两种计算方法：
        第一种方法：
        假设A为N日内收盘价涨幅的正数之和，B为N日内收盘价涨幅的负数之和再乘以（-1），
        这样，A和B均为正，将A，B代入RSI计算公式，则：
        RSI(N) = A ÷ （A + B） × 100
        第二种方法：
        RS(相对强度) = N日内收盘价涨数和之均值 ÷ N日内收盘价跌数和之均值
        RSI = 100 - 100 ÷ （1+RS）
        
    指标解读：
    80-100 极强 卖出
    50-80 强 观望，谨慎卖出
    20-50 弱 观望，谨慎买入
    0-20 极弱 买入        
    """
    df['rsi'] = talib.RSI(df['Close'], timeperiod=RSI_days)
    
    #=========== OBV：能量潮
    """
    OBV的英文全称是：On Balance Volume，是由美国的投资分析家Joe Granville所创。
    该指标通过统计成交量变动的趋势来推测股价趋势。
    OBV指标所谓股市人气，指投资者活跃在股市上的程度。
    如果买卖双方交易热情高，股价、成交量就上升，股市气氛则热烈。
    因此，利用股价和股票成交量的指标来反映人气的兴衰，就形成了OBV指标。
    
    OBV = 前一天的OBV ± 当日成交量
    说明：（当日收盘价高于前日收盘价，成交量定位为正值，取加号；
    当日收盘价低于前日收盘价，成交量定义为负值，取减号；二者相等计为0）
    
    指标解读：
    1、当股价上升而OBV线下降，表示买盘无力，股价可能会回跌。
    2、股价下降时而OBV线上升，表示买盘旺盛，逢低接手强股，股价可能会止跌回升。
    3、OBV线缓慢上升，表示买气逐渐加强，为买进信号。
    4、OBV线急速上升时，表示力量将用尽为卖出信号。
    5、OBV线从正的累积数转为负数时，为下跌趋势，应该卖出持有股票。反之，OBV线从负的累积数转为正数时，应该买进股票。
    6、OBV线最大的用处，在于观察股市盘局整理后，何时会脱离盘局以及突破后的未来走势，OBV线变动方向是重要参考指数，其具体的数值并无实际意义。    
    
    缺点
    葛兰碧的OBV指标是建立在国外成熟市场上的经验总结。
    用在内地股市坐庄的股票上就不灵了，这时股价涨得越高成交量反而越少。
    这是因为主力控盘较重，股价在上涨过程中没有获利筹码加以兑现，所以此时股票会涨得很“疯”，但成交量并不增加，OBV自然就无法发挥作用。
    另外，涨跌停板的股票也会导致指标失真。
    由于内地股市采用了涨跌停板的限制，很多股票在连续涨停的时候，由于股民预期后市会继续大涨，往往会持股观望，导致出现越涨越无量的现象。
    因此，对于那些达到涨跌停板的股票，OBV指标也无法正常发挥作用。    
    
    """
    df['obv'] = talib.OBV(df['Close'],df['Volume'])
    df['obv_ma'] = talib.MA(df['obv'],timeperiod=OBV_days)
    
    #=========== MA: 简单、加权移动平均
    """
    MA，又称移动平均线，是借助统计处理方式将若干天的股票价格加以平均，然后连接成一条线，用以观察股价趋势。
    移动平均线通常有3日、6日、10日、12日、24日、30日、72日、200日、288日、13周、26周、52周等等，不一而足，
    其目的在取得某一段期间的平均成本，而以此平均成本的移动曲线配合每日收盘价的线路变化分析某一期间多空的优劣形势，
    以研判股价的可能变化。
    一般来说，现行价格在平均价之上，意味着市场买力（需求）较大，行情看好；
    反之，行情价在平均价之下，则意味着供过于求，卖压显然较重，行情看淡。    
    """
    for mad in MA_days:
        df['ma'+str(mad)] = talib.MA(df['Close'],timeperiod=mad)
        df['ema'+str(mad)] = talib.EMA(df['Close'],timeperiod=mad)
    
    #=========== MACD：指数平滑异同平均线
    """
    计算方法：快速时间窗口设为12日，慢速时间窗口设为26日，DIF参数设为9日
        3.1) 计算指数平滑移动平均值（EMA）
        12日EMA的计算公式为：
        EMA(12) = 昨日EMA(12)  ×  11 ÷ 13 + 今日收盘价 × 2 ÷ 13
        26日EMA的计算公式为：
        EMA(26) = 昨日EMA(26) × 25 ÷ 27 + 今日收盘价 × 2 ÷ 27
        
        3.2) 计算离差值（DIF）
        DIF = 今日EMA(12) – 今日EMA(26)
        
        3.3) 计算DIF的9日DEA
        根据差值计算其9日的DEA，即差值平均
        今日DEA = 昨日DEA × 8 ÷ 10 + 今日DIF × 2 ÷ 10    
    
    形态解读：
        1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。
        2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
        3.DEA线与K线发生背离，行情反转信号。
        4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号。
        
    MACD一则去掉移动平均线频繁的假讯号缺陷，二则能确保移动平均线最大的战果。
        1. MACD金叉：DIF由下向上突破DEM，为买入信号。
        2. MACD死叉：DIF由上向下突破DEM，为卖出信号。
        3. MACD绿转红：MACD值由负变正，市场由空头转为多头。
        4. MACD红转绿：MACD值由正变负，市场由多头转为空头。        
    """
    df['DIFF'],df['DEA'],df['MACD']=talib.MACD(df['Close'], \
                                fastperiod=MACD_fastperiod, \
                                slowperiod=MACD_slowperiod, \
                                signalperiod=MACD_signalperiod)

    #=========== KDJ: 随机指标
    """
    计算公式：
        1) 以日KDJ数值的计算为例
        N日RSV = (CN – LN)÷(HN-LN) ×100
        说明：CN为第N日收盘价；LN为N日内的最低价；HN为N日内的最高价，RSV值始终在1~100间波动
        2) 计算K值与D值
        当日K值 = 2/3 × 前一日K值 + 1/3 × 当日RSV
        当日D值 = 2/3 × 前一日D值 + 1/3 × 当日K值
        如果没有前一日K值与D值，则可分别用50来代替
        3) 计算J值
        J = 3D – 2K    
    
    指标解读：
    
    """
    df['kdj_k'],df['kdj_d'] = talib.STOCH(df['High'],df['Low'],df['Close'], \
                        fastk_period=KDJ_fastk_period,
                        slowk_period=KDJ_slowk_period, 
                        slowk_matype=KDJ_slowk_matype, 
                        slowd_period=KDJ_slowd_period, 
                        slowd_matype=KDJ_slowd_matype)
    df['kdj_j'] = 3*df['kdj_k'] - 2*df['kdj_d']

    #=========== SAR: 抛物转向
    """
    计算过程：
        1）先选定一段时间判断为上涨或下跌
        2）如果是看涨，则第一天的SAR值必须是近期内的最低价；
        如果是看跌，则第一天的SAR值必须是近期的最高价。
        3）第二天的SAR值，则为第一天的最高价（看涨时）或是最低价（看跌时）与第一天的SAR值的差距乘上加速因子，
        再加上第一天的SAR值就可以求得。
        4）每日的SAR值都可用上述方法类推，公式归纳如下：
        SAR(N) = SAR(N-1) + AF × [(EP(N-1) – SAR(N-1))]
        SAR(N) = 第N日的SAR值
        SAR(N-1) = 第(N-1)日的SAR值
        说明：AF表示加速因子；EP表示极点价，如果是看涨一段期间，则EP为这段时间的最高价，
        如果是看跌一段期间，则EP为这段时间的最低价；EP(N-1)等于第(N-1)日的极点价
        5）加速因子第一次取0.02，假若第一天的最高价比前一天的最高价还高，则加速因子增加0.02，
        如无新高则加速因子沿用前一天的数值，但加速因子最高不能超过0.2。反之，下跌也类推
        6）如果是看涨期间，计算出某日的SAR值比当日或前一日的最低价高，则应以当日或前一日的最低价为某日之SAR值；
        如果是看跌期间，计算某日的SAR值比当日或前一日的最高价低，则应以当日或前一日的最高价为某日的SAR值。
        7）SAR指标基准周期的参数为2，如2日、2周、2月等，其计算周期的参数变动范围为2~8
        8）SAR指标在股价分析系统的主图上显示为“O”形点状图。    
    """
    df['sar'] = talib.SAR(df['High'],df['Low'])

    #=========== VOL: 成交量
    """
    柱状图是成交量，两条曲线是成交量的移动平均    
    """
    df['vol'+str(VOL_fastperiod)] = talib.MA(df['Volume'],timeperiod=VOL_fastperiod)
    df['vol'+str(VOL_slowperiod)] = talib.MA(df['Volume'],timeperiod=VOL_slowperiod)
    
    #=========== PSY: 心理线
    """
    计算公式：
    PSY(N) = A/N × 100
    说明：N为天数，A为在这N天之中股价上涨的天数    
    """
    df['ext_0'] = df['Close']-df['Close'].shift(1)
    df['ext_1'] = 0
    df.loc[df['ext_0']>0,'ext_1'] = 1
    df['ext_2'] = df['ext_1'].rolling(window=PSY_days).sum()
    df['psy'] = (df['ext_2']/float(PSY_days))*100
    
    df.drop(columns = ['ext_0','ext_1','ext_2'],inplace=True) 
    
    #=========== ARBR: 人气和意愿指标, AR为人气指标，BR为买卖意愿指标
    """
    计算公式：
    AR(N) = N日内（H-O）之和 ÷ N日内（O-L）之和 × 100
    说明：H表示当天最高价；L表示当天最低价；O表示当天开盘价；N表示设定的时间参数，一般原始参数日缺省值为26日
    BR(N) = N日内（H-CY）之和 ÷ N日内（CY-L）之和 × 100
    说明：H表示当天最高价；L表示当天最低价；CY表示前一交易日的收盘价，N表示设定的时间参数，一般原始参数缺省值为26日    
    """
    df['h_o'] = df['High'] - df['Open']
    df['o_l'] = df['Open'] - df['Low']
    df['h_o_sum'] = df['h_o'].rolling(window=ARBR_days).sum()
    df['o_l_sum'] = df['o_l'].rolling(window=ARBR_days).sum()
    df['ar'] = (df['h_o_sum']/df['o_l_sum'])*100
    df['h_c'] = df['High'] - df['Close']
    df['c_l'] = df['Close'] - df['Low']
    df['h_c_sum'] = df['h_c'].rolling(window=ARBR_days).sum()
    df['c_l_sum'] = df['c_l'].rolling(window=ARBR_days).sum()
    df['br'] = (df['h_c_sum']/df['c_l_sum'])*100

    df.drop(columns = ['h_o','o_l','h_o_sum','o_l_sum','h_c','c_l','h_c_sum','c_l_sum'],inplace=True) 

    #=========== CR: 带状能力线或中间意愿指标
    """
    计算过程：
    1）计算中间价，取以下四种中一种，任选：
    中间价 = （最高价 + 最低价）÷2
    中间价 = （最高价 + 最低价 + 收盘价）÷3
    中间价 = （最高价 + 最低价 + 开盘价 + 收盘价）÷4
    中间价 = （2倍的开盘价 + 最高价 + 最低价）÷4
    2）计算CR:
    CR = N日内（当日最高价 – 上个交易日的中间价）之和 ÷ N日内（上个交易日的中间价 – 当日最低价）之和
    说明：N为设定的时间周期参数，一般原始参数日设定为26日
    3）计算CR值在不同时间周期内的移动平均值：这三条移动平均曲线分别为MA1 MA2 MA3,时间周期分别为5日 10日 20日    
    """
    df['m_price'] = (df['High'] + df['Low'])/2
    df['h_m'] = df['High']-df['m_price'].shift(1)
    df['m_l'] = df['m_price'].shift(1)-df['Low']
    df['h_m_sum'] = df['h_m'].rolling(window=CR_days).sum()
    df['m_l_sum'] = df['m_l'].rolling(window=CR_days).sum()
    df['cr'] = (df['h_m_sum']/df['m_l_sum'])*100
    
    for crmad in CRMA_list:
        df['crma'+str(crmad)] = talib.MA(df['cr'],timeperiod=crmad)
    
    df.drop(columns = ['m_price','h_m','m_l','h_m_sum','m_l_sum'],inplace=True) 
    
    #=========== EMV: 简易波动指标
    """
    计算方法：
    1）先计算出三个因子A B C的数值。
    A = (当日最高价 + 当日最低价)÷2
    B = (上个交易日最高价 + 上个交易日最低价) ÷2
    C = 当日最高价 – 当日最低价
    2）求出EM数值
    EM = (A-B) ×C÷当日成交额
    3）求出EMV数值
    EMV = EM数值的N个交易日之和，N为时间周期，一般设为14日
    4）求出EMV的移动平均值EMVA
    EMVA = EMV的M日移动平均值，M一般设置9日    
    """
    df['a'] = (df['High']+df['Low'])/2
    df['b'] = (df['High'].shift(1)+df['Low'].shift(1))/2
    df['c'] = df['High'] - df['Low']
    
    df['Amount']=df['Close']*df['Volume']
    df['em'] = (df['a']-df['b'])*df['c']/df['Amount']
    df['emv'] = df['em'].rolling(window=EMV_days).sum()
    df['emva'] = talib.MA(df['emv'],timeperiod=EMV_madays)

    df.drop(columns = ['a','b','c'],inplace=True) 
    
    #=========== BOLL: 布林线指标
    """
    计算公式：
        中轨线 = N日的移动平均线
        上轨线 = 中轨线 + 两倍的标准差
        下轨线 = 中轨线 – 两倍的标准差
    计算过程：
        1）先计算出移动平均值MA
        MA = N日内的收盘价之和÷N
        2）计算出标准差MD的平方
        MD的平方 = 每个交易日的（收盘价-MA）的N日累加之和的两次方 ÷ N
        3）求出MD
        MD = （MD的平方）的平方根
        4）计算MID、UPPER、LOWER的数值
        MID = (N-1)日的MA
        UPPER = MID + 2×MD
        LOWER = MID – 2×MD
        说明：N一般原始参数日缺省值为20日    
    
    指标解读：
        BOLL指标即布林线指标，其利用统计原理，求出股价的标准差及其信赖区间，
        从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低价位，因而也被称为布林带。
        其上下限范围不固定，随股价的滚动而变化。布林指标股价波动在上限和下限的区间之内，
        这条带状区的宽窄，随着股价波动幅度的大小而变化，股价涨跌幅度加大时，带状区变宽，
        涨跌幅度狭小盘整时，带状区则变窄。    
    """
    df['upper'],df['mid'],df['lower'] = talib.BBANDS(df['Close'], \
                timeperiod=BULL_days, \
                nbdevup=BULL_nbdevup,nbdevdn=BULL_nbdevdn,matype=BULL_matype)                     
    
    #=========== TRIX：三重指数平滑移动平均指标
    """
    
    """
    df['trix'] = talib.TRIX(df['Close'],timeperiod=TRIX_days)
    df['trma'] = talib.MA(df['trix'],timeperiod=TRIX_madays)    

    #=========== DMA: 平均线差
    """
    计算公式：
    DDD(N) = N日短期平均值 – M日长期平均值
    AMA(N) = DDD的N日短期平均值
    计算过程：
    以求10日、50日为基准周期的DMA指标为例
    1）求出周期不等的两条移动平均线MA之间的差值
    DDD(10) = MA10 – MA50
    2）求DDD的10日移动平均数值
    DMA(10) = DDD(10)÷10
    """   
    df['ma_shortperiod'] = talib.MA(df['Close'],timeperiod=DMA_fastperiod)
    df['ma_longperiod'] = talib.MA(df['Close'],timeperiod=DMA_slowperiod)
    df['ddd'] = df['ma_shortperiod'] - df['ma_longperiod']
    df['dma'] = talib.MA(df['ddd'],timeperiod=DMA_madays)    
    
    df.drop(columns = ['ma_shortperiod','ma_longperiod','ddd'],inplace=True) 
    
    #=========== BIAS: 乖离率
    """
    N日BIAS = （当日收盘价 – N日移动平均价）÷N日移动平均价×100
    
    指标解读：
    6日BIAS＞＋5％，是卖出时机；＜-5％，为买入时机。
    12日BIAS＞＋6％是卖出时机；＜-5.5％,为买入时机。
    24日BIAS＞＋9％是卖出时机；＜－8％，为买入时机。
    """
    df['ma6'] = talib.MA(df['Close'],timeperiod=BIAS_list[0])
    df['ma12'] = talib.MA(df['Close'],timeperiod=BIAS_list[1])
    df['ma24'] = talib.MA(df['Close'],timeperiod=BIAS_list[2])
    df['bias'] = ((df['Close']-df['ma6'])/df['ma6'])*100
    df['bias2'] = ((df['Close']-df['ma12'])/df['ma12'])*100
    df['bias3'] = ((df['Close']-df['ma24'])/df['ma24'])*100    
    
    df.drop(columns = ['ma6','ma12','ma24'],inplace=True) 

    #=========== CCI: 顺势指标
    """
    计算过程：
    CCI(N日) = （TP-MA）÷MD÷0.015
    说明：TP = （最高价+最低价+收盘价）÷3；MA=最近N日收盘价的累计之和÷N；MD=最近N日（MA-收盘价）的累计之和÷N；0.015为计算系数；N为计算周期，默认为14天
    """    
    df['cci'] = talib.CCI(df['High'],df['Low'],df['Close'],timeperiod=CCI_days)

    #=========== W%R: 威廉指标   
    """
    N日W%R = [(Hn-Ct)/(Hn-Ln)]*100
    Ct是计算日的收盘价；Hn/Ln为包括计算日当天的N周期内的最高（低）价  
    
    指标解读：
        威廉指标(William's %R) 原理：用当日收盘价在最近一段时间股价分布的相对位置来描述超买和超卖程度。
        算法：N日内最高价与当日收盘价的差，除以N日内最高价与最低价的差，结果放大100倍。
        参数：N 统计天数 一般取14天
        用法：
        1.低于20，超买，即将见顶，应及时卖出 
        2.高于80，超卖，即将见底，应伺机买进 
        3.与RSI、MTM指标配合使用，效果更好    
    """
    n = WR_list[0]
    df['h_10'] = df['High'].rolling(window=n).max()
    df['l_10'] = df['Low'].rolling(window=n).min()
    df['wr10'] = ((df['h_10']-df['Close'])/(df['h_10']-df['l_10']))*100
    
    n2 = WR_list[1]
    df['h_6'] = df['High'].rolling(window=n2).max()
    df['l_6'] = df['Low'].rolling(window=n2).min()
    df['wr6'] = ((df['h_6'] - df['Close']) / (df['h_6'] - df['l_6'])) * 100

    df.drop(columns = ['h_10','l_10','h_6','l_6'],inplace=True) 
    
    #=========== ROC: 变动速率指标
    """
    计算过程：
    1）计算出ROC数值
    ROC = (当日收盘价 – N日前收盘价)÷N日前收盘价×100
    说明：N一般取值为12日
    2）计算ROC移动平均线（ROCMA）数值
    ROCMA = ROC的M日数值之和÷M
    说明：M一般取值为6日    
    """
    df['roc'] = talib.ROC(df['Close'],timeperiod=ROC_days)
    df['rocma'] = talib.MA(df['roc'],timeperiod=ROC_madays)    
    
    #=========== DMI: 趋向指标
    """

    """     
    df['pdi'] = talib.PLUS_DI(df['High'],df['Low'],df['Close'],timeperiod=DMI_DIdays)
    df['mdi'] = talib.MINUS_DI(df['High'],df['Low'],df['Close'],timeperiod=DMI_DIdays)
    df['adx'] = talib.ADX(df['High'],df['Low'],df['Close'],timeperiod=DMI_ADXdays)
    df['adxr'] = talib.ADXR(df['High'],df['Low'],df['Close'],timeperiod=DMI_ADXdays)    
    
    
    return df


#==============================================================================
#==============================================================================
#==============================================================================

if __name__ =="__main__":
    ticker='600519.SS'
    start='2022-6-1'
    end='2022-6-30'
    
    MA_days=[5,20]
    EMA_days=[5,20]
    
    MACD_fastperiod=12
    MACD_slowperiod=26
    MACD_signalperiod=9
    
    loc1='upper left'
    loc2='center right'
    
    resample_freq='H'
    smooth=True
    linewidth=1.5
    graph=['MA']
    graph=['EMA']
    graph=['MACD']
    printout=True

def security_MACD(ticker,start='default',end='default', \
             MA_days=[5,20],EMA_days=[5,20], \
             MACD_fastperiod=12,MACD_slowperiod=26,MACD_signalperiod=9, \
             resample_freq='6H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    套壳函数：可用于股票、交易所债券、交易所基金、部分期货期权(限美股)
    """
    df=stock_MACD(ticker=ticker,start=start,end=end, \
                 MA_days=MA_days,EMA_days=EMA_days, \
                 MACD_fastperiod=MACD_fastperiod,MACD_slowperiod=MACD_slowperiod, \
                 MACD_signalperiod=MACD_signalperiod, \
                 resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
                 loc1=loc1,loc2=loc2, \
                 graph=graph,printout=printout)
    return df
    
    
def stock_MACD(ticker,start='default',end='default', \
             MA_days=[5,20],EMA_days=[5,20], \
             MACD_fastperiod=12,MACD_slowperiod=26,MACD_signalperiod=9, \
             resample_freq='H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    功能：计算股票的技术分析指标MACD
    输入：df，四种股价Open/Close/High/Low，成交量Volume
    输出：df
    含有指标：
    MA5、MA20、MACD_fastperiod、 MACD_slowperiod、MACD_signalperiod
    """
    
    #=========== 导入需要的包
    try:
        import talib  
    except:
        print("  #Error(stock_MACD): lack of necessary module - ta-lib")
        talib_install_method()        
        return None
    
    #=========== 日期转换与检查
    # 检查日期：截至日期
    import datetime as dt; today=dt.date.today()
    if end in ['default','today']:
        end=today
    else:
        validdate,end=check_date2(end)
        if not validdate:
            print("  #Warning(stock_MACD): invalid date for",end)
            end=today

    # 检查日期：开始日期
    if start in ['default']:
        start=date_adjust(end,adjust=-31)
    else:
        validdate,start=check_date2(start)
        if not validdate:
            print("  #Warning(stock_MACD): invalid date for",start)
            start=date_adjust(todate,adjust=-31)
    
    #=========== 获取股价和成交量数据
    result,startpd,endpd=check_period(start,end)
    
    days_list=MA_days+EMA_days+[MACD_fastperiod]+[MACD_slowperiod]+[MACD_signalperiod]
    max_days=max(days_list)
    start1=date_adjust(start,adjust=-max_days * 3)
    
    df=get_price(ticker,start1,end)
    if df is None:
        print("  #Error(stock_MACD): no info found for",ticker,"from",start,"to",end)
        return None
    if len(df)==0:
        print("  #Error(stock_MACD): zero record found for",ticker,"from",start,"to",end)
        return None   
    
    #=========== MA: 简单、加权移动平均
    """
    MA，又称移动平均线，是借助统计处理方式将若干天的股票价格加以平均，然后连接成一条线，用以观察股价趋势。
    移动平均线通常有3日、6日、10日、12日、24日、30日、72日、200日、288日、13周、26周、52周等等，不一而足，
    其目的在取得某一段期间的平均成本，而以此平均成本的移动曲线配合每日收盘价的线路变化分析某一期间多空的优劣形势，
    以研判股价的可能变化。
    一般来说，现行价格在平均价之上，意味着市场买力（需求）较大，行情看好；
    反之，行情价在平均价之下，则意味着供过于求，卖压显然较重，行情看淡。    
    """
    #if ('MA' in graph) or ('ALL' in graph):
    if (graph in ['MA',['MA']]) or ('ALL' in graph):    
        MA_cols=[]
        for mad in MA_days:
            col='MA'+str(mad)+'简单移动均线'
            MA_cols=MA_cols+[col]
            df[col] = talib.MA(df['Close'],timeperiod=mad)
        
        # MA快慢线交叉
        dft=df.copy()
        dft['datepd']=dft.index
        dft['日期']=dft['datepd'].apply(lambda x: x.strftime("%Y-%m-%d"))
        
        dft['short-long']=dft[MA_cols[0]]-dft[MA_cols[1]]
        dft['sign']=dft['short-long'].apply(lambda x: 1 if x>0 else -1)
        dft['sign_cross']=dft['sign']-dft['sign'].shift(1)
        dft['交叉类型']=dft['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
        dft2=dft[dft['sign_cross'] != 0]
        dft3=dft2[(dft2.index >= startpd) & (dft2.index <= endpd)] 
        dft3.dropna(inplace=True)
            
        # 限定日期范围
        df1=df[(df.index >= startpd) & (df.index <= endpd)]    
    
        y_label="股价"
        import datetime as dt; today=dt.date.today()    
        source="数据来源：sina/yahoo/stooq/fred，"+str(today)
        footnote="MA参数："+str(MA_days)
        x_label=footnote+'\n'+source
        
        axhline_value=0
        axhline_label=''
    
        # 简单移动均线MA绘图：moving average
        df2=df1[['Close']+MA_cols]
        df2.rename(columns={'Close':'收盘价'},inplace=True)
        
        title_txt="股票价格走势分析："+codetranslate(ticker)+"，简单移动均线"
        
        print("  Rendering graphics ...")
        draw_lines(df2,y_label,x_label,axhline_value,axhline_label,title_txt, \
                   data_label=False,resample_freq=resample_freq,smooth=smooth,linewidth=linewidth*2)        
    
        if printout:
            if len(dft3)!=0:            
                print("\n== 简单移动均线交叉 ==")
                alignlist=['left','center']
                print(dft3[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
            else:
                print("  Note: no cross of lines incurred for",ticker,"from",start,"to",end)

    # 指数移动均线EMA绘图：exponential moving average
    """
    MA是用每天的收盘价来计算简单的平均值，
    而EMA是需要给每天的最高最低等价位数值做一个权重处理后，再平均计算，
    所以，EMA更具有平均价值一些。
    EMA最大特点也是由于它的计算方式导致的，因为后期的k线价格在计算均价时，比重更大，
    所以相同参数EMA比MA更加贴近行情，更加平滑，产生的变盘信号、交易信号也更加激进？
    EMA的变盘信号：熊市转牛市，比MA迟钝？牛市转熊市，比MA敏感？    
    """
    if ('EMA' in graph) or ('ALL' in graph):
        EMA_cols=[]
        for mad in EMA_days:
            col='EMA'+str(mad)+'指数加权均线'
            EMA_cols=EMA_cols+[col]
            df[col] = talib.EMA(df['Close'],timeperiod=mad)
        
        # EMA快慢线交叉
        dft=df.copy()
        dft['datepd']=dft.index
        dft['日期']=dft['datepd'].apply(lambda x: x.strftime("%Y-%m-%d"))
        
        dft['short-long']=dft[EMA_cols[0]]-dft[EMA_cols[1]]
        dft['sign']=dft['short-long'].apply(lambda x: 1 if x>0 else -1)
        dft['sign_cross']=dft['sign']-dft['sign'].shift(1)
        dft['交叉类型']=dft['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
        dft2=dft[dft['sign_cross'] != 0]
        dft3=dft2[(dft2.index >= startpd) & (dft2.index <= endpd)] 
        dft3.dropna(inplace=True)
            
        # 限定日期范围
        df1=df[(df.index >= startpd) & (df.index <= endpd)]    
    
        y_label="股价"
        import datetime as dt; today=dt.date.today()    
        source="数据来源：sina/yahoo/stooq/fred，"+str(today)
        footnote="EMA参数："+str(EMA_days)
        x_label=footnote+'\n'+source
        
        axhline_value=0
        axhline_label=''
        
        df3=df1[['Close']+EMA_cols]
        df3.rename(columns={'Close':'收盘价'},inplace=True)
        title_txt="股票价格走势分析："+codetranslate(ticker)+"，指数加权均线"
        draw_lines(df3,y_label,x_label,axhline_value,axhline_label,title_txt, \
                   data_label=False,resample_freq=resample_freq,smooth=smooth,linewidth=linewidth*2)        

        if printout:
            if len(dft3)!=0:            
                print("\n== 指数加权均线交叉 ==")
                alignlist=['left','center']
                print(dft3[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
            else:
                print("  Note: no cross of lines incurred for",ticker,"from",start,"to",end)
        
    #=========== MACD：指数平滑异同平均线
    """
    计算方法：快速时间窗口设为12日，慢速时间窗口设为26日，DIF参数设为9日
        3.1) 计算指数平滑移动平均值（EMA）
        12日EMA的计算公式为：
        EMA(12) = 昨日EMA(12)  ×  11 ÷ 13 + 今日收盘价 × 2 ÷ 13
        26日EMA的计算公式为：
        EMA(26) = 昨日EMA(26) × 25 ÷ 27 + 今日收盘价 × 2 ÷ 27
        
        3.2) 计算离差值（DIF）
        DIF = 今日EMA(12) – 今日EMA(26)
        
        3.3) 计算DIF的9日DEA
        根据差值计算其9日的DEA，即差值平均
        今日DEA = 昨日DEA × 8 ÷ 10 + 今日DIF × 2 ÷ 10    
    
    形态解读：
        1.DIF、DEA均为正，DIF向上突破DEA，买入信号。
        2.DIF、DEA均为负，DIF向下跌破DEA，卖出信号。
        3.DEA线与K线发生背离，行情反转信号。
        4.分析MACD柱状线，由红变绿(正变负)，卖出信号；由绿变红，买入信号。
        
    MACD一则去掉移动平均线频繁的假讯号缺陷，二则能确保移动平均线最大的战果。
        1. MACD金叉：DIF由下向上突破DEM，为买入信号。
        2. MACD死叉：DIF由上向下突破DEM，为卖出信号。
        3. MACD绿转红：MACD值由负变正，市场由空头转为多头。
        4. MACD红转绿：MACD值由正变负，市场由多头转为空头。        
    """
    if ('MACD' in graph) or ('ALL' in graph):
        df['DIF'],df['DEA'],df['MACD']=talib.MACD(df['Close'], \
                                    fastperiod=MACD_fastperiod, \
                                    slowperiod=MACD_slowperiod, \
                                    signalperiod=MACD_signalperiod)
        
        # DIF/DEA快慢线交叉
        dft=df.copy()
        dft['datepd']=dft.index
        dft['日期']=dft['datepd'].apply(lambda x: x.strftime("%Y-%m-%d"))
        
        dft['short-long']=dft['DIF']-dft['DEA']
        dft['sign']=dft['short-long'].apply(lambda x: 1 if x>0 else -1)
        dft['sign_cross']=dft['sign']-dft['sign'].shift(1)
        dft['交叉类型']=dft['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
        dft2=dft[dft['sign_cross'] != 0]
        dft3=dft2[(dft2.index >= startpd) & (dft2.index <= endpd)] 
        dft3.dropna(inplace=True)
            
        # 限定日期范围
        df1=df[(df.index >= startpd) & (df.index <= endpd)]    
        
        # MACD绘图
        df4=df1[['Close','DIF','DEA','MACD']]
        df4.rename(columns={'Close':'收盘价','DIF':'快线DIF','DEA':'慢线DEA','MACD':'柱线MACD'},inplace=True)
        title_txt="股票价格走势分析："+codetranslate(ticker)+"，MACD"
        
        import datetime as dt; today=dt.date.today()    
        source="数据来源：sina/yahoo/stooq/fred，"+str(today)
        
        # 设置绘图区的背景颜色为黑色
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.patch.set_facecolor('black')
        
        # 绘制曲线
        ax.plot(df4['快线DIF'],label='快线DIF',linewidth=linewidth*2,color='white')
        ax.plot(df4['慢线DEA'],label='慢线DEA',linewidth=linewidth*2,color='orange')
        
        # 绘制红绿柱子
        """
        MACD指标由三部分组成，分别是：DIF (差离值)、 DEA (差离值平均数)和BAR(柱状线)，
        DIF在图中用白线表示，称为“快线”，DEA在图中用黄线表示，称为“慢线”，
        最早的MACD只有这两条快慢线，通过两条曲线的聚合和分离来判断市场状况。
        后来随着MACD的广泛运用，又引入了柱状线(BAR)，俗称“红绿柱”。
        红绿柱表示的是快线与慢线之间的距离，对指标实质没有影响，只是为了更便于观察和使用指标。    
        """
        macd_plus=df4[df4['柱线MACD']>=0]
        macd_minus=df4[df4['柱线MACD']<=0]
        ax.bar(macd_plus.index,macd_plus['柱线MACD'],color='red')
        ax.bar(macd_minus.index,macd_minus['柱线MACD'],color='green',label='柱线MACD')
        
        # 绘制水平辅助线
        #plt.axhline(y=0,label='指标零线',color='cyan',linestyle=':',linewidth=linewidth*2) 
        plt.axhline(y=0,label='',color='cyan',linestyle=':',linewidth=linewidth*2) 
        
        # 设置左侧坐标轴
        ax.set_ylabel('DIF/DEA/MACD指标',fontsize=ylabel_txt_size)
        
        footnote="MACD参数："+str([MACD_fastperiod,MACD_slowperiod,MACD_signalperiod])
        x_label=footnote+'\n'+source
        ax.set_xlabel(x_label,fontsize=xlabel_txt_size)
        ax.legend(loc=loc1,fontsize=legend_txt_size)
        
        # 绘制股价在右侧
        #绘证券2：建立第二y轴
        
        #插值平滑
        if smooth:
            try:
                df5=df_smooth_manual(df4,resample_freq=resample_freq)
            except:
                df5=df4
        else:
            df5=df4
        
        ax2 = ax.twinx()
        ax2.plot(df5['收盘价'],label='收盘价',linewidth=linewidth,color='gray',ls='--')
        
        # 右侧坐标轴标记
        ax2.set_ylabel('收盘价',fontsize=ylabel_txt_size)
        ax2.legend(loc=loc2,fontsize=legend_txt_size)
        
        # 图示标题
        plt.title(title_txt,fontweight='bold',fontsize=title_txt_size)
        #plt.xticks(rotation=30)
        plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
        #plt.legend(loc='best',fontsize=legend_txt_size)
        plt.show()

        if printout:
            if len(dft3)!=0:
                print("\n== DIF与DEA交叉 ==")
                alignlist=['left','center']
                print(dft3[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
            else:
                print("  Note: no cross of lines incurred for",ticker,"from",start,"to",end)
    
    return df1

#==============================================================================
#==============================================================================
#==============================================================================

def talib_install_method():
    """
    功能：提示必需的talib安装方法
    """
    print("  Installation method 1: pip install TA_Lib")
    print("    Note: method 1 is subject to fail")
    print("  Installation method 2: conda install -c quantopian ta-lib")
    print("    Note: method 2 may need scientific internet access")
    print("  Installation method 3: ")
    print("    Step1. Goto website https://www.lfd.uci.edu/~gohlke/pythonlibs/")
    print("    Step2. On the web page, search for TA_lib")
    print("    Step3. Select the file suitable for the Python version and OS 32/64")
    print("    Step4. Download the file")
    print("    Step5. pip install <downloaded file name>")
    print("    Note: method 3 is troublesome, but more likely successful")
    
    print("  How to check the Python version in your computer? ")
    print("    python --version")
    print("  How to check the win32/win_amd64 in your computer? ")
    print("    On Windows, right click Start, click System")
    
    print("  Important: after installing ta-lib, restart Python environment.")
    
    return
#==============================================================================

if __name__ =="__main__":
    ticker='600519.SS'
    start='2022-1-1'
    end='2022-12-31'
    
    RSI_days=[6,12,24]
    RSI_lines=[20,50,80]
    
    loc1='upper left'
    loc2='center right'
    
    resample_freq='H'
    smooth=True
    linewidth=1.5
    graph=['ALL']
    printout=True

def security_RSI(ticker,start='default',end='default', \
             RSI_days=[6,12,24],RSI_lines=[20,50,80], \
             resample_freq='6H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    套壳函数，除了股票，还可用于交易所债券和交易所基金（如ETF和REITS）
    """
    df=stock_RSI(ticker=ticker,start=start,end=end, \
                 RSI_days=RSI_days,RSI_lines=RSI_lines, \
                 resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
                 loc1=loc1,loc2=loc2, \
                 graph=graph,printout=printout)
    return df

    
def stock_RSI(ticker,start='default',end='default', \
             RSI_days=[6,12,24],RSI_lines=[20,50,80], \
             resample_freq='H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    功能：计算股票的技术分析指标RSI
    输入：df，四种股价Open/Close/High/Low，成交量Volume
    输出：df
    含有指标：
    RSI1(快速线，周线，黄色)、RSI2(中速线，双周线，紫色)、RSI3(慢速线，月线，白色)
    """
    
    #=========== 导入需要的包
    try:
        import talib  
    except:
        print("  #Error(stock_RSI): lack of necessary module - ta-lib")
        talib_install_method()
        return None
    
    #=========== 日期转换与检查
    # 检查日期：截至日期
    import datetime as dt; today=dt.date.today()
    if end in ['default','today']:
        end=today
    else:
        validdate,end=check_date2(end)
        if not validdate:
            print("  #Warning(stock_RSI): invalid date for",end)
            end=today

    # 检查日期：开始日期
    if start in ['default']:
        start=date_adjust(end,adjust=-31)
    else:
        validdate,start=check_date2(start)
        if not validdate:
            print("  #Warning(stock_RSI): invalid date for",start)
            start=date_adjust(todate,adjust=-31)
    
    #=========== 获取股价和成交量数据
    result,startpd,endpd=check_period(start,end)
    
    days_list=RSI_days
    max_days=max(days_list)
    start1=date_adjust(start,adjust=-max_days * 3)
    
    df=get_price(ticker,start1,end)
    if df is None:
        print("  #Error(stock_RSI): no info found for",ticker,"from",start,"to",end)
        return None
    if len(df)==0:
        print("  #Error(stock_RSI): zero record found for",ticker,"from",start,"to",end)
        return None   
    
    #============ 计算RSI 
    #df['rsi'] = talib.RSI(df['Close'], timeperiod=RSI_days)
    RSI_cols=[]
    RSI_seq=1
    for mad in RSI_days:
        col='RSI'+str(RSI_seq)
        RSI_cols=RSI_cols+[col]
        df[col] = talib.RSI(df['Close'],timeperiod=mad)
        RSI_seq=RSI_seq+1
    
    df['datepd']=df.index
    df['日期']=df['datepd'].apply(lambda x: x.strftime("%Y-%m-%d"))
    del df['datepd']
    
    # RSI1/RSI3快慢线交叉
    dft1=df.copy()
    dft1['short-long']=dft1['RSI1']-dft1['RSI3']
    dft1['sign']=dft1['short-long'].apply(lambda x: 1 if x>0 else -1)
    dft1['sign_cross']=dft1['sign']-dft1['sign'].shift(1)
    dft1['RSI1/3交叉类型']=dft1['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
    dft1b=dft1[dft1['sign_cross'] != 0]
    dft1c=dft1b[(dft1b.index >= startpd) & (dft1b.index <= endpd)] 
    dft1c.dropna(inplace=True)
    
    # RSI2/RSI3快慢线交叉
    dft2=df.copy()
    dft2['short-long']=dft2['RSI2']-dft2['RSI3']
    dft2['sign']=dft2['short-long'].apply(lambda x: 1 if x>0 else -1)
    dft2['sign_cross']=dft2['sign']-dft2['sign'].shift(1)
    dft2['RSI2/3交叉类型']=dft2['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
    dft2b=dft2[dft2['sign_cross'] != 0]
    dft2c=dft2b[(dft2b.index >= startpd) & (dft2b.index <= endpd)] 
    dft2c.dropna(inplace=True)
        
    # RSI限定日期范围
    df1=df[(df.index >= startpd) & (df.index <= endpd)]    

    if len(graph) != 0:
        
        # RSI绘图
        df4=df1[['Close']+RSI_cols]
        df4.rename(columns={'Close':'收盘价'},inplace=True)
        title_txt="股票价格走势分析："+codetranslate(ticker)+"，RSI"
        
        import datetime as dt; today=dt.date.today()    
        source="数据来源：sina/yahoo/stooq/fred，"+str(today)
        footnote="RSI参数："+str(RSI_days)
        x_label=footnote+'\n'+source
        
        # 设置绘图区的背景颜色为黑色
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.patch.set_facecolor('black')
        
        # 绘制曲线
        if ('RSI1' in graph) or ('ALL' in graph):
            ax.plot(df4['RSI1'],label='快速(周)线RSI1',linewidth=linewidth*2,color='orange')
        if ('RSI2' in graph) or ('ALL' in graph):
            ax.plot(df4['RSI2'],label='中速(双周)线RSI2',linewidth=linewidth*2,color='purple')
        if ('RSI3' in graph) or ('ALL' in graph):
            ax.plot(df4['RSI3'],label='慢速(月)线RSI3',linewidth=linewidth*2,color='white')
        
        # 绘制水平辅助线
        hl_linestyle_list=['dashed','-.','dotted']
        #plt.axhline(y=0,label='指标零线',color='cyan',linestyle=':',linewidth=linewidth*2) 
        for hl in RSI_lines:
            pos=RSI_lines.index(hl)
            hl_ls=hl_linestyle_list[pos]
            plt.axhline(y=hl,label='',color='cyan',linestyle=hl_ls,linewidth=linewidth) 
        
        # 设置左侧坐标轴
        ax.set_ylabel('RSI指标',fontsize=ylabel_txt_size)
        ax.set_xlabel(x_label,fontsize=xlabel_txt_size)
        ax.legend(loc=loc1,fontsize=legend_txt_size)
        
        # 绘制股价在右侧
        #绘证券2：建立第二y轴
        
        #插值平滑
        if smooth:
            print("  Smoothening curves directly ...")
            try:
                df5=df_smooth_manual(df4,resample_freq=resample_freq)
            except:
                df5=df4
        else:
            df5=df4
        
        ax2 = ax.twinx()
        ax2.plot(df5['收盘价'],label='收盘价',linewidth=linewidth,color='gray',ls='--')
        
        # 右侧坐标轴标记
        ax2.set_ylabel('收盘价',fontsize=ylabel_txt_size)
        ax2.legend(loc=loc2,fontsize=legend_txt_size)
        
        # 图示标题
        plt.title(title_txt,fontweight='bold',fontsize=title_txt_size)
        #plt.xticks(rotation=30)
        plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
        #plt.legend(loc='best',fontsize=legend_txt_size)
        plt.show()

        if printout:
            if (('RSI1' in graph) & ('RSI3' in graph)) or ('ALL' in graph):
                if len(dft1c)!=0:
                    print("\n=== RSI1与RSI3的交叉点 ===")
                    alignlist=['left','center']
                    print(dft1c[['日期','RSI1/3交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
                else:
                    print("  Note: no RSI1/3 cross of lines incurred for",ticker,"from",start,"to",end)
        if printout:
            if (('RSI2' in graph) & ('RSI3' in graph)) or ('ALL' in graph):
                if len(dft2c)!=0:
                    print("\n=== RSI2与RSI3的交叉点 ===")
                    alignlist=['left','center']
                    print(dft2c[['日期','RSI2/3交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
                else:
                    print("  Note: no RSI2/3 cross of lines incurred for",ticker,"from",start,"to",end)
    
    return df1       
#==============================================================================
#==============================================================================
#==============================================================================

def findout_cross(df,start,end,fast_line,slow_line):
    """
    功能：技术分析，找出fast_line与slow_line两条线交叉的记录，并给出交叉类型：上穿，下穿
    """
    
    dft1=df.copy()
    dft1['short-long']=dft1[fast_line]-dft1[slow_line]
    dft1['sign']=dft1['short-long'].apply(lambda x: 1 if x>0 else -1)
    dft1['sign_cross']=dft1['sign']-dft1['sign'].shift(1)
    dft1['交叉类型']=dft1['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
    dft1b=dft1[dft1['sign_cross'] != 0]
    
    result,startpd,endpd=check_period(start,end)
    dft1c=dft1b[(dft1b.index >= startpd) & (dft1b.index <= endpd)] 
    
    dft1c.dropna(inplace=True)
    
    return dft1c

#==============================================================================
#==============================================================================
#==============================================================================


if __name__ =="__main__":
    ticker='600519.SS'
    start='2010-1-1'
    end='2022-12-31'
    
    KDJ_days=[9,3,3]
    matypes=[0,0]
    
    loc1='upper left'
    loc2='center right'
    
    resample_freq='H'
    smooth=True
    linewidth=1.5
    
    graph=['ALL']
    printout=True
    
    graph=False

def security_KDJ(ticker,start='default',end='default', \
             KDJ_days=[9,3,3],matypes=[0,0],KDJ_lines=[20,50,80], \
             resample_freq='6H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    套壳函数
    """
    df=stock_KDJ(ticker=ticker,start=start,end=end, \
                 KDJ_days=KDJ_days,matypes=matypes,KDJ_lines=KDJ_lines, \
                 resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
                 loc1=loc1,loc2=loc2, \
                 graph=graph,printout=printout)
    return df

    
def stock_KDJ(ticker,start='default',end='default', \
             KDJ_days=[9,3,3],matypes=[0,0],KDJ_lines=[20,50,80], \
             resample_freq='H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True):
    """
    功能：计算股票的技术分析指标KDJ
    输入：df，四种股价Open/Close/High/Low，成交量Volume
    输出：df
    含有指标：
    K线(快速线，黄色)、D线(慢速线，绿色)、J线(差额，紫色)
    """
    
    #=========== 导入需要的包
    try:
        import talib  
    except:
        print("  #Error(stock_KDJ): lack of necessary module - talib")
        talib_install_method()
        return None
    
    #=========== 日期转换与检查
    # 检查日期：截至日期
    import datetime as dt; today=dt.date.today()
    if end in ['default','today']:
        end=today
    else:
        validdate,end=check_date2(end)
        if not validdate:
            print("  #Warning(stock_KDJ): invalid date for",end)
            end=today

    # 检查日期：开始日期
    if start in ['default']:
        start=date_adjust(end,adjust=-31)
    else:
        validdate,start=check_date2(start)
        if not validdate:
            print("  #Warning(stock_KDJ): invalid date for",start)
            start=date_adjust(todate,adjust=-31)
    
    #=========== 获取股价和成交量数据
    result,startpd,endpd=check_period(start,end)
    
    days_list=KDJ_days
    max_days=max(days_list)
    start1=date_adjust(start,adjust=-max_days * 3)
    
    df=get_price(ticker,start1,end)
    if df is None:
        print("  #Error(stock_RSI): no info found for",ticker,"from",start,"to",end)
        return None
    if len(df)==0:
        print("  #Error(stock_RSI): zero record found for",ticker,"from",start,"to",end)
        return None   
    
    df['datepd']=df.index
    df['日期']=df['datepd'].apply(lambda x: x.strftime("%Y-%m-%d"))
    del df['datepd']
    
    #============ 计算KDJ
    """
    df['kdj_k'],df['kdj_d'] = talib.STOCH(df['High'],df['Low'],df['Close'], \
                        fastk_period=KDJ_fastk_period,
                        slowk_period=KDJ_slowk_period, 
                        slowk_matype=KDJ_slowk_matype, 
                        slowd_period=KDJ_slowd_period, 
                        slowd_matype=KDJ_slowd_matype)
    df['kdj_j'] = 3*df['kdj_k'] - 2*df['kdj_d']    
    """
    KDJ_cols=['K','D','J']
    df['K'],df['D'] = talib.STOCH(df['High'],df['Low'],df['Close'], \
                        fastk_period=KDJ_days[0],
                        slowk_period=KDJ_days[1], 
                        slowk_matype=matypes[0], 
                        slowd_period=KDJ_days[2], 
                        slowd_matype=matypes[1])
    df['J'] = 3*df['K'] - 2*df['D']    
    
    # 限制J线在0-100之间
    if graph:
        df['J']=df['J'].apply(lambda x:100 if x>100 else 0 if x<0 else x)
    
    if not graph:
        return df
    
    # J/K线交叉
    """
    dft1=df.copy()
    dft1['short-long']=dft1['J']-dft1['K']
    dft1['sign']=dft1['short-long'].apply(lambda x: 1 if x>0 else -1)
    dft1['sign_cross']=dft1['sign']-dft1['sign'].shift(1)
    dft1['J/K线交叉类型']=dft1['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
    dft1b=dft1[dft1['sign_cross'] != 0]
    dft1c=dft1b[(dft1b.index >= startpd) & (dft1b.index <= endpd)] 
    dft1c.dropna(inplace=True)
    """
    dft1c=findout_cross(df,start,end,'J','K')
    
    # J/D线交叉
    """
    dft2=df.copy()
    dft2['short-long']=dft2['J']-dft2['D']
    dft2['sign']=dft2['short-long'].apply(lambda x: 1 if x>0 else -1)
    dft2['sign_cross']=dft2['sign']-dft2['sign'].shift(1)
    dft2['J/D线交叉类型']=dft2['sign_cross'].apply(lambda x: '上穿' if x > 0 else '下穿' if x < 0 else '')
    dft2b=dft2[dft2['sign_cross'] != 0]
    dft2c=dft2b[(dft2b.index >= startpd) & (dft2b.index <= endpd)] 
    dft2c.dropna(inplace=True)
    """
    dft2c=findout_cross(df,start,end,'J','D')
    
    # K/D线交叉
    dft3c=findout_cross(df,start,end,'K','D')
        
    # 限定日期范围
    df1=df[(df.index >= startpd) & (df.index <= endpd)]    

    if len(graph) != 0:
        
        # 绘图
        df4=df1[['Close']+KDJ_cols]
        df4.rename(columns={'Close':'收盘价'},inplace=True)
        title_txt="股票价格走势分析："+codetranslate(ticker)+"，KDJ"
        
        import datetime as dt; today=dt.date.today()    
        source="数据来源：sina/yahoo/stooq/fred，"+str(today)
        footnote="KDJ参数："+str(KDJ_days)
        x_label=footnote+'\n'+source
        
        # 设置绘图区的背景颜色为黑色
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.patch.set_facecolor('black')
        
        # 绘制曲线
        if ('K' in graph) or ('ALL' in graph):
            ax.plot(df4['K'],label='快速线K',linewidth=linewidth*2,color='orange')
        if ('D' in graph) or ('ALL' in graph):
            ax.plot(df4['D'],label='慢速线D',linewidth=linewidth*2,color='green')
        if ('J' in graph) or ('ALL' in graph):
            ax.plot(df4['J'],label='超快确认线J',linewidth=linewidth*2,color='purple')
        
        # 绘制水平辅助线: 某些情况下不绘制，以便展现KDJ线细节
        maxK=df4['K'].max()
        maxD=df4['D'].max()
        maxJ=df4['J'].max()
        maxKDJ=max(maxK,maxD,maxJ)

        minK=df4['K'].min()
        minD=df4['D'].min()
        minJ=df4['J'].min()
        minKDJ=min(minK,minD,minJ)
        
        hl_linestyle_list=['dashed','dashed','-.','dotted','dotted']
        hl_color_list=['red','red','white','cyan','cyan']
        #plt.axhline(y=0,label='指标零线',color='cyan',linestyle=':',linewidth=linewidth*2) 
        for hl in KDJ_lines:
            draw=True
            if (hl > maxKDJ):
                draw=False
            if (hl < minKDJ):
                draw=False
            
            if draw:
                pos=KDJ_lines.index(hl)
                hl_ls=hl_linestyle_list[pos]
                hl_color=hl_color_list[pos]
                plt.axhline(y=hl,label='',color=hl_color,linestyle=hl_ls,linewidth=linewidth) 
        
        # 设置左侧坐标轴
        ax.set_ylabel('KDJ指标',fontsize=ylabel_txt_size)
        ax.set_xlabel(x_label,fontsize=xlabel_txt_size)
        ax.legend(loc=loc1,fontsize=legend_txt_size)
        
        # 设置纵轴刻度
        from matplotlib.pyplot import MultipleLocator
        y_major_locator=MultipleLocator(10)
        ax.yaxis.set_major_locator(y_major_locator)
        #ax.set_ylim(-5,105)
        
        # 绘制股价在右侧
        #绘证券2：建立第二y轴
        
        #插值平滑
        if smooth:
            print("  Smoothening curves directly ...")
            try:
                df5=df_smooth_manual(df4,resample_freq=resample_freq)
            except:
                df5=df4
        else:
            df5=df4
        
        ax2 = ax.twinx()
        ax2.plot(df5['收盘价'],label='收盘价',linewidth=linewidth,color='gray',ls='--')
        
        # 右侧坐标轴标记
        ax2.set_ylabel('收盘价',fontsize=ylabel_txt_size)
        ax2.legend(loc=loc2,fontsize=legend_txt_size)
        
        # 图示标题
        plt.title(title_txt,fontweight='bold',fontsize=title_txt_size)
        #plt.xticks(rotation=30)
        plt.gcf().autofmt_xdate() # 优化标注（自动倾斜）
        #plt.legend(loc='best',fontsize=legend_txt_size)
        plt.show()

        if printout:
            alignlist=['left','center']
            if (('J' in graph) & ('K' in graph)) or ('ALL' in graph):
                if len(dft1c)!=0:
                    print("\n**** J线与K线的交叉点")
                    print(dft1c[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
                else:
                    print("  Note: no J/K cross of lines incurred for",ticker,"from",start,"to",end)
 
            if (('J' in graph) & ('D' in graph)) or ('ALL' in graph):
                if len(dft2c)!=0:
                    print("\n**** J线与K线的交叉点")
                    alignlist=['left','center']
                    print(dft2c[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
                else:
                    print("  Note: no J/D cross of lines incurred for",ticker,"from",start,"to",end)
 
            if (('K' in graph) & ('D' in graph)) or ('ALL' in graph):
                if len(dft3c)!=0:
                    print("\n**** K线与D线的交叉点")
                    alignlist=['left','center']
                    print(dft3c[['日期','交叉类型']].to_markdown(index=False,tablefmt='plain',colalign=alignlist))
                else:
                    print("  Note: no K/D cross of lines incurred for",ticker,"from",start,"to",end)
    
    return df1       
#==============================================================================
#==============================================================================
#==============================================================================

if __name__ =="__main__":
    ticker='600519.SS'
    start='2020-1-1'
    end='2022-12-31'
    
    past_days=1
    momemtum_days=0
    future_days=1
    
    threshhold=0.001
    
    df=stock_KDJ(ticker,start,end,graph=False)
    
def price_trend_technical(df, \
                    past_days=1,momemtum_days=1,future_days=1, \
                    threshhold=0.001):
    """
    功能：检查技术结果中每日股价的变化趋势：上涨，下跌，振荡，转折
    past_days: 当前日期前几个交易日的算术收益率天数
    momemtum_days: 股价发生变化的惯性天数，从当前日期开始计算
    future_days: 当前日期未来几个交易日的算术收益率天数，从当前日期+惯性天数开始计算
    threshhold: 股价算术收益率变化的最低门槛，
    不小于threshhold：上涨，+；
    小于-threshhold：下跌，-；
    其余：振荡，~
    
    注意：可能存在尚不明了的问题！！！
    """  
    
    cols=list(df)
    cols.remove('Close')
    cols1=cols+['Close']
    df1=df[cols1]    
    
    df1['Close_past']=df1['Close'].shift(past_days)
    df1['ret_past']=df1['Close'] - df1['Close_past']
    
    # +=上涨，~=振荡，-=下跌
    df1['trend_past']=df1['ret_past'].apply(lambda x:'+' if x >= threshhold else 
                                            '-' if x <= -threshhold 
                                            else '~' if -threshhold < x < threshhold
                                            else '')
    if momemtum_days != 0:
        df1['Close_mom']=df1['Close'].shift(-momemtum_days)
    else:
        df1['Close_mom']=df1['Close']
        
    df1['Close_future']=df1['Close'].shift(-momemtum_days-future_days)
    df1['ret_future']=df1['Close_future'] - df1['Close_mom']
    df1['trend_future']=df1['ret_future'].apply(lambda x:'+' if x >= threshhold 
                                                else '-' if x <= -threshhold 
                                                else '~' if -threshhold < x < threshhold
                                                else '')

    df1['trend_past2future']=''
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '+2+' if (x['trend_past']=='+') & (x['trend_future']=='+') 
                                       else x['trend_past2future'],axis=1)
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '-2-' if (x['trend_past']=='-') & (x['trend_future']=='-') 
                                       else x['trend_past2future'],axis=1)
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '~2~' if (x['trend_past']=='~') & (x['trend_future']=='~') 
                                       else x['trend_past2future'],axis=1)
    
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '+2-' if (x['trend_past']=='+') & (x['trend_future']=='-') 
                                       else x['trend_past2future'],axis=1)
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '+2~' if (x['trend_past']=='+') & (x['trend_future']=='~') 
                                       else x['trend_past2future'],axis=1)
        
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '-2+' if (x['trend_past']=='-') & (x['trend_future']=='+') 
                                       else x['trend_past2future'],axis=1)
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '-2~' if (x['trend_past']=='-') & (x['trend_future']=='~') 
                                       else x['trend_past2future'],axis=1)
        
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '~2+' if (x['trend_past']=='~') & (x['trend_future']=='+') 
                                       else x['trend_past2future'],axis=1)
    df1['trend_past2future']=df1.apply(lambda x: 
                                       '~2-' if (x['trend_past']=='~') & (x['trend_future']=='-') 
                                       else x['trend_past2future'],axis=1)

    
    tempcols=['Close_past','ret_past','Close_mom','Close_future','ret_future']
    df1.drop(tempcols, axis=1, inplace=True)
    
    # 记录参数
    df1['past_days']=past_days
    df1['momemtum_days']=momemtum_days
    df1['future_days']=future_days
    df1['threshhold']=threshhold
    
    return df1
    
    
#==============================================================================
#==============================================================================

if __name__ =="__main__":
    
    ticker='600519.SS'
    start='2020-1-1'
    end='2022-12-31'
    df=stock_KDJ(ticker,start,end,graph=False)
    
    df1=price_trend_technical(df)
    KDJ_values=[20,20,10]
    J_days=3
    JvsK='above'
    JKcross='bottom up'
    value_type='ceiling'
    
    otc1,dfs1=check_KDJ_market(df1,start,end,KDJ_values=[50,50,50],value_type='floor')
    otc2,dfs2=check_KDJ_market(df1,start,end,KDJ_values=[80,80,100],J_days=3,value_type='floor')
    dfs_down=dfs2[dfs2['trend_future']=='-']
    
    otp1,dfs1=check_KDJ_market(df1,start,end,KDJ_values=[50,50,50],value_type='ceiling')
    otp2,dfs2=check_KDJ_market(df1,start,end,KDJ_values=[20,20,0],J_days=3,value_type='ceiling')
    dfs_up=dfs2[dfs2['trend_future']=='+']


def check_KDJ_market(df1,start,end,KDJ_values=[50,50,50],J_days=1,JvsK='any',JKcross='any',
                     value_type='ceiling'):
    """
    功能：检查KDJ计算结果中，多头/空头市场的股价趋势比例
    start,end：日期范围
    value_type='ceiling'：K、D、J值位于KDJ_values=[50,50,50]以下，假设为空头市场
    value_type='floor'：K、D、J值位于KDJ_values=[50,50,50]以上，假设为多头市场
    
    注意：可能存在尚不明了的问题！！！
    """
    import pandas as pd
    
    ticker=df1['ticker'].values[0]
    past_days=df1['past_days'].values[0]   
    momemtum_days=df1['momemtum_days'].values[0]   
    future_days=df1['future_days'].values[0]   
    threshhold=df1['threshhold'].values[0]   
    
    # J值的持续天数
    if J_days > 1:
        for jj in range(1,J_days):
            df1['J_'+str(jj)]=df1['J'].shift(jj)
    
    result,startpd,endpd=check_period(start,end)
    df2=df1[(df1.index >= startpd) & (df1.index <=endpd)]
    df2=df2[df2['trend_future'] != '']
    
    # 多头市场：KDJ值的下限floor；空头市场：KDJ值的上限ceiling
    if value_type == 'floor':
        df3=df2[(df2['K'] > KDJ_values[0]) & 
                (df2['D'] > KDJ_values[1]) & 
                (df2['J'] > KDJ_values[2])]
        if J_days > 1:
            for jj in range(1,J_days):
                #print('jj=',jj)
                df3=df3[df3['J_'+str(jj)] > KDJ_values[2]]
    elif value_type == 'ceiling':
        df3=df2[(df2['K'] < KDJ_values[0]) & 
                (df2['D'] < KDJ_values[1]) & 
                (df2['J'] < KDJ_values[2])]
        if J_days > 1:
            for jj in range(1,J_days):
                #print('jj=',jj)
                df3=df3[df3['J_'+str(jj)] < KDJ_values[2]]
    else:
        pass
    
    # J/K线上下位置
    if JvsK=='above':
        df3=df3[df3['J'] > df3['K']]
    elif JvsK=='below':
        df3=df3[df3['J'] < df3['K']]  
    else:
        pass
    
    # J/K线交叉
    if JKcross in ['bottom up','top down']:
        df3cross=findout_cross(df3,start,end,'J','K')
        df3cross2=pd.DataFrame(df3cross['交叉类型'])
        
        import pandas as pd
        df3=pd.merge(df3,df3cross2,how='inner',left_index=True,right_index=True)
        
        if JKcross == 'bottom up':
            df3=df3[df3['交叉类型']=='上穿']
        elif JKcross == 'top down':
            df3=df3[df3['交叉类型']=='下穿']
        else:
            pass
    
    if len(df3)==0:
        print("  #Warning(check_KDJ_market): no designated signals found for",ticker,"from",start,'to',end)
        return None,None
    
    # 未来上涨、下跌、振荡的比例
    df4a=df3[df3['trend_future'] == '+']
    pcta=len(df4a)/len(df3)
    df4b=df3[df3['trend_future'] == '-']
    pctb=len(df4b)/len(df3)
    df4c=df3[df3['trend_future'] == '~']
    pctc=len(df4c)/len(df3)

    # 未来转为下跌、上涨的比例
    df4d=df3[df3['trend_past2future'].isin(['+2-','~2-'])]
    pctd=len(df4d)/len(df3)
    df4e=df3[df3['trend_past2future'].isin(['-2+','~2+'])]
    pcte=len(df4e)/len(df3)
    
    import pandas as pd
    outcome=pd.DataFrame()
    
    row=pd.Series({'ticker':ticker,'start':start,'end':end, \
                   'K value':KDJ_values[0],'D value':KDJ_values[1],'J value':KDJ_values[2],
                   'J days':J_days,'JvsK':JvsK,'JKcross':JKcross,
                   'value type':value_type, \
                   'past_days':past_days,'momemtum_days':momemtum_days,'future_days':future_days,
                   'threshhold':threshhold, \
                   'future up ratio':pcta,'future down ratio':pctb,'future vibrate ratio':pctc, \
                   't2- ratio':pctd,'t2+ ratio':pcte})
    try:
        outcome=outcome.append(row,ignore_index=True)
    except:
        outcome=outcome._append(row,ignore_index=True)         
    
    return outcome,df3

#==============================================================================
#==============================================================================
if __name__ =="__main__":
    ticker='600518.SS'
    start='2013-1-1'
    end='2022-12-31'
    
    KDJ_days=[9,3,3]
    matypes=[0,0]
    
    past_days=1
    momemtum_days=0
    future_days=1
    threshhold=0.001
    
    KDJ_values=[50,50,50]
    J_days=1
    JvsK='above'
    JKcross='bottom up'
    
    value_type='floor'
    
    # 多头市场与空头市场
    dfs1=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],value_type='floor')
    dfs2=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],value_type='ceiling')
    
    # 超买区：茅台买家众多，即使在超买区，下跌趋势也比较有限
    dfs3=backtest_KDJ(ticker,start,end,KDJ_values=[80,80,80],value_type='floor')
    dfs4=backtest_KDJ(ticker,start,end,KDJ_values=[80,80,90],value_type='floor')
    dfs4=backtest_KDJ(ticker,start,end,KDJ_values=[80,80,90],J_days=3,value_type='floor')
     
    # 超卖区
    dfs12=backtest_KDJ(ticker,start,end,KDJ_values=[20,20,10],value_type='ceiling')
    dfs15=backtest_KDJ(ticker,start,end,KDJ_values=[20,20,0],J_days=3,value_type='ceiling')
   
    # K线在D线上方/下方
    dfs21=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],JvsK='above',value_type='floor')
    dfs22=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],JvsK='below',value_type='floor')
    
   # K/D线交叉
    dfs31=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],JKcross='top down',value_type='floor')
    dfs32=backtest_KDJ(ticker,start,end,KDJ_values=[50,50,50],JKcross='bottom up',value_type='floor') 
    dfs32=backtest_KDJ(ticker,start,end,KDJ_values=[20,20,10],JKcross='bottom up',value_type='ceiling') 

    # 高位死叉
    dfs33=backtest_KDJ(ticker,start,end,KDJ_values=[80,80,90],JKcross='top down',value_type='floor')
    
    # 低位金叉
    dfs34=backtest_KDJ(ticker,start,end,KDJ_values=[20,20,10],JKcross='bottom up',value_type='ceiling')

def backtest_KDJ(ticker,start,end,
                      KDJ_days=[9,3,3],matypes=[0,0],
                      past_days=3,momemtum_days=0,future_days=3,threshhold=0.005,
                      KDJ_values=[50,50,50],J_days=1,JvsK='any',JKcross='any',
                      value_type='floor'):
    """
    功能：验证KDJ指标对股价未来走势判断的准确度概率
    
    注意：可能存在尚不明了的问题！！！
    """
    # 计算KDJ指标
    df=stock_KDJ(ticker,start,end,KDJ_days=KDJ_days,matypes=matypes,graph=False)
    total_obs=len(df)
    
    # 计算股价波动率，约等于1，无法作为threshhold使用
    #=df['Close'].std() / df['Close'].mean()
    
    # 计算某一日期前后的股价走势及其变化
    df1=price_trend_technical(df,
                              past_days=past_days,
                              momemtum_days=momemtum_days,future_days=future_days,
                              threshhold=threshhold)
    
    # KDJ特定情景：股价走势情形概率
    checkdf,dfs=check_KDJ_market(df1,start,end,
                                 KDJ_values=KDJ_values,J_days=J_days,
                                 JvsK=JvsK,JKcross=JKcross,
                                 value_type=value_type)
    if checkdf is None:
        #print("  #Warning(backtest_KDJ): no KDJ signals found for",ticker)
        print("  Possible reasons: conditions are too strict, or period is too short")
        return None
    
    if value_type == 'floor':
        rel=' > '
    elif value_type == 'ceiling':
        rel=' < '
    else:
        rel=' ? '
        
    signals1="K"+rel+str(KDJ_values[0])+', D'+rel+str(KDJ_values[1])+', J'+rel+str(KDJ_values[2])
    
    signals2=''
    if J_days > 1:
        signals2='\n    J值条件至少持续'+str(J_days)+'个交易日' 
    
    signals3=''
    if JvsK=='above':
        signals3='\n    J线在K线上方'
    elif JvsK=='below':
        signals3='\n    J线在K线下方'
    else:
        pass
    
    signals4=''
    if JKcross=='bottom up':
        signals4='\n    J/K线出现金叉'
    elif JKcross=='top down':
        signals4='\n    J/K线出现死叉'
    else:
        pass
        
    signals=signals1 +signals2 +signals3 +signals4
    print_KDJ_result(checkdf,dfs,signals,ticker,start,end,total_obs,JKcross,
                     past_days,momemtum_days,future_days,threshhold)
    """
    market_upward=dfs[dfs['trend_future']=='+']
    market_downward=dfs[dfs['trend_future']=='-']
    market_vibrate=dfs[dfs['trend_future']=='~']
    market_upturn=dfs[dfs['trend_past2future'].isin(['~2+','-2+'])]
    market_downturn=dfs[dfs['trend_past2future'].isin(['~2-','+2-'])]
    """
    return dfs    



#==============================================================================
def print_KDJ_result(checkdf,dfs,KDJ_signals,
                     ticker,start,end,total_obs,JKcross,
                     past_days,momemtum_days,future_days,threshhold):
    """
    功能：打印KDJ验证结果
    注意：KDJ_signals需要提前编辑条件字符串输入，例如"K > 80, D > 80, J > 100且至少持续3个交易日"
    """
    
    print("\n*** KDJ研判股价趋势：回溯验证，"+codetranslate(ticker))
    print("  "+start+'至'+end+'，共计'+str(total_obs)+'个样本')
    
    print("  KDJ信号：期间内出现"+str(len(dfs))+'次')
    print("    "+KDJ_signals)
    
    print("  验证参数:")
    print("    之前趋势期间："+str(past_days)+'个交易日')
    
    if momemtum_days > 0:
        print("    滞后变化/提前反应：滞后"+str(momemtum_days)+'个交易日')
    elif momemtum_days == 0:
        print("    滞后变化/提前反应：无，立即变化")
    else:
        print("    滞后变化/提前反应：提前"+str(momemtum_days)+'个交易日')
        
    print("    之后趋势期间："+str(future_days)+'个交易日')
    print("    股价变化过滤门限："+str(threshhold*100)+'%')
    
    print("  回溯检验结果:")
    print("    之后出现股价上涨趋势的比例:",round(checkdf['future up ratio'].values[0]*100,1),'\b%')
    print("    之后出现股价下跌趋势的比例:",round(checkdf['future down ratio'].values[0]*100,1),'\b%')
    print("    之后出现股价振荡情形的比例:",round(checkdf['future vibrate ratio'].values[0]*100,1),'\b%')    
    
    """
    if JKcross =='bottom up':
        print("    出现JD金叉后股价上涨的比例:",round(checkdf['t2+ ratio'].values[0]*100,1),'\b%')
    elif JKcross =='top down':
        print("    出现JK死叉后股价下跌的比例:",round(checkdf['t2- ratio'].values[0]*100,1),'\b%')
    else:
        pass
    """
    
    return
#==============================================================================
#==============================================================================    
if __name__ =="__main__":
    ticker='600519.SS'
    fromdate='2023-1-1'
    todate='2023-6-25'
    boll_days=20
    graph=True
    smooth=False
    loc='best'
    date_range=False
    date_freq=False
    annotate=False

def security_Bollinger(ticker,start='default',end='default',boll_days=20, \
                         graph=True,smooth=True,loc='best', \
                         date_range=False,date_freq=False,annotate=False):
    """
    套壳函数，为了与security_MACD/RSI/KDJ保持相似
    """
    df=stock_Bollinger(ticker=ticker,start=start,end=end,boll_days=boll_days, \
                             graph=graph,smooth=smooth,loc=loc, \
                             date_range=date_range,date_freq=date_freq,annotate=annotate)
    return df

def stock_Bollinger(ticker,start='default',end='default',boll_days=20, \
                         graph=True,smooth=True,loc='best', \
                         date_range=False,date_freq=False,annotate=False):
    """
    套壳函数，为了与stock_MACD/RSI/KDJ保持相似
    """
    
    #=========== 日期转换与检查
    # 检查日期：截至日期
    import datetime as dt; today=dt.date.today()
    if end in ['default','today']:
        end=today
    else:
        validdate,end=check_date2(end)
        if not validdate:
            print("  #Warning(stock_Bollinger): invalid date for",end)
            end=today

    # 检查日期：开始日期
    if start in ['default']:
        start=date_adjust(end,adjust=-31)
    else:
        validdate,start=check_date2(start)
        if not validdate:
            print("  #Warning(stock_Bollinger): invalid date for",start)
            start=date_adjust(todate,adjust=-31)

    df=security_bollinger(ticker=ticker,fromdate=start,todate=end,boll_days=boll_days, \
                             graph=graph,smooth=smooth,loc=loc, \
                             date_range=date_range,date_freq=date_freq,annotate=annotate)
    return df


def security_bollinger(ticker,fromdate,todate,boll_days=20, \
                         graph=True,smooth=True,loc='best', \
                         date_range=False,date_freq=False,annotate=False):
    """
    功能：单个证券，绘制布林带
    date_range=False：指定开始结束日期绘图
    date_freq=False：指定横轴日期间隔，例如'D'、'2D'、'W'、'M'等，横轴一般不超过25个标注，否则会重叠
    
    解释布林带：
    1、上线：压力线；下线：支撑线；均线：中界线
    2、上下限之间：置信区间+/-2std
    3、价格由下向上穿越下线时，可视为买进信号；价格由下向上穿越中间线时，则有可能加速上行，是加仓买进的信号。
    4、价格在中界线与上线之间波动运行时为多头市场，可持多或加码；价格长时间在中界线与上线间运行后，由上往下跌破中间线为卖出信号。
    5、价格在中界线与下线之间向下波动运行时为空头市场，可持空或加抛。
    """
    # 提前开始日期
    fromdate1=date_adjust(fromdate,adjust=-365*1)
    
    try:
        pricedf=get_price(ticker,fromdate1,todate)
    except:
        print("  #Error(security_bollinger): price info not found for",ticker)
        return None
    
    # 滚动均值与标准差
    pricedf['bmiddle']=pricedf["Close"].rolling(window=boll_days).mean()
    pricedf['bsd']=pricedf["Close"].rolling(window=boll_days).std()
    pricedf['bupper']=pricedf["bmiddle"] + pricedf['bsd']*2
    pricedf['blower']=pricedf["bmiddle"] - pricedf['bsd']*2
    
    df=pricedf[['bupper','bmiddle','blower','Close']]
    df.rename(columns={'bupper':'上(压力)线','bmiddle':'中(界)线','blower':'下(支撑)线','Close':'收盘价'},inplace=True)

    # 截取时间段
    result,start,end=check_period(fromdate,todate)
    df1=df[(df.index >= start) & (df.index <= end)]

    y_label='价格'
    import datetime; today = datetime.date.today()
    x_label="数据来源：新浪/东方财富/stooq/雅虎财经，"+str(today)

    axhline_value=0
    axhline_label=''
    title_txt="证券价格布林带："+codetranslate(ticker)            
    
    """
        draw_lines(df1,y_label,x_label,axhline_value,axhline_label,title_txt, \
                   data_label=False,resample_freq='H',smooth=smooth,loc=loc,annotate=annotate)
    """
    #plt.rcParams['axes.facecolor']='gray'
    colorlist=['orange','black','purple','red']
    lslist=['--',':','-.','-']
    lwlist=[2.0,2.0,2.0,2.5]
    draw_lines2(df1,y_label,x_label,axhline_value,axhline_label,title_txt, \
               data_label=False,resample_freq='6H',smooth=smooth, \
               date_range=date_range,date_freq=date_freq,date_fmt='%Y-%m-%d', \
               colorlist=colorlist,lslist=lslist,lwlist=lwlist)

    return df1

#==============================================================================
def security_technical(ticker,start='default',end='default', \
             MA_days=[5,20],EMA_days=[5,20], \
             MACD_fastperiod=12,MACD_slowperiod=26,MACD_signalperiod=9, \
             RSI_days=[6,12,24],RSI_lines=[20,50,80], \
             KDJ_days=[9,3,3],matypes=[0,0],KDJ_lines=[20,50,80], \
             boll_days=20, \
             resample_freq='6H',smooth=True,linewidth=1.5, \
             loc1='lower left',loc2='lower right', \
             graph=['ALL'],printout=True, \
             date_range=False,date_freq=False,annotate=False, \
             technical=['MACD']):
    
    """
    套壳函数security_MACD/RSI/KDJ/Bollinger
    """
    # 检查类别
    if isinstance(technical,str):
        technical1=[technical]
    else:
        technical1=technical
    
    # 检查绘图种类
    if isinstance(graph,str):
        graph1=[graph]
    else:
        graph1=graph
    
    technical_list=['MACD','RSI','KDJ','Bollinger']    
    for t in technical1:
        if t not in technical_list:
            print("  Warning(security_technical): unsupported technical pattern",t)
            print("  Supported patterns:",technical_list)
        
    if 'MACD' in technical1:
        df=security_MACD(ticker=ticker,start=start,end=end, \
             MA_days=MA_days,EMA_days=EMA_days, \
             MACD_fastperiod=MACD_fastperiod,MACD_slowperiod=MACD_slowperiod,MACD_signalperiod=MACD_signalperiod, \
             resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
             loc1=loc1,loc2=loc2, \
             graph=graph1,printout=printout)
       
    if 'RSI' in technical1:
        df=security_RSI(ticker=ticker,start=start,end=end, \
             RSI_days=RSI_days,RSI_lines=RSI_lines, \
             resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
             loc1=loc1,loc2=loc2, \
             graph=graph1,printout=printout)

    if 'KDJ' in technical1:
        df=security_KDJ(ticker=ticker,start=start,end=end, \
             KDJ_days=KDJ_days,matypes=matypes,KDJ_lines=KDJ_lines, \
             resample_freq=resample_freq,smooth=smooth,linewidth=linewidth, \
             loc1=loc1,loc2=loc2, \
             graph=graph1,printout=printout)

    if 'Bollinger' in technical1:
        df=security_Bollinger(ticker=ticker,start=start,end=end,boll_days=boll_days, \
                         graph=True,smooth=smooth,loc=loc1, \
                         date_range=date_range,date_freq=date_freq,annotate=annotate)

    return df



#==============================================================================
#==============================================================================
#==============================================================================    

    