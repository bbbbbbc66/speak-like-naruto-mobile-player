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

核心不是词库，是**密度控制**——三条回复最多一个梗。塞满梗的回复一眼假，稀疏才像人。

- 完整设计思路：[`docs/design.md`](docs/design.md)
- 语言系统整理（分层结构 + 置信度清单）：[`docs/language-system.md`](docs/language-system.md)
- 语料证据台账：[`docs/verification-report.md`](docs/verification-report.md)
- 直播间语料采集记录（串词 / 评论话术 / 切片）：[`docs/live-room-corpus.md`](docs/live-room-corpus.md)
- 完整词表：[`skills/speak-like-naruto-mobile-player/references/glossary.md`](skills/speak-like-naruto-mobile-player/references/glossary.md)
- 验收用例：[`docs/test-cases.md`](docs/test-cases.md)

---

## 怎么装

三步。

### 1. 克隆

```bash
git clone https://github.com/18006608230/speak-like-naruto-mobile-player.git
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

10 个核心，够用。全量 40 条见 [glossary.md](skills/speak-like-naruto-mobile-player/references/glossary.md)。

| 梗 | 意思 | 例句 |
| --- | --- | --- |
| 嘉豪 | 装腔作势、用力过猛；也指忍者帅、能秀 | 很嘉豪，豪意值拉满了 |
| 串子 | 假装某群体成员，说离谱话引战招黑 | 别串了，一眼串子 |
| 卡了 | 万能借口，任何失误都说卡了 | 卡了，刚才那波网不好 |
| 我了猪 / 刚 / 塞 / 雷 | 看海的无意义惊叹词 | 我了猪，这也能赢 |
| 雷 / 刚 / 猪咪（形容词） | 无意义形容词，图个味 | 今天吃了个雷刚饭 |
| 断了 | 厉害、牛，夸人用 | 这把断了 |
| 欧打 / oda | 万能动词 | 先去欧打个饭 |
| 阴间 / 阳间 | 机制离谱 / 打法正经 | 这忍者太阴间了 |
| 穿三 | 一个忍者打掉对面三个 | 直接穿三 |
| 红温 / 破防 / 绷不住 | 急了 / 绷不住了 / 忍不住笑 | 没绷住 |

**注意**：「雷 / 刚 / 猪咪」当形容词时**没有实际含义**。别试图理解它，理解就输了。

---

## 项目结构

```
speak-like-naruto-mobile-player/
├── README.md                    ← 你在看这个
├── LICENSE                      MIT
├── CONTRIBUTING.md              怎么投稿新梗
├── .github/workflows/lint.yml   CI 校验
├── skills/speak-like-naruto-mobile-player/
│   ├── SKILL.md                 主文件，唯一入口
│   ├── references/
│   │   ├── glossary.md          梗词表（人读）
│   │   └── examples.md          10 组对话示例
│   └── data/
│       └── glossary.json        梗词表（机器读）
├── docs/
│   ├── design.md                设计决策记录
│   ├── language-system.md       语言系统整理（分层 + 置信度）
│   ├── verification-report.md   语料证据台账
│   ├── live-room-corpus.md      直播间语料采集（串词 / 评论 / 切片）
│   └── test-cases.md            验收用例
└── scripts/lint.py              本地校验脚本
```

---

## 关于词表

0.3.0 收 40 条，其中 27 条 `verified`、13 条 `pending`。

分层逻辑和每个词的置信度来路，见 [语言系统整理](docs/language-system.md)。简单说：

- **verified**：多个来源能对上，或有明确解释
- **pending**：只在弹幕、帖子里出现过，没找到明确解释

**为什么 pending 这么多**：不是没收够，是**不敢编**。比如「我了猪 / 刚 / 塞 / 雷」这组，原本是核心梗，但 2026-11-23 的抖音实查里一次都没抓到原词，只有近似句式。所以整组降级成 pending——自己定的规矩，自己先守。

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
