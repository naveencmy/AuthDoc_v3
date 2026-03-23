const { randomUUID } = require("crypto");

const store = require("../store/documentStore");
const { extract } = require("../services/extraction.service");
const { loadSchema } = require("../services/schemaLoader.service");
const { sendToOCR } = require("../services/pythonClient");
const { verify } = require("../services/verifier.service");


async function ingest(req, res) {

  const document_id = randomUUID();

  const ocr = await sendToOCR(req.file);

  const schema = loadSchema("marriage_fr");

  const extraction = extract(ocr.layout, schema);

  store.save(document_id, {
    schema,
    fields: extraction
  });

  res.status(201).json({ document_id });

}


async function ingestBatch(req, res) {

  const docs = [];

  for (const file of req.files) {

    const document_id = randomUUID();

    const ocr = await sendToOCR(file);

    store.save(document_id, ocr);

    docs.push({ document_id });

  }

  res.json({ documents: docs });

}


function verifySingle(req, res) {

  const { document_id } = req.body;

  const data = store.get(document_id);

  if (!data) {
    return res.status(404).json({ error: "Document not found" });
  }

  const result = verify(data);

  res.json({
    document_id,
    verification: result
  });

}


function verifyBatch(req, res) {

  const { document_ids } = req.body;

  const candidates = document_ids.map(id => {

    const data = store.get(id);

    if (!data) return null;

    const result = verify(data);

    return {
      document_id: id,
      overall_status: result.overall_status
    };

  }).filter(Boolean);
  res.json({ candidates });
}

module.exports = {
  ingest,
  ingestBatch,
  verifySingle,
  verifyBatch
};