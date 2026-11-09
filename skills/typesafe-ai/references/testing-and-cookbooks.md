# TypeSafe Live API Testing and Cookbooks

This reference details testing methodologies, debugging wrong answers, and established cookbook patterns for TypeSafe System One integrations.

## Test with the live API

Sending test requests to the live API is a great way to test questions against your data. Ask the
user for permission first. Get a budget for experimentation (TypeSafe is very inexpensive, so a
little can go a very long way), disclose what data will be sent (point out any personal or private
data), and say that their `TYPESAFE_API_KEY` will be used.

- Start with a few representative cases, plus hard ones and some whose answer is "no" or "nothing
  fits".
- Compare wordings by sending each variant as a separate question in one request, over the same
  state.
- Read individual answers, not only aggregates.
- Keep the exact request payload for each case so any result can be rerun.
- Check each change against cases you didn't use while tuning.

Make sure any agent that sends test requests has network access to the API endpoint.

### When an answer looks wrong

Check these, in this order:

1. the payload as actually sent;
2. the state, against the human test;
3. the options and candidates: is the right answer among them?
4. the scope of the questions: can each one be broken down into smaller judgments?
5. the wording.

If a clear question with complete state still gets an answer you're confident is wrong, check the
jaggedness page for the model you're using. It lists known weak spots and how to work around them.
If the behavior isn't listed, the TypeSafe team welcomes examples through the channel linked on
that page. In the meantime, work out an alternative approach with the user that avoids the weak
spot.

### Yellow flags

Typically, a good change is one that makes the definition clearer or improves the state. Check each
change on cases you didn't tune on. Wording written to produce a particular value is **prompt
gymnastics**, and it tends to break on new inputs and on the next model version. Some yellow flags:

- criteria that name specific test items, or that gain a clause for each failing case;
- caveats that explain away a model quirk;
- thresholds fitted to particular cases;
- tests that assert an exact probability;
- code that quietly overrides answers.

The structural fix is usually better state, a separate question, or code.


## Cookbooks

Each of these starting points combines questions to serve one goal. Ideas outside this list are
welcome.

- **Route and fill arguments.** One request identifies what the user is asking for and which
  values go in each argument. Code then calls the handler. See
  [function calling](https://docs.typesafe.ai/cookbooks/function_calling.md) and
  [intent routing](https://docs.typesafe.ai/patterns/intent-routing.md).
- **Select instead of generate.** Code finds candidate values or spans of text, the model picks
  the intended one, and code copies or normalizes it. See
  [value extraction](https://docs.typesafe.ai/cookbooks/pre_parsed_value_extraction_cookbook.md),
  [date extraction](https://docs.typesafe.ai/cookbooks/date_extraction_cookbook.md), and
  [structure recovery](https://docs.typesafe.ai/cookbooks/autoformat.md).
- **Find and judge evidence.** Retrieve candidates and ask how relevant each one is. See
  [line-by-line search](https://docs.typesafe.ai/cookbooks/semantic_find.md),
  [re-ranking](https://docs.typesafe.ai/cookbooks/rerank_typesafe.md), and
  [classifying RAG passages](https://docs.typesafe.ai/cookbooks/classifying_rag_passages.md).
- **Turn answers into data.** Score each dimension once, then let code or users change the weights
  and views. If you have labeled outcomes, the answers can become features for a model. See
  [composite scoring](https://docs.typesafe.ai/patterns/composite-scoring.md) and
  [feature discovery](https://docs.typesafe.ai/cookbooks/autoresearch_feature_discovery.md).
- **Verify and escalate.** Check claims or fields against their evidence, and send the cases that
  fail to a person or a reasoning model. See
  [citation checks](https://docs.typesafe.ai/cookbooks/citation_check.md) and
  [extraction cascades](https://docs.typesafe.ai/cookbooks/sde_cascade.md).

The TypeSafe team is constantly adding cookbooks of well-tested patterns to the live documentation.
It's a good idea to check the [cookbooks index](https://docs.typesafe.ai/go/cookbooks.md) for one
that fits the problem you're solving.
