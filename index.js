var http = require('http');
var os = require('os');
var express = require('express')
var responseTime = require('response-time')

var app = express()

app.use(responseTime())

app.get('/', function (req, res) {
  res.send(`<h1>I'm ${os.hostname()}</h1>`);
})

app.listen(8080)
