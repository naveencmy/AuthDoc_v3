const { getParser } = require("./parserRegistry.service");

function extract(layout, schema) {
  const results = {};
  for (const field of schema.fields) {
    const region = layout[field.region] || [];
    const paragraphs = Array.isArray(region[0]) ? region : [region];
    const parser = getParser(field.type);
    let candidates = [];
    for (const paragraph of paragraphs) {
      const text = paragraph.map(b => b.text).join(" ");
      const matches = parser.parse({
        text,
        keywords: field.keywords
      });
      if (!matches) continue;
      const confidence =
        paragraph.map(b => b.confidence)
        .reduce((a,b)=>a+b,0) / paragraph.length;
      candidates.push({
        value: matches,
        confidence,
        text
      });
    }
    if (candidates.length === 0) {
      results[field.name] = {
        value: null,
        confidence: 0
      };
      continue;
    }
    candidates.sort((a,b)=>b.confidence-a.confidence);
    results[field.name] = {
      value: candidates[0].value,
      confidence: candidates[0].confidence
    };
  }
  return results;
}

module.exports = { extract };