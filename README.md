# Appendix Literature Screening and Dataset Construction

## Literature screening

The literature search began with a list of 39 game categories. A large language model was used to expand the search expressions and develop a set of terms for database queries. Searches were then conducted in Scopus and Web of Science, and metadata were collected from each database. The Scopus search yielded Paper Set A, comprising 29,151 records, while the Web of Science search yielded Paper Set B, comprising 22,861 records. The two sets were combined, and duplicate records were removed within each game category, resulting in a candidate set of 35,550 records for subsequent screening.

The sources of the literature cover behavioral economics journals and general-interest economics journals. The former comprised the Journal of Behavioral and Experimental Economics (BEE), Games and Economic Behavior (GEB), Journal of Economic Behavior & Organization (EBO), and Experimental Economics. The latter comprised the American Economic Review (AER), Quarterly Journal of Economics (QJE), Journal of Political Economy (JPE), Review of Economic Studies (ReStud), and Econometrica. During automated preprocessing, records were screened by document type and publication source. Research articles published in the target journals were retained, while conference papers, book chapters, and preprints were excluded. This preprocessing can be completed before formal content screening to reduce the number of records requiring individual assessment.

Content screening addressed four dimensions: study type, topical relevance, publication quality, and data extractability. For study type, eligible studies were experiments involving human participants, including laboratory and online experiments. Assessment considered whether the paper described participants, treatment and control groups, experimental design, and statistical data. Purely theoretical studies, non-experimental survey studies, and purely computational simulations were excluded. For topical relevance, papers were required to explicitly involve game-based decision tasks or strategic interaction within a specified context. Studies concerned solely with gamification or recreational games, without relevance to economic decision-making experiments, were excluded. Publication screening also considered article length, excluding papers shorter than five pages. For data extractability, titles and abstracts were assessed for evidence of quantifiable experimental data. Studies from which experimental data could not be extracted, or that did not involve behavioral variables, were excluded.

Title and abstract screening followed a semi-automated process combining LLM-based classification with human validation. First, the LLM assigned each candidate paper one of three labels—“relevant,” “uncertain,” or “irrelevant”—and recorded the classification result and the confidence distribution across the three categories. “Relevant” indicated that the available information supported inclusion, whereas “irrelevant” indicated that it supported exclusion. “Uncertain” identified papers for which the title and abstract alone were insufficient to reach a clear judgment. These classifications served as preliminary screening results, with final inclusion determined through human validation.

Human validation combined stratified random sampling with equal allocation and a full review of uncertain cases. A random sample of 200 papers was drawn from each of the categories labeled “relevant” and “irrelevant” by the large language model, yielding 400 papers for verification. All papers labeled “uncertain” were submitted for human review. Human reviewers used only two labels, “relevant” and “irrelevant”; no “uncertain” category was used in human assessment.

Four reviewers conducted the assessment. Before reviewing, they established a common interpretation of the criteria for study type, topical relevance, publication quality, and data extractability, and discussed potentially ambiguous borderline cases. During the review, they independently read the titles and abstracts, made binary judgments against the screening criteria, and recorded the reasons for their decisions. When titles and abstracts provided insufficient information, reviewers consulted the methods, experimental design, and data descriptions in the full text before assigning a label.

After the independent assessments, the reviewers’ judgments were cross-checked, with inter-rater agreement reaching 95%. For papers with conflicting judgments, the four reviewers compared their reasoning, checked the relevant source passages, and reached a final classification through discussion. Independent assessments and final decisions following discussion were retained separately to distinguish initial agreement from the outcomes of disagreement resolution.

Using the adjudicated human labels as the reference, classification accuracy, recall, and F1 scores were calculated for the 400 papers sampled from the “relevant” and “irrelevant” strata to assess the reliability of the model’s determinate classifications. Papers labeled “uncertain” by the model were included or excluded based on the full human review and were not included in this binary performance evaluation. The final set of experimental studies was determined by combining the model’s initial screening, stratified sample verification, and human review of all uncertain cases. Following screening, 28,337 papers were excluded and 7,337 eligible papers were retained.

## Workflow

The workflow is designed as a multi-agent collaborative system. A Coordination Agent organizes experiment interpretation, observed-data construction, simulated-data construction, and independent validation, and consolidates the results. Each paper serves as the unit of workflow management. All agents produce intermediate outputs linked to specific source locations, providing an evidence base for subsequent stages.

At the input stage, the materials comprise a paper and its associated datasets. The Experiment Interpretation Agent extracts the game rules, payoff structure, and decision context. First, it identifies participant roles, the action space, the order of actions, matching mechanisms, outcome feedback, and game rules to construct a task description. Second, it identifies payoff matrices specifying the payoffs associated with different combinations of actions. For tasks involving contributions, bids, transfers, or continuous resource allocation, it extracts payoff functions, budget constraints, units, and conversion rates specifying how experimental tokens or points translate into actual remuneration. Finally, it determines what information participants possessed before each action, including their current role, known conditions, and prior history. Consequences of the current choice, future events, and unrevealed actions of other players are excluded. Participant attributes are included only when reliably supported by the source materials.

The observed dataset is constructed from actual experimental records. The Observed Data Construction Agent handles both mapping and behavioral data extraction. Drawing on the game rules, data dictionaries, and author-provided code, it establishes the correspondence between original data codes and actual actions. It then extracts participants’ recorded choices and converts each active decision into a single sample.

The simulated dataset is constructed from behavioral distributions reported in the paper. The Simulated Data Construction Agent handles both distributional evidence extraction and simulation. It extracts action frequencies, choice proportions, conditional distributions, or joint distributions from the main text, tables, figures, and supplementary materials. For each distribution, it records the corresponding task, experimental conditions, denominator, reported precision, rounding rules, and evidence location. It then generates virtual decision samples under these constraints using code with a fixed random seed.

Outputs from both branches are checked by the Validation Agent. Validation covers experimental rules, payoff relationships, field mappings, action validity, the timing of information availability, source correspondence, and counts of participants, rounds, decisions, missing records, and excluded records. Information timing determines which information may enter the input for the current decision. For example, when predicting a choice in round 3, feedback from rounds 1 and 2 may be included if the participant had already seen it before acting in round 3. For the observed-data branch, validation focuses on whether output labels faithfully represent the original behavioral records, while also checking experimental conditions and action frequencies. For the simulation branch, validation focuses on whether generated records satisfy the applicable frequencies, proportions, and constraints, and whether the same code and random seed reproduce the results. When problems are identified, the Coordination Agent routes the affected records and supporting evidence back to the responsible agent for correction. Tasks with unresolved critical semantics or statistical constraints remain pending, while construction continues for the portions that can be verified.

Finally, results from the two branches are consolidated, with their decision records organized separately into datasets sharing a common messages format. Each sample contains three messages: system, user, and assistant. “System” describes the game or experimental rules, payoff mechanism, available actions, and required output format. “User” specifies the current decision context, including the participant’s role, experimental group assignment, known numerical values, and visible history. “Assistant”contains only the corresponding valid choice, without explanation. All message content is stored as strings, and joint actions and other compound outputs follow a predefined format.

## Observed data example

Source: The Effect Of Similarity Perceptions On Human Cooperation And Confrontation [2]

**System:**

Predict a human participant's action from the experimental condition and the participant profile stated in the user message. The profile is information available to the predictor; it may be associated with behavior but does not determine the answer with certainty. This is a one-shot, two-person, simultaneous-choice game: each person makes one choice, there are no previous or later rounds, and the participant cannot see the other person's current choice. C and D are the experiment's action labels. In the Prisoner's Dilemma, C means cooperation and D means defection. In Chicken, C is the less confrontational action and D is the more confrontational action. In the Battle of the Sexes, C and D are the two alternatives; the raw file does not record the participant's preference role. Payoff pairs are written as (row-position payoff, column-position payoff), and larger payoffs are better. Do not use post-decision similarity ratings, later answers, or the eventual opponent choice. Do not invent missing information. Reply with exactly one letter: C or D.

**User:**

The participant is playing Prisoner's Dilemma under the low-threshold payoff condition, with p_s* = 0.61. The exact payoff table is: C/C -> (16, 16); C/D -> (1, 20); D/C -> (20, 1); D/D -> (4, 4). The first action is the row action and the second is the column action; the first number is the row-position payoff and the second is the column-position payoff. The participant must now choose C or D. The other participant's current choice is unknown, and both choices are made simultaneously. Participant profile available to the predictor: gender = F; age = 23 years; education = 12 years. These characteristics may be associated with behavior but do not determine it.

**Assistant:**

D

## Simulated data example

Source: Meeting And Missing Minds_ Children And Adults Use Alignment Of Intuitions To Solve Pure Coordination Games [3]

**System:**

Predict a human response in a pure coordination game. The goal is to choose the same answer as the other player or players, who are also trying to match. There is no communication to agree on an answer. This is a forced-choice verbal item: select one of the four named objects that could be found in the stated place. The four options are mutually exclusive responses; output exactly one object name: Book, Sock, Pillow, or Teddy.

**User:**

The participant is a child aged 4–5, tested individually in person with a female experimenter and an A5 booklet. The matching partner is Pippin, a parrot puppet behind a cardboard screen, who whispers its answers to the experimenter. Child and puppet cannot exchange answers to agree. The child selects a response with a counter. A sticker is offered at the end of a block. Current verbal question: In a bedroom, you would find a: Book / Sock / Pillow / Teddy. Predict the object this participant chooses to match the partner or other participants.

**Assistant:**

Pillow

### Distributions reported in the paper

| Participant group | Book | Sock | Pillow | Teddy | Total proportion | Used in the current simulated dataset |
| --- | --- | --- | --- | --- | --- | --- |
| Children aged 4–5 | 4% | 0% | 32% | 64% | 100% | Yes |
| Children aged 6–7 | 10% | 3% | 20% | 65% | 98% | No |
| Adults | 0% | 0% | 0% | 100% | 100% | Yes |

### Simulated data distribution

| Simulated participant group | Generated sample size | Book | Sock | Pillow | Teddy |
| --- | --- | --- | --- | --- | --- |
| Children aged 4–5 | 25 | 1 | 0 | 8 | 16 |
| Adults | 25 | 0 | 0 | 0 | 25 |
| Total | 50 | 1 | 0 | 8 | 41 |

## References

[1] List of games in game theory https://en.wikipedia.org/wiki/List_of_games_in_game_theory

[2] Fischer, I., & Savranevski, L. (2023). The effect of similarity perceptions on human cooperation and confrontation. Scientific Reports, 13, Article 19849. https://doi.org/10.1038/s41598-023-46609-8

[3] Perez-Zapata, D., McKenzie-Smart, X., Charest, I., & Apperly, I. (2025). Meeting and missing minds: Children and adults use alignment of intuitions to solve pure coordination games. Journal of Cognitive Psychology, 37(3), 277–292. https://doi.org/10.1080/20445911.2025.2452232
