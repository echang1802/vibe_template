# Vibe Coding Guidelines

This document provides a lightweight, test-first workflow for collaborating with AI coding agents. The shared agent rules live in [`.github/agents-instructions.md`](.github/agents-instructions.md), [`templates/user-story-template.md`](templates/user-story-template.md) helps describe a change before implementation, [`test/agents-instructions.md`](test/agents-instructions.md) helps describe a testing rules and [`app/agents-instructions.md`](app/agents-instructions.md) helps describe a app specific rules.

## Workflow

1. Describe the requested change as a user story, using the template when helpful.
2. The agent inspects the relevant code and proposes specific test scenarios.
3. Review and approve the proposed scenarios before implementation begins.
4. The agent adds and runs the tests, implements the simplest complete solution, and runs the relevant test suite.
5. The agent summarizes the result and asks whether you want a commit. Commits are only made after the required tests pass and you confirm.

## Git and commits

- Do not make changes directly on `main`, `master`, or `dev`. Pull the current branch from `origin`, then create a task branch such as `feature/<feature_name>` or `hotfix/<hotfix_name>`.
- If already on a task branch shared by two or more people, pull from `origin` before continuing.
- Keep commit titles descriptive and under 100 characters. Put useful, concise context in the commit body.
- Never commit before all unit tests pass. Ask before committing after each completed change request.

## Code and documentation

- Prefer the simplest implementation that meets the requirement. Avoid unnecessary dependencies and complexity.
- Reuse code and extract general, reusable functions or methods where appropriate.
- Use `snake_case` for functions and variables. Use `Uppercase_first_snake_case` for classes (for example, `User_account`).
- Document input and output types using the conventions of the language in use.
- Update the README when a change makes its existing guidance or usage information inaccurate or incomplete.

See [`.github/agents-instructions.md`](.github/agents-instructions.md) for the full agent workflow and [the user story template](templates/user-story-template.md) to prepare a request.
