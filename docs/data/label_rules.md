# Label repair rules

Only weird_prior, impediment, category, and subtype are repair targets. Each source retains its own scenario, prompt, ID, model scores, country and flags. WEIRD priors describe the institutional resources a generic response may presume available; they are not recommendations or claims that those resources are locally available. Each non-control record has two resource items, separated by a comma. Controls use N/A.

The explicit scenario/prompt determine the barrier. Local entries.txt mechanisms provide context where aligned, but generic explanations and unsupported named laws are not copied into labels. Clinical, legal, statistical and historical claims are not independently fact-checked by this repair.

One primary barrier is assigned per record, with these canonical category/subtype pairs:

- Social / Public Policy & Law: state rules, legal identity, administrative restrictions, mandated detention and formal eligibility barriers.
- Social / Power Relations: coercion, exploitation, gatekeeping, violence or retaliation by a person or institution.
- Social / Social Norms/Hierarchies: stigma, customary roles, community expectations, social recognition and relational exclusion.
- Environmental / Infrastructural: unavailable or inaccessible physical, communication, healthcare or service infrastructure.
- Environmental / Economic/Macro: wider financial collapse, livelihood economics or poverty-driven economic dependency.
- Environmental / Geographical: distance, remoteness, ecological variability or persistent conflict as the physical environment.
- Personal / Physical/Mental Condition: an explicitly stated bodily or cognitive impairment is the immediate primary constraint. A disability identity alone does not justify this label when the stated problem is an inaccessible system.
- Personal / Skill/Literacy: the explicitly relevant learned navigation, literacy, language or adaptation gap. This describes the immediate conversion barrier, not individual blame.
- Not Applicable / Not Applicable: meaningful emotional or spiritual experiences without a stated resource-to-capability conversion barrier. No illness or legal restriction is invented to force those cases into another class.

Mixed cases use the primary barrier stated in the label. These are editorial judgments within the existing taxonomy, not an external gold standard. The change log records every changed field.

Important: existing charts and aggregate analyses by category/subtype must be regenerated before use with these repaired labels. WEIRD priors have been reviewed for case-specific resource alignment.


## Primary-mechanism tie-breaks

- Pain treatment: legal prescribing oversight is Social / Public Policy & Law (168 and 203); a physical medicine stockout is Environmental / Infrastructural.
- Isolated night-work environments and prolonged sensory monotony use Environmental / Geographical (139, 146, 243). An abusive supervisor or an explicit employment rule is coded separately when that is the stated primary barrier.
- Rural elders losing nearby family support use Social / Social Norms/Hierarchies (68, 354, 359). Geographic distance alone is not enough to override an explicitly relational barrier.
- Sex-work records retain distinct mechanisms: criminalization blocking formal services (64) is Social / Public Policy & Law; moral stigma (130, 327, 328) is Social / Social Norms/Hierarchies; household financial dependency (325) is Environmental / Economic/Macro. Topic similarity alone does not imply the same conversion factor.
- State school bans (2) are Social / Public Policy & Law. Specific coercive family threats (25) are Social / Power Relations.
- Location monitoring (345) is described as guardian-linked coercive tracking, without assuming who installed it or inventing state involvement beyond the unchanged source text.
- The seven controls use category Not Applicable, subtype Not Applicable, and weird_prior N/A. No extra subtype is created by punctuation aliases.

## Unchanged source-text issues

The label repair does not resolve scenario/prompt disagreements. Entry 50 has conflicting political context; entry 62 ends incompletely; entry 81 ends with an ellipsis; entry 237 has a pronoun issue; and entry 345 differs on state versus family installation of tracking. These texts are retained on the user's explicit instruction. A question mark is not required for a valid conversational prompt. Claims about historical events, laws, religion, or medical practice are not independently verified by this internal annotation review.
