const axios = require('axios');
const EventSource = require('eventsource');

// 定义需要发送的数据
const data = {
  messages: [
    {
      role: 'user',
      content: '我就是随便问问'
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
        // console.log('==', jsonData.toString('utf8'))
        buffer = buffer.slice(jsonEnd + 1); // 更新缓冲区，去掉已解析的 JSON 对象


        try {
          jsonStr = jsonData.toString('utf8')
          if (jsonStr.startsWith('data:')) {
            const eventData = JSON.parse(jsonStr.slice(5));
            console.log(eventData.choices[0].delta);
            answer += eventData.choices[0].delta.content
            if (eventData.choices[0].finish_reason == 'stop'){
              console.log(answer)
              break
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



