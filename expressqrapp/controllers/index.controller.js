var express = require('express');
var axios = require('axios');


module.exports = {

uploadFile: async (req, res, next) => {
  
  
   console.log(JSON.stringify(req.files.myImage));
   console.log("*******************");
   console.log(JSON.stringify(req.files.myqr));
 
   filename = req.files["myImage"][0].filename;

   filenametwo = req.files["myqr"][0].filename;
  
   axios.post('http://127.0.0.1:5000/upload', {
    fileName: filename,
    fileNameTwo: filenametwo
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