var express = require('express');
var router = express.Router();
const indexController = require("../controllers/index.controller")

const multer = require("multer");
const path = require("path");

const storageData = multer.diskStorage({
    destination: (req, file, clb) => {
        clb(null, './public/images/');
    },
    filename: (req, file, cb) => {
        const newFileName = new Date().getTime().toString() + path.extname(file.originalname);
        cb(null, file.fieldname + '-' + Date.now()+ path.extname(file.originalname))
    }
});

const upload = multer({ storage : storageData })
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Covid Certificate Verification' });
});

router.route("/uploadFile")
  .post(upload.single("myImage") ,indexController.uploadFile)

  


module.exports = router;