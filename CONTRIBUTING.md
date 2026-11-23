# 投稿新梗

欢迎补梗。这里只有三条规矩，看完就能提交。

## 30 秒版（最常见：补一个词条）

1. 先 [搜一下词表](skills/speak-like-naruto-mobile-player/references/glossary.md)，确认没收过、也不是某条构式能生成的实例
2. 同时改 `data/glossary.json` 的 `terms` 和 `references/glossary.md` 的「词表」表，字段填满，拿不准就标 `pending`
3. 跑 `python3 scripts/lint.py`，通过再提交
4. PR 里写清楚出处（哪个直播、哪类评论区、哪张截图）

要补的是**规则、场景或词根**，往下看第 1 节判断投到哪一层。

**0.4.0 起数据模型是生成语法**：`data/glossary.json` 里不只有 `terms`，还有 `roots` / `constructions` / `functions` / `pragmatics`。投稿前先判断你要补的是哪一类。

## 1. 先判断投什么

| 你手里的东西 | 加到哪 | 必填字段 |
| --- | --- | --- |
| 一个具体词 / 忍者外号 | `terms` | `term` `pinyin` `meaning` `usage` `example` `source` `status` |
| 一条**可自由组合的规则**（如「我了 X」「臭 / 骚 + 动词」） | `constructions` | `id`（往下排 C7…）`name` `pattern` `function` `examples` `status` `source` |
| 某个场景该怎么说 | `functions` | `scene` `options` `mechanism` `source` |
| 一个新的词根 | `roots.thunder` | 必须附一手逐字语料；15 个词根以图 2 玩家自整理表为准，别凭语感加 |

**别把构式的无限实例收成词条**：「臭猪 a」「臭塞雷猪 a」是 C3 同一条规则的展开，逐条加进 `terms` 只会让词表无限膨胀。词根可以任意组合，没见过的组合不代表错，只要顺口押韵。

`terms` 里可加可选的 `construction` 字段，指向某条构式的 id（如 `"construction": "C6"`）。CI 会校验这个引用真实存在。

词条字段示例：

```json
{
  "term": "词本身",
  "pinyin": "拼音，空格分隔",
  "meaning": "一句话说清什么意思，别超过 30 字",
  "usage": "常见搭配，用、顿号隔开",
  "example": "一句真的能说出口的例句",
  "source": "看海直播 / 抖音评论 / 玩家口头禅",
  "status": "verified 或 pending"
}
```

**两个文件都要改**：`data/glossary.json`（机器读，唯一真源）和 `references/glossary.md`（人读）。CI 校验**五层同源**：词条一一对应、构式 id 一一对应、功能位场景一一对应、15 个词根都在人读版里；另外会检查构式引用是否有效、已合并进构式的词有没有被偷偷加回词条表。哪一层对不上，CI 直接拒。

## 2. 什么能收，什么不能收

能收：

- 火影手游、看海直播间里真实流传的说法
- 有具体出处（哪个直播、哪类评论区、哪个群、哪张一手截图）
- 意思能讲清楚，哪怕很无厘头
- **无意义词**：如实写「无实际含义，纯装饰」，别给它硬编一个意思

不能收：

- 真实人名、手机号、账号、任何能定位到具体个人的信息
- 纯脏话、人身攻击、地域/性别歧视
- 你自己现编的"梗"——看着像梗但没人说过，不收
- 为了凑数把同一个词换个写法再收一遍
- 平台 AI 生成的释义当**一手出处**（页面自标「仅供参考」，只能作旁证）
- 构式规则能生成的无限词串，逐条塞进 `terms`
- **0.4.1 已判定移除、0.4.2 起全仓清除的词形** —— 别加回来，`scripts/lint.py` 有黑名单校验，出现即报错。判定逻辑见 [`docs/language-system.md`](docs/language-system.md) 3.1 节

## 3. 不确定就标 pending

`status` 只有两个值，词条和构式都适用：

- `verified`：你确认过这个说法 / 规则在圈里真的这么用，意思也对
- `pending`：听说过、但不确定确切含义或出处，或只有二手转述

**宁标 pending，别硬编意思。** 编出来的释义会污染整个词表，比少一条严重得多。证据分级口径见 [`docs/verification-report.md`](docs/verification-report.md)。

## 提交

1. Fork 本仓库
2. 新建分支：`git checkout -b add-term-<词>` 或 `add-construction-<规则>`
3. 改完本地跑一遍 `python3 scripts/lint.py`，确保通过（五层同源 + 词形黑名单 + 死链检查都在里面）
4. 提 PR，标题写 `feat(glossary): 新增 <词>` 或 `feat(construction): 新增 <规则>`

PR 描述里请附上出处，一句"我在某个直播间听过"不够，说说具体场景。拿一手截图 / 逐字转写最有用。
