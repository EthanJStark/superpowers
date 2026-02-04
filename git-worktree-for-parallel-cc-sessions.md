# git worktree for parallel CC sessions

**Source:** https://illuminate.atlassian.net/wiki/spaces/TECH/pages/18466734504/git+worktree+for+parallel+CC+sessions
**Last Modified:** Aug 14, 2025
**Author:** Ethan Stark
**Space:** Nearpod Product and Technology (TECH)

---

## Basic flow

### Create a new worktree with a new branch (sibling directory to your current repo)

`git worktree add ../MY-SERVICE-feature-a -b feature-a`

### Or create a worktree for an existing branch (again as a sibling)

`git worktree add ../MY-SERVICE-bugfix bugfix-123`

### Navigate to your worktree and work in isolation

`cd ../MY-SERVICE-feature-a`

`claude`   open Claude Code here

`cd ../MY-SERVICE-bugfix`

`claude`   open Claude Code here

### List all worktrees

`git worktree list`

### When you're done with a worktree (e.g., after merging the branch):

`git worktree remove ../MY-SERVICE-feature-a`

### Optional cleanup of any stale metadata:

`git worktree prune`

---

#
Using git worktrees with nptools

Create worktrees wherever / however you want if you are just investigating, planning, or don't need to run the code in your worktree. Everything that follows is if you need to run the code in the worktree

nptools discovers services by recursively scanning the your \`localenv\` directory (the directory containing \`.nptools.json\`) for \`nptools.config.json\`. If you create a worktree inside your \`localenv\`, nptools will treat both the original repo and the worktree as separate service directories. This leads to duplicate service discovery and likely Docker Compose conflicts, because both will try to run the same compose service names within the same compose project (\`-p docker_nearpod\`).

Therefore, avoid placing worktrees inside your \`localenv\`. Use one of the safe patterns below.

### Safe patterns

* Keep worktrees outside your \`localenv\` so nptools doesn't discover them automatically.
* When you need to run the worktree's code with nptools, temporarily "swap in" the worktree via a symlink at the canonical service path, so only one copy is discovered.

### Recommended: symlink swap

Example for a service at \`\~/dev/localenv/microservices/MY-SERVICE\` and a worktree at `~/worktrees/MY-SERVICE-feature-a`

#### Stop any running containers for safety

`nptools stop MY-SERVICE`

#### In the microservices dir, move the original aside and link the worktree in its place

`cd ~/dev/localenv/microservices`

`mv MY-SERVICE MY-SERVICE.orig`

`ln -s ~/worktrees/MY-SERVICE-feature-a MY-SERVICE`

#### Run as usual (nptools will now discover only the symlinked path)

`nptools start -w MY-SERVICE -d`

#### When done, restore original

`rm MY-SERVICE`

`mv MY-SERVICE.orig MY-SERVICE`

\`\`\`

### Notes:

* Discovery is cached per nptools process; each command invocation recomputes from disk, so swaps take effect immediately in new runs.
* Do not keep both the original directory and the worktree present under your \`localenv\` with \`nptools.config.json\` files, or nptools will attempt to operate on both.

### ##Alternative: scoped your \`localenv\`

If you want a fully isolated environment pointing only at a worktree, create a small "scoped" your \`localenv\` by placing a \`.nptools.json\` file in a parent directory that contains just the worktree (and any required dependencies), then run nptools from somewhere under that directory. nptools will use the nearest \`.nptools.json\` it finds upward from the current working directory as the root for service discovery.

Pros: total isolation. Cons: you must ensure any required sibling repos or shared directories (e.g., data/aux repos) are present under that scoped root.

### ##What not to do

* Don't create worktrees as siblings inside `~/dev/localenv/...` alongside the original repo. That will cause duplicate discovery and container conflicts.
* Don't try to hide duplicates by removing `nptools.config.json` from a repo you still build/run. That will break nptools behavior.

‌
