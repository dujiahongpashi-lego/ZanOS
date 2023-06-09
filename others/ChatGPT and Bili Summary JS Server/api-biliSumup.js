const fetch = require('node-fetch')
const { ask_gpt } = require('./ask_gpt')
const { fetchBilibiliSubtitle } = require('./fetchBilibiliSubtitle')
const { getSmallSizeTranscripts } = require('./getSmallSizeTranscripts')
const { utf8_to_gbk } = require('./encode.js');

function handle(bvid, cb) {

  const pattern = /^BV[0-9A-Za-z]{10}$/;  // by chatgpt
  if(!pattern.test(bvid)){ 
    cb(utf8_to_gbk('BV格式不正确'))
    return false
  }

  fetchBilibiliSubtitle(bvid).then(
    (reslut) => {
      const { title, subtitlesArray, descriptionText } = reslut
      if(!title){
        cb(utf8_to_gbk('视频未找到'))
        return
      }
      const inputText = subtitlesArray ? getSmallSizeTranscripts(subtitlesArray, subtitlesArray) : descriptionText
      const userPrompt = getUserSubtitlePrompt(title, inputText)
      console.log(userPrompt)
      ask_gpt(userPrompt, cb)
    }
  )
  return true
}


const getUserSubtitlePrompt = (title, transcript) => {
  const videoTitle = title?.replace(/\n+/g, ' ').trim()
  const videoTranscript = limitTranscriptByteLength(transcript).replace(/\n+/g, ' ').trim()
  const language = 'zh-CN'
  const sentenceCount = 5
  const emojiTemplateText = ''
  const emojiDescriptionText = ''
  const shouldShowAsOutline = false
  const wordsCount = 15
  const outlineTemplateText = shouldShowAsOutline ? `\n    - Child points` : ''
  const outlineDescriptionText = shouldShowAsOutline
    ? `Use the outline list, which can have a hierarchical structure of up to ${videoConfig.outlineLevel} levels. `
    : ''
  const prompt = `Your output should use the following template:\n### Summary\n### Highlights\n- ${emojiTemplateText}Bulletpoint${outlineTemplateText}\n\nYour task is to summarise the text I have given you in up to ${sentenceCount} concise bullet points, starting with a short highlight, each bullet point is at least ${wordsCount} words. ${outlineDescriptionText}${emojiDescriptionText}Use the text above: {{Title}} {{Transcript}}.\n\nReply in ${language} Language.`

  return `Title: "${videoTitle}"\nTranscript: "${videoTranscript}"\n\nInstructions: ${prompt}`
}


const limitTranscriptByteLength = (str, byteLimit = 6200) => {
  const utf8str = unescape(encodeURIComponent(str))
  const byteLength = utf8str.length
  if (byteLength > byteLimit) {
    const ratio = byteLimit / byteLength
    const newStr = str.substring(0, Math.floor(str.length * ratio))
    return newStr
  }
  return str
}

module.exports = {
  handle: handle
};