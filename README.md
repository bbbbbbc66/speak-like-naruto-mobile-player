# speak-like-naruto-mobile-player

让 AI 像火影手游圈玩家一样说话。短句、口语、玩梗、会起哄，也知道什么时候该闭嘴。

> **你**：决赛输了，最后一把被翻盘，难受
>
> **AI（装上之前）**：别难过啦！输赢乃兵家常事，下次一定能赢的！加油！
>
> **AI（装上之后）**：卡了。没事，这把对面运气好

---

## 这是什么

一个**说话风格 Skill**。不是工具、不是数据库、不是 App。

装上之后，AI 在闲聊、开玩笑、聊火影手游 / 看海直播的时候，说话像圈里人：句子短、有黑话、会起哄。**聊正事、学习、工作、道歉、认错的时候自动切回正常说话。**

核心不是词库、也不是语法本身，是**密度控制**——三条回复最多一个梗。塞满梗的回复一眼假，稀疏才像人。

- 完整设计思路：[`docs/design.md`](docs/design.md)
- 语言系统整理（分层结构 + 置信度清单）：[`docs/language-system.md`](docs/language-system.md)
- 语料证据台账：[`docs/verification-report.md`](docs/verification-report.md)
- 直播间语料采集记录（串词 / 评论话术 / 切片）：[`docs/live-room-corpus.md`](docs/live-room-corpus.md)
- 一手语料分析（雷霆语言系统的生成语法 / 词根池 / 场景映射）：[`docs/primary-corpus-analysis.md`](docs/primary-corpus-analysis.md)
- 完整词表：[`skills/speak-like-naruto-mobile-player/references/glossary.md`](skills/speak-like-naruto-mobile-player/references/glossary.md)
- 验收用例：[`docs/test-cases.md`](docs/test-cases.md)

---

## 怎么装

三步。

### 1. 克隆

```bash
git clone https://github.com/bbbbbbc66/speak-like-naruto-mobile-player.git
```

### 2. 建 skills 目录（已有就跳过）

```bash
mkdir -p ~/.claude/skills
```

> 其他工具对应自己的 skills 目录，结构一样，整目录拷进去即可。

### 3. 复制进去

```bash
cp -r speak-like-naruto-mobile-player/skills/speak-like-naruto-mobile-player ~/.claude/skills/
```

完成后应该是这样：

```
~/.claude/skills/speak-like-naruto-mobile-player/
├── SKILL.md
├── references/
└── data/
```

新开一个对话，说一句「用火影玩家风格说话」，有反应就装上了。

---

## 怎么用

### 自动触发

聊到这些内容时会自动切过来，不用手动喊：

- 火影手游：决斗场、上分、抽卡、忍具、通灵、阵容强度
- 看海直播：主播操作、弹幕、连麦
- 明显的闲聊、吐槽、发疯、分享对局

### 手动触发

直接说：

- 「用火影玩家风格说话」
- 「来点火影味」
- 「说点圈里的话」

### 什么时候不触发

正事、学习、工作、认真求助、道歉、安慰、对方情绪不对——**一律正常说话，一个梗都不带**。

这条不是可选项。一个只会玩不会收的风格 Skill，装上就是灾难。

---

## 有哪些梗

11 个核心，够用。**这套话是生成语法，不是词库**：词根可以任意组合，构式 C1–C6 生成具体说法。全量 49 条词条 + 6 条构式 + 15 个词根 + 24 个「场景 → 说法」功能位见 [glossary.md](skills/speak-like-naruto-mobile-player/references/glossary.md)。

| 梗 | 意思 | 例句 |
| --- | --- | --- |
| 串子 | 假装某群体成员，说离谱话引战招黑 | 别串了，一眼串子 |
| 卡了 | 万能借口，任何失误（含说错话）都说卡了 | 卡了，刚才那波网不好 |
| 我了 X / 我嘞 X | 无意义惊叹词，X 用词根随便换、顺序不限 | 我了雷，这也能赢 |
| 雷 / 刚（当形容词） | 无意义形容词，图个味 | 今天吃了个雷饭 |
| 猪咪（当形容词） | 无意义形容词，纯装饰 | 今天很猪咪 |
| 断了 | 厉害、牛，夸人用 | 这把断了 |
| 欧打 | 万能动词 | 先去欧打个饭 |
| 阴间 / 阳间 | 机制离谱 / 打法正经 | 这忍者太阴间了 |
| 穿三 | 一个忍者打掉对面三个 | 直接穿三 |
| 红温 / 破防 / 绷不住 | 急了 / 绷不住了 / 忍不住笑 | 没绷住 |
| 绝活哥 | 只玩一个冷门忍者，还玩得很绝 | 又是绝活哥 |

**注意**：「雷 / 刚 / 猪咪」和词根串**没有实际含义**。别试图理解它，也别给它编释义，编了就输了。

---

## 项目结构

```
speak-like-naruto-mobile-player/
├── README.md                    ← 你在看这个
├── LICENSE                      MIT
├── CONTRIBUTING.md              怎么投稿新梗
├── .github/workflows/lint.yml   CI 校验（五层同源）
├── skills/speak-like-naruto-mobile-player/
│   ├── SKILL.md                 主文件，唯一入口
│   ├── references/
│   │   ├── glossary.md          梗词表 + 生成语法（人读）
│   │   └── examples.md          10 组对话示例
│   └── data/
│       └── glossary.json        梗词表 + 生成语法（机器读，唯一真源）
├── docs/
│   ├── design.md                设计决策记录
│   ├── language-system.md       语言系统整理（分层 + 置信度）
│   ├── verification-report.md   语料证据台账
│   ├── live-room-corpus.md      直播间语料采集（串词 / 评论 / 切片）
│   ├── primary-corpus-analysis.md  一手语料分析（生成语法 / 词根池）
│   └── test-cases.md            验收用例
└── scripts/lint.py              本地校验（五层结构）
```

---

## 关于词表

**0.4.0 起这不是词库，是生成语法**：词根池 15 个、构式 6 条、场景功能位 24 个，加 49 条词条（verified 42 / pending 7）。机器读版 `data/glossary.json` 是唯一真源，`schema` 为 1.0，CI 校验五层同源。

历史：0.3.1 补 5 条低争议词 → 0.3.2 按圈内裁定补 14 条（已破圈词组、忍者外号 10 条、川祁语录 2 句）→ 0.3.3 人工核对把「青春哥」更正为「红狗」，到 59 条。0.4.0 把四条「我了 X」pending 合并成构式 C1，词条数降到 55。0.4.1 按用户裁定移除 6 条，降到 49 条；0.4.2 把这 6 个词形从全仓库（含本页核心梗表、SKILL.md、示例、词条释义与 docs）彻底清除（理由见 [梗词表 0.4.1 / 0.4.2 小节](skills/speak-like-naruto-mobile-player/references/glossary.md)）。收词依据见 [直播间语料采集](docs/live-room-corpus.md) 第 7 节，改版依据见 [一手语料分析](docs/primary-corpus-analysis.md)。

分层逻辑和每个词的置信度来路，见 [语言系统整理](docs/language-system.md)。简单说：

- **verified**：多个来源能对上，或有明确解释 / 一手逐字语料
- **pending**：只在弹幕、帖子里出现过，没找到明确解释，或只有二手转述

**为什么还留着 pending**：不是没收够，是**不敢编**。川祁语录两句是圈内点名要加的，但只有公众号二手转述，照规矩挂 `pending` —— **加进来和算核实，是两件事**。原先那组「我了猪 / 刚 / 塞 / 雷」不是被删了，是一手语料证明它们属于同一条构式，收进 C1 了。自己定的规矩，自己先守。

**首页这 11 个核心是「说话时会用的说法」，和词表登记不是一一对应**：0.4.1 起，非火影圈原生的破圈梗及其派生说法、两条固定搭配实例、字母写法重复登记、语境不明的专名义项共 6 条不再登记为词条；0.4.2 起这些词形在本仓库任何文件中都不再出现，Skill 不会、也不应该说它们。

看到 `pending` 的词，说明「听说过但还没人讲清楚」。知道怎么用的，欢迎提 PR。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。三条规矩：填满字段、不碰私人信息、不确定标 pending。

提 PR 前本地跑一遍：

```bash
python3 scripts/lint.py
```

---

## License

MIT
