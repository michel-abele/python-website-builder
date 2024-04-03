[<< back](./js.md)

# JavaScript

## Partial files

JavaScript does not support the direct integration of other files by default. To get around this problem, I use comments. This method helps to avoid false-positive error messages or incorrect code highlighting in editors.

The file _./source/js/global/first.js_ is included with the following specification:
```js
// import: global/first
```
