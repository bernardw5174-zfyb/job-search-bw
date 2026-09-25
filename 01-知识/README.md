# 01-知识 — 知识页（用户区）

本目录存放**你自己**长出的求职知识：Agent 编译的草稿（`_drafts/`）与你确认后的知识页。

- ⚠️ **个人数据**——`_drafts/` 已被 `.gitignore` 排除；正式知识页请自行评估是否入库
- 本目录在独立使用场景生效；作为 knowledge-growth 垂直包挂载时，用户知识写 `vault/求职/01-知识/`

---

## 岗位词表（对标基准）

词表是本目录的标准产物（由 `skills/02-keyword-intelligence` 频率分析从 JD 语料生成）。规范：

- **晋升必须留痕**：词表从 `_drafts/` 晋升为正式页时，frontmatter 须记 `status: active` **且** `confirmed_at: YYYY-MM-DD`（用户确认晋升的日期，与 Core schema 的晋升留痕对齐）——无 `confirmed_at` 的 `active` 视为 Agent 自封，审计不过
- 语料不足门槛（<10 份）须标「近似」；语料变化未重算须标过期（`stale: true`/`corpus_status` 警示），数字不可引用
- 重算时旧版标 `superseded_by`，不删历史
- 交付前跑核验：单词表 `verify_table.py`，多列对照表 `verify_matrix.py`
