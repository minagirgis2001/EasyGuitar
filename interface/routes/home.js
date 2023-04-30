const express = require("express")
const router = express.Router()
const { spawn } = require('child_process');
router.get("/",(req,res)=>{
    res.render('home', { title: 'Hey', message: 'Hello there!' })
})
router.post('/', (req, res) =>{
    const scriptPath = __dirname + '/../../main.py';
    console.log(scriptPath)
    const pythonProcess = spawn('python', [scriptPath]) ;
    pythonProcess.stderr.pipe(process.stderr);

    pythonProcess.on('error', (err) => {
      console.error(err);
      return res.status(500).send(err);
    });
    
    pythonProcess.on('exit', (code) => {
      if (code === 0) {
        console.log('Python script exited successfully');
        res.redirect("/")
        
      } else {
        console.error(`Python script exited with code ${code}`);
        return res.status(500).send('Error occurred while processing the file');
      }
    });
})

module.exports=router