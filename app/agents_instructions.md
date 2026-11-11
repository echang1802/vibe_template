# App Coding Guidelines for Agents

Follow these guidelines when changing application code.

## Understand and Plan the Change

- Inspect the relevant implementation, configuration, and tests before making any changes. Treat existing code as the reference pattern for feature transformations.
- Express the requested change as a user story when the user, outcome, or scope is unclear.
- Follow the repository's test-first workflow: propose concrete test scenarios, obtain the user's approval, add or update those tests, and then implement the change.
- Keep changes limited to the requested behaviour. Preserve existing interfaces and functionality unless the request explicitly requires changes.

## Structure and Implementation

- Keep `main.py` and `app.py` focused on configuration and execution orchestration. Place reusable transformations in dedicated modules such as `feature_engineering.py`.
- Prefer small, reusable functions with a single responsibility. Avoid duplicated logic, unnecessary dependencies, and abstractions that do not solve a current problem.
- Use `pathlib.Path` for file and directory paths.
- Read configuration from YAML using safe parsing methods, and load tabular sales data into pandas `DataFrame` objects.
- Keep data transformations non-mutating: work on copies and return transformed data while preserving the original columns and row correspondence whenever applicable.
- Do not add validations that were not explicitly requested.
- Always use the simplest implementation that satisfies the requirement.
- Do not introduce additional libraries unless they are necessary. Avoid unnecessary abstractions (for example, do not introduce dataclasses when they provide no meaningful benefit), but continue using well-established utility functions such as `sklearn.model_selection.train_test_split` when appropriate.

## Python Conventions

- Use descriptive `snake_case` names for functions, methods, variables, and modules.
- Use `PascalCase` for class names.
- Add parameter and return type annotations. Use pandas and standard-library types explicitly whenever practical.
- Provide concise docstrings for public functions and methods, describing their purpose and inputs or outputs when they are not self-explanatory.
- Follow the surrounding formatting and import conventions. Keep comments limited to non-obvious reasoning.

## Validation and Completion

- Add deterministic pytest coverage for normal behaviour, meaningful edge cases, and invalid inputs.
- Use the project's configured test command, typically `python -m pytest`, and run focused tests while iterating. Never claim that a test passed unless it was executed successfully.
- Keep tests isolated. Use temporary paths for generated model artefacts when supported by the code, and do not leave test outputs in the repository.
- Update the relevant README whenever usage, configuration, or setup instructions change.
- Summarise the changed files and validation results. Ask before committing, and never commit until the required tests pass and the user confirms.
