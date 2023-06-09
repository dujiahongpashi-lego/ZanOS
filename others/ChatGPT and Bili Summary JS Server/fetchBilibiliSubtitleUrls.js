const { find, sample  }  = require('./fp')
const fetch = require('node-fetch')

const fetchBilibiliSubtitleUrls = async (
  videoId,
  pageNumber,
  SESSDATA = '30716af4%2C1697252732%2Cc5ebb%2A41'
) => {
  const sessdata = sample(SESSDATA?.split(','))
  const headers = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
    'User-Agent':
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    Host: 'api.bilibili.com',
    Cookie: `SESSDATA=${sessdata}`,
  }
  const commonConfig = {
    method: 'GET',
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    headers,
    referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
  }

  const params = videoId.startsWith('av') ? `?aid=${videoId.slice(2)}` : `?bvid=${videoId}`
  const requestUrl = `https://api.bilibili.com/x/web-interface/view${params}`
  console.log(`fetch`, requestUrl)
  const response = await fetch(requestUrl, commonConfig)
  const json = await response.json()
  // console.log( JSON.stringify(json.data))
  const { aid, pages } = json?.data || {}
  // support multiple parts of video
  if (pages && pages.length >0 ) {

    const { cid } = find(pages, { page: Number(1) }) || {}

    // https://api.bilibili.com/x/player/v2?aid=865462240&cid=1035524244
    const pageUrl = `https://api.bilibili.com/x/player/v2?aid=${aid}&cid=${cid}`
    console.log(`fetch`, pageUrl)
    const res = await fetch(pageUrl, commonConfig)
    const j = await res.json()
    // console.log( JSON.stringify(j.data))
    // r.data.subtitle.subtitles
    return { ...json.data, subtitle: { list: j.data.subtitle.subtitles } }
  }

  // return json.data.View;
  // { code: -404, message: '啥都木有', ttl: 1 }
  return json.data
}


module.exports = {
  fetchBilibiliSubtitleUrls: fetchBilibiliSubtitleUrls
};