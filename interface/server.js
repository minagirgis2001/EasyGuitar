const express = require("express");
const app = express();
const port = 5000;
app.set("view engine", "ejs")
const settingsRoute = require("./routes/settings")
const uploadRoute = require("./routes/upload")
const homeRoute = require("./routes/home")
app.use(express.static(__dirname + '/public'));
app.use("/",homeRoute)
app.use("/settings", settingsRoute)
app.use("/upload", uploadRoute)

app.listen(port, ()=>{
    console.log(`Server is up on port ${port}`)
})