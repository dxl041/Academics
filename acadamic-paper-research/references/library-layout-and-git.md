# 论文库的目录归属、副本判别与 git 化

本文件记录 2026-11 OrderedChaos 会话踩到的"库放哪里"问题与可复用解法。核心结论：**目录规范只能有一个事实源，且必须用文件系统实测确认，不能凭会话开头的 cwd 或旧记忆断言。**

---

## 1. 先判断两个路径是不是同一个目录

用户提到两个看起来一样的路径时（例如 `~/Academics` 与 `/mnt/d/ObsidianWorkspace/Academics`），**不要**凭"子目录名一致、文件大小与 mtime 一致"就认定是软链或挂载。实测三件套：

```bash
ls -ld <A> <B>
readlink -f <A>; readlink -f <B>          # 解析软链后仍不同 → 两份独立目录
stat -c '%d:%i %n' <A> <B>                # dev:inode；dev 不同 = 不同文件系统
df -h <B> | tail -1                        # /mnt/d 显示 9p/drvfs，~ 是 ext4
```

案例：两边 HARP 目录的 pdf/notes 大小与 mtime 完全相同，但 `dev` 分别是 2096(ext4) 与 70(drvfs) → 是历史 `cp -p/rsync` 出来的两份拷贝，不是同一目录。这类"双胞胎目录"会持续分叉（一侧多出 `Comparison/`，另一侧多出 `OrderedChaos/`）。

## 2. 删除"冗余副本"之前的安全清单

按顺序做，任何一步不通过就停下来问用户：

```bash
# ① 文件级差异（排除 .git，避免被对象文件淹没）
cd <A> && find . -type f -printf '%P\n' | sort > /tmp/a.txt
cd <B> && find . -type f -not -path './.git/*' -not -path './.obsidian/*' -printf '%P\n' | sort > /tmp/b.txt
comm -23 /tmp/a.txt /tmp/b.txt   # 只在 A 有
comm -13 /tmp/a.txt /tmp/b.txt   # 只在 B 有

# ② 若 A 是 git 仓库：是否有未推送内容
git -C <A> status --porcelain | wc -l          # 必须为 0（clean）
git -C <A> rev-list --left-right --count origin/main...main   # 必须 0 0
git -C <A> ls-remote --heads origin            # 远端可达且 SHA 与本地 HEAD 一致

# ③ 内容校验（迁移类操作）：sha256 两边一致再删源
sha256sum <A>/x.pdf <B>/x.pdf
```

**关键坑**：`comm` 报"只在旧副本存在"的目录，可能是**用户自己主动删掉的**（本例 `Comparison/` 就是）。不要当成数据丢失去抢救或迁移，先问一句；用户回"我自己删的"就按丢弃处理，并在报告里点明"该文件仍留在 GitHub 历史中"。

## 3. 目录规范的事实源（以及它会变）

优先级：**当前实测 > skill Phase 0 > memory > 会话开头的 system prompt cwd**。

- 会话开头的 `Current working directory` 可能指向已被删除/迁移的目录；回答"文件在哪"之前先 `pwd` + `ls -ld` 实测。本例中 `/mnt/d/ObsidianWorkspace/Academics` 在会话中已被用户删除，之后再按 system prompt 回答就会说错。
- 用户可能在两次会话之间整体搬库（本例：先迁到 D 盘 Obsidian 库，随后又把该库删掉、回到 `~/Academics` 并推到 GitHub）。**改规范时同步更新 skill Phase 0 + memory 两条，并按 §7 做一次全库 grep 清扫**，否则下个会话会按旧路径写文件。
- 用户说"以后放到 X"时，先确认是"这次拷一份"还是"永久改主目录"；永久改才动 skill/memory，一次性迁移只做拷贝 + 报告。

## 4. 把论文库 git 化（ext4 或 drvfs）

```bash
cd <库根>
git init -b main -q
git config core.filemode false    # drvfs 全 777，不改则所有文件永远显示 modified
git config core.autocrlf false    # 避免 Windows/WSL 互相改写行尾
git config core.quotepath false   # 中文文件名在 status/log 里直接可读
git add -A && git commit -m "初始化论文分析库"
```

`.gitignore` 模板（实测有效；`.pages` 用内容级忽略 + 译文例外，不能整目录忽略，否则 `!` 失效）：

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache
.dsh-cache/
.trash/
.obsidian/plugins/*/node_modules/
# 逐页正文/全文/翻译分片：可重建，不入库
**/.pages/**
!**/.pages/**/
# 例外：只放行「全文」中英对照译文（各论文统一命名 译文_中英对照.md）
# 章节/片段级译文（译文_中英对照_Sec5.md 这类）仍算中间产物，不入库
!**/.pages/**/译文_中英对照.md
.DS_Store
Thumbs.db
desktop.ini
*.tmp
~$*
```

要点：`**/.pages/**` 而非 `.pages/` —— 目录被整体忽略后 `!` 例外一律失效；`!**/.pages/**/` 必须先放行目录，深层文件（如 `.pages/MRC_Specification/xxx_翻译.md`）才找得回来。校验：`git check-ignore -v <file>` 应命中 `!` 行或无匹配，`git status -uall` 里应看到译文、看不到 `page_NN.txt`。

补充：
- **`.obsidian/plugins/*/node_modules/` 是体积大头**（lean-terminal 的 `node-pty` prebuilds 单个 .pdb 就 6 MB）。只忽略 `workspace.json` 不够。
- 入库前查一次大文件：`git ls-tree -r -l HEAD | awk '$4>50000000'`（GitHub 单文件上限 100 MB）。
- 首提交后核对：`git ls-files | wc -l`、`du -sh .git`、`git status -sb`（应只剩 `## main`）。
- **不要主动 add/commit/push**——用户 2026-11 明确要求「除非是我下的命令」。写完笔记把改动留在工作区，收尾时报告「未提交改动 N 个文件」，由用户决定何时提交；用户下令后才 `git add -A && git commit -m "<论文简称>: 分析笔记"`，再按需 `git push`。
- 需要写历史时也别自作主张 reset/force push：已推上去的提交要撤销，必须先说明影响（改写远端历史）再等用户点头。
- 旧仓库 histor 与新库不通时，**不要 force push**；要么新建远端仓库，要么先 graft 旧 `.git` 再提交，让用户选。

## 5. 交付报告里的路径约定

用户会直接问"你把产出放哪了、为什么放那"。所以**收尾报告的第一段就写绝对路径 + 放置理由**（主目录规则、与 PDF 同目录、中间产物进 `.pages/`），再写结论。事后解释成本远高于事前一句说明。

## 6. 本会话实测数据点（供对照）

- `~/Academics`：51 MB / 213 文件（其中 .git 172 个），git clone 自 `github.com/dxl041/Academics`
- D 盘副本：63 MB / 59 文件（含 34 MB 的 `.obsidian`）
- 迁移后库：`OrderedChaos/{OrderedChaos.pdf 2.5 MB, running_notes.md 107 KB/656 行, .pages/ 15 文件}`
- git 化后：63 文件入库，`.git` 24 MB，`main...origin/main` 0/0，工作区 clean

---

## 7. 目录规范变更后：全库清扫旧路径

只改 `SKILL.md` Phase 0 和 memory 不够。实测搬库后仍有 6 个文件指向旧路径（模板、两个 references、`obsidian-vault-management` 的另一条 pitfall），下个会话会照着旧路径写文件。改完规范立刻扫一遍：

```bash
grep -rn "<旧路径关键字，如 ObsidianWorkspace/Academics>" \
  ~/.hermes/skills ~/Academics/acadamic-paper-research 2>/dev/null
```

- **两处都要扫**：运行时 skill（`~/.hermes/skills/`）+ 仓库快照（`~/Academics/acadamic-paper-research/`，只用于推 GitHub）。
- 改完再 grep 复核一次：只允许「历史说明」性质的提及残留，并且必须带「已废弃 / 最终状态」字样，否则下个 agent 会当成现行规则。
- 本次残留清单（供同类清扫对照）：`templates/batch-four-element-analysis.md` 的产出目录、`references/batch-mode-long-paper.md` §5 产出目录、`references/industrial-paper-example.md` 的示例路径、`knowledge-management/obsidian-vault-management/SKILL.md` 的 pitfall 条目。

## 8. 交互效率：把核验压成一条命令

用户会直接问「这一步的交互怎么这么慢」。2026-11 实测慢的构成与对策：

| 来源 | 代价 | 对策 |
|---|---|---|
| 验证拆成 5~6 次终端调用（pwd / ls / df / mount / git log / grep 各一次） | 每次一个完整往返 | 一条 `bash -c` 里用 `echo "== X ==" ; cmd` 串起来，只回一次话 |
| `find /mnt/d -maxdepth N` 扫 Windows 盘 | 9p/drvfs 元数据比 ext4 慢一个量级 | 只 `ls` 到需要的层级；判断库在不在用 `ls /mnt/d/ObsidianWorkspace/` 足够 |
| https remote 的 push 挂起到超时 | 每次白等 60 s（实测连吃两次） | push 前先 `timeout 10 git ls-remote origin`：不通就 `git remote set-url origin git@github.com:<user>/<repo>.git` 再推；不要先让 push 自己撞超时 |
| 记忆写入超额反复重试 | 每次失败也要一个往返 | 命中 char 上限就直接压缩文案（删修饰、合并同义项），一次改到位 |

同理适用于「改动面判断」：先 `grep -rln` 一次拿到文件清单，再批量 patch，而不是边猜边改。
