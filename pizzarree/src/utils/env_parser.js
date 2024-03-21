const dotenv = require('dotenv');

const files = {
  ...dotenv.config({ path: '.env' }).parsed,
  ...dotenv.config({ path: `.env.${process.env.NODE_ENV}` }).parsed,
};

module.exports = () => {
  Object.keys(files, (key) => {
    if (typeof files[key] !== 'string') {
      files[key] = JSON.stringify(files[key]);
    }
  });
  return files;
};
