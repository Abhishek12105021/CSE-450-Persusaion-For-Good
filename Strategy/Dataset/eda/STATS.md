# Merged phase-1 dataset - EDA & statistics

Manual multi-label persuasion-strategy annotation of the **first 10,600 persuader turns**
of `persuader_turns.csv` (41 strategies / 11 categories, see
`taxonomy_multilabel.json` and `guideline_multi_strategy.md`).

Built by concatenating four independently-produced annotation segments in canonical
`persuader_turns.csv` order:

| Order | Annotator | Range | Turns | Source folder |
| --- | --- | --- | --- | --- |
| 1 | shimanto | turns 1-2000 | 2,000 | `annotation_first_2000_shimanto` |
| 2 | shovon | turns 2001-4000 | 2,000 | `annotation_shovon` |
| 3 | unassigned | turns 4001-6000 | 2,000 | `annotation_turns_4001_6000` (`model_id = claude-opus-3.7-batch`) |
| 4 | shovon | turns 6001-7000 | 1,000 | `annotation_shovon` |
| 5 | abhishek | turns 7001-10600 | 3,600 | `annotation_7001_10600_abhishek` |

Categories in every record are recomputed from the strategy set via the taxonomy,
so the strategy/category views are always consistent.

## Overview (whole dataset)

| Metric | Value |
| --- | --- |
| Turns | 10,600 |
| Dialogues | 1,017 |
| Turns / dialogue | mean 10.42 (min 4, max 15) |
| Mean labels / turn | 1.679 |
| Median labels / turn | 1.0 |
| Std. dev. | 1.061 |
| Empty-set turns | 707 (6.7%) |
| Multi-label turns (>=2) | 48.9% |
| Max labels on a turn | 6 |
| Distinct strategies used | 41 / 41 |
| Distinct categories used | 11 / 11 |

## Labels per turn

| Labels | Turns | % |
| --- | --- | --- |
| 0 | 707 | 6.7 |
| 1 | 4,707 | 44.4 |
| 2 | 3,443 | 32.5 |
| 3 | 1,098 | 10.4 |
| 4 | 392 | 3.7 |
| 5 | 175 | 1.7 |
| 6 | 78 | 0.7 |

## Category prevalence

| Category | Turns | % |
| --- | --- | --- |
| Relational and Interactive | 4,897 | 46.2 |
| Information Provision | 3,823 | 36.1 |
| Emotional Appeal | 1,645 | 15.5 |
| Social Influence | 1,263 | 11.9 |
| Reciprocity and Exchange | 1,078 | 10.2 |
| Framing and Presentation | 1,004 | 9.5 |
| Credibility Appeal | 896 | 8.5 |
| Rational Appeal | 751 | 7.1 |
| Threat and Pressure | 249 | 2.3 |
| Commitment and Consistency | 169 | 1.6 |
| Urgency and Scarcity | 163 | 1.5 |

## Strategy prevalence (all 41)

| Strategy | Category | Turns | % |
| --- | --- | --- | --- |
| rapport_building | Relational and Interactive | 2,860 | 27.0 |
| organization_information | Information Provision | 1,735 | 16.4 |
| donation_procedure_information | Information Provision | 1,417 | 13.4 |
| personal_related_inquiry | Relational and Interactive | 1,328 | 12.5 |
| personal_story | Relational and Interactive | 1,150 | 10.8 |
| emotion_appeal | Emotional Appeal | 1,023 | 9.7 |
| gratitude_and_appreciation | Reciprocity and Exchange | 966 | 9.1 |
| minimization_framing | Framing and Presentation | 849 | 8.0 |
| task_clarification | Information Provision | 770 | 7.3 |
| hope_and_positive_impact | Emotional Appeal | 628 | 5.9 |
| self_modeling | Social Influence | 619 | 5.8 |
| source_related_inquiry | Relational and Interactive | 615 | 5.8 |
| in_group_appeal | Social Influence | 598 | 5.6 |
| impact_information | Information Provision | 477 | 4.5 |
| organizational_credibility | Credibility Appeal | 389 | 3.7 |
| evidence_and_statistics | Rational Appeal | 378 | 3.6 |
| logical_appeal | Rational Appeal | 304 | 2.9 |
| transparency_and_accountability | Credibility Appeal | 274 | 2.6 |
| source_citation | Credibility Appeal | 193 | 1.8 |
| persistent_repetition | Threat and Pressure | 167 | 1.6 |
| urgency_appeal | Urgency and Scarcity | 150 | 1.4 |
| donor_benefit | Reciprocity and Exchange | 109 | 1.0 |
| anchoring | Framing and Presentation | 94 | 0.9 |
| value_consistency_appeal | Commitment and Consistency | 79 | 0.7 |
| personal_credibility | Credibility Appeal | 78 | 0.7 |
| obligation_pressure | Threat and Pressure | 78 | 0.7 |
| comparison_framing | Framing and Presentation | 74 | 0.7 |
| social_proof | Social Influence | 67 | 0.6 |
| empathy_and_perspective_taking | Emotional Appeal | 66 | 0.6 |
| feasibility_and_ease | Rational Appeal | 55 | 0.5 |
| foot_in_the_door | Commitment and Consistency | 53 | 0.5 |
| incremental_ask | Commitment and Consistency | 35 | 0.3 |
| guilt_induction | Emotional Appeal | 31 | 0.3 |
| cost_benefit_framing | Rational Appeal | 27 | 0.3 |
| loss_versus_gain_framing | Framing and Presentation | 21 | 0.2 |
| reciprocity | Reciprocity and Exchange | 14 | 0.1 |
| scarcity_appeal | Urgency and Scarcity | 8 | 0.1 |
| negative_consequence_warning | Threat and Pressure | 7 | 0.1 |
| authority_endorsement | Social Influence | 5 | 0.0 |
| deadline_pressure | Urgency and Scarcity | 5 | 0.0 |
| door_in_the_face | Commitment and Consistency | 2 | 0.0 |

## Per-annotator / per-segment statistics

### shimanto  (turns 1-2000)

| Metric | Value |
| --- | --- |
| Turns | 2,000 |
| Dialogues | 192 |
| Turns / dialogue | mean 10.42 (min 5, max 14) |
| Mean labels / turn | 2.384 |
| Median labels / turn | 2.0 |
| Std. dev. | 1.558 |
| Empty-set turns | 180 (9.0%) |
| Multi-label turns (>=2) | 66.8% |
| Max labels on a turn | 6 |
| Distinct strategies used | 38 / 41 |

Top strategies: `personal_story` (608), `in_group_appeal` (574), `rapport_building` (550), `organization_information` (390), `emotion_appeal` (377), `task_clarification` (255), `personal_related_inquiry` (251), `minimization_framing` (218)

### shovon  (turns 2001-4000 + 6001-7000)

| Metric | Value |
| --- | --- |
| Turns | 3,000 |
| Dialogues | 290 |
| Turns / dialogue | mean 10.34 (min 1, max 13) |
| Mean labels / turn | 1.78 |
| Median labels / turn | 2.0 |
| Std. dev. | 0.82 |
| Empty-set turns | 14 (0.5%) |
| Multi-label turns (>=2) | 58.3% |
| Max labels on a turn | 5 |
| Distinct strategies used | 31 / 41 |

Top strategies: `rapport_building` (1121), `organization_information` (545), `personal_related_inquiry` (478), `donation_procedure_information` (471), `task_clarification` (347), `hope_and_positive_impact` (303), `gratitude_and_appreciation` (285), `minimization_framing` (263)

### unassigned  (turns 4001-6000)

| Metric | Value |
| --- | --- |
| Turns | 2,000 |
| Dialogues | 191 |
| Turns / dialogue | mean 10.47 (min 2, max 15) |
| Mean labels / turn | 1.614 |
| Median labels / turn | 1.0 |
| Std. dev. | 0.77 |
| Empty-set turns | 39 (2.0%) |
| Multi-label turns (>=2) | 49.6% |
| Max labels on a turn | 5 |
| Distinct strategies used | 28 / 41 |

Top strategies: `rapport_building` (552), `donation_procedure_information` (363), `organization_information` (302), `impact_information` (279), `emotion_appeal` (225), `gratitude_and_appreciation` (180), `personal_related_inquiry` (165), `minimization_framing` (155)

### abhishek  (turns 7001-10600)

| Metric | Value |
| --- | --- |
| Turns | 3,600 |
| Dialogues | 348 |
| Turns / dialogue | mean 10.34 (min 2, max 14) |
| Mean labels / turn | 1.24 |
| Median labels / turn | 1.0 |
| Std. dev. | 0.773 |
| Empty-set turns | 474 (13.2%) |
| Multi-label turns (>=2) | 30.8% |
| Max labels on a turn | 6 |
| Distinct strategies used | 40 / 41 |

Top strategies: `rapport_building` (637), `organization_information` (498), `personal_related_inquiry` (434), `donation_procedure_information` (393), `gratitude_and_appreciation` (308), `self_modeling` (231), `source_related_inquiry` (220), `minimization_framing` (213)

> **Annotation-style note.** The four segments were labelled independently and show
> clearly different label *densities* - shimanto's segment averages ~2.4 strategies
> per turn while abhishek's averages ~1.2. This is a labelling-granularity effect, not
> a property of the conversations, and matters for any model trained on the pooled
> data or for cross-segment agreement studies. See `flags` for turns the annotators
> marked as uncertain / edge cases.
