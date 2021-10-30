const path = require('path');
const fs = require("fs");

const normalizedPath = path.join(__dirname, '../maps');

const trimExtension = (file) => file.replace(path.extname(file), '');

const filterFiletypes = (file) => path.extname(file) === '.json';

/**
 * Locates and loads all json files within the maps directory
 * @returns {Object} A JSON object mapping to all of the nested maps within the maps directory
 */
const exportMaps = () => {
  return fs.readdirSync(normalizedPath)
    .filter(filterFiletypes)
    .reduce((fullJson, file) => {
      const trimmedFilename = trimExtension(file);
      const newFile = {
        [trimmedFilename]: JSON.parse(fs.readFileSync(path.join(normalizedPath, file), 'utf-8'))
      };
      return { ...fullJson, ...newFile};
    }, {});
}

module.exports = {
  exportMaps
}
