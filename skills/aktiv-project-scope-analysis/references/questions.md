# Gaps, and the questions that close them

## The gap taxonomy

Walk this list against every requirement. These are the categories that actually cost
time on Odoo projects, in rough order of how often they bite.

**1. Client-supplied dependencies.** The requirement is clear and buildable, but it
needs something only the client has: webfont files and their licence, logo variants,
photography, real copy, product data, API credentials, social URLs, legal text. This is
the most common cause of a finished module that cannot go live. Every one of these is a
dated deliverable with a named owner, not a footnote.

**2. Hosting conflicts.** The requirement implies server-side behaviour on a platform
that will not run it. Re-read it, say what survives, say what does not.

**3. Presentation mistaken for enforcement.** "Hide", "restrict", "only X should see" —
find out whether they mean the screen or the data. The answers have different costs and
different platforms.

**4. Hidden multiplicity.** Multi-language, multi-company, multi-website, multi-currency,
multi-warehouse. Each one multiplies build and test. None of them is usually stated.
Ask explicitly; never assume one of anything.

**5. Unstated maintenance model.** Who edits this after go-live, and where? Backend
records, the website editor, or a developer? On website work this decides the
architecture, so it cannot be deferred — and clients answer it readily when asked plainly.

**6. Missing acceptance criteria.** The requirement cannot be marked done. "Fast",
"user-friendly", "like competitor X", "professional looking". Convert each into
something observable, propose it, and let the client correct you.

**7. Duplicate of standard Odoo.** The client is asking to pay for what they already
have. Say so — it buys credibility for the rows where you do ask for budget.

**8. Integration with no contract.** A named system with no API documentation, no
credentials, no sample payload, no error handling expectation, no sync direction and no
frequency. Every one of those is a separate question.

**9. Migration with no source.** A data migration with no source format, no volume, no
sample export, no rule for what happens to records that fail validation.

**10. Legal and compliance load.** Testimonials and reviews carry disclosure rules —
in the US, FTC 16 CFR Part 255 requires endorsements to be genuine and material
connections disclosed, which makes invented demo testimonials a go-live blocker rather
than a copy task. Personal data carries GDPR. Pricing and tax display carry local rules.
Flag these as findings even when nobody asked; the client's counsel decides, not you,
but they cannot decide what they were never told.

**11. Volume and scale unstated.** Record counts, concurrent users, file sizes, catalogue
size. A carousel of 10 products and one of 10,000 are different builds.

**12. Reporting and exports assumed.** "They'll need a report" with no columns, no
filters, no format, no recipient, no schedule.

**13. Roles and permissions assumed.** Who sees this, who edits it, who approves it. Often
entirely absent from website and portal scopes.

**14. Silence.** The requirement in a returned SOW with an empty response cell. The
wireframe band nobody wrote about. The feature in the writing that was never drawn.
Absence is a finding — record it as one rather than passing over it.

## Writing questions the client will answer

A client given thirty flat questions answers none. These rules come from questions that
did get answered.

**Group by decision, not by document.** The client thinks in outcomes, not in your
row numbers.

**Say what changes based on the answer.** *"Should prices be hidden from the page, or
genuinely unobtainable? The first is straightforward on your current hosting; the second
needs server-side code, which Odoo Online will not run, so it would mean moving to
Odoo.sh."* That is a question a client can answer in one sitting.

**Offer options with a recommendation.** Closed questions with a named default get
answered far more often than open ones. Give two or three concrete choices, say which
you recommend and why, and make clear they can pick another.

**Ask in the client's language.** Not "should `is_published` gate the carousel" but
"should unpublished products still show on the home page".

**One decision per question.** A question containing "and" gets half an answer.

**Mark what blocks.** Split the list in two:

- **Blocking** — the estimate or the build cannot proceed. Keep this list short. If
  everything is blocking, nothing is.
- **Needed before go-live** — real, dated, but work continues meanwhile.

**Never ask what the documents answer.** Re-read before sending. Asking a client
something they already wrote down costs more credibility than any single answer is worth.

**Carry an assumption for everything not blocking.** *"Assumed one company, one website,
English only — tell us if not."* That keeps work moving and puts the correction on
record. Every assumption goes in the analysis under its own heading.

## Format

Number them, and use those numbers everywhere — the matrix references them, so an answer
maps straight back to the rows it unblocks.

```
Q3  (Blocking — affects hosting choice)
    Should prices be hidden from the page, or genuinely unobtainable?

    Removing them from the page stops them being read or scraped from the site,
    and works on your current Odoo Online plan. Making them genuinely
    unobtainable means server-side changes, which Odoo Online does not permit —
    that would mean moving to Odoo.sh.

    We recommend the first unless the price list is commercially sensitive.

    Affects requirements: R12, R13, R14
```
