const express = require("express")
const router = express.Router()
const fs = require('fs');
const path = require('path');
//have the router be able to access the body of the request
//define localstorage for rotuer
// const localStorage = require('node-localstorage').LocalStorage;
router.use(express.urlencoded({extended: true}))
router.get("/",(req,res)=>{
    res.render('settings', { title: 'Hey', message: 'Hello there!' })
})
const dataFilePath = path.join(__dirname, 'data.json');

// Define routes for isPaused, speed, and isLooped
router.get('/ispaused', (req, res) => {
  // Retrieve data from the data file (if available)
  const data = readDataFromFile();
  const isPaused = data ? data.isPaused : null;
  res.send({ isPaused });
});

router.post('/isPaused', (req, res) => {
  const isPaused = req.body.isPaused;
  console.log(req.body)
  // Store data in the data file
  const data = readDataFromFile() || {};
  data.isPaused = isPaused;
  writeDataToFile(data);
  res.send("completed")
});

router.get('/speed', (req, res) => {
  // Retrieve data from the data file (if available)
  const data = readDataFromFile();
  const speed = data ? data.speed : null;
  res.send({speed})
});

router.post('/speed', (req, res) => {
  const speed = req.body.speed;
  // Store data in the data file
  const data = readDataFromFile() || {};
  data.speed = speed;
  writeDataToFile(data);
  res.send(speed)
});

router.get('/isLooped', (req, res) => {
  // Retrieve data from the data file (if available)
  const data = readDataFromFile();
  const isLooped = data ? data.isLooped : null;
  res.send({isLooped})
});

router.post('/isLooped', (req, res) => {
  const isLooped = req.body.isLooped;
  // Store data in the data file
  const data = readDataFromFile() || {};
  data.isLooped = isLooped;
  writeDataToFile(data);
  res.send(isLooped)
});

// Helper function to read data from the data file
function readDataFromFile() {
  try {
    const data = fs.readFileSync(dataFilePath, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    console.error(err);
    return null;
  }
}

// Helper function to write data to the data file
function writeDataToFile(data) {
  try {
    fs.writeFileSync(dataFilePath, JSON.stringify(data));
  } catch (err) {
    console.error(err);
  }
}
module.exports = router;