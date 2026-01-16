# Credit Channel Classification - Quick Start Guide

## The Core Question

**Does the speaker express a belief about whether credit market conditions affect or amplify economic activity?**

The quote must mention BOTH credit conditions AND real economic activity with a causal connection.

---

## Quick Decision Tree

```
1. Does the quote mention BOTH credit/financial conditions AND real economic activity?
   NO  -> NULL
   YES -> Continue to #2

2. Does the speaker connect them causally?
   NO  -> NULL (just mentioning both isn't enough)
   YES -> Continue to #3

3. What type of relationship does the speaker describe?
   - Amplification/feedback language -> STRONG or MODERATE (see below)
   - Direct effect (credit -> activity) -> MODERATE
   - Denial of effect -> WEAK
```

---

## Category Definitions

### STRONG
Credit conditions **SIGNIFICANTLY AMPLIFY** shocks through feedback effects.

**Look for:**
- Feedback language: "self-reinforcing", "spiral", "vicious/virtuous cycle", "feedback loop"
- Amplification language: "magnify", "amplify", "exacerbate", "compound"
- Closed-loop chains: "tighter credit -> weaker activity -> tighter credit"

**Example:** "Credit conditions are amplifying the downturn as weakening balance sheets further constrain lending"

### MODERATE
Either (a) **QUALIFIED amplification** OR (b) **DIRECT credit effects** without feedback language.

**Type A - Hedged amplification:**
- "some amplification", "modest feedback", "may be reinforcing"
- "less amplification than past cycles"

**Type B - Direct credit effects:**
- "Tighter credit is slowing investment"
- "Weak balance sheets are restraining consumption"
- "Credit availability is affecting business spending"

**Example:** "Balance sheet repair will take years, restraining growth"

### WEAK
Credit conditions have **LITTLE or NO effect** on economic activity.

**Look for:**
- "despite tight credit", "credit hasn't constrained", "minimal impact"
- "strong balance sheets", "well-capitalized", "robust credit access"
- "driven by fundamentals not credit", "credit channel is weak"

**Example:** "Despite tighter lending standards, business investment has remained robust"

### NULL (Default)
No credit channel belief expressed.

**Use when:**
- Missing credit conditions OR real activity component
- Mentions both but no causal connection
- Pure wealth effects without credit mechanism
- Pure interest rate transmission without credit frictions
- Just forecasts or describes data

---

## Common Mistakes to Avoid

### Mistake 1: Classifying Pure Interest Rate Effects as Credit Channel
- "Lower rates stimulate demand" -> **NULL** (no credit friction logic)
- "Easing will boost the economy" -> **NULL** (no mechanism stated)

### Mistake 2: Classifying Wealth Effects as Credit Channel
- "Falling home prices reduce consumption via wealth effects" -> **NULL**
- "Falling home prices constrain home equity borrowing" -> **MODERATE** (credit mechanism)

### Mistake 3: Confusing Duration with Amplification
- "Balance sheet repair will take years, restraining growth" -> **MODERATE** (prolonged direct effect)
- "Balance sheet problems create self-reinforcing weak growth" -> **STRONG** (feedback)

---

## The Key Distinctions

| Relationship | Example | Classification |
|-------------|---------|----------------|
| Amplification (unhedged) | "Credit tightening is amplifying the downturn" | STRONG |
| Amplification (hedged) | "Some amplification, but effects are modest" | MODERATE |
| Direct effect | "Tight credit is slowing investment" | MODERATE |
| Denial | "Despite tight credit, growth remains strong" | WEAK |
| No relationship | "Growth was 3% last quarter" | NULL |

---

## Workflow Tips

1. **Save every 20-30 arguments** - Download your CSV regularly
2. **When in doubt, choose NULL** - It's the default for a reason
3. **Use the notes field** - Flag uncertain cases for later review
4. **Take breaks** - Fresh eyes catch more nuance

---

## Example Classifications

| Quote | Classification | Why |
|-------|---------------|-----|
| "The feedback between falling house prices and tighter credit is amplifying the downturn" | STRONG | Explicit feedback/amplification |
| "Credit tightening is slowing business investment" | MODERATE | Direct effect, no feedback language |
| "Some amplification, but less than in 2008" | MODERATE | Hedged amplification |
| "Banks are well-capitalized, limiting credit effects" | WEAK | Explicitly says limited effects |
| "Despite tighter lending, investment remains robust" | WEAK | Denial of effect |
| "GDP grew 3% last quarter" | NULL | Just data, no credit-economy link |
| "Credit conditions are tight" | NULL | Only mentions credit, not real economy |
| "Lower rates will boost spending" | NULL | Interest rate channel, not credit channel |
