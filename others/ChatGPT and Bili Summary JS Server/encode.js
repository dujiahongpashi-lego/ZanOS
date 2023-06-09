const iconv = require('iconv-lite');


const utf8_to_gbk = (utf8Str) => {
    const buf = iconv.encode(utf8Str, 'gbk');
    // console.log(buf, buf.toString('hex'))
    return buf.toString('hex'); // 显示16进制数的字符串，用于传回python，在python侧转为bytes对象后直接可以用于支持gbk的设备显示
}


const gbk_to_utf8 = (gbkStr) => {
    const binary = gbkStr.replace(/\\x([0-9a-fA-F]{2})/g, (match, p1) => {
        // 将匹配到的 16 进制字符串转为整数，并将其转为相应的字符。 By ChatGPT
        return String.fromCharCode(parseInt(p1, 16));
    });
    const buf = Buffer.from(binary, 'binary');
    return iconv.decode(buf, 'gbk'); // UTF-8 字符串，可以直接用于网络请求的参数或者console.log输出
}

module.exports = {
    utf8_to_gbk: utf8_to_gbk,
    gbk_to_utf8: gbk_to_utf8

};