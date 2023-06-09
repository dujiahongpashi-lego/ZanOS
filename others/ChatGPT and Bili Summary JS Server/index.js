const url = require('url');
const http = require('http');
const apiEncode = require('./api-encode.js');
const apiChatGPT = require('./api-chatGPT.js');
const apiBiliSumup = require('./api-biliSumup.js');

const PORT = 80;
const SESSDATA = '3c1ee2d2%2C1697166058%2Cd6a40%2A41'

http.createServer((req, res) => {
    var resp_msg = ''
    if (req.method === 'GET') {
        const queryObject = url.parse(req.url, true).query;
        if (queryObject.api === 'encode') {
            resp_msg = apiEncode.handle(queryObject.data)
            doResponse(resp_msg, res)
        }
        else if (queryObject.api === 'chatgpt') {
            apiChatGPT.handle(queryObject.data, (resp_msg) => doResponse(resp_msg, res))
        }
        else if (queryObject.api === 'bilisumup') {
            apiBiliSumup.handle(queryObject.data, (resp_msg) => doResponse(resp_msg, res))
        }
        else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Invalid API');
        }
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Invalid Method');
    }


}).listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}/`);
});

function doResponse(data, res) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    msg = { data }
    res.end(JSON.stringify(msg));
}