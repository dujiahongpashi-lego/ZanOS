const axios = require('axios');
const EventSource = require('eventsource');

// 定义需要发送的数据
const data = {"prompt":"你好呀","options":{"parentMessageId":"chatcmpl-7JiOfu2icZRhic84q3xGzfSgZPD1m"}};

let buffer = Buffer.from(''); // 创建一个空的缓冲区对象

// 发送 POST 请求并接收事件流
axios.post('https://chatbot.theb.ai/api/chat-process', data, {
  headers: {
    'Content-Type': 'application/json'
  },
  responseType: 'stream' // 声明响应类型为事件流
}).then(response => {
  const es = new EventSource('https://chatbot.theb.ai/api/chat-process'); // 创建一个空的事件流对象

  // 处理返回的事件流数据
  response.data.on('data', chunk => {
    buffer = Buffer.concat([buffer, chunk]); // 合并新的数据到缓冲区中

    console.log('----', buffer.slice())

    // 查找缓冲区中是否有一个完整的 JSON 对象
    let jsonEnd = -1;
    do {
      jsonEnd = buffer.indexOf('\n');
      if (jsonEnd >= 0) {
        const jsonData = buffer.slice(0, jsonEnd);
        console.log('==', jsonData.toString('utf8'))
        buffer = buffer.slice(jsonEnd + 1); // 更新缓冲区，去掉已解析的 JSON 对象

        try {
          const eventData = JSON.parse(jsonData.toString('utf8'));
          console.log(eventData.choices[0].text);
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