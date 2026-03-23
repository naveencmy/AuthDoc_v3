function parse({ blocks }) {

  if (!blocks || blocks.length === 0) return null;
  const nameCandidates = [];
  for (let i = 0; i < blocks.length - 1; i++) {
    const line1 = blocks[i].text.trim();
    const line2 = blocks[i + 1].text.trim();
    const pattern = /^[A-Za-z]{3,}$/;
    if (pattern.test(line1) && pattern.test(line2)) {
      const candidate = line1 + " " + line2;
      nameCandidates.push({
        value: candidate,
        confidence: (blocks[i].confidence + blocks[i + 1].confidence) / 2
      });
    }
  }
  if (nameCandidates.length === 0) return null;
  nameCandidates.sort((a, b) => b.confidence - a.confidence);
  return nameCandidates[0].value;
}
module.exports = { parse };