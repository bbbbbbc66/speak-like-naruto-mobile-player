# speak-like-naruto-mobile-player

让 AI 像火影手游圈玩家一样说话。短句、口语、玩梗、会起哄，也知道什么时候该闭嘴。

[![lint](https://github.com/bbbbbbc66/speak-like-naruto-mobile-player/actions/workflows/lint.yml/badge.svg)](https://github.com/bbbbbbc66/speak-like-naruto-mobile-player/actions/workflows/lint.yml)
![data 0.4.2](https://img.shields.io/badge/data-0.4.2-blue.svg)
![schema 1.0](https://img.shields.io/badge/schema-1.0%20generative-blueviolet.svg)
[![license MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**跳到**：[效果](#demo) · [安装](#install) · [怎么用](#usage) · [核心梗表](#memes) · [为什么是语法](#grammar) · [文档地图](#docs) · [数据现状](#data)

---

<a id="demo"></a>

> **你**：决赛输了，最后一把被翻盘，难受
>
> **AI（装上之前）**：别难过啦！输赢乃兵家常事，下次一定能赢的！加油！
>
> **AI（装上之后）**：卡了。没事，这把对面运气好

> **你**：残血一打三赢了，我是不是有点东西
>
> **AI**：断了。

> **你**：帮我写个请假条，明天上午要去医院
>
> **AI**：好，把时间、事由和抬头给我，我给你写。请假条里一个梗都不会有。

三组合起来才是这个 Skill 的重点：**会玩，也会收**。

---

## 这是什么

一个**说话风格 Skill**。不是工具、不是数据库、不是 App。

装上之后，AI 在闲聊、开玩笑、聊火影手游 / 看海直播的时候，说话像圈里人：句子短、有黑话、会起哄。**聊正事、学习、工作、道歉、认错的时候自动切回正常说话。**

三个设计点，比词表本身重要：

| | 做法 | 为什么 |
| --- | --- | --- |
| **生成语法** | 收 15 个词根 + 6 条构式 + 24 个「场景 → 说法」，而不是把所有词串列成词库 | 词根可以任意组合、顺序不限，合法性靠顺口押韵不靠词典。逐条登记等于把一门语法记成单词表 |
| **密度控制** | 三条回复最多一个梗 | 塞满梗的回复一眼假，稀疏才像人 |
| **会收** | 正事 / 情绪不对时一个梗都不带 | 一个只会玩不会收的风格 Skill，装上就是灾难 |

完整取舍见 [`docs/design.md`](docs/design.md)。

---

<a id="install"></a>

## 怎么装

三步，不需要装依赖、不需要跑服务。

```bash
git clone https://github.com/bbbbbbc66/speak-like-naruto-mobile-player.git
cd speak-like-naruto-mobile-player
```

挑一个你的工具对应的 skills 目录，把整个 Skill 文件夹拷进去：

```bash
# Claude Code
mkdir -p ~/.claude/skills
cp -r skills/speak-like-naruto-mobile-player ~/.claude/skills/

# WorkBuddy
mkdir -p ~/.workbuddy/skills
cp -r skills/speak-like-naruto-mobile-player ~/.workbuddy/skills/
```

> 其他支持 Skill 的工具同理，认准自己的 skills 目录，整目录拷进去即可。

完成后应该是这样：

```
~/.claude/skills/speak-like-naruto-mobile-player/
├── SKILL.md          主文件，唯一入口
├── references/       人读版词表 + 对话示例
└── data/             机器读版，唯一真源
```

新开一个对话，说一句「用火影玩家风格说话」，有反应就装上了。想自己验收，照着 [`docs/test-cases.md`](docs/test-cases.md) 跑几条。

---

<a id="usage"></a>

## 怎么用

### 自动触发

聊到这些内容时会自动切过来，不用手动喊：

- 火影手游：决斗场、上分、抽卡、忍具、通灵、阵容强度
- 看海直播：主播操作、弹幕、连麦
- 明显的闲聊、吐槽、发疯、分享对局

### 手动触发

直接说：「用火影玩家风格说话」／「来点火影味」／「说点圈里的话」。

### 什么时候不触发

正事、学习、工作、认真求助、道歉、安慰、对方情绪不对——**一律正常说话，一个梗都不带**。这条不是可选项。

---

<a id="memes"></a>

## 有哪些梗

11 个核心，够用。全量 49 条词条 + 6 条构式 + 15 个词根 + 24 个「场景 → 说法」功能位见 [梗词表（人读版）](skills/speak-like-naruto-mobile-player/references/glossary.md)。

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

<a id="grammar"></a>

## 为什么是语法，不是词库

一手语料里有一句被作者赞过的教学评论，直接推翻了「把每个词串都登记成词条」的做法：

> 雷、塞、猪、刚、爆、霆这几个字都可以用，甚至可以**两两相组，不用在乎顺序，也没有固定搭配**……只要读着顺口押韵即可。

于是数据层是这么组织的：

```
L0  词根池    霆 雷 塞 钢 爆 珠 蛋 骚 缸 猪 裂 球 阴 亏 替
       ↓  任意顺序、任意长度、两两相组，只求顺口押韵
L1  自由串词  钢蛋雷塞球爆珠 / 雷塞钢霆 / 爆骚缸
       ↓  加词缀、加动物/语气词，递归堆叠
L2  词缀构式  臭 / 骚 + 动词 → 臭a、骚顶、臭砍
               极限形态 → 雷霆暴力无敌大臭雷塞猪头肉a
```

**没见过的组合不代表错**，只要顺口。所以 `constructions` 只收规则，不收规则生成出来的无限实例；词表里剩下的 49 条是**不能由规则推出来、需要单独记住**的词。这层的完整推导见 [`docs/primary-corpus-analysis.md`](docs/primary-corpus-analysis.md)。

---

<a id="docs"></a>

## 文档怎么读

文档不少，先按目的挑，别从头顺着读。完整导航见 [`docs/README.md`](docs/README.md)。

| 你想… | 看这份 |
| --- | --- |
| **装来用** | 本页 [安装](#install) ＋ [`docs/test-cases.md`](docs/test-cases.md)（自己验收） |
| **看 AI 到底会怎么说话** | [`SKILL.md`](skills/speak-like-naruto-mobile-player/SKILL.md)（这是给 AI 读的主文件）＋ [10 组对话示例](skills/speak-like-naruto-mobile-player/references/examples.md) |
| **查一个词 / 一条规则** | [梗词表（人读版）](skills/speak-like-naruto-mobile-player/references/glossary.md)，字段与 [机器读版](skills/speak-like-naruto-mobile-player/data/glossary.json) 一一对应 |
| **搞懂为什么这么设计** | [`docs/design.md`](docs/design.md)（10 条取舍）＋ [`docs/language-system.md`](docs/language-system.md)（分层结构、置信度、社会学成因） |
| **查证据、看考据过程** | [`docs/verification-report.md`](docs/verification-report.md)（证据分级）＋ [`docs/live-room-corpus.md`](docs/live-room-corpus.md)（直播间逐字语料）＋ [`docs/primary-corpus-analysis.md`](docs/primary-corpus-analysis.md)（9 张一手截图） |
| **补一个新词 / 一条构式** | [`CONTRIBUTING.md`](CONTRIBUTING.md) |

> `docs/` 里带「当时」「已解除」「0.3.x」字样的段落是**过程记录**，不是现行规则。现行规则只以 `data/glossary.json` 和 `SKILL.md` 为准。

---

## 项目结构

```
speak-like-naruto-mobile-player/
├── README.md                    ← 你在看这个
├── LICENSE                      MIT
├── CONTRIBUTING.md              怎么投稿新梗
├── .github/workflows/lint.yml   CI 校验
├── skills/speak-like-naruto-mobile-player/   ← 安装时拷这个目录
│   ├── SKILL.md                 主文件，唯一入口（AI 读）
│   ├── references/
│   │   ├── glossary.md          梗词表 + 生成语法（人读）
│   │   └── examples.md          10 组对话示例
│   └── data/
│       └── glossary.json        唯一真源（机器读，schema 1.0）
├── docs/
│   ├── README.md                文档地图 / 阅读顺序
│   ├── design.md                设计决策记录
│   ├── language-system.md       语言系统整理（分层 + 置信度）
│   ├── verification-report.md   语料证据台账
│   ├── live-room-corpus.md      直播间语料采集
│   ├── primary-corpus-analysis.md  一手语料分析 / 生成语法推导
│   └── test-cases.md            验收用例
└── scripts/lint.py              本地校验（五层同源 + 黑名单防回退）
```

---

<a id="data"></a>

## 数据现状

当前 **0.4.2**（`schema 1.0 / generative`）：**49 条词条**（verified 42 / pending 7）＋ **6 条构式** ＋ **15 个雷霆词根** ＋ **24 个场景功能位**。机器读版 `data/glossary.json` 是唯一真源，人读版与它五层同源，CI 逐项校验，另外有一条黑名单防止已移除的词形被加回来。

版本怎么演化、移除了什么、为什么，折叠在 [梗词表的版本变更记录](skills/speak-like-naruto-mobile-player/references/glossary.md#版本变更记录) 里，首页不重复。

这里只留两条结论：

- **verified**：多个来源能对上，或有明确解释 / 一手逐字语料
- **pending**：只在弹幕、帖子里出现过，没找到明确解释，或只有二手转述

`pending` 不是没收够，是**不敢编**。**加进来和算核实是两件事**——含义讲不清就先挂着，别硬造释义污染整张表。知道某个 pending 怎么用的，欢迎提 PR。

---

## 贡献

见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。三条规矩：填满字段、不碰私人信息、不确定标 `pending`。

提 PR 前本地跑一遍：

```bash
python3 scripts/lint.py
```

---

## License

MIT
