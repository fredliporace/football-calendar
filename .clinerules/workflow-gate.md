## Implementation phases (multi-file tasks)

For any task touching more than one file or adding new functions/classes,
follow these phases in order. Do not mix phases.

### Phase 1 — Logic and tests
- Implement the required logic and corresponding tests.
- Do not run pre-commit during this phase.
- Docstrings may be omitted or left as stubs (e.g. `"""TODO"""`) during
  this phase.
- When logic and tests are complete, explicitly state: "Phase 1 complete.
  Ready for pre-commit pass." and wait for confirmation before proceeding.
- Make sure unit tests passes before proceeding to Phase 2

### Phase 2 — Pre-commit cleanup
- Re-read every file modified in Phase 1 before touching anything.
- Complete all stub docstrings using Google convention before running
  pre-commit for the first time — pydocstyle will flag them all otherwise.
- Run pre-commit on all modified files, fix failures, and apply the
  failure budget (max 2 fix-and-retry cycles per file).
- After a clean pre-commit make sure unit tests are passing before proceeding.
- Only after a clean pre-commit run across all files, summarize changes.