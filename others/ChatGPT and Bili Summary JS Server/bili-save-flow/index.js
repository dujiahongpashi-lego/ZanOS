const { fetchBilibiliSubtitle } = require('./fetchBilibiliSubtitle')
const { getSmallSizeTranscripts } = require('./getSmallSizeTranscripts')

fetchBilibiliSubtitle('BV1Uv4y1h7Gb').then(
    (reslut) => {
        const { title, subtitlesArray, descriptionText } = reslut 
        const inputText = subtitlesArray ? getSmallSizeTranscripts(subtitlesArray, subtitlesArray) : descriptionText
        const userPrompt = getUserSubtitlePrompt(title, inputText)
        console.log(userPrompt)
    }
)

function getUserSubtitlePrompt(title, transcript) {
    const videoTitle = title?.replace(/\n+/g, ' ').trim()
    const videoTranscript = limitTranscriptByteLength(transcript).replace(/\n+/g, ' ').trim()
    const language = 'zh-CN'
    const sentenceCount = 7
    const emojiTemplateText =  ''
    const emojiDescriptionText =  ''
    const shouldShowAsOutline = false
    const wordsCount = 15
    const outlineTemplateText = shouldShowAsOutline ? `\n    - Child points` : ''
    const outlineDescriptionText = shouldShowAsOutline
      ? `Use the outline list, which can have a hierarchical structure of up to ${videoConfig.outlineLevel} levels. `
      : ''
    const prompt = `Your output should use the following template:\n## Summary\n## Highlights\n- ${emojiTemplateText}Bulletpoint${outlineTemplateText}\n\nYour task is to summarise the text I have given you in up to ${sentenceCount} concise bullet points, starting with a short highlight, each bullet point is at least ${wordsCount} words. ${outlineDescriptionText}${emojiDescriptionText}Use the text above: {{Title}} {{Transcript}}.\n\nReply in ${language} Language.`
  
    return `Title: "${videoTitle}"\nTranscript: "${videoTranscript}"\n\nInstructions: ${prompt}`
  }
  

 function limitTranscriptByteLength(str, byteLimit = 6200) {
    const utf8str = unescape(encodeURIComponent(str))
    const byteLength = utf8str.length
    if (byteLength > byteLimit) {
      const ratio = byteLimit / byteLength
      const newStr = str.substring(0, Math.floor(str.length * ratio))
      return newStr
    }
    return str
  }