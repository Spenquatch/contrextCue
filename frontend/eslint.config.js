// ESLint Flat Config for React + TypeScript (ESLint v9+)
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  js.configs.recommended,
  ...tseslint.configs.recommended,
  ...tseslint.configs.react,
  {
    files: ["**/*.ts", "**/*.tsx"],
    languageOptions: {
      parser: tseslint.parser,
      parserOptions: {
        project: "./tsconfig.json",
      },
    },
    rules: {
      "react/jsx-uses-react": "off", // For React 17+
      "react/react-in-jsx-scope": "off",
    },
  },
];