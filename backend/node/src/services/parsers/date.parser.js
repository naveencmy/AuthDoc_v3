function parse({ text }) {
  if (!text) return null;
  const match = text.match(/\d{1,2}\s+\w+\s+\d{4}/);
  return match ? match[0] : null;
}
module.exports = { parse };