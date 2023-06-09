const { gbk_to_utf8, utf8_to_gbk } = require('./encode.js');

function handle(data) {
    if(!data){
        return 'Empty Question'
    }
    gbk = gbk_to_utf8(data)
    console.log(data, gbk)
    return utf8_to_gbk('回应' + gbk)
}

module.exports = {
    handle: handle
};