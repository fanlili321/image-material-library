#!/usr/bin/env python3
import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

LIBRARY = Path(os.environ.get(
    "IMAGE_MATERIAL_LIBRARY",
    "/Users/fanlili/Desktop/范丽丽./图片素材库",
))
DB = LIBRARY / "library.db"
UPLOADS = LIBRARY / "static" / "uploads"


def connect():
    if not DB.is_file():
        raise SystemExit(f"数据库不存在：{DB}")
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def info(_args):
    conn = connect()
    counts = {}
    for table in ("assets", "versions", "tags", "asset_tags"):
        counts[table] = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.close()
    raw_images = sum(
        1 for root in ("static/uploads", "ppt_jpegs", "speech_jpegs")
        for p in (LIBRARY / root).rglob("*")
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
    )
    print(json.dumps({
        "library": str(LIBRARY),
        "database": str(DB),
        "raw_images": raw_images,
        **counts,
    }, ensure_ascii=False, indent=2))


def search(args):
    terms = [term.lower() for term in args.query.split() if term]
    conn = connect()
    rows = conn.execute("""
        SELECT a.id, a.name, COALESCE(a.description,'') description,
               COALESCE(a.source,'') source, COALESCE(a.link,'') link,
               GROUP_CONCAT(DISTINCT t.name) tags,
               v.filename, v.original_name
        FROM assets a
        LEFT JOIN asset_tags at ON at.asset_id=a.id
        LEFT JOIN tags t ON t.id=at.tag_id
        LEFT JOIN versions v ON v.asset_id=a.id AND v.is_current=1
        GROUP BY a.id
        ORDER BY a.updated_at DESC
    """).fetchall()
    conn.close()
    results = []
    for row in rows:
        haystack = " ".join(str(row[k] or "") for k in ("name", "description", "source", "tags")).lower()
        if terms and not all(term in haystack for term in terms):
            continue
        item = dict(row)
        item["path"] = str(UPLOADS / row["filename"]) if row["filename"] else ""
        results.append(item)
        if len(results) >= args.limit:
            break
    print(json.dumps(results, ensure_ascii=False, indent=2))


def serve(args):
    app = LIBRARY / "app.py"
    if not app.is_file():
        raise SystemExit(f"应用不存在：{app}")
    env = os.environ.copy()
    env["FLASK_RUN_PORT"] = str(args.port)
    raise SystemExit(subprocess.call([sys.executable, str(app)], cwd=LIBRARY, env=env))


def main():
    parser = argparse.ArgumentParser(description="图片素材库命令行入口")
    sub = parser.add_subparsers(required=True)
    p_info = sub.add_parser("info", help="显示素材库状态")
    p_info.set_defaults(func=info)
    p_search = sub.add_parser("search", help="搜索已编目素材")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)
    p_search.set_defaults(func=search)
    p_serve = sub.add_parser("serve", help="启动网页素材库")
    p_serve.add_argument("--port", type=int, default=5001)
    p_serve.set_defaults(func=serve)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

