# TypeSafe Integration Architecture: State, Requests, and Answer Processing

## Design the state

A useful check for any question is the **human test**: could a smart person, shown only this state
and this question, answer quickly by intuition? When a question fails the test, the fix is usually
in the state, not in the wording.

- **Give what a person would look at.** That means who sent each message, the full thread rather
  than a truncated last line, names rather than raw IDs or @-mention markup, and the item the
  question is about rather than the whole catalogue. State facts your code already knows, such as
  "all messages in `replies` were sent after the refund was issued", rather than leaving the model
  to work them out again.
- **Supply facts the model may lack**, such as what an internal product name or codename refers
  to.
- **Ensure every field in the state is relevant.** Irrelevant detail clutters the context and
  reduces accuracy. A field added for one question can sway the answer to another, and the model
  can read an empty list as a signal.
- **Be mindful when truncating.** Truncate long strings only when you need to, and check that the
  cut doesn't remove context the questions need.
- **Structure with named fields.** JSON objects with descriptive keys work better than a string of
  serialized JSON. They also let a question refer to each part by its path. Stable names such as
  `candidates.refund_policy` are easier to refer to than array positions.
- **Consider leaving out what no person could judge**, such as an unreadable crop or a distinction
  experts dispute. The model's answer there tends to be noise, and code will treat that noise as
  signal.


## Compose requests

**Bundle questions that share state.** A handy heuristic: if two calls would send the same state
with different questions, they can likely be one call. Questions are cheap and run in parallel, and
the state is read and paid for once. See
[parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions.md).

**Ask speculatively**, meaning ask a question before you know whether you'll need its answer. A
question that only matters in some cases can go in the same request as the question that
identifies the case. Ask "Is `order` a return request?" and "Which item in `order.items` is being
returned?" together, and have code read the second answer only when the first is yes. The second
question doesn't need an "if" clause, because code handles the condition. See
[speculative fan-out](https://docs.typesafe.ai/patterns/fan-out.md).

A second request is usually worth it when:

- code needs an answer to build the next state, fetch evidence, or choose the next options;
- a state field needed for one question measurably misleads another;
- different sets of questions need to be cached or versioned separately.


## Read the answers

### Confidence is rarely the gate

Naive implementations often use an answer's `confidence` as the check that decides whether code
acts. Confidence measures how concentrated an answer's probability distribution is, which is not
the same as how likely the answer is to be correct. Think about what the probabilities should look
like in your use case; another calculation over them may suit it better.

### Probabilities and thresholds

- **A probability is the likelihood that an answer is correct.** Jev isn't a calculator for
  probability problems. Ask it for judgments, and do any math on odds or probabilities in code. A
  Noul near 0.5 usually means the state doesn't settle the question.
- **The top answer is a good default**: the Choice's top option, or the Score's position.
- **0.7 and 0.3 make good starting thresholds for a Noul**: above 0.7 reads as yes, below 0.3 as no,
  and the band between means the question isn't settled, which can get its own row in the truth
  table. Adjust them when the application calls for it, and be wary of over-fitting them to a
  handful of test cases.
- **Look at Score distributions.** The Score's position can get pulled toward the middle and hide
  two-peaked answers, so look at the level probabilities before deciding which value your code
  reads.
