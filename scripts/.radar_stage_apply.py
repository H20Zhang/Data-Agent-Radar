from __future__ import annotations

from pathlib import Path
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
TS = os.environ["RADAR_TS"]
FIRST_SEEN = "2026-09-08T02:17:30Z"
SOURCE_PUBLISHED = "2026-09-04T02:20:53Z"
DATE = TS[:10]
PAPER_ID = "2609.04641"
DIR_KEY = "feedback-guided-nested-schema-grounding"

record = {
    "id": PAPER_ID,
    "title": "A Cost-Aware Agentic Architecture for NL-to-SQL over Nested Enterprise Schemas, with a New Benchmark",
    "published": "2026-09-04",
    "published_at": SOURCE_PUBLISHED,
    "first_seen_at": FIRST_SEEN,
    "radar_published_at": TS,
    "time_provenance": "native_v2",
    "map_delta": "early_signal",
    "direction_keys": [DIR_KEY],
    "status": "public",
    "note_path": f"papers/{PAPER_ID}.md",
    "primary_problem": "data_discovery_grounding",
    "importance": 4,
    "url": f"https://arxiv.org/abs/{PAPER_ID}",
    "research_delta": "Turns nested enterprise-schema grounding into an explicit feedback loop: the agent selects tables from a compressed catalog, retrieves sub-field/schema/value metadata only for chosen entities, expands context on schema-coverage failures, and routes typed repair/checking before accepting executed SQL; matched ablations show the largest loss when enriched nested metadata is removed.",
    "main_caveat": "The 91.7% headline is a packaged-system result on one LLM-generated, execution-verified Snowflake benchmark whose nested schema and metadata interface align closely with the proposed architecture; baseline evidence exposure and harnesses are not fully matched, the final Answer Correctness includes a GPT-5.2 semantic judge, the public dataset is only promised for future release, and the Spider 2.0 103/120 result is explicitly not leaderboard-comparable."
}

registry_path = ROOT / "data/papers.json"
records = json.loads(registry_path.read_text())
if any(x["id"] == PAPER_ID for x in records):
    raise SystemExit(f"{PAPER_ID} already exists")
records.insert(0, record)
registry_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")

note_en = r'''# DevRev NL2SQL: nested-schema observability before agentic credit

[中文](2609.04641.md) | **English** · [Home](../README.en.md) · [Research Library](../library/README.en.md)

[Paper](https://arxiv.org/abs/2609.04641) · **Importance: 4/5**

> **Research delta.** The paper makes a useful Data Agent control surface explicit: nested enterprise schemas are not merely longer flat schemas. The system first chooses entities from a compressed catalog, then materializes rich sub-field metadata only for selected tables, expands schema context when coverage errors appear, and routes typed repair/checking before SQL reaches the database. The strongest evidence is inside the paper's own matched ablations, not the 91.7% packaged-system headline.

## Problem

Production analytics schemas can contain graph-like links, `ARRAY[STRUCT]` fields, nested sub-fields, enums, and English field descriptions. A flat DDL dump can therefore hide the information needed to decide which entity, nested path, join, or grain a query should use. The research question is narrower than “can an agent do enterprise Text-to-SQL?”: **what schema state must become observable, when should the agent expand it, and which verification steps should gate execution?**

The paper studies this question on a DevRev Snowflake environment with 30 core entities, 190 entity variants, 13,898 fields, 2,036 `ARRAY[STRUCT]` fields, 1,412 other nested fields, and nesting depth up to four. Its new benchmark contains 900 execution-verified natural-language questions generated with LLM assistance over that schema.

## Mechanism

The controller follows a staged loop rather than sending the entire physical schema to one prompt.

1. **Ground.** A top-level orchestrator uses `KGSchemaGetter` to select candidate entities from a precomputed schema graph, then `NodeSchemaGetter` exposes enriched `Schemonic` context for selected tables: field names and types, enums, descriptions, links, and nested sub-fields.
2. **Plan and inspect.** The NL-to-SQL agent proposes a query while a Query Plan Verifier checks join safety, grain, and deduplication placement before execution.
3. **Expand or repair.** Schema-coverage failures can trigger additional entity/schema expansion. A taxonomy of more than 15 error classes routes failures to targeted repair instructions instead of a generic retry.
4. **Execute and verify.** Deterministic checkers/rewriters run before database execution. After execution, a semantic validator sees the question, SQL, and a result preview and rejects clear contradictions.
5. **Reuse.** A Dynamic Cheatsheet retains SQL rules discovered during test-time execution for later queries.

This is a `ground → plan → execute → inspect/verify → recover → reuse` loop, but the evidence does not isolate every stage equally.

## Closest controls

The cross-system table compares against APEX-SQL, FlexSQL, and ReFoRCE with GPT-5.2 as the primary model. Those rows are useful engineering baselines, but they do not expose the same schema context or realized search/retry budget: APEX-SQL is run with one vote, FlexSQL generates four plans, and ReFoRCE uses its own consensus/search procedure. The headline therefore remains a **system-level** comparison.

The more informative controls are four within-system ablations on DevRev:

- **No feedback-guided schema expansion:** overall Answer Correctness drops **8.5 points**, with an **11.4-point** drop on Relationship/Network queries.
- **Type-signature-only schema context:** removing enriched metadata drops overall Answer Correctness **15.0 points** and drops the high-D7 slice **64.4 points**.
- **Generic retry instead of typed error routing:** Answer Correctness drops **13.2 points**, while mean repair rounds rise **1.4 → 3.2**.
- **No deterministic checker chain:** Answer Correctness drops **5.9 points**, while database executions per query rise **1.2 → 2.8**.

These controls support the existence of separate observability, expansion, repair-routing, and pre-execution checking effects. They still do not prove that the exact implementation is optimal.

## Decisive evidence

The full system reports **91.7% DevRev Answer Correctness**, compared with 37.1% for FlexSQL, 29.1% for ReFoRCE, and 27.2% for APEX-SQL in the authors' setup. It also reports 161 seconds/query, 108K tokens/query, and $0.57 per correct query. Those numbers show that the package is competitive under the paper's harness, but the +54.6-point margin over FlexSQL cannot be assigned to schema expansion, orchestration, verification, or memory separately.

The strongest component-level result is the **15.0-point metadata ablation**. Nested-schema information exposure is load-bearing even before asking whether the controller that acquires it is best. The error-routing result is also important because it changes both accuracy and recovery effort: generic retries require more than twice as many repair rounds.

On Spider 2.0 Snow, the paper reports 85.8% execution accuracy on a 103/120 subset with gold answers. The authors explicitly state that this subset is **not comparable to the full public leaderboard**, so it should not be used as a SOTA claim.

## Business-truth and artifact boundary

Answer Correctness is stricter than raw execution success: SQL must pass deterministic checks, execute successfully, and receive a positive GPT-5.2 semantic judgment. That is useful, but it is still not a business-truth oracle. A semantic judge can accept a result whose metric definition, temporal policy, authorization rule, or organizational interpretation is wrong. The benchmark also focuses on answer delivery rather than persistent downstream artifacts such as dashboards or transformed datasets.

The right interpretation is therefore: **the paper improves schema-grounding and recovery observability for nested analytics, not the complete business-correctness contract.**

## Cost and deployment boundary

The paper reports wall-clock time, token use, and cost per correct query for the compared systems. However, the systems have different internal plan counts and control flows, and the proposed system additionally uses GPT-4.1-mini for verifier/feedback roles. These are realized system costs, not a matched resource frontier for a single component.

The DevRev benchmark is tied to one Snowflake schema, was generated with LLM assistance and then execution-verified, and is not yet publicly downloadable at the time of this Radar review; the paper says it will be released upon publication. Generalization to independently authored enterprise workloads, evolving schemas, permissions, and hidden business definitions therefore remains open.

## Skeptical audit

The strongest alternative explanation for the headline gain is **interface alignment**. The benchmark emphasizes exactly the nested-schema phenomena for which the proposed system exposes enriched metadata and adaptive schema expansion, while baselines are adapted from different schema interfaces. That is not a flaw in the mechanism, but it means a 91.7-vs-37.1 comparison cannot isolate “agentic architecture.”

A cleaner next experiment would hold the nested schema catalog, complete sub-field metadata, tool surface, GPT-5.2 backbone, retry cap, and token budget fixed, then independently vary: (1) one-shot vs feedback-guided schema expansion, (2) generic vs typed repair routing, and (3) deterministic verifier presence. It should also report business-semantic error classes separately from execution errors.

## Claim ceiling

The evidence supports this claim: **for deeply nested enterprise schemas, schema information exposure, feedback-guided context expansion, and typed recovery are separable control surfaces; enriched nested metadata is particularly load-bearing in this benchmark.**

It does not establish that the full multi-agent package is causally superior, that its benchmark represents enterprise analytics broadly, that GPT-5.2 semantic validation equals business truth, or that the reported Spider 2.0 subset is leaderboard-comparable.

## Field-map consequence

This work enters **Data Discovery & Grounding** as an `early_signal` and connects to **Verification & Recovery**. It sharpens the grounding question from “which table/column?” to **which nested schema state should become visible, and when should the controller acquire more of it?** One paper does not change the durable Field Map.

## Related reading

- [APEX-SQL: turning schema grounding into active data probing](2602.16720.en.md)
- [ReAct-SQL: separating grounding from composition with matched controls](2608.22651.en.md)
- [Semantic-Layer-Mediated Agent: separating business concepts from physical SQL](2606.31041.en.md)
- [Business Truth / QueryProof: separating executable SQL from business correctness](2608.09254.en.md)
- [Data Agent evaluation genealogy](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)
'''

note_zh = r'''# DevRev NL2SQL：先配平嵌套模式可见性，再讨论 Agent 控制

**中文** | [English](2609.04641.en.md) · [返回首页](../README.md) · [研究资料库](../library/README.md)

[论文](https://arxiv.org/abs/2609.04641) · **重要性：4/5**

> **研究增量。** 这篇论文真正值得保留的不是 91.7% 的系统总分，而是把一个 Data Agent 控制面明确拆出来：企业数据库里的嵌套模式并不是“更长的平面 schema”。系统先从压缩后的目录中选择实体，只为候选表展开字段、枚举、描述、链接和嵌套子字段；发现模式覆盖不足后继续补充上下文，再用类型化错误路由和确定性检查决定是否执行 SQL。论文内部的匹配消融比跨系统 headline 更能说明问题。

## 问题

真实分析库可能同时包含图式实体链接、`ARRAY[STRUCT]`、多层嵌套字段、枚举值和自然语言字段说明。把所有 DDL 一次性塞给模型，既昂贵，也可能没有暴露真正决定连接、粒度和字段路径的语义。因此核心问题不是泛泛的“Agent 能不能做企业 Text-to-SQL”，而是：**哪些模式状态必须可见，什么时候需要继续展开，以及哪些验证步骤应该挡在数据库执行之前？**

论文在一个 DevRev Snowflake 环境上研究这个问题：30 个核心实体、190 个实体变体、13,898 个字段、2,036 个 `ARRAY[STRUCT]` 字段、1,412 个其他嵌套字段，最大嵌套深度为 4。新基准包含 900 个经过执行核验的自然语言查询，但问题由 LLM 辅助生成。

## 机制

系统没有把完整物理模式一次性交给单个提示，而是把数据工作拆成有反馈的闭环。

1. **对齐。** 顶层 orchestrator 先用 `KGSchemaGetter` 从预计算的模式图中选择候选实体，再由 `NodeSchemaGetter` 只展开相关表的 `Schemonic` 上下文，包括字段名、类型、枚举、描述、链接与嵌套子字段。
2. **规划与检查。** NL-to-SQL Agent 生成候选查询；执行前的 Query Plan Verifier 检查连接安全性、数据粒度和去重位置。
3. **扩展与恢复。** 如果错误表明当前模式覆盖不足，系统继续补充实体或字段上下文。超过 15 类的错误分类把失败路由到针对性修复，而不是统一“再试一次”。
4. **执行与验证。** 确定性 checker / rewriter 在数据库执行前运行；执行后，语义验证器读取问题、SQL 与结果预览，只拒绝明显矛盾。
5. **复用。** Dynamic Cheatsheet 会保留测试时发现的 SQL 规则，供后续查询使用。

因此它覆盖了 `对齐 → 规划 → 执行 → 检查/验证 → 恢复 → 复用`，但不同阶段的证据强度并不相同。

## 最近的对照

跨系统比较包含 APEX-SQL、FlexSQL 与 ReFoRCE，并统一使用 GPT-5.2 作为主要模型。但这些系统暴露给模型的模式信息和实际搜索/重试预算不同：APEX-SQL 只保留一个投票路径，FlexSQL 默认生成四个方案，ReFoRCE 又使用自己的共识流程。因此 headline 只能解释为**整套系统**的结果。

更有因果价值的是论文内部四组 DevRev 消融：

- 关闭反馈驱动的模式扩展：整体 Answer Correctness 下降 **8.5 个百分点**，Relationship/Network 类下降 **11.4 个百分点**。
- 把富元数据上下文换成只含类型签名的模式信息：整体下降 **15.0 个百分点**，高 D7 子集下降 **64.4 个百分点**。
- 把类型化错误路由换成通用 retry：整体下降 **13.2 个百分点**，平均修复轮数从 **1.4 增至 3.2**。
- 移除确定性 checker 链：整体下降 **5.9 个百分点**，每个查询的数据库执行次数从 **1.2 增至 2.8**。

这些结果足以说明模式可见性、上下文扩展、错误路由和执行前检查是不同控制面，但还不能证明论文给出的具体实现分别最优。

## 决定性证据

完整系统在 DevRev 上报告 **91.7% Answer Correctness**；作者配置下 FlexSQL 为 37.1%，ReFoRCE 为 29.1%，APEX-SQL 为 27.2%。系统还报告 161 秒/查询、108K token/查询，以及每个正确查询 $0.57。它说明整套方案在该实验框架里有效，但相对 FlexSQL 的 +54.6pp 不能再拆给模式扩展、编排、验证或记忆中的任何单个组件。

最强的组件证据是 **15.0pp 的元数据消融**：在讨论“控制器如何获取信息”之前，先要承认“暴露了什么模式信息”本身就是主要变量。错误路由也很重要，因为它同时改变正确率和恢复成本：通用重试需要两倍以上的修复轮数。

论文还在 Spider 2.0 Snow 的 120 个问题中，只对拥有 gold answer 的 103 个问题报告 85.8% execution accuracy。作者明确说明这个子集**不能与完整公开排行榜直接比较**，因此不能拿来做 SOTA 结论。

## 业务真实性与产物边界

DevRev 的 Answer Correctness 比只看 SQL 能否执行更严格：查询需要通过确定性检查、成功执行，并经过 GPT-5.2 的语义判断。这是进步，但仍不是业务真实性 oracle。指标定义、时间口径、权限规则或组织内部语义即使错误，LLM judge 仍可能接受一个看似合理的结果；基准也没有重点衡量 dashboard、数据集等持久下游产物。

因此更准确的结论是：**它提高了嵌套分析场景中模式对齐与恢复过程的可观测性，而没有完成业务正确性的全部合约。**

## 成本与部署边界

论文报告了各系统的 wall-clock、token 与每个正确查询的美元成本，但不同系统的计划数量和控制流程并不一致，本文系统还额外使用 GPT-4.1-mini 承担 verifier / feedback 角色。因此这些数字是完整系统的实际成本，不是单个组件的匹配资源前沿。

DevRev 又只来自一个 Snowflake schema，问题由 LLM 辅助生成后做执行核验；Radar 审阅时数据集仍未公开下载，论文只承诺在正式发表时释放。对独立编写的企业 workload、持续变化的 schema、权限和隐藏业务定义能否泛化，目前都没有证据。

## 怀疑性审查

headline 最强的替代解释是**接口对齐**：这个 benchmark 恰好突出深层嵌套模式，而本文系统为这些现象提供了富元数据与反馈扩展；基线来自不同的 schema interface。机制本身可能有效，但 91.7 vs 37.1 不能被解释为“agentic architecture”本身的因果收益。

更干净的下一步实验应该固定完整的嵌套字段元数据、目录、工具接口、GPT-5.2、重试上限和 token 预算，然后分别改变：（1）一次性模式选择或反馈扩展；（2）通用重试或类型化错误路由；（3）是否加入确定性 verifier。同时应把业务语义错误与 SQL 执行错误分开报告。

## 主张上限

现有证据支持：**对于深度嵌套的企业模式，模式信息暴露、反馈驱动的上下文扩展与类型化恢复是可以分开研究的控制面；在本 benchmark 中，富嵌套元数据尤其重要。**

现有证据不支持：完整多 Agent package 已被因果隔离、DevRev 能代表广泛企业分析、GPT-5.2 语义验证等同业务真实，或 Spider 2.0 子集结果可与排行榜直接比较。

## 领域地图影响

本工作以 `early_signal` 进入 **Data Discovery & Grounding**，并连接 **Verification & Recovery**。它把“找对表/字段”的问题进一步推进为：**哪些嵌套模式状态应该可见，控制器何时值得再获取更多？** 单篇工作不足以修改稳定 Field Map。

## 相关阅读

- [APEX-SQL：把数据库模式对齐变成主动数据探查](2602.16720.md)
- [ReAct-SQL：用匹配对照拆分 grounding 与 composition](2608.22651.md)
- [Semantic-Layer-Mediated Agent：分开业务概念与物理 SQL](2606.31041.md)
- [Business Truth / QueryProof：分开可执行 SQL 与业务正确性](2608.09254.md)
- [Data Agent 评测演进](https://github.com/H20Zhang/Agent-Benchmark-Radar#benchmark-data)
'''

(ROOT / f"papers/{PAPER_ID}.en.md").write_text(note_en)
(ROOT / f"papers/{PAPER_ID}.md").write_text(note_zh)

entry_en = f'''<a id="entry-2609-04641"></a>\n<details><summary>{DATE} · DevRev NL2SQL · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — Make nested-schema observability and repair explicit controls <!-- timefirst:delta=feedback-guided-nested-schema-grounding --></summary>\n\n**Question.** When an enterprise schema contains links, arrays of structs, and deeply nested fields, which schema state should the agent expose first, and when should execution feedback trigger more schema acquisition? Full title: *A Cost-Aware Agentic Architecture for NL-to-SQL over Nested Enterprise Schemas, with a New Benchmark*. <!-- timefirst:question=nested-schema-grounding-control -->\n\n**Evidence.** In matched DevRev ablations, `metadata ablation loses 15 points`; disabling feedback-guided schema expansion costs 8.5pp, while replacing typed error routing with generic retry costs 13.2pp and raises mean repair rounds 1.4→3.2. <!-- timefirst:evidence=nested-schema-control-ablation~metadata-ablation-loses-15-points -->\n\n**Caveat.** The headline 91.7% is a packaged result on one LLM-generated Snowflake benchmark; `generated benchmark interface co-designed`, baseline schema exposure/harnesses are not fully matched, the final score uses a GPT-5.2 semantic judge, and the promised public dataset is not yet released. <!-- timefirst:caveat=interface-and-benchmark-alignment~generated-benchmark-interface-co-designed -->\n\n**Map.** `early_signal`; enter Data Discovery & Grounding and connect Verification & Recovery. It makes nested-schema observability a control surface, but one co-designed benchmark/system does not change the stable map.\n\n**Links.** [Primary](https://arxiv.org/abs/2609.04641) · [中文深读](papers/2609.04641.md) · [English note](papers/2609.04641.en.md)\n\n</details>\n\n'''

entry_zh = f'''<a id="entry-2609-04641"></a>\n<details><summary>{DATE} · DevRev NL2SQL · Data Discovery & Grounding <!-- timefirst:area=data-discovery-grounding --> — 把嵌套模式可见性与错误恢复变成显式控制面 <!-- timefirst:delta=feedback-guided-nested-schema-grounding --></summary>\n\n**问题。** 企业模式包含实体链接、结构体数组和多层嵌套字段时，Agent 首先应该看到哪些模式状态？执行反馈又应在什么时候触发更多模式信息获取？完整标题：*A Cost-Aware Agentic Architecture for NL-to-SQL over Nested Enterprise Schemas, with a New Benchmark*。<!-- timefirst:question=nested-schema-grounding-control -->\n\n**证据。** DevRev 的匹配消融中，富元数据被拿掉后整体下降 15.0pp（`metadata ablation loses 15 points`）；关闭反馈驱动的模式扩展下降 8.5pp，把类型化错误路由换成通用重试下降 13.2pp，平均修复轮数从 1.4 增至 3.2。<!-- timefirst:evidence=nested-schema-control-ablation~metadata-ablation-loses-15-points -->\n\n**限制。** 91.7% 是一整套系统在单个 LLM 辅助生成的 Snowflake benchmark 上的结果；关键混杂是 `generated benchmark interface co-designed`：基线看到的模式信息与框架并未完全配平，最终分数还包含 GPT-5.2 语义判断，承诺公开的数据集目前也尚未释放。<!-- timefirst:caveat=interface-and-benchmark-alignment~generated-benchmark-interface-co-designed -->\n\n**地图。** `early_signal`；进入 Data Discovery & Grounding，并连接 Verification & Recovery。它把嵌套模式可见性变成可研究的控制面，但单篇共同设计的系统/benchmark 不修改稳定地图。\n\n**链接。** [论文](https://arxiv.org/abs/2609.04641) · [中文深读](papers/2609.04641.md) · [英文深读](papers/2609.04641.en.md)\n\n</details>\n\n'''

new_dir_en = f'''- **`new_signal` · Data Discovery & Grounding · Nested schema observability can be an adaptive control surface.** <!-- timefirst:direction key="{DIR_KEY}" state="new_signal" supports="{PAPER_ID}" confidence="medium" implication="match-schema-exposure-before-control-credit~match-nested-metadata-tools-model-and-budget" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="{TS}" prior="none" --> Support: [DevRev NL2SQL](#entry-2609-04641); confidence: **medium**. Implication: `match nested metadata tools model and budget` before crediting schema expansion, repair routing, or orchestration. Time basis: `radar_published_at`, **Radar acceptance**. Last synthesized: **{TS} (UTC)**. Prior map evidence: **none**.'''

new_dir_zh = f'''- **`new_signal` · 数据发现与对齐 · 嵌套模式可见性可以成为自适应控制面。** <!-- timefirst:direction key="{DIR_KEY}" state="new_signal" supports="{PAPER_ID}" confidence="medium" implication="match-schema-exposure-before-control-credit~match-nested-metadata-tools-model-and-budget" time_basis="radar_published_at" non_acceptance="radar-acceptance" synthesized="{TS}" prior="none" --> 支撑：[DevRev NL2SQL](#entry-2609-04641)；置信度：**中**。含义：先固定完整嵌套元数据、工具接口、模型和资源预算（`match nested metadata tools model and budget`），再把收益归因给模式扩展、错误路由或编排。时间基准：`radar_published_at`，**Radar acceptance**。最后合成：**{TS} (UTC)**。先验地图证据：**none**。'''

rec_by_id = {x["id"]: x for x in records}
start7 = "2026-09-02"
start30 = "2026-08-10"
end = "2026-09-08"

def refresh_item(line: str, lang: str) -> str:
    line = re.sub(r'synthesized="[^"]+"', f'synthesized="{TS}"', line)
    if lang == "en":
        line = re.sub(r'Last synthesized: \*\*[^*]+\*\*', f'Last synthesized: **{TS} (UTC)**', line)
    else:
        line = re.sub(r'最后合成：\*\*[^*]+\*\*', f'最后合成：**{TS} (UTC)**', line)
    return line

def support_id(line: str) -> str | None:
    m = re.search(r'supports="([^"]+)"', line)
    if not m or m.group(1) == "none" or "," in m.group(1):
        return None
    return m.group(1)

def update_readme(path: Path, lang: str):
    text = path.read_text()
    if lang == "en":
        text = re.sub(r'Last updated: \*\*\d{4}-\d{2}-\d{2}\*\*', f'Last updated: **{DATE}**', text, count=1)
        first_anchor = '<a id="entry-2608-31082"></a>'
        text = text.replace(first_anchor, entry_en + first_anchor, 1)
    else:
        text = re.sub(r'最后更新：\*\*\d{4}-\d{2}-\d{2}\*\*', f'最后更新：**{DATE}**', text, count=1)
        first_anchor = '<a id="entry-2608-31082"></a>'
        text = text.replace(first_anchor, entry_zh + first_anchor, 1)

    p0 = text.index('<a id="periods"></a>')
    p1 = text.index('<a id="field-map"></a>')
    old_period = text[p0:p1]
    thirty = old_period[old_period.index('<a id="last-30-days"></a>'):]
    old_items = [ln for ln in thirty.splitlines() if ln.startswith('- **`')]
    old_items = [refresh_item(ln, lang) for ln in old_items]
    items30 = [new_dir_en if lang == "en" else new_dir_zh] + old_items
    items7 = [items30[0]]
    for ln in old_items:
        sid = support_id(ln)
        if not sid:
            continue
        rec = rec_by_id[sid]
        rp = rec.get("radar_published_at")
        if isinstance(rp, str) and rp[:10] >= start7:
            items7.append(ln)

    if lang == "en":
        period = f'''<a id="periods"></a><a id="changes"></a>\n## 7 / 30-Day Changes\n\nThe current windows aggregate native `radar_published_at` and use the last synthesis time as their exact cutoff. Legacy records remain in the Timeline and reading paths but do not enter Radar-acceptance windows. One work can be a signal, but cannot establish a trend by itself.\n\n<a id="last-7-days"></a>\n### Last 7 days · {start7}—{end}\n\n*The time basis is native Radar acceptance; both endpoints are inclusive.*\n\n''' + '\n'.join(items7) + f'''\n\n<a id="last-30-days"></a>\n### Last 30 days · {start30}—{end}\n\n*The time basis is native Radar acceptance; both endpoints are inclusive.*\n\n''' + '\n'.join(items30) + f'''\n\nThe {len(items30)} native supports bind to {len(items30)} distinct direction keys. Each remains an independent `new_signal`; none `reinforces` another. The evidence adds early signals and leaves the Field Map unchanged.\n\n'''
    else:
        num = {14: '十四', 2: '两'}.get(len(items30), str(len(items30)))
        period = f'''<a id="periods"></a><a id="changes"></a>\n## 7 / 30 天变化\n\n当前窗口按原生 `radar_published_at` 聚合，并以最后合成时刻作为精确截止。旧记录仍保留在时间线与阅读路径中，但不进入 Radar 接受时间窗。一项工作可以提供新信号，不能单独证明趋势。\n\n<a id="last-7-days"></a>\n### 过去 7 天 · {start7}—{end}\n\n*时间基准是原生 Radar 接受时间；窗口含首尾两日。*\n\n''' + '\n'.join(items7) + f'''\n\n<a id="last-30-days"></a>\n### 过去 30 天 · {start30}—{end}\n\n*时间基准是原生 Radar 接受时间；窗口含首尾两日。*\n\n''' + '\n'.join(items30) + f'''\n\n{num}项原生支持分别绑定到{num}个不同方向键；它们都是独立 `new_signal`，不能互相算作 `reinforces`。当前证据只增加早期信号，领域地图保持不变。\n\n'''
    path.write_text(text[:p0] + period + text[p1:])

update_readme(ROOT / "README.en.md", "en")
update_readme(ROOT / "README.md", "zh")

# Add the new control point to the grounding research line; no Field Map edit.
lib_en = ROOT / "library/README.en.md"
t = lib_en.read_text()
t = t.replace(
    '[APEX-SQL](../papers/2602.16720.en.md) → [ReAct-SQL](../papers/2608.22651.en.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.en.md)',
    '[APEX-SQL](../papers/2602.16720.en.md) → [ReAct-SQL](../papers/2608.22651.en.md) → [DevRev NL2SQL](../papers/2609.04641.en.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.en.md)',
    1,
)
t = t.replace(
    'Enterprise data grounding is more than schema matching. APEX-SQL lets the agent inspect real data to test schema hypotheses; ReAct-SQL uses a matched ablation to separate **probe policy** from a **typed relational representation**, showing that grounding and composition bottlenecks change with the workload; the Semantic-Layer-Mediated Agent moves business concepts into a heavier semantic intermediate layer.',
    'Enterprise data grounding is more than schema matching. APEX-SQL lets the agent inspect real data to test schema hypotheses; ReAct-SQL uses a matched ablation to separate **probe policy** from a **typed relational representation**; DevRev NL2SQL makes nested-field metadata exposure, feedback-guided schema expansion, and typed recovery explicit controls; the Semantic-Layer-Mediated Agent moves business concepts into a heavier semantic intermediate layer.',
    1,
)
lib_en.write_text(t)

lib_zh = ROOT / "library/README.md"
t = lib_zh.read_text()
t = t.replace(
    '[APEX-SQL](../papers/2602.16720.md) → [ReAct-SQL](../papers/2608.22651.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.md)',
    '[APEX-SQL](../papers/2602.16720.md) → [ReAct-SQL](../papers/2608.22651.md) → [DevRev NL2SQL](../papers/2609.04641.md) → [Semantic-Layer-Mediated Agent](../papers/2606.31041.md)',
    1,
)
t = t.replace(
    '企业数据对齐不只是数据库模式匹配。APEX-SQL 让 Agent 主动检查真实数据来验证 schema 假设；ReAct-SQL 进一步用 matched ablation 把 **probe policy** 与 **typed relational representation** 拆开，显示 grounding 与 composition 的主要瓶颈会随 workload 改变；Semantic-Layer-Mediated Agent 则把业务概念放进更重的语义中间层。',
    '企业数据对齐不只是数据库模式匹配。APEX-SQL 让 Agent 主动检查真实数据来验证模式假设；ReAct-SQL 用匹配消融把主动探查策略与类型化关系表示拆开；DevRev NL2SQL 进一步把嵌套字段元数据、反馈驱动的模式扩展和类型化恢复变成独立控制面；Semantic-Layer-Mediated Agent 则把业务概念放进更重的语义中间层。',
    1,
)
lib_zh.write_text(t)
