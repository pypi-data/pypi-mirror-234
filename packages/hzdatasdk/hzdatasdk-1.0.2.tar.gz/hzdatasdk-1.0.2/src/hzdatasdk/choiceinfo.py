# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CaiwuInfoReport(Base):
    __tablename__ = 'caiwu_info_report'
    __table_args__ = (
        Index('uk_code_date', 'stockcode', 'report_date', unique=True),
        {'comment': '财务信息表_报告期'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    stockcode = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    stockname = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    gdhs = Column(INTEGER(11), comment='股东户数 [ 户 ]')
    yysr = Column(DECIMAL(20, 2), comment='营业收入 [ 元 ]')
    yysrtb = Column(DECIMAL(10, 2), comment='营业收入同比增长率 [ % ]')
    jlr = Column(DECIMAL(20, 2), comment='净利润 [ 元 ]')
    jlrhb = Column(DECIMAL(10, 2), comment='净利润环比增长率 [ % ]')
    jlrtb = Column(DECIMAL(10, 2), comment='净利润同比增长率 [ % ]')
    yysrhb = Column(DECIMAL(10, 2), comment='营业收入环比增长率 [ % ]')
    mllhb = Column(DECIMAL(10, 2), comment='毛利率环比增长率 [ % ]')
    gsymgsgdjlrhb = Column(DECIMAL(10, 2), comment='归属母公司股东的净利润环比增长率 [ % ]')
    jyhdcsdxjlljehb = Column(DECIMAL(10, 2), comment='经营活动产生的现金流量净额环比增长率 [ % ]')
    zcfzl = Column(DECIMAL(10, 2), comment='资产负债率 [ % ]')
    fldzcbl = Column(DECIMAL(10, 2), comment='非流动资产比率 [ % ]')
    mgjzc = Column(DECIMAL(10, 2), comment='每股净资产 [ 元 ]')
    mgzbgj = Column(DECIMAL(10, 2), comment='每股资本公积 [ 元 ]')
    mgwfplr = Column(DECIMAL(10, 2), comment='每股未分配利润 [ 元 ]')
    mgjyhdcsdxjllje = Column(DECIMAL(10, 2), comment='每股经营活动产生的现金流量净额 [ 元 ]')
    mglcsy = Column(DECIMAL(10, 2), comment='每股留存收益 [ 元 ]')
    mgyygj = Column(DECIMAL(10, 2), comment='每股盈余公积 [ 元 ]')
    mgyysr = Column(DECIMAL(10, 2), comment='每股营业收入 [ 元 ]')
    mgyyzsr = Column(DECIMAL(10, 2), comment='每股营业总收入 [ 元 ]')
    xsjll = Column(DECIMAL(10, 2), comment='销售净利率 [ % ]')
    mll = Column(DECIMAL(10, 2), comment='毛利率 [ % ]')
    yfzkzzl = Column(DECIMAL(10, 2), comment='应付账款周转率 [不含应付票据] [ % ]')
    chzzl = Column(DECIMAL(10, 2), comment='存货周转率 [ % ]')
    yyzq = Column(DECIMAL(10, 2), comment='营业周期 [ 天 ]')
    yfzkzzts = Column(DECIMAL(10, 2), comment='应付账款周转天数 [不含应付票据] [ 天 ]')
    zzcbcl = Column(DECIMAL(10, 2), comment='总资产报酬率 [ % ]')
    zzczzl = Column(DECIMAL(10, 2), comment='总资产周转率 [ % ]')
    chzzts = Column(DECIMAL(10, 2), comment='存货周转天数 [ 天 ]')
    cqbl = Column(DECIMAL(10, 2), comment='产权比率 [ % ]')
    ldbl = Column(DECIMAL(10, 2), comment='流动比率 [ % ]')
    sdbl = Column(DECIMAL(10, 2), comment='速动比率 [ % ]')
    cfotonetlibility = Column(DECIMAL(10, 2), comment='经营活动产生的现金流量净额/净债务 [ % ]')
    nonoperateprofittoebt = Column(DECIMAL(10, 2), comment='营业外收支净额/利润总额 [ % ]')
    lrzehb = Column(DECIMAL(10, 2), comment='利润总额环比增长率 [ % ]')
    jzctb = Column(DECIMAL(10, 2), comment='净资产同比增长率 [ % ]')
    zzctb = Column(DECIMAL(10, 2), comment='总资产同比增长率 [ % ]')
    jzcsyl_1y = Column(DECIMAL(10, 2), comment='1年净资产收益率 [ % ]')
    jzcsyl_2y = Column(DECIMAL(10, 2), comment='2年净资产收益率 [ % ]')
    jzcsyl_3y = Column(DECIMAL(10, 2), comment='3年净资产收益率 [ % ]')
    xssjl = Column(DECIMAL(10, 2), comment='销售税金率 [ % ]')
    yylrl = Column(DECIMAL(10, 2), comment='营业利润率 [ % ]')
    jlrxjhl = Column(DECIMAL(10, 2), comment='净利润现金含量 [ % ]')
    gdzcbl = Column(DECIMAL(10, 2), comment='固定资产比率 [ % ]')
    csdbl = Column(DECIMAL(10, 2), comment='超速动比率 [ % ]')
    wxzcbl = Column(DECIMAL(10, 2), comment='无形资产比率 [ % ]')
    yxjzzwl = Column(DECIMAL(10, 2), comment='有形净值债务率 [ % ]')
    cqfzyyyzjbl = Column(DECIMAL(10, 2), comment='长期负债与营运资金比率 [ % ]')
    cqfzyzczjzb = Column(DECIMAL(10, 2), comment='长期负债与资产总计之比 [ % ]')
    roebdl = Column(DECIMAL(10, 2), comment='净资产收益率波动率 [ % ]')
    mlrhb = Column(DECIMAL(10, 2), comment='毛利润环比增长率 [ % ]')
    zchbl_1y = Column(DECIMAL(10, 2), comment='1年资产回报率 [ % ]')
    zchbl_2y = Column(DECIMAL(10, 2), comment='2年资产回报率 [ % ]')
    zchbl_3y = Column(DECIMAL(10, 2), comment='3年资产回报率 [ % ]')
    kfjzcsyl = Column(DECIMAL(10, 2), comment='扣非净资产收益率 [ % ]')
    czhdcsdxjlljetb = Column(DECIMAL(20, 2), comment='筹资活动产生的现金流量净额同比增长率 [ % ]')
    ldzczzl_ttm = Column(DECIMAL(10, 2), comment='流动资产周转率TTM [ % ]')
    report_date = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CaiwuInfoTradedate(Base):
    __tablename__ = 'caiwu_info_tradedate'
    __table_args__ = (
        Index('uk_code_date', 'stockcode', 'trade_date', unique=True),
        {'comment': '财务信息表_交易日'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    stockcode = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    stockname = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    zgb = Column(BIGINT(20), comment='总股本 [ 元 ]')
    ltgb = Column(BIGINT(20), comment='流通股本 [ 元 ]')
    ltsz = Column(DECIMAL(15, 2), comment='流通市值 [ 按股东权益修正 ] [ 元 ]')
    zsz = Column(DECIMAL(20, 2), comment='总市值 [ 元 ]')
    sjl = Column(DECIMAL(10, 2), comment='市净率 [ % ]')
    pjzc = Column(DECIMAL(10, 2), comment='破净资产 [ % ]')
    bp = Column(DECIMAL(10, 2), comment='BP [ % ]')
    syl = Column(DECIMAL(10, 2), comment='市盈率 [ % ]')
    ep = Column(DECIMAL(10, 2), comment='EP [ % ]')
    syl_ttm = Column(DECIMAL(10, 2), comment='市盈率TTM [ % ]')
    sxl = Column(DECIMAL(10, 2), comment='市销率 [ % ]')
    sxl_ttm = Column(DECIMAL(10, 2), comment='市销率TTM [ % ]')
    gxl = Column(DECIMAL(10, 2), comment='股息率 [ % ]')
    mgsy_ttm = Column(DECIMAL(10, 2), comment='每股收益TTM [ 元 ]')
    mgxjllje_ttm = Column(DECIMAL(10, 2), comment='每股现金流量净额TTM [ 元 ]')
    mgyysr_ttm = Column(DECIMAL(10, 2), comment='每股营业收入TTM [ 元 ]')
    cfotooperateincome_ttm = Column(DECIMAL(10, 2), comment='经营活动产生的现金流量净额/经营活动净收益TTM [ % ]')
    nitogr_ttm = Column(DECIMAL(10, 2), comment='净利润/营业总收入TTM [ % ]')
    roe_ttm = Column(DECIMAL(10, 0), comment='净资产收益率TTM [ % ]')
    operateexpensetogr_ttm = Column(DECIMAL(10, 2), comment='财务费用/营业总收入TTM [ % ]')
    mggx = Column(DECIMAL(10, 2), comment='每股股息 [ 元 ]')
    mgyyzsr_ttm = Column(DECIMAL(10, 2), comment='每股营业总收入TTM [ 元 ]')
    mgxjjdjwye = Column(DECIMAL(10, 2), comment='每股现金及现金等价物余额 [ 元 ]')
    mgyylr_ttm = Column(DECIMAL(10, 2), comment='每股营业利润TTM [ 元 ]')
    jyhd_ttm = Column(DECIMAL(10, 2), comment='经营活动产生的现金流量净额与企业价值之比TTM [ % ]')
    scgg = Column(DECIMAL(10, 2), comment='市场杠杆')
    zzcxjhsl = Column(DECIMAL(10, 2), comment='总资产现金回收率 [ % ]')
    trade_date = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
