# 素材库布局

- 根目录：`/Users/fanlili/Desktop/范丽丽./图片素材库`
- 网页应用：`app.py`、`templates/`、`static/`
- 健康检查：`/health`
- 回收站：`/recycle`
- 素材质量中心：`/quality`
- 每日自动备份：`backups/auto/library-YYYYMMDD.db`
- SQLite 目录：`library.db`
- 待处理扫描器：`inventory.py`
- 视觉分析与 OCR 处理器：`processor.py`
- 元数据建议器：`suggestions.py`
- 已编目图片：`static/uploads/`
- PPT 页图：`ppt_jpegs/`
- 私募/高净值 PPT 页图：`private_jpegs/`
- 演讲素材页图：`speech_jpegs/`
- 最新图表版本：`version_sheet_jpegs/`
- 导入及维护工具：根目录中的 `batch_import.py`、`import_speech_ppt.py`、`analyze_ppt_pages.py`、`check_updates.py` 和 `patch_*.py`

核心表：

- `assets`：素材名称、描述、来源、链接和更新时间状态
- `versions`：文件名、原始名、版本说明和当前版本标记
- `tags`：标签及父标签
- `asset_tags`：素材与标签的关联
- `inbox_items`：原始页图、SHA-256、重复关系和人工处理状态
- `audit_log`：回收与恢复等关键操作日志

网页应用通过 `/api/assets` 搜索已编目资产，通过 `/api/ppt-search` 搜索公募直播、私募直播和对外演讲的完整历史 PPT 页图，通过 `/uploads/<filename>` 提供当前图片文件。
待处理工作台位于 `/workbench`，扫描 `ppt_jpegs/`、`private_jpegs/`、`speech_jpegs/` 和 `version_sheet_jpegs/`；入库时复制原图，不移动或覆盖来源文件。螺丝钉学院来源已停用，不得重新同步入库。
`processor.py` 为原始图片生成感知哈希和相似组；OCR 使用本地 Tesseract，缺少可执行文件时安全跳过。
相似组接口为 `/api/inbox/groups`，用于并排审核，不执行自动批量跳过。
待处理图片可通过 `/api/inbox/<item_id>/add-version` 复制为已有素材的新版本。
`/api/inbox/<item_id>/suggestions` 从期次目录、页码、日期、文件名和 OCR 文本生成可编辑的元数据建议。
