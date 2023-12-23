import { TextEncoder, TextDecoder } from 'util';
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

const { JSDOM } = require("jsdom");
const jsdomConfig = {
  url: 'https://*', // Adjust to match your specific URL pattern
  resources: 'usable',
  runScripts: 'dangerously',
  beforeParse(window) {
    window.eval(`
      document.__defineGetter__('cspHeaders', function () {
        return {
          'default-src': ["*"],
          'style-src': ["'self'", "*.stripe.com", "'unsafe-inline'"],
          'script-src': ["*", "'self'", "'unsafe-inline'", "localhost:*", "*.stripe.com", "'unsafe-eval'"],
          'img-src': ["'self'", "data", "localhost:*", "*.stripe.com", "'unsafe-inline'"],
        };
      });
    `);
  },
};

const dom = new JSDOM(
  '<!DOCTYPE html>' +
  '<head><meta http-equiv="Content-Security-Policy" content="default-src *; style-src \'self\' *.stripe.com \'unsafe-inline\'; script-src * \'self\' \'unsafe-inline\' localhost:* *.stripe.com \'unsafe-eval\'; img-src \'self\' data localhost:* *.stripe.com \'unsafe-inline\';"></head>' +
  '<body><div id="q-app"></div></body>',
  jsdomConfig);


global.window = dom.window;
global.document = dom.window.document;

