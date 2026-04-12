# Accessibility

OpsFlow AI aims to provide a usable interface for operators and reviewers. Accessibility is an ongoing goal as the product evolves.

## Current state (Milestone 2)

The web UI is a functional development interface built with React. It includes:

- Semantic HTML structure where practical (`main`, headings, labels on form fields)
- Keyboard-accessible form controls on login and request creation flows
- Text-based status and error messages (not color alone)

Known limitations:

- Full WCAG 2.2 AA audit has not been completed
- Screen reader testing is limited
- Focus management across client-side route changes may be incomplete

## Feedback

If you encounter accessibility barriers, please open an issue using the **Bug report** template and tag the report with accessibility details (assistive technology, browser, and steps to reproduce).

For sensitive reports, use the contact method in [SECURITY.md](SECURITY.md).

## Goals

Future milestones should:

- Improve keyboard navigation and visible focus indicators
- Ensure sufficient color contrast in the UI theme
- Add automated accessibility checks in CI when the UI stabilizes
