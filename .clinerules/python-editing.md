# Python File Editing Rules

## Always re-read before editing
- Before modifying any Python file, always use read_file to get the current state of that file, even if you read it earlier in this session. Never edit from memory or from a plan-phase snapshot.

## Prefer small, surgical edits
- Use replace_in_file with the smallest possible SEARCH block that uniquely identifies the location. Include 2-3 lines of context above and below the change target. Never use replace_in_file with SEARCH blocks larger than ~20 lines.

## Never use write_to_file on existing Python files
- Do not use write_to_file to modify existing .py files. Only use write_to_file for brand new files. If replace_in_file fails twice on the same block, stop and ask the user for guidance instead of falling back to write_to_file.

## One logical change per replace_in_file call
- Do not bundle multiple unrelated edits into one replace_in_file call.
- Make one change, verify (or re-read), then proceed to the next.

## Validate syntax after edits
- After modifying any Python file run from project root and fix reported errors: pre-commit run --files <filename>
- Wait for the command to complete before proceeding to the next changed file, do not keep it running on the background.
- Report any errors immediately before proceeding.

## No speculative edits
- Do not edit files that are not directly required by the current task.
- If you think another file may need changing, ask first.