const express = require("express");
const router = express.Router();

const { singleUpload, batchUpload } = require("../middleware/upload.middleware");
const controller = require("../controllers/verify.controller");

// Upload single document
router.post("/ingest", singleUpload, controller.ingest);

// Upload batch documents
router.post("/ingest/batch", batchUpload, controller.ingestBatch);

// Verify single document
router.post("/verify", controller.verifySingle);

// Verify batch documents
router.post("/verify/batch", controller.verifyBatch);

module.exports = router;