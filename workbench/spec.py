"""L03 · 只检查结构的 Spec 解析器。

⭐ 职责边界（辅导资料 §5）：
  只检查六个章节**在不在**、顺序**对不对**、正文**空不空**、围栏**闭没闭**。
  ⚠️ **不裁决业务** —— 「给通用解析器硬编码库存公式，会让下一种需求无法复用，
     不能用扩大解析器职责代替业务审查。」
⇒ 所以本模块**不认识** available / 在库 / 预占 这些词。

六个章节映射为六个字段（**辅导资料 §5 的字段名**）：
  来源 → source ／ 目标 → goal ／ 非目标 → non_goals ／
  约束 → constraints ／ 验收用例 → acceptance ／ 完成定义 → done
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SECTIONS: tuple[tuple[str, str], ...] = (
    ("来源", "source"),
    ("目标", "goal"),
    ("非目标", "non_goals"),
    ("约束", "constraints"),
    ("验收用例", "acceptance"),
    ("完成定义", "done"),
)
HEADING_TO_FIELD = dict(SECTIONS)
FIELDS = tuple(f for _, f in SECTIONS)
FENCE = chr(96) * 3          # 三个反引号


class SpecError(ValueError):
    """结构错误。

    ⚠️ 继承 `ValueError`（**辅导资料与 L03 PPT 里参考实现的报错形式**：
    `ValueError: Spec 缺少必要章节：非目标`）。
    `code` 供程序判断，`message` 给人读。
    """

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class ParsedSpec:
    fields: dict[str, str]
    path: str | None = None

    def __getitem__(self, key: str) -> str:
        return self.fields[key]

    def as_dict(self) -> dict[str, str]:
        return dict(self.fields)


def _scan(text: str) -> tuple[list[tuple[int, str, str]], list[str]]:
    """返回 [(行号, 标题, 正文)] 与围栏错误。

    ⭐ **只在围栏外识别 `## ` 标题**；围栏没闭合 ⇒ 拒绝
    （**辅导资料 §5：「围栏没结束时应拒绝，避免吞掉后面的合同」**）。
    """
    lines = text.splitlines()
    found: list[tuple[int, str, str]] = []
    errors: list[str] = []
    open_fence = False
    current: tuple[int, str] | None = None
    body: list[str] = []

    def flush() -> None:
        if current is not None:
            found.append((current[0], current[1], "\n".join(body).strip()))

    for i, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if stripped.startswith(FENCE):
            open_fence = not open_fence
            if current is not None:
                body.append(raw)      # 围栏本身留在正文里（**原样返回**）
            continue
        if open_fence:
            if current is not None:
                body.append(raw)      # 围栏内的 ## 只是示例 ⇒ 不当标题
            continue
        if raw.startswith("## "):
            flush()
            current = (i, raw[3:].strip())
            body = []
            continue
        if current is not None:
            body.append(raw)
    flush()

    if open_fence:
        errors.append("代码围栏未闭合：无法确定后面的内容属于正文还是合同")
    return found, errors


def parse_spec(text: str, path: str | None = None) -> ParsedSpec:
    """把六段合同文本解析为六个原文字段。**只读 ✗ 不改文本。**"""
    if not isinstance(text, str):
        raise SpecError("输入必须是文本", "input_not_text")
    found, errors = _scan(text)
    if errors:
        raise SpecError("；".join(errors), "unclosed_fence")

    seen: dict[str, tuple[int, str]] = {}
    for lineno, title, body in found:
        if title not in HEADING_TO_FIELD:
            raise SpecError(
                f"未知二级标题：{title}（第 {lineno} 行）；只允许六个合同标题", "unknown_heading")
        if title in seen:
            raise SpecError(
                f"重复标题：{title}（第 {lineno} 行，首次在第 {seen[title][0]} 行）；"
                "重复不能悄悄覆盖", "duplicate_section")
        seen[title] = (lineno, body)

    for title, _ in SECTIONS:
        if title not in seen:
            raise SpecError(f"Spec 缺少必要章节：{title}", "missing_section")

    order = [t for _, t, _ in found]
    expected = [t for t, _ in SECTIONS]
    if order != expected:
        raise SpecError(
            "章节顺序不正确：实际 " + " → ".join(order) + "；应为 " + " → ".join(expected),
            "section_out_of_order")

    for title, _ in SECTIONS:
        if not seen[title][1].strip():
            raise SpecError(f"章节正文为空：{title}", "empty_section")

    return ParsedSpec({HEADING_TO_FIELD[t]: seen[t][1] for t, _ in SECTIONS}, path)


def load_spec(path: str | Path) -> ParsedSpec:
    """用 UTF-8 读文件再解析。**不改原文件。**"""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SpecError(f"Spec 文件不存在：{p}", "spec_not_found") from None
    except UnicodeDecodeError as error:
        raise SpecError(f"Spec 不是 UTF-8：{p}（{error}）", "spec_not_utf8") from error
    except OSError as error:
        raise SpecError(f"Spec 不可读取：{p}（{error}）", "spec_unreadable") from error
    return parse_spec(text, str(p))
