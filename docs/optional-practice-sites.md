# Optional Practice Sites

Done with the SauceDemo exercises? Here are additional sites you can practice testing against.
All of these work with Robot Framework and Browser Library — the same tools you've been using.

Credit: [free-sites-to-practice-testing](https://github.com/JapneetSachdeva1/free-sites-to-practice-testing)

## Web UI Testing

These sites have rich UIs with forms, tables, dynamic content, and edge cases:

| Site | What to Test |
|------|-------------|
| [The Internet](https://the-internet.herokuapp.com/) | Huge collection of common UI patterns: dropdowns, file uploads, drag & drop, iframes, dynamic loading, alerts, hovers, and more |
| [Practice Software Testing (Toolshop)](https://practicesoftwaretesting.com/) | Full e-commerce app with login, products, cart, checkout, contact form, admin panel |
| [Automation Exercise](https://www.automationexercise.com/) | E-commerce site with 25+ guided test cases covering signup, products, cart, subscription |
| [UI Testing Playground](http://uitestingplayground.com/) | Focused challenges: dynamic IDs, hidden layers, click interception, AJAX, client-side delay |
| [Coffee Cart](https://coffee-cart.app/) | Simple ordering app — great for quick E2E flow practice |
| [Evil Tester Test Pages](https://testpages.eviltester.com/styled/index.html) | Grab bag of forms, APIs, iframes, and deliberate edge cases |
| [Practice Automation](https://practice-automation.com/) | Popups, sliders, file operations, form validation, hover menus |

## API Testing (Browser-Based)

These sites have browser UIs backed by REST APIs you can test with both Browser Library and RequestsLibrary:

| Site | What to Test |
|------|-------------|
| [Restful Booker](https://restful-booker.herokuapp.com/apidoc/index.html) | Hotel booking API with CRUD operations, auth tokens, partial updates |
| [Reqres](https://reqres.in/) | Fake user API — login, register, paginated lists, delayed responses |
| [ServeRest](https://serverest.dev/) | Virtual store API — users, products, carts, login with JWT |
| [BookCart](https://bookcart.azurewebsites.net/) | Bookstore with both web UI and [Swagger API docs](https://bookcart.azurewebsites.net/swagger/index.html) |

## Enterprise / Domain Applications

Larger apps that mimic real enterprise software:

| Site | What to Test |
|------|-------------|
| [OrangeHRM](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login) | HR management system — login, employee records, leave management (demo credentials on page) |
| [ParaBank](https://parabank.parasoft.com/parabank/index.htm) | Online banking — accounts, transfers, bill pay, loan requests |
| [Applitools Demo](https://demo.applitools.com/) | Banking login — minimal but good for visual testing practice |
| [GlobalSQA Banking](https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login) | Angular banking app — customer login, transactions, deposits |

## Exercise Ideas

Pick a site and try one of these patterns:

1. **Smoke Test:** Navigate to the site, verify the page loads, check key elements exist
2. **Login Flow:** Test valid login, invalid credentials, empty fields, locked accounts
3. **CRUD Operations:** Create, read, update, delete a record (if the app supports it)
4. **Form Validation:** Submit forms with missing fields, invalid data, boundary values
5. **Navigation:** Verify links, breadcrumbs, menu items work correctly
6. **Cross-site Keywords:** Create a resource file for a new site following the same page object pattern used in the SauceDemo resources
