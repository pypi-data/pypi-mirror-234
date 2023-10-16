from sqlalchemy.orm.query import Query
from .utils import *
from .choiceinfo import *
from .choice import *


# 获取财务类的sql语句
def get_finance_sql(query_object):
    if not isinstance(query_object, Query):
        raise AssertionError(
            "query_object must be a sqlalchemy's Query object."
            " But what passed in was: " + str(type(query_object))
        )

    # 编译 query 对象为纯 sql
    sql = compile_query(query_object)
    return sql


# choiceinfo库
caiwu_info_report = CaiwuInfoReport
caiwu_info_tradedate = CaiwuInfoTradedate

# choice库
csd_hs_gzzb_ltsz = CsdHsGzzbLtsz
csd_hs_zjlx_zljlr = CsdHsZjlxZljlr
css_hs_bbfz_yfzc = CssHsBbfzYfzc
css_hs_cwbb_xjllb_jyhdcsdxjll = CssHsCwbbXjllbJyhdcsdxjll
css_hs_cwbb_ybqy_lrb = CssHsCwbbYbqyLrb
css_hs_cwbb_ybqy_zcfzb = CssHsCwbbYbqyZcfzb
css_hs_cwfx_bgqttm = CssHsCwfxBgqttm
css_hs_cwfx_cznl = CssHsCwfxCznl
css_hs_cwfx_cznl_nnzzl = CssHsCwfxCznlNnzzl
css_hs_cwfx_cznl_tbzzl = CssHsCwfxCznlTbzzl
css_hs_cwfx_djdcwzb = CssHsCwfxDjdcwzb
css_hs_cwfx_mgzb = CssHsCwfxMgzb
css_hs_cwfx_mgzb_mgsyttm = CssHsCwfxMgzbMgsyttm
css_hs_cwfx_syzl = CssHsCwfxSyzl
css_hs_cwfx_xjll_ttm = CssHsCwfxXjllTtm
css_hs_cwfx_ylnl = CssHsCwfxYlnl
css_hs_cwfx_ylnl_jzcsylttm = CssHsCwfxYlnlJzcsylttm
css_hs_cwfx_yynl = CssHsCwfxYynl
css_hs_cwfx_zbjg = CssHsCwfxZbjg
css_hs_fhzb_fhzb = CssHsFhzbFhzb
css_hs_fxfx_zdycszb = CssHsFxfxZdycszb
css_hs_gbzb_gbbd = CssHsGbzbGbbd
# css_hs_gbzb_gbbd_bak = CssHsGbzbGbbdBak
css_hs_gdzb_bgqgdhszb = CssHsGdzbBgqgdhszb
css_hs_gdzb_gdggzjc = CssHsGdzbGdggzjc
css_hs_gdzb_gqzy = CssHsGdzbGqzy
css_hs_gdzb_hgtgzcg = CssHsGdzbHgtgzcg
css_hs_gdzb_jgcgbl = CssHsGdzbJgcgbl
css_hs_gdzb_sdgd = CssHsGdzbSdgd
css_hs_gpzb_fhzb = CssHsGpzbFhzb
css_hs_gpzb_pgzb = CssHsGpzbPgzb
css_hs_gpzb_zfzb = CssHsGpzbZfzb
css_hs_gzzb_bkhcgz = CssHsGzzbBkhcgz
css_hs_hqzb_qjhq = CssHsHqzbQjhq
css_hs_hqzb_rzrq = CssHsHqzbRzrq
css_hs_jbzl_zqzl_date = CssHsJbzlZqzlDate
css_hs_jgdyzb_ggrqjgdyzb = CssHsJgdyzbGgrqjgdyzb
# css_hs_lb.bak = CssHsLb.bak
css_hs_qq_yhbdl = CssHsQqYhbdl
css_hs_sfzb_sfssbx = CssHsSfzbSfssbx
css_hs_ylyc_org_info = CssHsYlycOrgInfo
css_hs_ylyc_ssgsyjyg = CssHsYlycSsgsyjyg
css_hs_ylyc_swhy_org_info = CssHsYlycSwhyOrgInfo
css_hs_ylyc_tzpjzhz = CssHsYlycTzpjzhz
css_hs_ylyc_ycyplmxz = CssHsYlycYcyplmxz
css_hs_ylyc_ycyplmxz_ybsl = CssHsYlycYcyplmxzYbsl
css_hs_ylyc_ylyczhz = CssHsYlycYlyczhz
css_hs_ylyc_ylyczhz_gd = CssHsYlycYlyczhzGd
css_hs_zcfz_fldzc = CssHsZcfzFldzc
css_jj_jjqbzb_jbzl = CssJjJjqbzbJbzl
css_jj_jjqbzb_tzzh_cgmx = CssJjJjqbzbTzzhCgmx
css_zs_gzzb_pettm = CssZsGzzbPettm
css_zs_hq_qjhq = CssZsHqQjhq
edb_hgsj_hl_rmbhl = EdbHgsjHlRmbhl
sector_hs_scl_abstock = SectorHsSclAbstock
sector_hs_scl_arrangestock = SectorHsSclArrangestock
sector_hs_scl_delistedstock = SectorHsSclDelistedstock
sector_hs_scl_issuingstock = SectorHsSclIssuingstock
sector_hs_scl_pendingstock = SectorHsSclPendingstock
sector_hs_scl_sststock = SectorHsSclSststock
sector_hs_scl_ststock = SectorHsSclStstock
sector_hs_scl_swhyfl_stock = SectorHsSclSwhyflStock



def _collect_item():
    items = []
    for item in globals().keys():
        for prefix in ["csd_", "css_", "caiwu_info_"]:
            if item.startswith(prefix):
                items.append(item)
    return items


__all__ = [
    "query",
    "get_finance_sql",
]

__all__.extend(_collect_item())

del _collect_item

