const multer = require("multer");
const path = require("path");
const os = require("os");

/*
-----------------------------------------
ALLOWED FILE TYPES
-----------------------------------------
*/

const ALLOWED_TYPES = [
  "application/pdf",
  "image/jpeg",
  "image/png",
  "image/tiff"
];

/*
-----------------------------------------
STORAGE CONFIG
-----------------------------------------
*/

const storage = multer.diskStorage({

  destination: (req, file, cb) => {
    cb(null, os.tmpdir());
  },

  filename: (req, file, cb) => {

    const ext = path.extname(file.originalname);

    const name =
      Date.now() +
      "-" +
      Math.random().toString(36).substring(2, 8) +
      ext;

    cb(null, name);
  }

});

/*
-----------------------------------------
FILE FILTER
-----------------------------------------
*/

function fileFilter(req, file, cb) {

  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    return cb(new Error("Unsupported file type"), false);
  }

  cb(null, true);
}

/*
-----------------------------------------
MULTER INSTANCE
-----------------------------------------
*/

const upload = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
    files: 10
  }
});

/*
-----------------------------------------
EXPORT MIDDLEWARE
-----------------------------------------
*/

module.exports = {

  singleUpload: upload.single("file"),

  batchUpload: upload.array("files", 10)

};