# TypeSafe Questions, Primitives, and Criteria Guide

This reference details question types, primitives, and criteria patterns for TypeSafe System One models.

## Write the questions

Break complex judgments or decisions into their parts, and combine the answers in code with
weighted sums, boolean logic, thresholds, or other heuristics to reach the final decision. For
example, rather than asking "Is this fraud?" or "Is this spam?", ask the set of atomic questions
about what might make something fraud or spam. Each question tends to work best when it asks for
**one judgment** that a person could make at a glance.

- **Ask the concrete, observable thing.** Aim for something a person could point to: "Is a SQL
  query built by string concatenation here?" rather than "Are there SQL injection risks?".
- **One judgment per question; beware the "or".** Two conditions joined by "or" or "and" usually
  work better as two questions. Likewise, a list of rules usually works better as one question per
  rule.
- **Anchor intent to the goal.** When the judgment is about what someone wants, it helps to name
  their goal: "Which of these files does the user want copied?" rather than "Which of these names
  the main input?".
- **Name the subject directly.** "Where is the coffee mug in `photo`?" reads better than "Where is
  `target` in `photo`?" with the target defined somewhere else. Context that only one question
  needs, including an image, usually fits best in that question's instructions (the question text)
  or its criteria (the descriptions of its options, its levels, or what yes and no mean). Context
  that many questions share can go in the state once, and each question can refer to it by its
  exact path in backticks. When you ask the same question about many items, it usually works better
  to put each item into its own question than to give an ID the model has to look up in a shared
  list.
- **Each question is answered on its own.** Questions in a request can't see each other or each
  other's answers. Any context a question relies on belongs in the state or in that question.
- **Write plainly.** A question isn't an LLM prompt. Preambles, "consider X, Y, and Z" lists, and
  output-format instructions add noise. Descriptions of the options belong in the criteria, not in
  the question. Phrase the question so that a true answer means yes. Watch for double negatives,
  and for presuppositions such as "the next step".
- **Name the case that causes confusion.** If answers keep mixing up two outcomes, say in the
  criteria what separates them, using the specific case. For example, for "Is this a refund
  request?", note that a question about the refund policy is not a request. A vague exclusion such
  as "not other kinds of message" helps less, and can draw attention to the wrong answer.

### Criteria

- **Ask about the null case separately.** A Box always returns a location and a Choice always picks
  an option, even when nothing fits. Pair either one with a Noul in the same request that asks
  whether anything fits ("Is there a coffee mug in `photo`?", "Does `message` name any of our
  products?"), so code can tell when nothing does. As of Jev 1.14, this companion Noul usually works
  better than a "none of the above" option.
- **Option names are sent to the model; question IDs are not.** Names that describe the content
  (`refund_request`, `shipping_delay`) help the model. Positional names (`A`, `left`, `option_1`)
  give it nothing meaningful to go on and can bias the answer.
- **Keep options distinct and concrete.** Wording that options share with each other, or with the
  input, can pull probability toward those options. An option that covers several meanings is
  often worth splitting, because its probability can't tell code which meaning applied. Direction
  and magnitude usually work better as separate questions, so that the answer to one doesn't get
  mixed into the other.
- **Describe each Score level as a situation.** Each level should make sense when read on its own:
  "The customer mentions a minor inconvenience" rather than "More upset than the previous level".
- **Describe a Noul's `false` criterion as a concrete situation**, such as "the package arrived on
  time", rather than as "not late".
- **Use a Noul per statement when more than one can be true.** A Choice picks one option, so a
  message that is both a refund request and a complaint forces it to split probability between the
  two. Separate Nouls let each one be true on its own.
