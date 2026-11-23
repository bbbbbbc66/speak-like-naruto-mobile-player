# 文档地图

`docs/` 不是按顺序写的，是几轮考据叠出来的。这份地图说明**每份解决什么问题、什么时候该看、哪些是过程记录**。

## 一句话导航

| 文档 | 解决什么 | 什么时候看 | 性质 |
| --- | --- | --- | --- |
| [README.md](../README.md) | 装上、触发、看效果 | 所有人，先读这个 | 现行 |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | 怎么投稿新词 / 新构式 / 新场景 | 想补数据 | 现行 |
| [design.md](design.md) | 10 条设计取舍：为什么只做 Skill、为什么控制主文件长度、为什么留 pending | 想知道「凭什么这么设计」 | 现行 |
| [language-system.md](language-system.md) | 这套语言的结构：四层、置信度、句法音系、社会学成因 | 想系统理解，而不是只会用 | 现行 + 判定记录 |
| [primary-corpus-analysis.md](primary-corpus-analysis.md) | 9 张一手截图逐字转录，推出「生成语法」 | 想知道 0.4.0 重构的依据 | 现行结论 + 当时过程 |
| [live-room-corpus.md](live-room-corpus.md) | 直播间逐字语料、串词、评论话术、热门切片清单 | 想查原始语料出处 | 采集记录（第三轮） |
| [verification-report.md](verification-report.md) | 证据分级 A–F、每个词的来路、忍者外号候选 | 想核对某词凭什么叫 verified | 第二轮快照（分级口径仍有效） |
| [test-cases.md](test-cases.md) | 6 条验收用例：会不会收、梗密度对不对 | 装完想自己验一遍 | 现行 |
| [梗词表（人读版）](../skills/speak-like-naruto-mobile-player/references/glossary.md) | 全量词条 + 生成语法 | 查某一个词 / 某一条规则 | 现行（唯一真源的人读镜像） |
| [SKILL.md](../skills/speak-like-naruto-mobile-player/SKILL.md) | AI 实际读到的行为规则 | 想改说话行为 | 现行（给 AI 读） |

## 三条推荐路径

1. **只想用**：README → 安装 → 照 `test-cases.md` 验收。其余不用看。
2. **想改数据 / 补词**：CONTRIBUTING → 人读版词表 → `verification-report.md` 确认证据等级 → 提 PR。
3. **想搞懂这套语言**：`design.md` → `language-system.md` → `primary-corpus-analysis.md` → 回 `live-room-corpus.md` 查原文。

## 阅读时请注意

- **过程记录 ≠ 现行规则**。`verification-report.md`、`live-room-corpus.md`、`primary-corpus-analysis.md` 里带「当时」「第二轮」「0.3.x」「已解除」「已执行」的段落，是几轮考据留下的现场记录。里面写的「当时 40 条」「当时只记文档、不改词条释义」不是当前状态，别照着改数据。
- **现行规则只有两个出处**：`data/glossary.json`（数据）和 `SKILL.md`（行为），两者都由 `scripts/lint.py` 校验，人读版与机器读版五层同源。
- **已移除的词形不会再出现**：0.4.1 判定移除、0.4.2 起全仓库清除，lint 有黑名单防回退。判定逻辑保留在 `language-system.md` 3.1 节，但不作为可用说法。
- **隐私边界**：真实姓名、账号、联系方式、可定位到个人的信息一律不收录；平台 AI 解析只作旁证，不作一手出处。

## 版本现状

**0.4.2** / `schema 1.0 / generative`：49 条词条（verified 42 / pending 7）、6 条构式、15 个雷霆词根、24 个「场景 → 说法」功能位。版本怎么演化、移除了什么、为什么，折叠在 [梗词表的「版本变更记录」](../skills/speak-like-naruto-mobile-player/references/glossary.md#版本变更记录)。
