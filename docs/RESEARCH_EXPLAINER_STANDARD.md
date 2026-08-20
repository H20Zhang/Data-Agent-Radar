# Research Explainer Standard

Use this standard for high-value Data Agent paper notes, README folds, Research Library lines, and field arguments. It fixes the reasoning sequence, not the sentence template.

## 1. Research delta

State the smallest change that matters:

`previous data-work design → changed control/state/interface → consequence`

## 2. Problem that survives the closest baseline

Explain what still fails after giving the baseline a competent schema/metadata interface, tool harness, and reasonable execution budget. Distinguish syntax/execution failure from semantic/business failure.

## 3. Mechanism / data-work flow

Describe the actual loop:

`intent → discover/ground → plan → execute/transform → inspect/verify → recover → learn/reuse → deliver`

Name whether the contribution changes semantic grounding, planning, tool/execution capacity, verification, recovery, or persistent reusable state.

## 4. Closest comparison

Always answer:

- closest meaningful alternative;
- model, semantic layer, schema context, tool interface, harness, retry policy, and budget held fixed;
- what still changes together.

If a smaller model has richer scaffolding than a larger baseline, do not frame the result as a clean model-size win.

## 5. Decisive evidence

Keep only 1–3 belief-changing results. Separate when possible:

- execution correctness;
- business-semantic correctness;
- clarification / abstention;
- artifact verification;
- tool/OS grounding;
- recovery rate;
- test-time branching and cost.

## 6. What remains unproven

Surface the strongest gap:

- semantic-layer curation/coverage;
- harness/tool mismatch;
- hidden business definitions;
- synthetic tasks;
- exploration/test-time scaling cost;
- tool reliability;
- schema/workload drift;
- lack of matched single-agent or direct-execution control.

## 7. Field-map consequence

State which data-work boundary changes: discovery/grounding, semantic planning, execution/transformation, verification/recovery, or learning/reuse.

## 8. Related reading

Choose 2–4 works for contrast or continuation. Benchmark genealogy should link to Agent Benchmark Radar rather than being duplicated here.

## README compression

A 60–90 second fold should preserve the surviving problem, actual data/control flow, closest comparison, decisive evidence, and strongest caveat in 2–4 natural paragraphs.

## Epistemic discipline

Keep paper-reported fact, curator interpretation, and open hypothesis / decisive next test distinct in wording.
