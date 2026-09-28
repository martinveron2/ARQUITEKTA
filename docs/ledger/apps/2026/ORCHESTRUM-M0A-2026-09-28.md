# ORCHESTRUM — Backend Milestone 0A checkpoint

Date: 2026-09-28  
Repository: `martinveron2/ORCHESTRUM`  
Working branch: `feat/backend-milestone-0a`  
Status: **IN PROGRESS — NOT DONE**

## Goal

Complete the first durable vertical slice:

```text
POST /tasks
→ PostgreSQL
→ claim
→ worker
→ FakeExecutor
→ finalize
→ event
→ SSE
→ mobile/web client
```

No DAG, Redis, planner, consensus, or real AI provider is required for Milestone 0A.

## Architecture frozen for V1

- PostgreSQL is source of truth and the initial durable queue.
- Redis is deferred until measured load justifies it.
- Worker execution is separated from FastAPI.
- `run_id` is the fencing token.
- idempotency keys remain stable across retries for the same side effect.
- events are append-only operational trace.
- PROJECT_LEDGER is project governance and is separate from runtime events.
- infrastructure must remain replaceable behind ports/adapters.

## Implemented locally

### Data layer
- `tasks`
- `subtasks`
- `execution_runs`
- `events`
- SQLAlchemy models
- Alembic initial migration
- partial index for READY claims
- partial index for RUNNING lease checks
- atomic event sequence per task

### Queue/runtime
- Postgres claim path
- reclaim of expired RUNNING leases
- stable ordering with ID tiebreak
- max-attempt guard
- retry scheduling
- heartbeat
- fencing with `run_id`
- stable idempotency key by subtask/side effect
- `finalize_success`
- `finalize_failure`
- minimum reaper
- reservation release on stale reclaimed run
- task budget reservation

### Execution
- `ExecutionPort`
- `FakeExecutor`
- durable worker skeleton

## Verified evidence

PostgreSQL 16 was run in Docker for integration tests.

```text
4 passed in 1.32s
```

Verified cases:

1. **Concurrent claim**
   - two workers race for the same subtask
   - only one receives the claim

2. **Zombie worker fencing**
   - worker A loses lease
   - worker B reclaims with a new run_id
   - worker A later attempts to finalize
   - stale result is rejected/fenced

3. **Reaper**
   - stale RUNNING subtask on final attempt
   - becomes FAILED
   - error code: MAX_ATTEMPTS_EXHAUSTED
   - old execution run becomes TIMED_OUT

4. **Concurrent budget reservation**
   - multiple workers reserve simultaneously
   - total reserved amount does not exceed task budget

Alembic migration was also verified from a clean PostgreSQL schema and created:

```text
alembic_version
tasks
subtasks
execution_runs
events
```

## Important unfinished work

### Required to close Milestone 0A
- [ ] verify complete Python test suite
- [ ] implement persistent event read contract for SSE
- [ ] add SSE endpoint with Last-Event-ID
- [ ] heartbeat comments / reconnect contract
- [ ] connect durable task creation path to API
- [ ] run full end-to-end test
- [ ] commit durable runtime changes
- [ ] push branch
- [ ] verify GitHub Actions CI green
- [ ] update ORCHESTRUM PROJECT_STATUS / ROADMAP after evidence exists

### Explicitly deferred
- DAG/planner
- approvals
- Redis
- multi-provider routing
- real LLM provider
- distributed workers
- advanced observability

## Current blocker / interruption

During full-suite verification the remote EC2 command channel began timing out. Therefore the full suite result was not accepted as evidence and no DONE claim was made.

## Next action

Resume on `feat/backend-milestone-0a` and execute, in this order:

1. verify repository working tree and durable runtime files
2. rerun full Python suite against PostgreSQL 16
3. implement SSE from persisted `events`
4. build the E2E path
5. run concurrency + E2E + legacy tests
6. commit and push
7. verify CI
8. only then mark Milestone 0A DONE

## Definition of DONE

```text
IMPLEMENTED
+ TESTED AGAINST REAL POSTGRES
+ E2E VERIFIED
+ DOCUMENTED
+ COMMITTED/PUSHED
+ CI GREEN
```


## Closure protocol result

Applied on 2026-09-28.

### HECHO
- durable runtime code committed and pushed on `feat/backend-milestone-0a`
- PostgreSQL 16 local integration suite verified: **14 passed in 1.63s**
- Alembic migration verified from clean schema
- M0A state synchronized in ORCHESTRUM PROJECT_LEDGER / PROJECT_STATUS / ROADMAP / ARCHITECTURE / CHANGELOG
- draft PR #12 opened
- issue #2 updated with checkpoint evidence
- unrelated local files preserved and excluded from milestone commit

### PENDIENTE
- durable FastAPI path
- persisted SSE / Last-Event-ID
- E2E vertical slice
- verify GitHub Actions green
- only after that: mark M0A DONE

### ESTADO GIT
Milestone work is committed/pushed on the feature branch. The EC2 working tree still contains unrelated frontend/common-module changes generated or owned outside this backend slice; they were intentionally not reset, deleted or included.

### PRÓXIMO PASO
Resume branch `feat/backend-milestone-0a` → wire durable API path → SSE → E2E → full tests → CI → M0A DONE.


### CI closure check

GitHub Actions run #144 was checked after the closure push and is **not green**.

Observed:
- web: failure
- Python 3.11: cancelled
- Python 3.12: failure
- job metadata returned no executed steps and runner_id = 0

The exact GitHub-side cause was not resolved during closure. Local PostgreSQL verification remains: **14 passed in 1.63s**. M0A stays IN PROGRESS.

Next session must inspect/re-run CI before any DONE claim.
