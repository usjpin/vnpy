const express = require('express')
const path = require('path')
const app = express()

const dotenv = require('dotenv')
dotenv.config()

const views = path.join(__dirname, 'public')
app.use(express.static(views))

const PORT = process.env.PORT
const server = app.listen(PORT)