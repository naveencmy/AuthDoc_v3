const dateParser = require("./parsers/date.parser");
const personParser = require("./parsers/person_name.parser");
const genericParser = require("./parsers/generic.parser");

const PARSERS = {
  date: dateParser,
  person_name: personParser,
  text: genericParser
};

function getParser(type) {
  return PARSERS[type] || genericParser;
}

module.exports = { getParser };