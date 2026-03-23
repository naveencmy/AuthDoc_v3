const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");
const path = require("path");

const OCR_URL = "http://127.0.0.1:8000/extract";

async function sendToOCR(file) {
  try {
    const form = new FormData();
    form.append("file", fs.createReadStream(file.path), {
      filename: file.originalname
    });
    const response = await axios.post(OCR_URL, form, {
      headers: form.getHeaders(),
      timeout: 20000
    });
    return response.data;
  } catch (err) {
    console.error("OCR SERVICE FAILED:", err.message);
    return { text_blocks: [] };
  }
}
module.exports = { sendToOCR };
