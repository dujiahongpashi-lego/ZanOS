function doResponse(data, res) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    msg = { data }
    res.end(JSON.stringify(msg));
}

module.exports = {
    doResponse: doResponse
};