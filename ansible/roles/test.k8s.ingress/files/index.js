'use strict';

const express = require('express');

// Constants
const PORT = 3000;
const HOST = '0.0.0.0';

// App
const app = express();
app.get('/*', (req, res) => {
  const ar = [];
  ar.push(`Host ${req.hostname}`);
  ar.push(`Path ${req.path}`);
  ar.push(`ReqIP: ${req.ip}`);
  ar.push(`PodName: ${process.env.POD_NAME}`);
  ar.push(`<b>ServiceName:${process.env.SERVICE_NAME} </b>`);
  res.send(ar.join("<br />"));
});

app.listen(PORT, null, () => {
  console.log(`Running on http://${HOST ? "*" : HOST}:${PORT}`);
});