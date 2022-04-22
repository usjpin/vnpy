const express = require('express')
const path = require('path')
const app = express()

const views = path.join(__dirname, 'views')
app.use(express.static(views))

const server = app.listen(8080)