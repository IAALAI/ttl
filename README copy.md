# ttl

Victoria 3 内容模组：新增若干可建国的霸权级国家，并围绕 **西欧联合帝国（BAF）** 提供日志与脚本按钮玩法。

## 新增国家一览

| Tag | 英文名 | 中文名 | 等级 | 成立模式 | 首都 | 主要玩法 |
|-----|--------|--------|------|----------|------|----------|
| `BAF` | Western Europe | 西欧 | hegemony | 主要 | 伦敦郡 `STATE_HOME_COUNTIES` | 西欧风云 / 征服日志链 |
| `EAS` | Eurasian Soviet Socialist People's Republic | 欧亚苏维埃社会主义人民共和国 | hegemony | 主要 | 莫斯科 `STATE_MOSCOW` | 占位向建国 |
| `GCH` | Greater China | 大中华 | hegemony | 次要（默认） | 未设 | 需汉文化 + 控制北京 |
| `TWO` | Terminus Dominators | 终焉支配者 | hegemony | 主要 | 未设 | 内容未完成 |

以上均为模组在 `common/country_definitions/` 中新增的 tag；旗帜、动态国名等见对应目录。

---

## BAF — 西欧 / 联合帝国

**定位：** 英、法及西欧遗产的统一霸权。主流文化：`british`、`french`、`wallonian`、`dutch`、`portuguese`、`spanish`。

**建国：** Major formation  
- 宣称地：不列颠诸州、低地、法国本土核心、伊比利亚核心（约需 80%）  
- 外交博弈：`dp_unify_baf` / `dp_leadership_baf`  
- AI 不会主动建国（`ai_will_do = no`）

**动态国名（节选）**

| 条件 | 名称 |
|------|------|
| 默认 | 帝国联邦 / Union of the West |
| 君主制或神权 | 不列颠及法兰西联合帝国 |
| 委员会共和 | 人民公社 |

**`特色能力`**

具备不列颠特色 IG + 法兰西特色 IG, 超绝 小市民 神棍 军队 资本家

属性惊人战力高,合并简单,日志全是buff和奖励,巨爽巨轮椅

**配套内容**

1. **西欧风云** — 整合低地、伊比利亚等内部问题  
2. **西欧征服** — 中欧（莱茵 / 多瑙邦联）、北美（含哈德逊湾公司）、南美、北非、中东、南亚、东南亚等扩张日志与按钮  

日志会借用原版 tag 作为傀儡/工具国（非本模组新建国定义），例如：

- `RHN` 莱茵邦联  
- `KUK` 多瑙侧相关  
- `HBC` 哈德逊湾公司  

---

## EAS — 欧亚苏维埃社会主义人民共和国

**定位：** 横跨欧亚的红色霸权向建国目标。首都莫斯科。  

**主流文化：** `russian`、`han`、`east_german`、`ryukyuan`、`tatar`、`vietnamese` 等（需与建国国共享至少一个主流文化，建国选项才会出现）。

**建国：** Major formation  
- 宣称地（需全部控制）：伦敦、巴黎、北京、京都  
- 目前复用德国统一类外交博弈（占位）  
- `possible = always`，AI 不会主动建国  

旗帜暂复用俄国 CoA

**`特色能力`**

超高劳动力比例,特色LAW阶级叙事,特色迁移重工业

---

## GCH — 大中华

**定位：** 泛中华文化圈的统一国家。主流文化覆盖汉、满、藏、朝、越、蒙及多种华南/西南文化等。

**建国：** 非常规 major（无独立 unify/leadership 博弈）  
- 宣称地：中国本土、满蒙藏新、朝鲜、中南半岛北部及部分西伯利亚 / 中亚相关州  
- 条件：主流文化为 `han`，且控制北京  

**动态国名（节选）**

| 政体倾向 | 名称 |
|----------|------|
| 默认 | 泛中华 |
| 君主 / 神权 | 中华帝国 |
| 共和 | 泛中华合众国 |
| 社会主义 | 中华社会主义人民共和国联盟 |
| 法西斯 | 大华夏国 |

旗帜定义里写的是 `GHC`（与国家 tag `GCH` 不一致），若国旗异常需核对 `flag_definitions`。

以后记得微调颜色,比如默认与传统形态是暗黄色,蓝线和红色都是亮红色,黑线是暗红色

**`特色能力`**

还要啥自行车...啊!都这样了,还要啥自行车啊!!!

---

## TWO — 终焉支配者

**定位：** 终局向「世界秩序」霸权。文化混合：`british`、`han`、`french`、`north_german`、`south_german`、`russian`。

**建国：** 标了 Major，但宣称州列表与 `possible` 仍为空，外交博弈暂复用德国统一；内容尚未完成，目前基本不可正常使用。

---

## 相关文件

```
ttl/common/
├── country_definitions/023_country_definitions.txt
├── country_formation/023_formation_countries.txt
├── dynamic_country_names/23_dynamic_country_names.txt
├── flag_definitions/ttl.txt
├── coat_of_arms/coat_of_arms/23_countries_ttl.txt
├── diplomatic_plays/tw_diplomatic_plays.txt      # BAF 统一博弈
├── journal_entries_j/30_baf.txt                  # BAF 日志
├── journal_entry_groups/001_two_groups.txt
└── scripted_buttons/30_baf.txt                   # BAF 按钮
```

本地化：`localization/english/tw_l_english.yml`、`localization/simp_chinese/tw_l_simp_chinese.yml`
