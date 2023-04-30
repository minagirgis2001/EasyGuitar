const express = require("express")
const router = express.Router()
const fileUpload = require('express-fileupload')
const { spawn } = require('child_process');

router.use(fileUpload())
router.get("/",(req,res)=>{
    res.render('upload', { title: 'Hey', message: 'Hello there!' })
})
router.post('/', (req, res) =>{
    
    let sampleFile;
    let uploadPath;
    console.log(req.files)
    if (!req.files || Object.keys(req.files).length === 0) {
      return res.status(400).send('No files were uploaded.');
    }
  
    // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    sampleFile = req.files.song;
    sampleFile.name = "song.wav"
    uploadPath = __dirname + "/../../" + sampleFile.name;
    console.log(uploadPath);
    // Use the mv() method to place the file somewhere on your server
    sampleFile.mv(uploadPath, function(err) {
      if (err){
        return res.status(500).send(err);

      }
      res.redirect("/")
    })

    });
module.exports=router