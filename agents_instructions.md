# Vibe Coding Guidelines

This document defines a lightweight, test-first workflow for collaborating with AI coding agents. Its purpose is to standardize development practices, maintain code quality, and ensure human oversight throughout the implementation process.

The guidelines are organized into specialized documents:

- [`.github/agents-instructions.md`](.github/agents-instructions.md) defines the shared agent workflow and Git management rules.
- [`templates/user-story-template.md`](templates/user-story-template.md) provides a structured template for describing changes before implementation.
- [`test/agents-instructions.md`](test/agents-instructions.md) defines testing guidelines, conventions, and frameworks.
- [`app/agents-instructions.md`](app/agents-instructions.md) defines application-specific coding guidelines.
- [`agents_concerns_and_suggestions.md`](agents_concerns_and_suggestions.md): Centralized log of concerns, potential risks, and improvement suggestions identified by AI agents during development.

## Workflow

1. **Define the requirement:** Describe the requested change as a user story, using the provided template when appropriate.
2. **Analyze and propose tests:** The agent inspects the relevant code and proposes specific test scenarios based on the requirements.
3. **Review and approve:** The user reviews and approves the proposed test scenarios before implementation begins.
4. **Implement and validate:** The agent writes and runs the approved tests, implements the simplest complete solution that satisfies the new tests, and executes the relevant test suite.
5. **Document and suggest:** The agent apply changes in the documentation if needed and inlcude any concern or suggestion in the `agents_concerns_and_suggestions.md` file.
6. **Summarize and confirm:** The agent summarizes the changes, reports the test results, and asks for permission to commit. Commits must only be created after the required tests pass and the user explicitly approves.

## Git and Commits

- Never make changes directly to `main`, `master`, or `dev`. Update the appropriate base branch from `origin` before creating a task branch, such as `feature/<feature_name>` or `hotfix/<hotfix_name>`.
- When working on an existing task branch shared by multiple developers, synchronize it with `origin` before making changes. Avoid overwriting or discarding other developers' work, if there is a conflict, ask the user.
- Use descriptive commit messages with titles under 100 characters. Include concise, relevant context in the commit body when appropriate.
- Never push changes unless all required unit tests pass.
- Always request explicit user approval before creating a commit for each completed change request.

## Code and documentation

- Prefer the simplest implementation that meets the requirement. Avoid unnecessary dependencies and complexity.
- Reuse code and extract general, reusable functions or methods where appropriate.
- Use `snake_case` for functions and variables. Use `PascalCase` for classes (for example, `UserAccount`).
- Document input and output types using the conventions of the language in use.
- Update the README when a change makes its existing guidance or usage information inaccurate or incomplete.

## Agent guidelines files

- [`app/agents-instructions.md`](app/agents-instructions.md) with coding guidelines and workflow.
- [`test/agents-instructions.md`](test/agents-instructions.md) for the guideline to generate tests and the framework used.
- [`.github/agents-instructions.md`](.github/agents-instructions.md) for the full agent workflow and Git branches management.
- [`templates/user-story-template.md`](templates/user-story-template.md) User story template with required information to generate a new feature.
- [`agents_concerns_and_suggestions.md`](agents_concerns_and_suggestions.md) to list all concern and suggestions generated while vibe coding.


