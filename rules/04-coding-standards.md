# Coding Standards Rules

These rules ensure readability, maintainability, type safety, and robust error handling across all source code.

## 1. Naming & Readability
- Use clear, unambiguous, domain-oriented naming for variables, functions, classes, and modules.
- Avoid cryptic abbreviations, single-letter identifiers (except standard loop indices), and misleading naming.
- Keep functions small and focused on a single responsibility (Single Responsibility Principle).

## 2. Type Safety & Contracts
- All languages supporting static typing or type hints (TypeScript, Python 3.10+, Go, Rust, Java, C#) must include explicit types on public interfaces, function parameters, and return values.
- Avoid escape hatches (`any` in TypeScript, bare `Object` in Java, untyped `Any` in Python) unless strictly necessary and documented.

## 3. Robust Error Handling
- Never catch generic exceptions and swallow them silently (e.g., `except: pass` or `catch(e) {}`).
- Always log or wrap exceptions with actionable context explaining what operation was occurring when the error happened.
- Differentiate between transient/recoverable errors and unrecoverable programmer defects.

## 4. Code Formatting & Linting
- All code must pass language-specific linters and formatters without warnings before advancing past Gate G4.
- Automated code reviews verify compliance using `python scripts/gate_validator.py --gate G4`.
