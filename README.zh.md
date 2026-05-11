# agent-colleague-dashboard · 中文版

[English](README.md) | **中文**

![banner](docs/screenshots/social-preview.png)

> 把你的 Claude Code `CLAUDE.md` 和 `subagent` **变成可看、可对话、可审计**的"博主主页"——配上推理透明 + `CLAUDE.md` ↔ `agent` 服从度检查。

## 📖 术语对照（先记住这几个英文 → 对应的真实文件）

| 文中说的 | 实际是磁盘上的什么 | 说明 |
|---|---|---|
| **`CLAUDE.md`** | `<项目根>/CLAUDE.md` 或 `~/.claude/CLAUDE.md` | 项目"宪章" / 全局行为守则。Claude Code 启动时会自动读 |
| **`agent.md`** / **`subagent`** | `.claude/agents/<name>.md`（项目级）<br>或 `~/.claude/agents/<name>.md`（用户级） | 单个 subagent 的 prompt 定义文件 |
| **`SKILL.md`** | `.claude/skills/<skill-name>/SKILL.md` | Claude Code 的"插件" — 本项目就是 4 个 skill |
| **`/dashboard`** 等 | Slash command | 在 Claude Code 终端里直接输入触发 |
| **frontmatter** | `.md` 文件开头的 `---` 包裹的 YAML | 比如 agent 的 `name` `tools` `model` 字段 |
| **persona JSON** | LLM 从 `.md` 推断出来的人物画像数据 | 缓存在 `~/.claude/dashboard-cache/<hash>.json` |

一个包含 4 个 Claude Code skill 的 bundle，你能用它：

| Slash 命令 | 干嘛的 |
|---|---|
| `/dashboard` | 把你的 CLAUDE.md 和 `agents/*.md` 渲染成拟人化 HTML 主页（自动判断 Focus / Team / Charter 布局） |
| `/agent-create <name> "<描述>"` | 用自然语言起草一个新 agent（自动继承 CLAUDE.md 风格） |
| `/agent-edit <name> "<需求>"` | 用自然语言改 agent（带备份 + diff 预览 + 你确认） |
| `/claude-edit "<需求>"` | 同上，改的是 CLAUDE.md |

4 个 skill 形成完整闭环：**Read**（dashboard）→ **Create**（agent-create）→ **Update**（agent-edit / claude-edit）。全程留在你的终端 + 本地浏览器。**无 server、无 API key 管理、零外部依赖。**

---

## 为什么要做这个

每个 Claude Code 重度用户都会撞上同一堵墙：

1. **看不见你装了啥**。`CLAUDE.md` 和 `.claude/agents/*.md` 都是裸 markdown，给新人 onboard 像让他读法律条文。
2. **记不住 agent 名字**。从各种 plugin 装了一打 subagent？谁还记得每个干啥的。
3. **agent 之间会暗中打架**。CLAUDE.md 说"先想再写"，某个 vibe-coder agent 说"ship fast, fix later"。**无声冲突**，到生产出 bug 才发现。
4. **改起来烦**。想让某条规则宽松一点？得手撕 YAML frontmatter 和长 prompt。

**这套 skill 把你的配置当一个能看见、能对话、能调整的团队**——而不是当配置文件。

---

## 你会拿到什么

### `/dashboard` —— 4 种布局，自动判断

```
0 个 agent  → CLAUDE.md Charter 模式（全屏宪章）
1 个 agent  → Focus 模式（单 agent 完整人物主页）
2+ agent    → Team 模式（CLAUDE.md hero + 可点击卡片墙）
```

每页都渲染：

- **人设** —— 中文花名、头像 emoji、MBTI、6 维性格雷达、贴纸 hashtag
- **行为** —— 口头禅、招牌技能、典型一天、瞳孔地震警告（厌恶清单）
- **同事关系** —— 跟哪些 agent 默契、跟谁理念摩擦、跟谁水火不容
- **同事评价** —— App Store 风的星级吐槽
- **🔬 推理报告** —— 每个推断字段配 verbatim 源 prompt 引用 + 推理逻辑。**LLM 的解读是可审计的**，不是黑盒
- **📄 源 .md（只读）** —— 页面底部，跟人设对照核对原文
- **✏️ 修改 FAB** —— 右下角浮动按钮 → 弹窗写自然语言 → 复制 `/agent-edit` 命令

### CLAUDE.md ↔ agent 服从度评分 —— 这是真差异化

打开 `/dashboard --claude` 时，dashboard 会对每个 agent 算一个 **0–100 的"服从度"分数**，低于 50 自动 flag + 给具体修复建议。

> ⚠️ 阿强 服从度仅 28 — 他的 prompt 鼓励 "ship fast, fix later"，跟原则 1/2 直接冲突。建议：要么改阿强的 prompt（让它加一条"验证再宣告完成"），要么承认这条原则不适合 vibe-coder 类型的角色。

**你的配置文件第一次会自己讲"我们团队内部理念冲突"**。这是 dashboard 从"展示工具"变成"诊断工具"的关键。

### 用自然语言改

```
/agent-edit code-reviewer "对 magic number 宽容一点"
/agent-edit vibe-coder "加一条 when invoked: 先看现有测试"
/agent-edit planner "把 model 从 sonnet 换成 opus"

/claude-edit "在末尾加原则 5：组合优于继承"
/claude-edit "把原则 3 改得宽松一些，允许显式要求时重构"
```

每次编辑：
1. 自动备份（`.bak.<纳秒时间戳>`）
2. 失效 dashboard 缓存
3. 调 Claude Code **Edit 工具**——展示 diff 给你看，**写入前**等你 approve
4. 报告：改了啥 + 备份在哪 + 怎么看新版人设

**不写自定义 diff UI / 权限代码**——复用平台已有的信任边界。

---

## 安装

### 方案 1 —— 用户级（所有项目共用）

```bash
git clone https://github.com/luck1ncoder/agent-colleague-dashboard.git
cp -R agent-colleague-dashboard/.claude/skills/* ~/.claude/skills/
# 重启 Claude Code
```

之后在任何项目里：`/dashboard`（或其他 3 个命令）。

### 方案 2 —— 项目级（只装这一个项目）

```bash
cd your-project
git clone https://github.com/luck1ncoder/agent-colleague-dashboard.git /tmp/acd
cp -R /tmp/acd/.claude/skills/* .claude/skills/
# 在这个项目里重启 Claude Code
```

### 要求

- Claude Code v2.0+
- Python 3（macOS 自带；**不需要 pip install 任何东西**，纯 stdlib）
- macOS（用了 `open` 启浏览器；改 `xdg-open` / `start` 即可移植 Linux/Windows）

---

## 技术架构

```
.md 文件 → 解析 frontmatter → LLM 推断 persona JSON → render.py + HTML 模板 → open 浏览器
```

- **模板引擎**：105 行手写，支持 `{{var}}` / `{{var.path}}` / `{{#each list}}...{{/each}}`（支持嵌套）/ `{{#if cond}}...{{/if}}`。stdlib only。
- **Frontmatter 解析**：30 行，处理 agent 文件实际用到的简单 YAML 子集。
- **模式检测**：扫 project + user dir，去重，按 agent 数量挑布局。
- **缓存**：内容 SHA256 hex 16 → persona JSON 存 `~/.claude/dashboard-cache/`。同内容不重推断。
- **编辑流程**：备份 → 失效缓存 → Edit 工具弹 diff → 你 approve → 写入。**Edit 工具本身就是 diff/确认 UX**。

**43 个单元 + E2E 测试**，stdlib `unittest` 写的，零外部测试 dep。

---

## 项目结构

```
.claude/skills/
├── dashboard/                    # /dashboard
│   ├── SKILL.md
│   ├── scripts/                  # render.py / tmpl_engine.py / frontmatter.py / ...
│   ├── templates/                # 3 个 HTML 模板（Focus / Team / Charter）
│   ├── samples/                  # 标准 persona JSON 样本
│   └── tests/                    # 43 个测试
├── agent-create/SKILL.md         # /agent-create
├── agent-edit/SKILL.md           # /agent-edit
└── claude-edit/SKILL.md          # /claude-edit
```

---

## Demo 流程

```bash
# 装好之后，在任何含 .claude/agents/*.md 的项目里
/dashboard
# → 浏览器开 Team 或 Focus 视图，看 agent 数量决定

/agent-create design-reviewer "审 UI 一致性、组件 token 用法、a11y 基础"
# → 起草新 agent 文件，给你看完整内容，你 approve

/dashboard --agent design-reviewer
# → 看新 agent 的完整人物主页

# 1 分钟后：在任何页面点 ✏️，写要改的东西，复制命令粘到终端
/agent-edit design-reviewer "也加一条：检查响应式断点"
# → 备份 + diff + 你 approve + 完成
```

---

## 命名梗 · 阿珍 × 阿强

两个种子 agent 用了《阿珍爱上了阿强》的歌名：

- **阿珍** = code-reviewer（ISTJ 完美主义，严谨到 bug 都怕）
- **阿强** = vibe-coder（ENFP ship 党，"先跑起来再说"）

正好对应 `coop: bad` 的"水火不容"关系——**这对名字本身就是一个 affinity 失败案例**，跟我们的服从度评分形成 self-referential 的小彩蛋。

---

## 路线图（还没做）

- 服从度的**双向调整建议**：不只 flag 冲突，还给具体 patch
- `/agent-delete` + 每个 agent 的编辑历史时间线 + 一键回滚
- **跨项目 CLAUDE.md 对比**："这 5 种流行的项目宪章风格"
- 真本地 web app 模式（跳过复制粘贴循环）
- **可导出"团队海报"**（一张 PNG 分享朋友圈）

---

## 致谢

- **Andrej Karpathy** 的 CLAUDE.md（4 大原则：先想再写 / 极简为先 / 外科手术式改动 / 目标驱动）—— 整个项目的设计语言和服从度评分概念都受他启发
- **VoltAgent 的 `awesome-claude-code-subagents`** —— agent prompt 模式参考
- **Anthropic** —— Claude Code 的 skill 系统 + Edit/Write 工具的权限 prompt，是这套方案不需要写后端的关键

---

## License

MIT —— 见 [LICENSE](LICENSE)。

---

## 一句话宣传

> **把你的 AI 团队当人看。让 CLAUDE.md 和 subagent 像同事一样被看见，用聊天的方式编辑，让 dashboard 告诉你哪些配置正在暗中打架。**
