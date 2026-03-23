const fs = require("fs");
const path = require("path");

const SCHEMA_DIR = path.join(__dirname, "../config/schemas");

exports.loadSchema = (schemaName = "marriage_fr") => {

  const file = path.join(SCHEMA_DIR, `${schemaName}.json`);

  if (!fs.existsSync(file)) {
    throw new Error(`Schema ${schemaName} not found`);
  }

  const schema = JSON.parse(fs.readFileSync(file));

  return schema;
};