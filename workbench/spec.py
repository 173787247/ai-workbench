"""L03 合同结构解析器：只检查六段结构是否完整。

**它只回答一个问题：合同的六段结构是否完整？**
**它不判断业务口径是否正确**（例如库存公式对不对）——
业务验收归人，见 `AGENTS.md` 的「自动检查与具名人工接受是两件事」。

接口（供 CLI 与后续讲次复用）：
    load_spec(path) -> ParsedSpec     读 UTF-8 文件，只读，不修改输入
    parse_spec(text) -> ParsedSpec    解析文本
    ParsedSpec.as_dict() -> dict      六个原文字段
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

#: 六个必要章节，顺序即合同要求的顺序
REQUIRED_SECTIONS: tuple[str, ...] = (
    "来源", "目标", "非目标", "约束", "验收用例", "完成定义",
)

# 接受 "## 1. 来源"、"## 来源"、"## 1 来源" 等编号变体
# 只认二级标题：## 后面不能再跟 #，否则 ### 三级标题会被误当成章节
_HEADING = re.compile(r"^##(?!#)\s*(?:(\d+)\s*[.、]?\s*)?(\S.*?)\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")


class SpecError(Exception):
    """结构错误。消息里必须能定位问题（缺哪章、第几行等）。"""


def _strip_number(title: str) -> str:
    return re.sub(r"^\d+\s*[.、]?\s*", "", title).strip()


@dataclass(frozen=True)
class ParsedSpec:
    """解析结果：只保留六段的**原文**。"""

    source: str
    goal: str
    non_goal: str
    constraints: str
    acceptance: str
    definition_of_done: str

    def as_dict(self) -> dict[str, str]:
        return {
            "来源": self.source,
            "目标": self.goal,
            "非目标": self.non_goal,
            "约束": self.constraints,
            "验收用例": self.acceptance,
            "完成定义": self.definition_of_done,
        }


def _split_sections(text: str) -> list[tuple[int, str, str]]:
    """按行扫描，返回 [(行号, 标题, 正文)]。跳过代码围栏内的标题。"""
    lines = text.splitlines()
    sections: list[tuple[int, str, str]] = []
    in_fence = False
    fence_mark = ""
    current: tuple[int, str] | None = None
    buffer: list[str] = []

    def flush():
        nonlocal current, buffer
        if current is not None:
            sections.append((current[0], current[1], "\n".join(buffer).strip()))
        buffer = []

    for index, line in enumerate(lines, start=1):
        fence = _FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence, fence_mark = True, marker
            elif marker == fence_mark:
                in_fence, fence_mark = False, ""
            if in_fence or not in_fence:
                if current is not None:
                    buffer.append(line)
                continue
        if in_fence:
            if current is not None:
                buffer.append(line)
            continue
        match = _HEADING.match(line)
        if match:
            flush()
            current = (index, _strip_number(match.group(2)))
            continue
        if current is not None:
            buffer.append(line)
    flush()

    if in_fence:
        raise SpecError(
            f"第 {len(lines)} 行附近有未闭合的代码围栏（{fence_mark}）："
            "后续内容无法判定是否为章节，拒绝解析"
        )
    return sections


def parse_spec(text: str) -> ParsedSpec:
    """解析合同文本。结构不合法时抛 SpecError，且**不改动任何外部状态**。"""
    if not isinstance(text, str):
        raise SpecError("parse_spec 需要字符串输入")
    sections = _split_sections(text)
    if not sections:
        raise SpecError("没有找到任何 '## ' 章节标题：这不像是六段式合同")

    seen: dict[str, int] = {}
    order: list[tuple[int, str]] = []
    for lineno, title in [(s[0], s[1]) for s in sections]:
        if title not in REQUIRED_SECTIONS:
            raise SpecError(
                f"第 {lineno} 行出现未知标题「{title}」："
                f"六段只允许 {', '.join(REQUIRED_SECTIONS)}"
            )
        if title in seen:
            raise SpecError(
                f"第 {lineno} 行出现重复章节「{title}」："
                f"它已在第 {seen[title]} 行出现过"
            )
        seen[title] = lineno
        order.append((lineno, title))

    missing = [s for s in REQUIRED_SECTIONS if s not in seen]
    if missing:
        raise SpecError(f"缺章：{', '.join(missing)}（六段必须齐全）")

    indices = [REQUIRED_SECTIONS.index(t) for _, t in order]
    if indices != sorted(indices):
        got = " → ".join(t for _, t in order)
        raise SpecError(
            f"顺序错误：章节必须按 {', '.join(REQUIRED_SECTIONS)} 排列，实际为 {got}"
        )

    bodies = {title: body for _, title, body in sections}
    empty = [s for s in REQUIRED_SECTIONS if not bodies.get(s, "").strip()]
    if empty:
        raise SpecError(f"空章：{', '.join(empty)}（章节存在但正文为空）")

    return ParsedSpec(
        source=bodies["来源"],
        goal=bodies["目标"],
        non_goal=bodies["非目标"],
        constraints=bodies["约束"],
        acceptance=bodies["验收用例"],
        definition_of_done=bodies["完成定义"],
    )


def load_spec(path: str | Path) -> ParsedSpec:
    """读 UTF-8 合同文件并解析。**只读：不修改输入文件，不创建任何数据。**"""
    p = Path(path)
    if not p.is_file():
        raise SpecError(f"合同文件不存在：{p}")
    try:
        text = p.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise SpecError(f"合同不是合法 UTF-8：{p}（{error}）") from error
    except OSError as error:
        raise SpecError(f"合同不可读取：{p}（{error}）") from error
    return parse_spec(text)
