const { gbk_to_utf8, utf8_to_gbk } = require('./encode.js');
const fetch = require('node-fetch')
const axios = require('axios');
const EventSource = require('eventsource');

const gpts = [
  {
    url: 'https://ai.mengxins.cn/api/generate', // 萌新网 https://ai.mengxins.cn/
    post: (question) => {
      return JSON.stringify({
        "messages": [
          {
            "role": "user",
            "content": "Answer the question '" + question + "' Reply in zhCN Language.",
          }
        ],
        "config": {
          "temperature": 0.6,
          "top_p": 1
        }
      });
    }
  },
  {
    url: 'https://api.aichatos.cloud/api/generateStream', // AIChatOS https://chat5.aichatos.com/     
    post: (question) => {
      return JSON.stringify({
        "prompt": question,
        "userId": "#/chat/1681888572542",
        "network": true,
        "apikey": "",
        "system": "",
        "withoutContext": false
      });
    }
  },

  {
    url: 'https://chatbot.theb.ai/api/chat-process', //  https://chatbot.theb.ai/     
    post: (question) => {
      return JSON.stringify({ "prompt": question, "options": {} });
    }
  },

]


const ask_gpt_old = (question, cb) => {
  const url = gpts[2].url
  const postData = gpts[2].post(question)
  console.log(question, url, postData)

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: postData
  })
    //.then(res => res.text())
    .then(body => {
      console.log(body)
      cb(utf8_to_gbk(fixOddLengthEnglish(body)))
    });
}


const ask_gpt = (question, cb) => {
  // 定义需要发送的数据
  const data = {
    messages: [
      {
        role: 'user',
        content: question
      }
    ],
    model: 'gpt-3.5-turbo',
    stream: true,
    temperature: 1,
    top_p: 0.7
  };

  let buffer = Buffer.from(''); // 创建一个空的缓冲区对象

  answer = ''
  // 发送 POST 请求并接收事件流
  axios.post('https://api.openai.yuxin-proxy.asia/v1/chat/completions', data, { //https://chat.kunshanyuxin.com/
    headers: {
      'Content-Type': 'application/json'
    },
    responseType: 'stream' // 声明响应类型为事件流
  }).then(response => {
    const es = new EventSource('https://api.openai.yuxin-proxy.asia/v1/chat/completions'); // 创建一个空的事件流对象

    // 处理返回的事件流数据
    response.data.on('data', chunk => {
      buffer = Buffer.concat([buffer, chunk]); // 合并新的数据到缓冲区中
      // console.log('----', buffer.slice())

      // 查找缓冲区中是否有一个完整的 JSON 对象
      let jsonEnd = -1;
      do {
        jsonEnd = buffer.indexOf('\n');
        if (jsonEnd >= 0) {
          const jsonData = buffer.slice(0, jsonEnd);
          buffer = buffer.slice(jsonEnd + 1); // 更新缓冲区，去掉已解析的 JSON 对象

          try {
            jsonStr = jsonData.toString('utf8')
            if (jsonStr.startsWith('data:')) {
              const eventData = JSON.parse(jsonStr.slice(5));
              // console.log(eventData.choices[0].delta);
              if (eventData.choices[0].delta.content){
                answer += eventData.choices[0].delta.content
              }
              if (eventData.choices[0].finish_reason == 'stop') {
                console.log(answer)
                cb(utf8_to_gbk(fixOddLengthEnglish(answer)))
              }
            }
          } catch (error) {
            //console.error(error);
          }
        }
      } while (jsonEnd >= 0);
    });

    // 监听错误事件
    response.data.on('error', err => {
      console.error(err);
      es.close();
    });

    // 监听关闭事件
    response.data.on('end', () => {
      console.log('Server closed the connection.');
      es.close();
    });
  }).catch(error => {
    console.error(error);
  });
}

function fixOddLengthEnglish(str, filler = ' ') { // By chatgpt 将单字符部分补充成双数，用于适配LCD显示
  const pattern = /[\w!@#$%^&*()_+\-=[\]{};':"\\|,.<>\/?]+/g;
  let result = str
  let m, lastEnd = 0

  while ((m = pattern.exec(str))) {
    const start = m.index
    const end = m.index + m[0].length

    // 如果长度是单数且不在字符串末尾则补充一个空格
    if ((end - start) % 2 !== 0 && end < str.length) {
      const replacement = m[0] + filler
      result = result.slice(0, lastEnd + start)
        + replacement
        + result.slice(lastEnd + end)
      lastEnd += replacement.length - (end - start)
    } else {
      lastEnd = end
    }
  }

  return result
}

module.exports = {
  ask_gpt: ask_gpt
};