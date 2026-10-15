"""L16 的修复动作：库存按商品名关键词查本组织全部库存。

单独一个文件，是为了不再把带转义的多行补丁塞进 shell heredoc —— 那样做已经坏过两次。
被 tools/l15-codex-exec.py 导入，作为 write_scope 命中 flowerp/inventory.py 时的动作。
"""

from __future__ import annotations

import ast
from pathlib import Path


def patch_inventory_keyword(workspace: Path) -> str:
    """四层都改：业务查询先匹配再分页、接口转发关键词、页面加搜索框并明说空结果。"""
    changed: list[str] = []

    # ① 业务查询：关键词进 WHERE，先匹配本组织的全部数据，再分页。
    #    先取一页再筛会漏项；先读全库再在页面隐藏会泄漏数据。
    business = workspace / "flowerp" / "inventory.py"
    text = business.read_text(encoding="utf-8")
    if "keyword" in text.split("def list_balances")[1][:400]:
        return "inventory.py 已经是 L16 修复后的版本"

    old_sig = (
        '    def list_balances(self, principal: Principal, site_id: str = "", product_id: str = "",\n'
        '                      low_stock_only: bool = False) -> list[dict]:'
    )
    new_sig = (
        '    def list_balances(self, principal: Principal, site_id: str = "", product_id: str = "",\n'
        '                      low_stock_only: bool = False, keyword: str = "") -> list[dict]:'
    )
    if old_sig not in text:
        raise SystemExit("inventory.py 的 list_balances 签名与预期不符，先核对候选")
    text = text.replace(old_sig, new_sig, 1)

    # 同一段初始化在 inventory.py 里出现三次（list_counts / list_balances / ledger），
    # 所以不能对全文 replace —— 那会把关键词块插进第一个同名方法里，而这个方法没有
    # keyword 参数，list_balances 则完全没被改到。先把 list_balances 切出来，段内替换。
    start = text.index("    def list_balances(")
    end = text.find("\n    def ", start + 1)
    if end < 0:
        end = len(text)
    body = text[start:end]

    anchor = '        params: list[object] = [principal.organization_id]'
    if body.count(anchor) != 1:
        raise SystemExit(f"list_balances 里的参数初始化出现 {body.count(anchor)} 次，锚点不唯一，停止")
    addition = (
        anchor
        + '\n        if keyword:\n'
        + '            # 在当前组织允许访问的数据里按商品名匹配，再分页；\n'
        + '            # 先取一页再筛会漏项，先读全库再在页面隐藏会泄漏数据。\n'
        + '            filters.append("(p.sku LIKE ? OR p.name LIKE ?)")\n'
        + '            params.extend([f"%{keyword}%", f"%{keyword}%"])'
    )
    text = text[:start] + body.replace(anchor, addition, 1) + text[end:]
    ast.parse(text)
    business.write_text(text, encoding="utf-8")
    changed.append("flowerp/inventory.py")

    # ② HTTP 接口：接收约定条件并转发；页面与直接接口调用遵守同一业务规则。
    api = workspace / "workbench" / "api_v2.py"
    api_text = api.read_text(encoding="utf-8")
    old_call = (
        'self.inventory.list_balances(principal, query.get("site_id", ""), '
        'query.get("product_id", ""), query.get("low_stock", "false") == "true")'
    )
    new_call = (
        'self.inventory.list_balances(principal, query.get("site_id", ""), '
        'query.get("product_id", ""), query.get("low_stock", "false") == "true", '
        'query.get("keyword", ""))'
    )
    if old_call not in api_text:
        raise SystemExit("api_v2.py 的库存余额调用与预期不符")
    api_text = api_text.replace(old_call, new_call, 1)
    ast.parse(api_text)
    api.write_text(api_text, encoding="utf-8")
    changed.append("workbench/api_v2.py")

    # ③ 客户页面：加搜索框与空结果说明，用户要能看出这次查询是否有效。
    page = workspace / "web" / "index.html"
    page_text = page.read_text(encoding="utf-8")
    old_panel = (
        '<article class="panel tab-panel" data-tab-panel="balances">'
        '<div class="table-scroll" id="inventory-table"></div></article>'
    )
    new_panel = (
        '<article class="panel tab-panel" data-tab-panel="balances">'
        '<div class="inventory-search">'
        '<input id="inventory-keyword" type="search" placeholder="按商品名或编码查询本组织全部库存" />'
        '<button class="button primary" id="inventory-search-run">查询</button>'
        '<span id="inventory-search-state" class="muted"></span></div>'
        '<div class="table-scroll" id="inventory-table"></div></article>'
    )
    if old_panel not in page_text:
        raise SystemExit("web/index.html 的库存面板与预期不符")
    page.write_text(page_text.replace(old_panel, new_panel, 1), encoding="utf-8")
    changed.append("web/index.html")

    # ④ 客户页面：把关键词发给 API，不再全量渲染；空结果不留旧列表。
    app = workspace / "web" / "app.js"
    app_text = app.read_text(encoding="utf-8")
    marker = 'api("/api/v1/inventory/balances")'
    if marker not in app_text:
        raise SystemExit("web/app.js 的库存请求与预期不符")
    keyword_expr = (
        '(document.getElementById("inventory-keyword")||{}).value||""'
    )
    app_text = app_text.replace(
        marker,
        'api("/api/v1/inventory/balances?keyword="+encodeURIComponent(' + keyword_expr + '))',
        1,
    )
    old_state = "state.inventory=result[0].items;"
    if old_state in app_text:
        app_text = app_text.replace(
            old_state,
            old_state
            + "\n  {const s=document.getElementById(\"inventory-search-state\");"
            + "if(s)s.textContent=state.inventory.length?\"\":\"没有匹配的库存记录\";}",
            1,
        )
    app.write_text(app_text, encoding="utf-8")
    changed.append("web/app.js")

    return "四层都改：" + "、".join(changed)
