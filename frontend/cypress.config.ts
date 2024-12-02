import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
    specPattern: [
      'cypress/integration/**/*.cy.ts',
      'cypress/e2e/**/*.cy.ts',
    ],
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
  },
});
