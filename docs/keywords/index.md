# Keyword Documentation

Auto-generated documentation for all resource files, produced by Robot Framework's
[libdoc](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#libdoc) tool.

## Resource Files

| Resource | Description |
|----------|-------------|
| [Common](common.html) | Shared setup/teardown and variables |
| [Login Page](login_page.html) | Login page keywords |
| [Products Page](products_page.html) | Products/inventory page keywords |
| [Cart Page](cart_page.html) | Shopping cart keywords |
| [Checkout Page](checkout_page.html) | Checkout flow keywords |

## How Keywords Work

In Robot Framework, **keywords** are reusable building blocks — like functions in programming.
Resource files group related keywords together following the **page object pattern**:

- Each page of the application gets its own resource file
- Keywords abstract away CSS selectors and DOM interactions
- Tests use descriptive keyword names instead of raw selectors

```
Test Case → Keywords (resource file) → Browser Library → Playwright → Browser
```
