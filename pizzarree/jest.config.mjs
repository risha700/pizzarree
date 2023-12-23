/** @type {import('jest').Config} */
export default {
  preset: '@quasar/quasar-app-extension-testing-unit-jest',
  // collectCoverage: true,
  // coverageThreshold: {
  //   global: {
  //      branches: 50,
  //      functions: 50,
  //      lines: 50,
  //      statements: 50
  //   },

  // },
   setupFiles: [
    // '<rootDir>/test/setups/jest-setup.js',
  ],
  // testEnvironment: 'jsdom',// default quasar
  testEnvironmentOptions: {
        // resources: 'usable',
        // runScripts: 'dangerously',
        customExportConditions: ["node", "node-addons"],
    },
  transform: {
    '.*\\.js$': 'babel-jest',
  },
};
