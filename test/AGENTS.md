# Test-writing guidelines 

Follow these guidelines when adding or changing tests for a feature in this project. Use the existing tests in this folder as examples, while preferring clear behavior-focused checks over checks that only confirm implementation details.

## Test framework and naming

- Write tests with `pytest`.
- Name test files `test_<area>.py` and test functions `test_<behavior>()` so pytest discovers them.
- Use plain `assert` statements for outcomes and `pytest.raises(ExpectedError)` for expected exceptions.
- Give each test one clear purpose. Use descriptive names that explain the scenario and expected behavior.
- Run the suite from the project root with `python -m pytest`. Run a focused file during iteration, for example `python -m pytest tests/experiments_tests.py`.

## Organize by test scope

Use the scope markers `unit_test`, `integration_test`, `e2e_test` to make test intent clear:

- `@pytest.mark.unit_test` for isolated functions and components, such as feature engineering or training behavior.
- `@pytest.mark.integration_test` for interactions among pipeline steps or different functions/app components, input data, and model output.
- `@pytest.mark.e2e_test` for a representative user workflow through the complete pipeline.

Register custom markers in the project's pytest configuration when one exists or is added, so pytest does not emit unknown-marker warnings.

## Test behavior, not just structure

- Test observable results and important contracts. Prefer checking that a function produces correct feature values, predictions, metrics, or saved output over checking only that an attribute exists or is callable.
- Include useful assertions for output shape, required fields, expected values, and relevant invariants. Add an assertion message when it makes a failure easier to diagnose.
- Avoid exact concrete-type checks unless the concrete type is part of the public contract. Prefer `isinstance` or assertions on the required behavior.
- Cover invalid inputs and failure behavior as well as successful use. Assert the specific exception type and, when useful, its message.
- For forecasting or other time-dependent features, verify ordering, group boundaries, lag values, and that future/target information is not leaked into features.
- For saved artifacts, verify the expected file exists and is usable. Use a temporary directory such as pytest's `tmp_path` fixture when the code allows an output path; do not leave generated models or other test artifacts in the repository.

## Fixtures, parametrization, and repeatability

- Reuse shared input data through fixtures in `conftest.py`; give fixtures descriptive names and document their return types.
- Keep fixtures small and focused on the scenario. Build special edge-case inputs in the test that needs them rather than overloading a shared fixture.
- Use `@pytest.mark.parametrize` when the same behavior must be checked across multiple meaningful inputs, such as several lag lengths or boundary values.
- Make tests deterministic. Seed random-number generators or use fixed values for synthetic data; do not let unseeded randomness make assertions flaky.
- Do not mutate shared fixture data in a way that affects another test. Copy mutable data before changing it.

## Test independence and maintenance

- Tests must run independently and in any order. Do not rely on files, models, or state created by another test.
- Avoid network access, real credentials, production data, long-running searches, or unnecessary heavyweight training in unit tests.
- Keep end-to-end coverage representative but bounded; use smaller datasets and inexpensive settings for test runs.
- When a test exposes a defect, fix the implementation rather than weakening the assertion to make it pass.
- When behavior intentionally changes, update the affected tests and any fixtures to match the approved requirement. Keep unrelated tests intact.

## Suggested coverage for a new feature

Before implementation, identify the feature's expected behavior and propose test scenarios for review. Include, as applicable:

1. A typical valid input and expected result.
2. Important boundary or variant inputs, using parametrization when appropriate.
3. Invalid or missing input and the expected explicit failure.
4. Interactions with related components or pipeline steps.
5. A user-level end-to-end scenario when the feature changes the complete workflow.

After adding tests, run the focused tests and then `python -m pytest`. Report what ran and any failures; do not claim success for tests that were not executed.