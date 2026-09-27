# 01-知识 — 知识页（用户区）

本目录存放**你自己**长出的求职知识：Agent 编译的草稿（`_drafts/`）与你确认后的知识页。

- ⚠️ **个人数据**——`_drafts/` 已被 `.gitignore` 排除；正式知识页请自行评估是否入库
- 本目录在独立使用场景生效；作为 knowledge-growth 垂直包挂载时，用户知识写 `vault/求职/01-知识/`

---

## 岗位词表（对标基准）

词表是本目录的标准产物（由 `skills/02-keyword-intelligence` 频率分析从 JD 语料生成）。规范：

- **晋升留痕（词表特殊路径）**：词表是统计产物，**不走 `_drafts/` 草稿流程**——用户在对话中确认（"落盘/确认"）即视为晋升指令，Agent 落盘时 frontmatter 必须记 `status: active` **且** `confirmed_at: YYYY-MM-DD`（用户确认的日期，与 Core schema 的晋升留痕对齐）——无 `confirmed_at` 的 `active` 视为 Agent 自封，审计不过（validate 会 ERROR 拦截）
- **计数口径必须自洽**：frontmatter `corpus_size` 指**计入词表的份数**；若 `corpus:` 指向的目录已含未计入的新 JD（归档但未重算），页内必须标注「目录已含 N 份未计入新件（YYYY-MM-DD 归档）」（重算时旧版标 `superseded_by`，不删历史）——**杜绝"按目录复核数字对不上"**
- 语料不足门槛（<10 份）须标「近似」；语料变化未重算须标过期（`stale: true`/`corpus_status` 警示），数字不可引用
- 重算时旧版标 `superseded_by`，不删历史
- **交付前核验（文字清单，无需脚本）**：① 语料目录实况与 `corpus_size` 对得上（含"未计入新件"标注）；② 平台噪声裁剪（猎聘温馨提示/猜你喜欢/51job SEO 区等）已执行并说明口径；③ frontmatter 有 `status: active` + `confirmed_at`；④ 英文主体/逐字重复/语境歧义词已按语料健康度规则处理
