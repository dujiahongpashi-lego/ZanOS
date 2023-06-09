const { fetchBilibiliSubtitleUrls } = require('./fetchBilibiliSubtitleUrls')
const { reduceBilibiliSubtitleTimestamp } = require('./reduceSubtitleTimestamp')

async function fetchBilibiliSubtitle(
  videoId,
  pageNumber,
  shouldShowTimestamp,
) {
  const res = await fetchBilibiliSubtitleUrls(videoId, pageNumber)
  const { title, desc, dynamic, subtitle } = res || {}
  const hasDescription = desc || dynamic
  const descriptionText = hasDescription ? `${desc} ${dynamic}` : undefined
  const subtitleList = subtitle?.list
  if (!subtitleList || subtitleList?.length < 1) {
    return { title, subtitlesArray: null, descriptionText }
  }
  const betterSubtitle = subtitleList.find(({ lan }) => lan === 'zh-CN') || subtitleList[0]
  const subtitleUrl = betterSubtitle?.subtitle_url?.startsWith('//')
    ? `https:${betterSubtitle?.subtitle_url}`
    : betterSubtitle?.subtitle_url
  console.log('fetch', subtitleUrl)
  const subtitleResponse = await fetch(subtitleUrl)
  const subtitles = await subtitleResponse.json()
  console.log(JSON.stringify(subtitles))
  const transcripts = reduceBilibiliSubtitleTimestamp(subtitles?.body, shouldShowTimestamp)
  return { title, subtitlesArray: transcripts, descriptionText }
}


module.exports = {
  fetchBilibiliSubtitle: fetchBilibiliSubtitle,
};