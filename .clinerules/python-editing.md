# Python File Editing Rules

## Always re-read before editing
- Before modifying any Python file, always use read_file to get the current
  state of that file, even if you read it earlier in this session. Never edit
  from memory or from a plan-phase snapshot.

## Prefer small, surgical edits
- Use replace_in_file with the smallest possible SEARCH block that uniquely
  identifies the location. Include 2-3 lines of context above and below the
  change target. Never use replace_in_file with SEARCH blocks larger than
  ~20 lines.

## Never use write_to_file on existing Python files
- Do not use write_to_file to modify existing .py files. Only use
  write_to_file for brand new files. If replace_in_file fails twice on the
  same block, stop and ask the user for guidance instead of falling back to
  write_to_file.

## One logical change per replace_in_file call
- Do not bundle multiple unrelated edits into one replace_in_file call.
- Make one change, verify (or re-read), then proceed to the next.

## No speculative edits
- Do not edit files that are not directly required by the current task.
- If you think another file may need changing, ask first.

## Declare your plan before a multi-file edit
- If a task requires changing more than 2 files, list all files and the
  intended change for each before making any edits. Wait for confirmation.

## Summarize changes at the end
- After all edits and a clean pre-commit run, output a brief summary:
  which files changed, what was changed, and the final pre-commit result.
  Do not proceed to new tasks without this summary.

## Pre-commit hook stack

Hooks run in this order. Each must pass before proceeding to the next file.

1. **black** — reformats code automatically. Never manually format code;
   black will override it. Line length is black's decision, not yours.

2. **isort** (profile: black) — sorts imports automatically, compatible with
   black's style. Never manually reorder imports; isort will override it.
   If adding a new import, place it roughly correctly; isort will fix order.

3. **pylint** (local, sees project packages) — semantic linter. Common issues:
   - Missing or incorrect type annotations
   - Unused imports or variables (remove them, do not comment out)
   - Undefined names (check actual project imports, do not guess)
   - Naming convention violations
   If pylint fails, read the full message including the message code (e.g.
   C0114, W0611). Fix only the flagged lines. Do not refactor surrounding
   code to "clean up" — that risks new violations.

4. **pydocstyle** (convention: google) — enforces Google-style docstrings.
   Every public module, class, method, and function needs a docstring.
   Google style requires: summary line, blank line, then Args:/Returns:/
   Raises: sections as applicable. One-liners are only valid for trivial
   functions with no arguments to document. Do not use numpy or sphinx style.

5. **mypy** (strict, via mypy.ini) — static type checker.
   - pydantic and pydantic-settings stubs are available
   - types-requests and types-pytz are available
   - Do not use `# type: ignore` to silence errors unless explicitly asked
   - If a type error seems unfixable without ignoring, stop and report it

## Pre-commit interaction rules
- black and isort run first and auto-fix; after they run, re-read the file
  before attempting any manual fix, because the file content will have changed.
- pylint and pydocstyle do NOT auto-fix; their errors require manual edits.
- A pylint error does not imply a pydocstyle error and vice versa — treat
  each hook's output independently.
- If black/isort would fix something, do not pre-empt them manually.
- Wait for completion. Do not run it in the background.
- **Before attempting any fix**, re-read the full current state of the file.
- Identify the exact line(s) flagged. Fix only those lines — do not touch
  surrounding code that is not part of the error.
- You are allowed at most 2 fix-and-retry cycles per file per task.
  If the file still fails after 2 attempts, stop immediately and report:
  (1) the hook name, (2) the exact error lines, (3) what you tried.
  Do not loop further.