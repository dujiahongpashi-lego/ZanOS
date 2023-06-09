const { ask_gpt } = require('./ask_gpt')
const { gbk_to_utf8 } = require('./encode.js');

function handle(question, cb) {
  ask_gpt(gbk_to_utf8(question), cb)
  return 'OK'
}

module.exports = {
  handle: handle
};