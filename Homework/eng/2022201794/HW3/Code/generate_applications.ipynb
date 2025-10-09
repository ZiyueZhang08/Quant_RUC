#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import sys
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

import pandas as pd
from docxtpl import DocxTemplate


# --------------------------
# 可在此自定义个人信息（模板中可引用这些占位符）
# --------------------------
PERSONAL_INFO: Dict[str, str] = {
    "full_name": "Derek Lee"
}

# 大学列表字段别名映射（尽量兼容常见命名）
UNIV_COL_ALIASES: Dict[str, List[str]] = {
    "university_name": ["university_name", "university", "school", "name", "college"],
    "department": ["department", "dept", "school_of", "faculty"],
    "program": ["program", "programme", "major", "degree_program"],
}

# 研究方向字段别名映射
AREA_COL_ALIASES: Dict[str, List[str]] = {
    "research_area": ["research_area", "area", "field", "topic", "interest"],
    "journals": ["journals", "target_journals", "top_journals", "pub_targets"],
    "skills": ["skills", "skillset", "strengths", "competencies"],
    "career_goal": ["career_goal", "career goal", "goal", "career_objective", "objective"],
}

# 在 build_context 之前添加：姓名键集合
NAME_KEYS = {
    "full_name", "name", "applicant_name", "student_name", "candidate_name", "applicant", "姓名", "名字"
}


def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def project_paths() -> Tuple[str, str, str, str]:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    templates_dir = os.path.join(base_dir, "templates")
    output_dir = os.path.join(base_dir, "output")
    return base_dir, data_dir, templates_dir, output_dir


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def sanitize_filename(name: str, replacement: str = "_") -> str:
    name = re.sub(r"[\\/:*?\"<>|]+", replacement, name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


def load_excel(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"未找到文件: {path}")
    try:
        df = pd.read_excel(path, engine="openpyxl")
        if df is None or df.empty:
            raise ValueError(f"Excel 文件为空: {path}")
        # 统一列名为小写去空格
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df
    except Exception as e:
        raise RuntimeError(f"读取 Excel 失败: {path} -> {e}") from e


def find_first_existing_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def map_row_by_aliases(row: pd.Series, alias_map: Dict[str, List[str]]) -> Dict[str, str]:
    mapped: Dict[str, str] = {}
    for canonical, aliases in alias_map.items():
        value = ""
        for alias in aliases:
            if alias in row and pd.notna(row[alias]):
                value = row[alias]
                break
        # 统一转字符串，NaN/NaT 转为空
        if pd.isna(value):
            value = ""
        mapped[canonical] = str(value).strip()
    return mapped


def format_date_value(v) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)) or (isinstance(v, str) and not v.strip()):
        return ""
    if isinstance(v, (datetime, date)):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, pd.Timestamp):
        return v.strftime("%Y-%m-%d")
    # 尝试解析字符串日期
    try:
        parsed = pd.to_datetime(v, errors="coerce")
        if not pd.isna(parsed):
            return parsed.strftime("%Y-%m-%d")
    except Exception:
        pass
    return str(v)


def enrich_university_record(rec: Dict[str, str]) -> Dict[str, str]:
    # 规范日期
    rec["deadline"] = format_date_value(rec.get("deadline", ""))
    # 兜底字段
    for k in UNIV_COL_ALIASES.keys():
        rec.setdefault(k, "")
        if rec[k] is None:
            rec[k] = ""
    return rec


def enrich_area_record(rec: Dict[str, str]) -> Dict[str, str]:
    for k in AREA_COL_ALIASES.keys():
        rec.setdefault(k, "")
        if rec[k] is None:
            rec[k] = ""
    return rec


def load_universities(universities_xlsx: str) -> List[Dict[str, str]]:
    df = load_excel(universities_xlsx)

    # 至少需要有大学名称列
    name_col = find_first_existing_column(df, UNIV_COL_ALIASES["university_name"])
    if not name_col:
        raise ValueError(f"大学列表缺少必需列：{UNIV_COL_ALIASES['university_name']} 之一")
    df = df.dropna(subset=[name_col])

    # 行映射
    records: List[Dict[str, str]] = []
    for _, row in df.iterrows():
        row_dict = {c: row[c] for c in df.columns}
        mapped = map_row_by_aliases(row_dict, UNIV_COL_ALIASES)
        records.append(enrich_university_record(mapped))

    if not records:
        raise ValueError("大学列表为空，无法生成申请信。")
    return records


def load_research_areas(areas_xlsx: str) -> List[Dict[str, str]]:
    df = load_excel(areas_xlsx)

    # 至少需要有研究方向名称列
    area_col = find_first_existing_column(df, AREA_COL_ALIASES["research_area"])
    if not area_col:
        raise ValueError(f"研究方向列表缺少必需列：{AREA_COL_ALIASES['research_area']} 之一")
    df = df.dropna(subset=[area_col])

    records: List[Dict[str, str]] = []
    for _, row in df.iterrows():
        row_dict = {c: row[c] for c in df.columns}
        mapped = map_row_by_aliases(row_dict, AREA_COL_ALIASES)
        records.append(enrich_area_record(mapped))

    if not records:
        raise ValueError("研究方向列表为空，无法生成申请信。")
    return records


def build_context(
    personal: Dict[str, str],
    university: Dict[str, str],
    area: Dict[str, str],
) -> Dict[str, str]:
    ctx: Dict[str, str] = {}
    today = date.today()
    ctx["today"] = today.strftime("%Y-%m-%d")
    ctx["year"] = str(today.year)

    # 姓名（只从 personal，且不允许被覆盖）
    name = (personal.get("full_name") or "").strip()
    ctx["full_name"] = name
    # 兼容多种模板占位符别名
    for alias in NAME_KEYS:
        ctx.setdefault(alias, name)

    # 大学信息（避免覆盖姓名键）
    for k, v in university.items():
        if k in NAME_KEYS:
            continue
        ctx[k] = v or ""

    # 研究方向信息（避免覆盖姓名键）
    for k, v in area.items():
        if k in NAME_KEYS:
            continue
        ctx[k] = v or ""

    # 便捷别名
    ctx["university"] = university.get("university_name", "")
    ctx["dept"] = university.get("department", "")
    ctx["program_name"] = university.get("program", "")
    ctx["area"] = area.get("research_area", "")
    ctx["area_keywords"] = area.get("keywords", "")
    ctx["advisor"] = area.get("advisor_preference", "")

    # 关键字段优先顺序
    ctx["program"] = (area.get("program") or university.get("program") or "").strip()
    ctx["skills"] = (area.get("skills") or "").strip()
    ctx["journals"] = (area.get("journals") or "").strip()
    ctx["career_goal"] = (area.get("career_goal") or "").strip()

    return ctx


def generate_documents(
    template_path: str,
    universities: List[Dict[str, str]],
    areas: List[Dict[str, str]],
    output_dir: str,
) -> int:
    ensure_dir(output_dir)

    count = 0
    total = len(universities) * len(areas)
    logging.info(f"开始生成申请信，总数预计: {total} 封")

    for ui, u in enumerate(universities, start=1):
        uni_name = u.get("university_name", f"University{ui}") or f"University{ui}"
        for ai, a in enumerate(areas, start=1):
            area_name = a.get("research_area", f"Area{ai}") or f"Area{ai}"
            ctx = build_context(PERSONAL_INFO, u, a)

            # 文件名：序号_大学_方向.docx
            fname = f"{count + 1:03d}_{sanitize_filename(uni_name)}_{sanitize_filename(area_name)}.docx"
            out_path = os.path.join(output_dir, fname)

            try:
                tpl = DocxTemplate(template_path)

                # 调试：提示模板中未提供的占位符（若模板用的是 name/姓名 等，可据此确认）
                try:
                    missing = tpl.get_undeclared_template_variables(ctx)
                    if missing:
                        logging.debug(f"模板占位符在上下文中未提供: {sorted(missing)}")
                except Exception:
                    pass

                tpl.render(ctx)
                tpl.save(out_path)
                count += 1
                logging.debug(f"生成: {out_path}")
            except Exception as e:
                logging.error(f"生成失败: {out_path} -> {e}")

    logging.info(f"生成完成: 成功 {count} / 预计 {total} 封。输出目录: {output_dir}")
    return count


def parse_args() -> argparse.Namespace:
    base_dir, data_dir, templates_dir, output_dir = project_paths()
    parser = argparse.ArgumentParser(
        description="根据 Excel 列表和 Word 模板批量生成研究生申请信（SOP）"
    )
    parser.add_argument(
        "--universities",
        "-u",
        default=os.path.join(data_dir, "universities_list.xlsx"),
        help="大学列表 Excel 文件路径（默认：data/universities_list.xlsx）",
    )
    parser.add_argument(
        "--areas",
        "-a",
        default=os.path.join(data_dir, "research_areas.xlsx"),
        help="研究方向 Excel 文件路径（默认：data/research_areas.xlsx）",
    )
    parser.add_argument(
        "--template",
        "-t",
        default=os.path.join(templates_dir, "SOP_template.docx"),
        help="SOP Word 模板路径（默认：templates/SOP_template.docx）",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=output_dir,
        help="输出目录（默认：output/）",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="显示调试日志",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    setup_logging(args.verbose)

    # 校验模板
    if not os.path.exists(args.template):
        logging.error(f"未找到模板文件: {args.template}")
        return 2

    try:
        universities = load_universities(args.universities)
        areas = load_research_areas(args.areas)
    except Exception as e:
        logging.error(str(e))
        return 3

    generated = generate_documents(
        template_path=args.template,
        universities=universities,
        areas=areas,
        output_dir=args.output,
    )

    # 如果需要严格 90 封，可在此进行校验（30×3）
    # if len(universities) == 30 and len(areas) == 3 and generated != 90:
    #     logging.warning(f"期望 90 封，实际生成 {generated} 封。")

    return 0 if generated > 0 else 4


if __name__ == "__main__":
    sys.exit(main())