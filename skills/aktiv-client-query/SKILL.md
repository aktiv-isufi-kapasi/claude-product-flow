---
name: aktiv-client-query
description: "Draft a message to the client asking for the information or decisions we need. Written for the client to read and answer quickly, not for a developer."
---

Draft a message to the client asking for the information or decisions we need. Written for the client to read and answer quickly, not for a developer.

## Steps

1. Read the topic from the arguments (e.g. `fonts and photography`, `spanish scope`, `hero shadow`). If none is given, use the open questions from this session.

2. Collect the candidate questions, in this order:
   - What the user named in the arguments.
   - What came up in this session: work that was blocked, an assumption that had to be made, a choice that is the client's to make, anything delivered with a caveat.
   - Open items already recorded in the project notes or docs, so a long-standing blocker is not forgotten.

3. Drop anything we can answer ourselves. Check the code, the database or the site first. Never ask the client something a two minute look would settle.

4. Check whether it has been asked before. If it has, say so in the draft ("asked on <date>, no reply yet") rather than asking again as if it were new.

5. If there are more than five questions, group them by topic and ask the user which group to send now. One message, one topic, five questions at most.

6. Confirm the two things that change the wording:
   ```
   Who is this going to? (Enter for the client contact)
   Anything that must NOT go in? (Enter for nothing)
   ```

7. Write the draft in the format below and present it in the chat, ready to paste.

8. Offer to save it as a txt file: `~/Desktop/query_<YYYY-MM-DD>_<topic>.txt`, plain text, no markdown.

## Format

```
Subject: <what we need, in five words or so>

<One or two sentences of context: what we are working on and why this is needed now.>

1. <The question, in one sentence.>
   Why we need it: <what it unblocks, in plain language.>
   If we do not hear back: <the default we will go with.>
   Options: <a, b or c, where there is a sensible shortlist.>

2. <Next question, same shape.>

<Closing line: what we will do next, and by when we need an answer for it not to hold anything up.>
```

Leave out any line that adds nothing. A question with no sensible default and no options is just the question and the why.

## Rules

**Language**
- Write for someone who does not use Odoo. No field names, model names, module names, version numbers or file paths.
- Describe what the client sees on their site or screen, not how it is built.
- Short sentences. A client should be able to answer from their phone.
- Never use em dashes. Use `:` or `-` instead.

**Questions**
- Every question gets a recommended default, so silence still lets the work continue.
- Offer a shortlist wherever the answer is a choice. Asking somebody to compose a paragraph gets no reply; asking them to pick one of three does.
- One decision per question. If it has two parts, it is two questions.
- Say what each answer unblocks. Never write "as soon as possible": state what waits on it.
- Mark a blocker as a blocker, plainly, and say what stops if it stays unanswered.

**Honesty**
- Only ask about things that actually came up. Never invent a question to fill the list.
- Never attribute something to the client that they did not say.
- If we already chose a direction and are asking them to confirm it, say that we have already built it that way.

**Safety**
- No credentials, no database names, no internal URLs or server paths.
- No staff names other than the sender. Refer to the team as "we".
- Do not attach or quote internal notes; rewrite the point in the client's terms.
