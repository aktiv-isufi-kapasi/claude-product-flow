# Proving the verdict

"Odoo does that already" and "that needs custom code" are the two most expensive
sentences in the analysis. Neither is ever written from memory.

## First, write down the platform baseline

Three answers, and all three change verdicts. Put them at the top of the analysis.

### Hosting — what may be built

| | Odoo Online (SaaS) | Odoo.sh | On-premise |
|---|---|---|---|
| Custom Python | No | Yes | Yes |
| Module delivery | Apps → Import Module, data only | git push | any |
| Controllers / routes | No | Yes | Yes |
| ORM overrides, compute, constraints | No | Yes | Yes |
| Automation | `ir.cron` / `ir.actions.server` sandboxed code | full | full |
| Shell, cron, external services | No | Yes | Yes |
| Third-party apps | Only data-only ones | Yes | Yes |

On Odoo Online, every requirement that implies server-side logic needs re-reading. Some
survive as data-only work, some become presentation-level only, and some are genuinely
not feasible as written. Say which, per requirement — "SaaS limitation" as a blanket
note is not an analysis.

The distinction that catches people: **presentation-level is not enforcement.** Removing
a value from a rendered page stops it being read or scraped from that page; it does not
stop a crafted request to a JSON endpoint. If the requirement is "customers must not see
prices", that is presentation. If it is "prices must not be obtainable", that needs
server-side work and therefore rules out Odoo Online. Ask which one the client means —
they are rarely aware there is a difference.

### Edition — what exists at all

Community and Enterprise are different products. A requirement met by an Enterprise app
on a Community project is custom work, and vice versa is a licence cost. Check which
tree the module lives in before calling anything standard. Studio, and everything that
depends on it, is Enterprise.

### Version — what is standard this year

Behaviour moves between versions. A verdict from 17.0 does not transfer to 19.0. If the
source for the target version is not available, say so in the analysis and mark those
verdicts provisional rather than quietly answering from a version you do have.

## Proving "standard"

Grep the source for the target version and edition. Typical checkouts:

```
~/odoo-versions/18    community
~/odoo-versions/18e   enterprise
~/odoo-versions/19    community
~/odoo-versions/19e   enterprise
```

Ask the user for the path if it is not there — do not substitute a different version.

```bash
V=~/odoo-versions/18          # and 18e for enterprise
ls $V/addons | grep -i <keyword>                       # is there a module for it
grep -rn "<field_or_method>" $V/addons/<module>/        # does it do the specific thing
grep -rln "<setting label>" $V/addons/*/views/          # is it a configuration option
```

Record the evidence in the matrix: the module name, and `file.py:line` where the
behaviour itself is the question. A verdict of Standard with no module named is not a
verdict.

Two failure modes to avoid:

- **Near-miss standard.** A module that does *almost* this. Say what it does and what it
  does not — `ecommerce_access` gates the whole shop, it does not hide prices. A
  near-miss recorded as Standard becomes a defect in UAT.
- **Standard but not for this user.** Behaviour that exists for internal users and not
  for portal or public, or that a record rule hides. Check who the requirement is for.

## Proving "config"

Find the setting. Name the menu path — *Settings → Website → Shop → Product Prices*.
If you cannot find the path, it is not config.

## Proving "an app covers it"

Search `apps.odoo.com` for the target version, then record:

| | |
|---|---|
| URL | the listing |
| Version | must match the target; an app for 17.0 is not an answer for 19.0 |
| Price | per month or one-off, and per user where that applies |
| Maintainer | Odoo SA, a known partner, or an unknown |
| Last updated | an app untouched for two versions is a liability |
| Hosting | does it install on Odoo Online — most do not, being Python |
| Licence | OPL / AGPL / LGPL, and whether it can be modified |

Then say whether you recommend it. "An app exists" is not a recommendation — a
€300/month app for one checkbox is a finding, not a solution. Where an app covers 80% of
the requirement, say which 20% it does not.

Never state a price or a URL you have not read. If the search is unavailable, mark the
row Unclear and raise it as a question rather than guessing.

## Proving "not feasible as specified"

Three things, always together:

1. The constraint that stops it, named specifically.
2. The nearest thing that *is* feasible.
3. What the client loses by taking it.

A "not feasible" with no alternative reads as a refusal and gets escalated. With an
alternative it reads as a decision and gets answered.

## Accounting for existing development

On a change request, read what is already built before classifying anything. A module
directory, its context file, or the live instance. Requirements already delivered are
current scope, not gaps — and a gap list padded with delivered work destroys the
client's trust in the rest of it.

Where existing work partly covers a requirement, say how far it goes and what the delta
is. That delta is the estimable unit.
