const express = require("express")
const router = express.Router()

router.get("/",(req,res)=>{
    res.render('settings', { title: 'Hey', message: 'Hello there!' })
})

module.exports=router