var express = require('express');
var axios = require('axios');


module.exports = {

uploadFile: async (req, res, next) => {

   filename = req.file.filename
   console.log(filename)
  
   axios.post('http://127.0.0.1:5000/upload', {
    fileName: filename,
 })
 .then(function (response) {
    console.log(response);
    res.render('result', { result: response.data } )
 })
 .catch(function (error) {
    console.log(error);
 });

  
},


}