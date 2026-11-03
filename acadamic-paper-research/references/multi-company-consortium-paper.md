# 多公司联合工业论文分析参考

当论文作者来自 ≥3 家不同公司时，元数据提取和呈现方式需调整。

## 特征识别

- 第一页作者列表按机构分组排列（通常用上标或分段标识）
- 多家公司各指定至少一位通讯作者（corresponding author）
- 可能出现知名学术研究者以企业身份参与（如 Mark Handley 以 OpenAI、Torsten Hoefler 以 Microsoft）
- 致谢名单通常极长（50-120+人），反映大规模工程合作
- 通常为 arXiv 预印本或行业白皮书，不标注投稿会议

## 元数据提取调整

### 作者分组

按机构列出，不用传统的"作者-单位"一对一表：

```
| 机构 | 核心作者 | 通讯作者 |
|------|---------|---------|
| OpenAI | Joao Araujo, Alex Chow, ... | Mark Handley |
| Microsoft | S. Anantharamu, ... | Jithin Jose |
```

### 通讯作者处理

- 每家公司至少一位通讯作者
- 如有学术名人以企业身份参与，特别标注：
  `Mark Handley (UCL)，以 OpenAI 身份参与`
  `Torsten Hoefler (ETH Zurich)，以 Microsoft 身份参与`

### 课题组

纯工业论文标注："纯工业界论文，无学术课题组"
学术合作者标注其原机构。

### 致谢段

大型工业论文致谢通常包含：
- 各公司工程团队完整名单（50+ 人）
- 不需要逐人列出，概述规模即可
- 如无资助项目编号，标注"未列出具体资助号"

## 案例：MRC + SRv6 论文 (arXiv:2605.04333)

5家公司联合，约50+作者：
- OpenAI (11人，通讯: Mark Handley)
- Microsoft (10人，通讯: Jithin Jose)  
- AMD (10人，通讯: Rip Sohan)
- Broadcom (10人，通讯: Eric Spada)
- Nvidia (10人，通讯: Sayantan Sur)

致谢约120+人名。无会议信息（arXiv预印本）。
