# Selenium Basics & QA Concepts - Hands-On Solutions (1-7)

**Author:** Gopika R  
**Track:** Digital Nurture 5.0 - Python Full Stack Engineer Track  
**Module:** QA Concepts & Test Automation — Selenium Basics  

---

## Folder Structure

```
SeleniumBasics/gopika_r/
├── requirements.txt                # Python package dependencies
├── README.md                       # Documentation & POM Maintainability Explanation
├── conftest.py                     # Shared Pytest fixtures & screenshot-on-failure hooks
├── report.html                     # Self-contained HTML test execution report
├── written_exercises/
│   ├── qa_concepts.md              # Hands-On 1: QA Concepts & Defect Lifecycle
│   ├── v_model_analysis.md         # Hands-On 2: SDLC vs TDLC & V-Model Analysis
│   └── automation_strategy.md      # Hands-On 3: Automation Process & Framework Types
├── automation_scripts/
│   ├── setup_test.py               # Hands-On 4 (Task 1): Selenium Architecture & Setup
│   ├── navigation_test.py          # Hands-On 4 (Task 2): Navigation & Window Commands
│   └── locators_waits_test.py      # Hands-On 5: Locators & Explicit/Fluent Waits
├── pages/                          # Hands-On 7: Page Object Model (POM Page Classes)
│   ├── __init__.py
│   ├── base_page.py                # Base Page object encapsulating driver & waits
│   ├── simple_form_page.py         # Simple Form page actions & locators
│   ├── checkbox_page.py            # Checkbox page actions & locators
│   ├── dropdown_page.py            # Select Dropdown page actions & locators
│   └── input_form_page.py          # Input Form Submit page actions & locators
├── test_playground.py              # Hands-On 6: Pytest flat test suite & reporting
└── tests/                          # Hands-On 7: POM Refactored Test Suite
    ├── __init__.py
    └── test_pom_suite.py           # POM compliance test suite (ZERO find_element calls)
```

---

## Step 59: Page Object Model (POM) Maintainability Explanation

### Problem in Flat (Non-POM) Automation Scripts
In a flat, non-POM automation suite, element locators (e.g., `driver.find_element(By.ID, "submit")`) are hardcoded directly inside test functions across dozens or hundreds of test files.

#### What happens if the Submit button ID changes from `'submit'` to `'btn-submit'`?
- **High Maintenance Overhead:** Developers must manually search and update the string `"submit"` in 50+ individual test files.
- **High Risk of Missing Updates:** If even one test file is missed, test suite execution fails with `NoSuchElementException`, leading to flaky builds and wasted triage time.
- **Code Duplication:** Duplicating raw Selenium calls increases code noise and reduces test readability.

### How Page Object Model (POM) Solves This Problem
The Page Object Model strictly separates **"What to Test"** (test files) from **"How to Interact with UI"** (page files).

1. **Single Source of Truth:** Locators are defined once as class-level constants inside page classes:
   ```python
   # Inside pages/simple_form_page.py
   SUBMIT_BUTTON = (By.ID, "btn-submit")  # Only 1 line updated in 1 file!
   ```
2. **Zero Maintenance Changes in Test Files:** Test files call high-level business methods (`page.click_submit()`). Not a single line of code in the test suite files needs to be changed when element IDs or HTML structures change.
3. **Improved Readability:** Test code reads like business specification requirements rather than raw HTML interaction code:
   ```python
   # Fully readable POM test:
   page.enter_message("Hello Selenium")
   page.click_submit()
   assert page.get_displayed_message() == "Hello Selenium"
   ```

---

## How to Run the Test Suites

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Execute Standalone Selenium Automation Scripts (Hands-On 4 & 5)
```bash
python automation_scripts/setup_test.py
python automation_scripts/navigation_test.py
python automation_scripts/locators_waits_test.py
```

### 3. Execute Pytest Suites & Generate Self-Contained HTML Reports (Hands-On 6 & 7)
```bash
# Run Hands-On 6 Flat Pytest Suite
pytest test_playground.py -v --html=report.html --self-contained-html

# Run Hands-On 7 Page Object Model (POM) Test Suite
pytest tests/ -v --html=report.html --self-contained-html
```
