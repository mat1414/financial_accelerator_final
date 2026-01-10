# Financial Accelerator Classification - Quick Start Guide

## The Core Question

**Does the speaker express a belief about whether credit market conditions AMPLIFY economic shocks through feedback effects?**

This is NOT about whether credit affects the economy directly. It's about **amplification and feedback loops**.

---

## Quick Decision Tree

```
1. Does the quote mention BOTH credit/financial conditions AND real economic activity?
   NO  -> NONE
   YES -> Continue to #2

2. Does the speaker connect them through AMPLIFICATION or FEEDBACK language?
   NO  -> NONE (just mentioning both isn't enough)
   YES -> Continue to #3

3. What is the strength of the amplification belief?
   - "Significant", "powerful", "self-reinforcing" -> STRONG
   - "Limited", "modest", "some" -> MODERATE
   - "Minimal", "weak", "not seeing", "despite" -> WEAK
```

---

## Category Definitions

### STRONG
Credit markets **significantly amplify** economic shocks through feedback.

**Look for:**
- "amplifies", "magnifies", "self-reinforcing", "spiral", "feedback loop"
- "balance sheet effects feed back into credit"
- "vicious cycle", "cascade", "contagion"

**Example:** "Tighter credit is amplifying the downturn as weakening balance sheets further constrain lending"

### WEAK
Credit markets have **little or no amplifying effect**.

**Look for:**
- "despite tight credit", "resilient to", "hasn't constrained"
- "credit channel is weak", "limited transmission"
- "well-capitalized", "strong balance sheets limit amplification"

**Example:** "Despite tighter lending standards, business investment has remained robust"

### MODERATE
**Qualified or partial** amplification.

**Look for:**
- "some amplification", "modest feedback", "limited reinforcement"
- "depends on", "varies by sector", "less than past cycles"

**Example:** "Credit conditions are creating some amplification, but effects are more modest than in previous cycles"

### NONE (Default)
No financial accelerator belief expressed.

**Use when:**
- Only mentions credit OR real activity (not both)
- Mentions both but no amplification/feedback connection
- Describes direct effects without feedback dynamics
- Just forecasts or describes data

---

## Common Mistakes to Avoid

### Mistake 1: Classifying Direct Effects as STRONG
- "Higher rates reduce borrowing" -> **NONE** (direct effect, no amplification)
- "Credit conditions affect spending" -> **NONE** (no feedback mechanism)

### Mistake 2: Confusing Forecasts with Beliefs
- "Growth will slow" -> **NONE** (just a forecast)
- "Growth will slow because credit tightening amplifies the shock" -> **STRONG**

### Mistake 3: Historical Description vs. Endorsement
- "Credit was tight in 2008" -> **NONE** (just description)
- "2008 showed how credit dynamics amplify shocks" -> **STRONG** (endorses mechanism)

---

## The Key Distinction

**Direct effect (NONE):** A -> B
- "Tight credit reduces investment"

**Amplification (classify):** A -> B -> A -> B...
- "Tight credit reduces investment, which weakens balance sheets, which tightens credit further"

---

## Workflow Tips

1. **Save every 20-30 arguments** - Download your CSV regularly
2. **When in doubt, choose NONE** - It's the default for a reason
3. **Use the notes field** - Flag uncertain cases for later review
4. **Take breaks** - Fresh eyes catch more nuance

---

## Example Classifications

| Quote | Classification | Why |
|-------|---------------|-----|
| "The feedback between falling house prices and tighter credit is amplifying the downturn" | STRONG | Explicit feedback/amplification |
| "Banks are well-capitalized, limiting any credit channel effects" | WEAK | Explicitly says limited effects |
| "Some credit tightening, but less than in 2008" | MODERATE | Qualified/partial |
| "GDP grew 3% last quarter" | NONE | Just data, no credit-economy link |
| "Credit conditions are tight" | NONE | Only mentions credit, not real economy |
| "We should ease policy" | NONE | Policy preference, no mechanism |
