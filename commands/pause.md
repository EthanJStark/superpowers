---
description: Pause plan execution gracefully with resume command
---

# Pause Execution

Complete your current in-progress task, then:

1. **Update acceptance criteria** for all completed tasks (passes: true)
2. **Output resume command** in this exact format:

---
**Session paused.** To continue in a fresh session, copy-paste:

```
/superpowers-fork:execute-plan $PLAN_PATH

RESUME INSTRUCTIONS: Examine plan's acceptance criteria. Tasks with passes: true are already complete. Start execution from the first task whose acceptance criteria has passes: false. Do not re-execute completed tasks.
```

Where $PLAN_PATH is the absolute path to the plan file.
---

3. **Stop execution** - do not continue to next task
