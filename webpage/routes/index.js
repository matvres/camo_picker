var express = require('express');
var router = express.Router();

const slike = require('./upload');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'CAMOPICKER' });
});

router.get('/about', function(req, res, next) {
  res.render('about', { title: 'O strani' });
});


router.post('/upload', slike.upload_img)




module.exports = router;
