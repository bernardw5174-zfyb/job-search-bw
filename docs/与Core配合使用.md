# 与 Core 配合使用（knowledge-growth 垂直包模式）

> 本包有**双重身份**：①独立包（clone 即用）；②**knowledge-growth Core 的垂直包**（只读挂载，与用户私有工作区分离）。
> 本文档讲身份 ②。独立使用（身份 ①）见 `docs/第一次用从这里开始.md`。

## 模型 A：只读包 + 私有工作区

```text
vault/                                  ← Core 工作区根（Agent 从根打开）
├── 00-系统/                             ← Core 结构规则、索引、配置
├── _packages/                           ← 公共垂直包挂载区（只读参考区）
│   └── job-search-bw/      ← 本包（git clone 所得；只读）
└── 求职/                                ← 用户私有工作区（Core 五层，可写）
    ├── 00-raw/                          ← 我的 JD、简历、面试记录
    ├── 01-知识/                         ← 我的草稿与确认后的知识页
    ├── 02-框架/                         ← 我自己长出的判断规则
    ├── 03-实战/                         ← 我的投递记录、行动与验证
    └── 04-复盘/                         ← 我的结果与修正
```

**核心边界**：
- `_packages/job-search-bw/` = **方法论提供者的内容，只读**；更新靠 `git pull`
- `vault/求职/` = **用户自己的领域资产，可写**；正常维护
- 两者**不共用目录树**——`git pull` 永远不碰用户数据

## 挂载（两步）

```bash
cd vault/
mkdir -p _packages
git clone https://github.com/bernardw5174-zfyb/job-search-bw.git _packages/job-search-bw
```

然后在 Agent 里说：**"我要开始求职"** —— Agent 会：
1. 扫描 `_packages/*/manifest.yaml`，按 `domain` 字段匹配（本包 `domain: 求职`）
2. 命中 → 读本包 `skills/` 匹配任务（诊断/关键词/改写）
3. 产出写入 `vault/求职/`（用户工作区）——**绝不写回 `_packages/`**

> 发现机制：Agent 靠读 `manifest.yaml` 发现包，不靠目录名猜测。见 Core 协议（`AGENTS.md`「已挂载的垂直包」节——✅ **已随 Core v0.1.4 落地**，2026-09-18）。

## 升级

```bash
cd vault/_packages/job-search-bw/
git pull
```

- 用户数据零风险（写入从来不在这个目录树里）
- 假设注册表 #14 从 🔶 升 ✅ → `git pull` 即拿到最新验证状态

## 不会 git？三条路径并列

| 路径 | 做法 | 代价 |
|------|------|------|
| **git clone**（推荐） | 上面两步 | 无 |
| **独立 clone** | clone 到任何位置，Agent 打开该目录 | 不用 Core，拿不到 Core 治理能力 |
| **ZIP 下载** | GitHub Release 下载 zip → 解压 → 放入 `_packages/<包名>/` | **无法 `git pull`**——包内方法论的后续更新（含验证状态推进）需手动重下覆盖；不影响用户工作区 |

> ZIP 路径不是"等价入口"：功能上有真实损失（拿不到后续更新）。它解决的是"环境不允许 git"，不是"更简单"。
>
> 💡 **解压工具提示**（2026-09-18 实测）：zip 内文件名为中文（UTF-8 编码），**旧版 `unzip` 命令行工具可能报错**——请用 **Finder 双击／7-Zip／Keka／Windows 资源管理器（Win10+）**解压；命令行可用 `ditto -x -k`（macOS）或 `bsdtar -xf`。

## 边界声明

- **本 repo 不承载任何用户数据**：简历、JD、投递记录等全部在用户工作区（`vault/求职/` 或独立使用时的本地 `00-raw/`、`01-知识/_drafts/`）
- 本包内 `00-raw/`、`01-知识/` 目录为空占位，**仅为独立使用场景保留**；Core 场景下用户数据一律落 `vault/求职/`
- 案例回流：只有人工脱敏、抽象后的共性规律才会回流本 repo（见 `04-复盘/假设注册表-公开版.md` 更新记录）
