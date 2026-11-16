# Agent Instructions

Apply these guidelines to every coding task in this workspace.

## Before implementation

- Understand the user's request as a user story: who needs the change, what they need, and why. If the prompt does not clearly communicate this, help the user express it as a user story and confirm the intended scope before coding.
- Inspect the relevant code, tests, and existing project conventions before proposing a solution.
- Follow test-driven development. Propose concrete new or updated test scenarios that cover expected behavior and important edge cases. Show them to the user and wait for approval before implementing the change.
- After approval, add or update the tests and run them. Implement the change to satisfy the approved scenarios, then run the relevant tests again.
- If tests fail, investigate and report the failure; do not make a commit.

## Implementation

- Choose the simplest complete implementation. Do not add dependencies or complexity without a demonstrated need.
- Avoid duplicating logic. Reuse existing helpers or create small, general functions or methods when appropriate.
- Use `snake_case` for functions and variables.
- Use `Uppercase_first_snake_case` for classes (for example, `User_account`).
- Document input and output types using the language's established type annotation or documentation conventions.
- Preserve existing behavior outside the requested change.
- Update the README when the change makes its existing usage or guidance inaccurate or incomplete.

## Git workflow

- Check the current branch before making changes.
- Do not work directly on `main`, `master`, or `dev`. If currently on one of these branches, pull it from `origin` and create a task-specific branch before editing. Use a descriptive prefix such as `feature/<feature_name>` for a feature or `hotfix/<hotfix_name>` for a hotfix.
- If already on a task branch shared by two or more people, pull from `origin` before continuing.
- Do not switch branches or overwrite existing work without checking for uncommitted changes first. Preserve the user's work.
- Keep commit titles descriptive and under 100 characters. Add concise, relevant details in the commit body without overwhelming it.
- After each completed change request, ask the user whether they want a commit. Do not commit unless the user confirms and all unit tests pass.

## Completion

- Report the changes made and the tests run, including any failures or tests that could not be run.
- Do not claim tests passed unless they were actually run and passed.
- Ask whether to commit only when the change is ready; if unit tests fail, explain that a commit must wait until they pass.
