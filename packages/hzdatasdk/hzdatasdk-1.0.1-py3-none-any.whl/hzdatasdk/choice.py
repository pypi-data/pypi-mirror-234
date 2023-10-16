# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CsdHsGzzbLtsz(Base):
    __tablename__ = 'csd_hs_gzzb_ltsz'
    __table_args__ = (
        Index('uk_code_time', 'CODE', 'INFOTIME', unique=True),
        {'comment': '沪深股票_估值指标_个股流通市值数据表'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    EQUITYADJLIQMV = Column(DECIMAL(15, 2), nullable=False, server_default=text("'0.00'"), comment='流通市值 [ 按股东权益修正 ]')
    INFOTIME = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CsdHsHqzbBak(Base):
    __tablename__ = 'csd_hs_hqzb.bak'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'YEAR', unique=True),
        {'comment': '历史行情_行情指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    YEAR = Column(INTEGER(11), comment='年份')
    OPEN = Column(DECIMAL(6, 2), comment='开盘价')
    CLOSE = Column(DECIMAL(6, 2), comment='收盘价')
    HIGH = Column(DECIMAL(6, 2), comment='最高价')
    LOW = Column(DECIMAL(6, 2), comment='最低价')
    CHANGE1 = Column(DECIMAL(6, 2), comment='涨跌CHANGE')
    PCTCHANGE = Column(DECIMAL(11, 6), comment='涨跌幅')
    VOLUME = Column(BIGINT(15), comment='成交量')
    AMOUNT = Column(DECIMAL(18, 2), comment='成交金额')
    TURN = Column(DECIMAL(11, 6), comment='换手率')
    AMPLITUDE = Column(DECIMAL(11, 6), comment='振幅')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CsdHsZjlxZljlr(Base):
    __tablename__ = 'csd_hs_zjlx_zljlr'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'Date', unique=True),
        {'comment': '个股主力净流入资金信息表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    NETINFLOW = Column(DECIMAL(15, 1), comment='(日)主力净流入资金')
    Date = Column(INTEGER(11), nullable=False, comment='交易日')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsBbfzYfzc(Base):
    __tablename__ = 'css_hs_bbfz_yfzc'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '沪深股票指标_报表附注_研发支出'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    RDEXPENDALL = Column(DECIMAL(20, 2), comment='研发支出合计')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwbbXjllbJyhdcsdxjll(Base):
    __tablename__ = 'css_hs_cwbb_xjllb_jyhdcsdxjll'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务报表_现金流量表_经营活动产生的现金流量'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    CASHFLOWSTATEMENT39 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='经营活动产生的现金流量净额')
    CASHFLOWSTATEMENT77 = Column(DECIMAL(20, 2), comment='筹资活动产生的现金流量净额')
    CASHFLOWSTATEMENT84 = Column(DECIMAL(20, 2), comment='期末现金及现金等价物余额')
    CASHFLOWSTATEMENT11 = Column(DECIMAL(20, 2), comment='收到其他与经营活动有关的现金')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwbbYbqyLrb(Base):
    __tablename__ = 'css_hs_cwbb_ybqy_lrb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务报表_一般企业_利润表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    INCOMESTATEMENT9 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='营业收入')
    INCOMESTATEMENT83 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='营业总收入')
    INCOMESTATEMENT80 = Column(DECIMAL(8, 4), nullable=False, server_default=text("'0.0000'"), comment='基本每股收益')
    INCOMESTATEMENT60 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='净利润')
    INCOMESTATEMENT61 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='归属于母公司股东的净利润')
    INCOMESTATEMENT10 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='营业成本')
    INCOMESTATEMENT55 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='利润总额')
    INCOMESTATEMENT19 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='利息收入')
    INCOMESTATEMENT20 = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='利息支出')
    INCOMESTATEMENTQ_89 = Column(DECIMAL(20, 2), nullable=False, comment='单季度.研发费用')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwbbYbqyZcfzb(Base):
    __tablename__ = 'css_hs_cwbb_ybqy_zcfzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务报表_一般企业_资产负债表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    BALANCESTATEMENT_141 = Column(DECIMAL(20, 4), nullable=False, server_default=text("'0.0000'"), comment='股东权益合计')
    BALANCESTATEMENT_78 = Column(DECIMAL(24, 4), comment='应付账款')
    BALANCESTATEMENT_77 = Column(DECIMAL(24, 4), comment='应付票据')
    BALANCESTATEMENT_14 = Column(DECIMAL(24, 4), comment='预付款项')
    BALANCESTATEMENT_140 = Column(DECIMAL(24, 4), comment='归属于母公司股东权益合计')
    BALANCESTATEMENT_31 = Column(DECIMAL(24, 4), comment='固定资产')
    BALANCESTATEMENT_32 = Column(DECIMAL(24, 4), comment='工程物资')
    BALANCESTATEMENT_33 = Column(DECIMAL(24, 4), comment='在建工程')
    BALANCESTATEMENT_9 = Column(DECIMAL(24, 4), comment='货币资金')
    BALANCESTATEMENT_224 = Column(DECIMAL(24, 4), comment='交易性金融资产')
    BALANCESTATEMENT_11 = Column(DECIMAL(24, 4), comment='应收票据')
    BALANCESTATEMENT_12 = Column(DECIMAL(24, 4), comment='应收账款')
    BALANCESTATEMENT_222 = Column(DECIMAL(24, 4), comment='其他应收款项合计')
    BALANCESTATEMENT_93 = Column(DECIMAL(24, 4), comment='流动负债合计')
    BALANCESTATEMENT_103 = Column(DECIMAL(24, 4), comment='非流动负债合计')
    BALANCESTATEMENT_25 = Column(DECIMAL(24, 4), comment='流动资产合计')
    BALANCESTATEMENT_37 = Column(DECIMAL(24, 4), comment='无形资产')
    BALANCESTATEMENT_128 = Column(DECIMAL(24, 4), comment='负债合计')
    BALANCESTATEMENT_21 = Column(DECIMAL(24, 4), comment='其他流动资产')
    BALANCESTATEMENT_74 = Column(DECIMAL(24, 4), comment='资产总计')
    BALANCESTATEMENT_39 = Column(DECIMAL(24, 4), comment='商誉')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxBgqttm(Base):
    __tablename__ = 'css_hs_cwfx_bgqttm'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_衍生报表数据'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    NPTTMRP = Column(DECIMAL(20, 4), server_default=text("'0.0000'"), comment='净利润TTM')
    GRTTMR = Column(DECIMAL(20, 4), comment='营业总收入TTM')
    BTAATTMRP = Column(DECIMAL(20, 4), comment='营业税金及附加TTM')
    EBTTTMR = Column(DECIMAL(20, 4), comment='利润总额TTM')
    OPTTMR = Column(DECIMAL(20, 4), comment='营业利润TTM')
    FINAEXPENSETTMR = Column(DECIMAL(20, 4), comment='财务费用TTM')
    GCTTMR = Column(DECIMAL(20, 4), comment='营业总成本TTM')
    OPERATEEXPENSETTMR = Column(DECIMAL(20, 4), comment='销售费用TTM')
    NETLIBILITY = Column(DECIMAL(20, 4), comment='净债务')
    CFTTMR = Column(DECIMAL(20, 4), comment='现金净流量TTM')
    ORTTMR = Column(DECIMAL(20, 4), comment='营业收入TTM')
    EXTRAORDINARY = Column(DECIMAL(20, 4), comment='非经常性损益')
    KCFJCXSYJLRTTMR = Column(DECIMAL(20, 4), comment='扣除非经常性损益净利润TTM')
    PNITTMR = Column(DECIMAL(20, 4), comment='归属母公司股东的净利润TTM')
    CFOTTMR = Column(DECIMAL(20, 4), comment='经营活动现金净流量TTM')
    CAPEXR = Column(DECIMAL(20, 4), comment='资本支出TTM')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxCznl(Base):
    __tablename__ = 'css_hs_cwfx_cznl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_偿债能力_产权比率'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    LIBILITYTOEQUITY = Column(DECIMAL(20, 4), server_default=text("'0.0000'"), comment='产权比率')
    CURRENTTATIO = Column(DECIMAL(10, 2), comment='流动比率')
    QUICKTATIO = Column(DECIMAL(10, 2), comment='速动比率')
    CFOTONETLIBILITY = Column(DECIMAL(12, 2), comment='经营活动产生的现金流量净额/净债务')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxCznlNnzzl(Base):
    __tablename__ = 'css_hs_cwfx_cznl_nnzzl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_成长能力_N年增长率'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    NYGROWTHRATEROE1Y = Column(DECIMAL(10, 2), server_default=text("'0.00'"), comment='1年净资产收益率')
    NYGROWTHRATEROE2Y = Column(DECIMAL(10, 2), comment='2年净资产收益率')
    NYGROWTHRATEROE3Y = Column(DECIMAL(10, 2), comment='3年净资产收益率')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxCznlTbzzl(Base):
    __tablename__ = 'css_hs_cwfx_cznl_tbzzl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_成长能力_同比增长率'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    YOYOR = Column(DECIMAL(13, 6), server_default=text("'0.000000'"), comment='营业收入同比增长率')
    YOYNI = Column(DECIMAL(14, 6), server_default=text("'0.000000'"), comment='净利润同比增长率')
    YOYGR = Column(DECIMAL(13, 6), comment='营业总收入同比增长率')
    YOYEQUITY = Column(DECIMAL(14, 6), comment='净资产同比增长率')
    YOYASSET = Column(DECIMAL(14, 6), comment='总资产同比增长率')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxDjdcwzb(Base):
    __tablename__ = 'css_hs_cwfx_djdcwzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '沪深股票指标_财务分析_单季度财务指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    QDEDUCTEDPROFIT = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='扣除非经常损益后的净利润')
    QCGRNI = Column(DECIMAL(10, 2), comment='净利润环比增长率')
    QQOQOR = Column(DECIMAL(10, 2), comment='营业收入环比增长率')
    QQOQGPMARGIN = Column(DECIMAL(10, 2), comment='毛利率环比增长率')
    QCGRPNI = Column(DECIMAL(10, 2), comment='归属母公司股东的净利润环比增长率')
    QQOQCFO = Column(DECIMAL(24, 2), comment='经营活动产生的现金流量净额环比增长率')
    QQOQOP = Column(DECIMAL(10, 2), comment='营业利润环比增长率')
    QQOQEBT = Column(DECIMAL(10, 2), comment='利润总额环比增长率')
    QYOYCFO = Column(DECIMAL(24, 2), comment='经营活动产生的现金流量净额同比增长率')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxMgzb(Base):
    __tablename__ = 'css_hs_cwfx_mgzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_每股指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    BPS = Column(DECIMAL(10, 6), server_default=text("'0.000000'"), comment='每股净资产BPS')
    CAPITALRESERVEPS = Column(DECIMAL(15, 6), server_default=text("'0.000000'"), comment='每股资本公积')
    UNDISTRIBUTEDPS = Column(DECIMAL(9, 6), server_default=text("'0.000000'"), comment='每股未分配利润')
    CFOPS = Column(DECIMAL(15, 2), comment='每股经营活动产生的现金流量净额')
    RETAINEDPS = Column(DECIMAL(15, 2), comment='每股留存收益')
    CFPS = Column(DECIMAL(15, 2), comment='每股现金流量净额')
    SURPLUSRESERVEPS = Column(DECIMAL(15, 2), comment='每股盈余公积')
    ORPS = Column(DECIMAL(15, 2), comment='每股营业收入')
    GRPS = Column(DECIMAL(15, 2), comment='每股营业总收入')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxMgzbMgsyttm(Base):
    __tablename__ = 'css_hs_cwfx_mgzb_mgsyttm'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '财务分析_每股指标_每股收益TTM'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    EPSTTM = Column(DECIMAL(16, 6), server_default=text("'0.000000'"), comment='每股收益TTM')
    CFOPSTTM = Column(DECIMAL(16, 4), comment='每股经营活动产生的现金流量净额(TTM)')
    CFPSTTM = Column(DECIMAL(16, 4), comment='每股现金流量净额(TTM)')
    ORPSTTM = Column(DECIMAL(16, 4), comment='每股营业收入(TTM)')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxSyzl(Base):
    __tablename__ = 'css_hs_cwfx_syzl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '沪深股票指标_财务分析_收益质量'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NONOPERATEPROFITTOEBT = Column(DECIMAL(20, 2), comment='营业外收支净额/利润总额')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxXjllTtm(Base):
    __tablename__ = 'css_hs_cwfx_xjll_ttm'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '财务分析_现金流量_经营活动产生的现金流量净额/经营活动净收益(TTM)'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    CFOTOOPERATEINCOMETTM = Column(DECIMAL(12, 2), server_default=text("'0.00'"), comment='经营活动产生的现金流量净额/经营活动净收益(TTM)')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxYlnl(Base):
    __tablename__ = 'css_hs_cwfx_ylnl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_盈利能力'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    CODENAME = Column(String(255), comment='股票名称')
    ROEWA = Column(DECIMAL(16, 6), server_default=text("'0.000000'"), comment='净资产收益率ROE(加权)')
    NPMARGIN = Column(DECIMAL(12, 6), server_default=text("'0.000000'"), comment='净利率')
    GPMARGIN = Column(DECIMAL(12, 6), server_default=text("'0.000000'"), comment='毛利率')
    ANNUROE = Column(DECIMAL(7, 2), comment='年化净资产收益率')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxYlnlJzcsylttm(Base):
    __tablename__ = 'css_hs_cwfx_ylnl_jzcsylttm'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '财务分析_盈利能力_净资产收益率TTM'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    ROETTM = Column(DECIMAL(16, 6), server_default=text("'0.000000'"), comment='净资产收益率TTM')
    GPMARGINTTM = Column(DECIMAL(16, 6), comment='销售毛利率(TTM)')
    NITOGRTTM = Column(DECIMAL(12, 2), comment='净利润/营业总收入(TTM) ')
    OPERATEEXPENSETOGRTTM = Column(DECIMAL(12, 2), comment='销售费用/营业总收入(TTM)')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxYynl(Base):
    __tablename__ = 'css_hs_cwfx_yynl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_营运能力'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    ASSETTURNRATIO = Column(DECIMAL(10, 6), server_default=text("'0.000000'"), comment='总资产周转率')
    INVTURNRATIO = Column(DECIMAL(12, 6), server_default=text("'0.000000'"), comment='存货周转率')
    TURNDAYS = Column(DECIMAL(12, 2), comment='营业周期')
    APTURNDAYSNONP = Column(DECIMAL(12, 2), comment='应付账款周转天数(不含应付票据)')
    INVTURNDAYS = Column(DECIMAL(12, 2), comment='存货周转天数')
    APTURNRATIONONP = Column(DECIMAL(12, 2), comment='应付账款周转率(不含应付票据)')
    ROA = Column(DECIMAL(12, 2), comment='总资产报酬率')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsCwfxZbjg(Base):
    __tablename__ = 'css_hs_cwfx_zbjg'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '财务分析_资本结构'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    LIBILITYTOASSET = Column(DECIMAL(15, 6), nullable=False, server_default=text("'0.000000'"), comment='资产负债率')
    NCATOASSET = Column(DECIMAL(12, 2), nullable=False, server_default=text("'0.00'"), comment='非流动资产/总资产 [ 非流动资产比率 ]')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsFhzbFhzb(Base):
    __tablename__ = 'css_hs_fhzb_fhzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'Payyear', unique=True),
        {'comment': '沪深股票指标-分红指标-分红指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    DIVANNUACCUM = Column(DECIMAL(20, 2), comment='年度累计分红总额')
    Payyear = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='年度')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsFxfxZdycszb(Base):
    __tablename__ = 'css_hs_fxfx_zdycszb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '风险分析_自定义参数指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    STDEV = Column(DECIMAL(12, 2), comment='波动率')
    BETA = Column(DECIMAL(12, 2), comment='Beta')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGbzbGbbd(Base):
    __tablename__ = 'css_hs_gbzb_gbbd'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '股本变动数据表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    TOTALSHARE = Column(BIGINT(20), comment='总股本')
    LIQASHARE = Column(BIGINT(20), comment='流通A股')
    LIQBSHARE = Column(BIGINT(20), comment=' 流通B股')
    SHARECHANGEDATE = Column(INTEGER(11), comment='股本变动时间')
    SHARECHANGECAUSE = Column(String(100), comment='股本变动原因')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGbzbGbbdBak(Base):
    __tablename__ = 'css_hs_gbzb_gbbd_bak'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '股本变动数据表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    TOTALSHARE = Column(BIGINT(20), comment='总股本')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbBgqgdhszb(Base):
    __tablename__ = 'css_hs_gdzb_bgqgdhszb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '沪深股票指标_股东指标_股东户数指标_报告期股东户数指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    STMTHOLDNUM = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='股东人数 [ 户 ]')
    STMTHOLDAVGNUM = Column(DECIMAL(15, 4), nullable=False, server_default=text("'0.0000'"), comment='户均持股数量 [ 股/户 ]')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbGdggzjc(Base):
    __tablename__ = 'css_hs_gdzb_gdggzjc'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '沪深股票_股东指标_股东高管增减持'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    HOLDEXCHGNUM = Column(DECIMAL(14, 2), nullable=False, server_default=text("'0.00'"), comment='高管变动股数合计 [ 股 ]')
    HOLDEXCHGRATE = Column(DECIMAL(5, 2), nullable=False, server_default=text("'0.00'"), comment='高管变动股数占流通股比例 [ % ]')
    DECRENEWMAXSHANUM = Column(DECIMAL(16, 2), comment='最新计划减持股份数量上限 [ 股 ]')
    DECRENEWMINSHANUM = Column(DECIMAL(16, 2), comment='最新计划减持股份数量下限 [ 股 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间 [ 最新大股东减持公告日期(计划) ]')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbGqzy(Base):
    __tablename__ = 'css_hs_gdzb_gqzy'
    __table_args__ = {'comment': '股东指标_股权质押'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    PLEDGERATIO = Column(DECIMAL(5, 2), comment='质押比例')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbHgtgzcg(Base):
    __tablename__ = 'css_hs_gdzb_hgtgzcg'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '沪深股票_股东指标_沪（深）港通港资持股数据表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    NAME = Column(String(10), nullable=False, comment='股票名称')
    SHAREHDNUM = Column(DECIMAL(16, 2), nullable=False, server_default=text("'0.00'"), comment='持股数量 [ 股 ]')
    SHAREHDPCT = Column(DECIMAL(16, 2), nullable=False, server_default=text("'0.00'"), comment='持股比例 [ % ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbJgcgbl(Base):
    __tablename__ = 'css_hs_gdzb_jgcgbl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'REPORTDATE', unique=True),
        {'comment': '沪深股票指标_股东指标_机构持股指标_机构持股比例'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    HOLDPCTBYFUND = Column(DECIMAL(10, 4), nullable=False, server_default=text("'0.0000'"), comment='基金持股比例 [ % ]')
    HOLDPCTBYSSFUND = Column(DECIMAL(10, 4), nullable=False, server_default=text("'0.0000'"), comment='社保基金持股比例 [ % ]')
    HOLDPCTBYQFII = Column(DECIMAL(10, 4), nullable=False, server_default=text("'0.0000'"), comment='QFII持股比例 [ % ]')
    REPORTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGdzbSdgd(Base):
    __tablename__ = 'css_hs_gdzb_sdgd'
    __table_args__ = {'comment': '股东指标_十大股东/十大流通股东信息表'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    NAME = Column(String(15), nullable=False, comment='股票名称')
    SHAREHOLDNAME = Column(String(255), comment='股东名称')
    SHAREHOLDTYPE = Column(TINYINT(4), comment='股东类型 [ 1: 十大股东    2: 十大流通股东 ]')
    SHAREHOLDRANK = Column(INTEGER(11), comment='股东排名')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
    identity = Column(String(34), nullable=False, unique=True, server_default=text("''"), comment='唯一键 [ 爬虫去重用 ]')


class CssHsGpzbFhzb(Base):
    __tablename__ = 'css_hs_gpzb_fhzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'DIVEXDATE', unique=True),
        {'comment': '分红送股信息表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    DIVCASHPSBFTAX = Column(DECIMAL(8, 6), comment='每股股利(税前)')
    DIVSTOCKPS = Column(DECIMAL(8, 6), comment='每股红股(送股)')
    DIVCAPITALIZATIONPS = Column(DECIMAL(8, 6), comment='每股转增股本(转股)')
    DIVRECORDDATE = Column(INTEGER(11), nullable=False, comment='股权登记日')
    DIVEXDATE = Column(INTEGER(11), nullable=False, comment='除权除息日')
    DIVCASHANDSTOCKPS = Column(String(255), nullable=False, server_default=text("''"), comment='分红送转')
    DIVPAYDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='派息日')
    DIVBONUSLISTEDDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='送转股份上市交易日')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGpzbPgzb(Base):
    __tablename__ = 'css_hs_gpzb_pgzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'RTISSEXDIVDATE', unique=True),
        {'comment': '配股指标信息表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    RTISSPERTISSHARE = Column(DECIMAL(10, 6), nullable=False, server_default=text("'0.000000'"), comment='每股配股数')
    RTISSREGISTDATE = Column(INTEGER(11), nullable=False, comment='股权登记日')
    RTISSEXDIVDATE = Column(INTEGER(11), nullable=False, comment='配股除权日')
    RTISSPRICE = Column(DECIMAL(6, 2), nullable=False, server_default=text("'0.00'"), comment='配股价格')
    RTISSLISTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='配股上市日')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGpzbZfzb(Base):
    __tablename__ = 'css_hs_gpzb_zfzb'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'FELLOWLISTEDDATE', unique=True),
        {'comment': '增发指标相关数据表'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    FELLOWVOL = Column(DECIMAL(12, 2), nullable=False, server_default=text("'0.00'"), comment='增发数量（股）')
    FELLOWPRICE = Column(DECIMAL(7, 2), nullable=False, server_default=text("'0.00'"), comment='增发价格（元/股）')
    FELLOWTOTALSHAREBF = Column(DECIMAL(15, 2), nullable=False, server_default=text("'0.00'"), comment='增发前股本（元）')
    FELLOWTOTALSHAREAF = Column(DECIMAL(15, 2), nullable=False, server_default=text("'0.00'"), comment='增发后股本（元）')
    FELLOWLISTEDDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='增发上市日')
    FELLOWREGISTDATE = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='增发股权登记日')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsGzzbBkhcgz(Base):
    __tablename__ = 'css_hs_gzzb_bkhcgz'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'tradday', unique=True),
        {'comment': '估值指标_不可回测估值'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    MV = Column(DECIMAL(20, 4), comment='总市值')
    PETTM = Column(DECIMAL(11, 4), comment='市盈率TTM')
    PB = Column(DECIMAL(10, 4), comment='市净率')
    FREEFLOATMV = Column(DECIMAL(20, 4), comment='自由流通市值')
    DIVIDENDYIELD = Column(DECIMAL(5, 2), comment='股息率(股票获利率)')
    PE = Column(DECIMAL(12, 2), comment='市盈率')
    PSTTM = Column(DECIMAL(12, 2), comment='市销率TTM')
    PS = Column(DECIMAL(12, 2), comment='市销率')
    EVWITHOUTCASH = Column(DECIMAL(20, 2), comment='企业价值(剔除货币资金)')
    tradday = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsHqzbQjhq(Base):
    __tablename__ = 'css_hs_hqzb_qjhq'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '行情指标_区间行情'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    AVGTURNP = Column(DECIMAL(8, 4), nullable=False, server_default=text("'0.0000'"), comment='区间日均换手率')
    DIFFERRANGEN = Column(DECIMAL(10, 4), nullable=False, server_default=text("'0.0000'"), comment='20日涨跌幅 [ % ]')
    AMOUNTN = Column(DECIMAL(18, 4), nullable=False, server_default=text("'0.0000'"), comment='20日成交额 [ 元 ]')
    TURNN = Column(DECIMAL(10, 4), nullable=False, server_default=text("'0.0000'"), comment='20日换手率 [ % ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='交易日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsHqzbRzrq(Base):
    __tablename__ = 'css_hs_hqzb_rzrq'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '沪深股票指标_行情指标_融资融券相关数据'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='股票名称')
    FINBALANCE = Column(DECIMAL(16, 2), nullable=False, server_default=text("'0.00'"), comment='融资余额 [ 元 ]')
    FINPURCH = Column(DECIMAL(16, 2), nullable=False, server_default=text("'0.00'"), comment='融资买入额 [ 元 ]')
    FINPMT = Column(DECIMAL(16, 2), nullable=False, server_default=text("'0.00'"), comment='融资偿还额 [ 元 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsJbzlZqzlDate(Base):
    __tablename__ = 'css_hs_jbzl_zqzl_date'
    __table_args__ = {'comment': '基本资料_证券资料_上市/摘牌日期'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, unique=True, comment='股票代码')
    NAME = Column(String(10), nullable=False, comment='股票名称')
    LISTDATE = Column(INTEGER(11), comment='首发上市日期')
    DELISTDATE = Column(INTEGER(11), comment='摘牌日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsJgdyzbGgrqjgdyzb(Base):
    __tablename__ = 'css_hs_jgdyzb_ggrqjgdyzb'
    __table_args__ = (
        Index('uk_code_type_date', 'CODE', 'TYPE', 'TradeDate', unique=True),
        {'comment': '机构调研指标_按公告日期机构调研指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    RESERCHINSTITUTENUMN = Column(INTEGER(11), comment='机构来访接待量')
    TYPE = Column(TINYINT(4), comment='时间范围 [ 1：近5个交易日   2：近一月 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsLbBak(Base):
    __tablename__ = 'css_hs_lb.bak'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '沪深_历史行情_行情指标'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    TradeDate = Column(INTEGER(11), comment='交易日')
    VOLRATIO = Column(DECIMAL(11, 6), comment='量比')
    TURN = Column(DECIMAL(11, 6), comment='换手率')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsQqYhbdl(Base):
    __tablename__ = 'css_hs_qq_yhbdl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '上交所300ETF股票期权当月/下月到期期权相关信息'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(20), nullable=False, server_default=text("''"), comment='期权代码')
    NAME = Column(String(25), nullable=False, server_default=text("''"), comment='期权名称')
    SECURITYCODE = Column(String(30), nullable=False, server_default=text("''"), comment='合约交易代码')
    CLOSE = Column(DECIMAL(10, 4), comment='收盘价')
    OI = Column(BIGINT(20), nullable=False, server_default=text("'0'"), comment='持仓量')
    EMPTMDAYS = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='剩余期限 [ 天 ]')
    EMBLSIMPV = Column(DECIMAL(10, 4), comment='隐含波动率 [ % ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsSfzbSfssbx(Base):
    __tablename__ = 'css_hs_sfzb_sfssbx'
    __table_args__ = {'comment': '首发指标_首发上市表现'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    IPOLSTDAYS = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='上市天数')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycOrgInfo(Base):
    __tablename__ = 'css_hs_ylyc_org_info'
    __table_args__ = {'comment': '盈利预测_机构相关信息表'}

    OrgId = Column(INTEGER(11), primary_key=True, server_default=text("'0'"), comment='机构代码')
    OrgName = Column(String(15), nullable=False, server_default=text("''"), comment='机构名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycSsgsyjyg(Base):
    __tablename__ = 'css_hs_ylyc_ssgsyjyg'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'PROFITNOTICEDATE', unique=True),
        {'comment': '盈利预测_上市公司业绩预告'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, comment='股票代码')
    NAME = Column(String(255), comment='股票名称')
    PROFITNOTICESTYLE = Column(String(255), nullable=False, server_default=text("''"), comment='业绩预告类型')
    PROFITNOTICEABSTRACT = Column(String(255), nullable=False, server_default=text("''"), comment='业绩预告摘要')
    PROFITNOTICEDATE = Column(INTEGER(11), nullable=False, comment='业绩预告日期')
    PROFITNOTICELASTESTREPORTDATE = Column(INTEGER(11), nullable=False, comment='业绩预告最新报告期')
    PROFITNOTICEFORECASTL = Column(DECIMAL(15, 2), comment='预告归属于母公司的净利润下限')
    PROFITNOTICECHGPCTL = Column(DECIMAL(12, 3), comment='预告归属于母公司的净利润增长下限(%)')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycSwhyOrgInfo(Base):
    __tablename__ = 'css_hs_ylyc_swhy_org_info'
    __table_args__ = (
        Index('uk_id_code', 'SwhyCode', 'OrgId', unique=True),
        {'comment': '盈利预测_机构与申万行业关联信息表'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增id')
    SwhyCode = Column(String(20), nullable=False, server_default=text("''"), comment='申万行业代码')
    SwhyName = Column(String(10), nullable=False, server_default=text("''"), comment='申万行业名称')
    OrgId = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='机构代码')
    OrgName = Column(String(15), nullable=False, server_default=text("''"), comment='机构名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycTzpjzhz(Base):
    __tablename__ = 'css_hs_ylyc_tzpjzhz'
    __table_args__ = (
        Index('uk_code_date_type', 'CODE', 'TradeDate', 'DateType', unique=True),
        {'comment': '盈利预测_投资评级综合值'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    WRATINGNUMOFBUY = Column(INTEGER(11), comment='评级买入家数 [ 家 ]')
    WRATINGNUMOFOUTPERFORM = Column(INTEGER(11), comment='评级增持家数 [ 家 ]')
    WRATINGNUMOFHOLD = Column(INTEGER(11), comment='评级中性家数 [ 家 ]')
    WRATINGNUMOFUNDERPERFORM = Column(INTEGER(11), comment='评级减持家数 [ 家 ]')
    WRATINGNUMOFSELL = Column(INTEGER(11), comment='评级卖出家数 [ 家 ]')
    WRATINGAVG = Column(DECIMAL(6, 3), comment='综合评级 [ 数值 ]')
    DateType = Column(TINYINT(4), nullable=False, server_default=text("'0'"),
                      comment='综合值周期 [ 0：默认    1：90日    2：180日 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycYcyplmxz(Base):
    __tablename__ = 'css_hs_ylyc_ycyplmxz'
    __table_args__ = (
        Index('uk_code_date_orgid', 'CODE', 'OrgId', 'TradeDate', unique=True),
        {'comment': '盈利预测_预测与评级明细值'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    ESTSCORERATINGINST = Column(DECIMAL(8, 2), comment='机构投资评级(标准化得分)')
    ESTPRESCORERATINGINST = Column(DECIMAL(8, 2), comment='前次机构投资评级(标准化得分)')
    ESTNEWRATINGDATEINST = Column(INTEGER(11), comment='机构最近评级时间')
    OrgId = Column(INTEGER(11), comment='机构ID')
    OrgName = Column(String(50), comment='机构名称')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycYcyplmxzYbsl(Base):
    __tablename__ = 'css_hs_ylyc_ycyplmxz_ybsl'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '盈利预测_预测与评级明细值_研究报告数量'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    REPORTNUM = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='研报数量')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycYlyczhz(Base):
    __tablename__ = 'css_hs_ylyc_ylyczhz'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '盈利预测_盈利预测综合值'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(15), nullable=False, server_default=text("''"), comment='股票名称')
    ESTINSTNUM = Column(INTEGER(11), comment='每股收益预测机构家数 [ 家 ]')
    ESTAVGOP = Column(DECIMAL(20, 2), comment='预测营业利润平均值 [ 元 ]')
    ESTYOYSALES = Column(DECIMAL(8, 2), comment='预测营业总收入增长率 [ % ]')
    ESTEPS = Column(DECIMAL(12, 2), comment='预测每股收益平均值 [ 元 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsYlycYlyczhzGd(Base):
    __tablename__ = 'css_hs_ylyc_ylyczhz_gd'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '盈利预测_盈利预测综合值（滚动）'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='股票代码')
    NAME = Column(String(20), nullable=False, server_default=text("''"), comment='股票名称')
    SESTNIF12 = Column(DECIMAL(20, 3), comment=' 一致预测归属母公司净利润(未来12个月) [ 元 ]')
    SESTGRFY1 = Column(DECIMAL(20, 3), comment='一致预测总营业收入(FY1) [ 元 ]')
    SESTGRYOY = Column(DECIMAL(10, 3), comment='一致预测总营业收入(同比) [ % ]')
    SESTNIYOY = Column(DECIMAL(10, 3), comment='一致预测归属母公司净利润同比 [ % ]')
    SESTROEYOY = Column(DECIMAL(10, 3), comment='一致预测ROE(同比) [ % ]')
    SESTROEFY1 = Column(DECIMAL(10, 3), comment='一致预测ROE(FY1) [ % ]')
    TradeDate = Column(INTEGER(11), nullable=False, comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssHsZcfzFldzc(Base):
    __tablename__ = 'css_hs_zcfz_fldzc'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'ReportDate', unique=True),
        {'comment': '财务报表_资产负债表_非流动资产'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    BALANCESTATEMENT46 = Column(DECIMAL(16, 2), server_default=text("'0.00'"), comment='非流动资产合计')
    BALANCESTATEMENT74 = Column(DECIMAL(17, 2), server_default=text("'0.00'"), comment='资产总计')
    BALANCESTATEMENT39 = Column(DECIMAL(16, 2), server_default=text("'0.00'"), comment='商誉')
    ReportDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssJjJjqbzbJbzl(Base):
    __tablename__ = 'css_jj_jjqbzb_jbzl'
    __table_args__ = (
        Index('uk_code_reportdate', 'CODE', 'ReportDate', unique=True),
        {'comment': '基金_基金全部指标_基金基本资料数据表'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(20), nullable=False, server_default=text("''"), comment='基金代码')
    FNAME = Column(String(50), comment='基金全称')
    FUNDMANAGER = Column(String(100), comment='基金经理(现任)')
    FIRSTINVESTTYPE = Column(String(50), comment='投资类型(一级分类)')
    SECONDINVESTTYPE = Column(String(50), comment='投资类型(二级分类)')
    FUNDSCALE = Column(DECIMAL(20, 2), comment='基金规模 [ 元 ]')
    ReportDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssJjJjqbzbTzzhCgmx(Base):
    __tablename__ = 'css_jj_jjqbzb_tzzh_cgmx'
    __table_args__ = (
        Index('uk_code_rank_date', 'CODE', 'RANK', 'ReportDate', unique=True),
        {'comment': '基金_基金全部指标_投资组合_持股明细'}
    )

    id = Column(INTEGER(10), primary_key=True, comment='自增ID')
    CODE = Column(String(20), nullable=False, server_default=text("''"), comment='基金代码')
    PRTKEYSTOCKCODE = Column(String(10), comment='重仓股股票代码')
    PRTKEYSTOCKNUM = Column(DECIMAL(20, 2), comment='重仓股股票数量 [ 股 ]')
    PRTKEYSTOCKVALUE = Column(DECIMAL(20, 2), comment='重仓股股票市值 [ 元 ]')
    PRTKEYPROPORTIONTOLIQ = Column(DECIMAL(10, 2), comment='重仓股持仓占流通股比例 [ % ]')
    RANK = Column(TINYINT(255), nullable=False, server_default=text("'0'"), comment='排名 [ 1 -- 10   默认0 ]')
    ReportDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='报告期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssZsGzzbPettm(Base):
    __tablename__ = 'css_zs_gzzb_pettm'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '东财全A指数市盈率(PE)TTM信息表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(20), nullable=False, server_default=text("''"), comment='期权代码')
    PETTM = Column(DECIMAL(10, 4), comment='PETTM')
    AMOUNT = Column(DECIMAL(20, 2), comment='成交额 [ 元 ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='此条数据对应日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class CssZsHqQjhq(Base):
    __tablename__ = 'css_zs_hq_qjhq'
    __table_args__ = (
        Index('uk_code_date', 'CODE', 'TradeDate', unique=True),
        {'comment': '指数_行情指标_区间行情'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, server_default=text("''"), comment='指数代码')
    NAME = Column(String(10), nullable=False, server_default=text("''"), comment='指数名称')
    DIFFERRANGEP = Column(DECIMAL(8, 4), nullable=False, server_default=text("'0.0000'"), comment='5日涨跌幅 [ % ]')
    TradeDate = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='交易日期')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class EdbHgsjHlRmbhl(Base):
    __tablename__ = 'edb_hgsj_hl_rmbhl'
    __table_args__ = {'comment': '宏观数据_汇率'}

    id = Column(INTEGER(11), primary_key=True, comment='自增id')
    EMM00058124 = Column(DECIMAL(7, 5), server_default=text("'0.00000'"), comment='中间价：美元兑人民币')
    EMM00058126 = Column(DECIMAL(7, 5), server_default=text("'0.00000'"), comment='中间价：港元兑人民币')
    Date = Column(INTEGER(11), nullable=False, unique=True, comment='时间')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclAbstock(Base):
    __tablename__ = 'sector_hs_scl_abstock'
    __table_args__ = {'comment': '全部AB股'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclArrangestock(Base):
    __tablename__ = 'sector_hs_scl_arrangestock'
    __table_args__ = {'comment': '退市整理股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclDelistedstock(Base):
    __tablename__ = 'sector_hs_scl_delistedstock'
    __table_args__ = {'comment': '已摘牌股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclIssuingstock(Base):
    __tablename__ = 'sector_hs_scl_issuingstock'
    __table_args__ = {'comment': '正在发行的股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclPendingstock(Base):
    __tablename__ = 'sector_hs_scl_pendingstock'
    __table_args__ = {'comment': '已发行待上市股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclSststock(Base):
    __tablename__ = 'sector_hs_scl_sststock'
    __table_args__ = {'comment': '*ST股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclStstock(Base):
    __tablename__ = 'sector_hs_scl_ststock'
    __table_args__ = {'comment': 'ST股票'}

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(50), nullable=False, unique=True, comment='股票代码')
    CODENAME = Column(String(50), nullable=False, comment='股票名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')


class SectorHsSclSwhyflStock(Base):
    __tablename__ = 'sector_hs_scl_swhyfl_stock'
    __table_args__ = (
        Index('uk_code_hycode', 'CODE', 'SWHYCODE', unique=True),
        {'comment': '申万行业股票分类信息表'}
    )

    id = Column(INTEGER(11), primary_key=True, comment='自增ID')
    CODE = Column(String(10), nullable=False, comment='股票代码')
    CODENAME = Column(String(10), nullable=False, comment='股票名称')
    SWHYCODE = Column(String(20), nullable=False, server_default=text("''"), comment='申万行业代码')
    SWHYNAME = Column(String(10), nullable=False, server_default=text("''"), comment='申万行业名称')
    insert_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='入库时间')
    update_time = Column(TIMESTAMP, nullable=False,
                         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
