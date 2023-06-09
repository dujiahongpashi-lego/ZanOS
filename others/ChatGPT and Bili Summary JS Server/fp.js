const sample = (arr = []) => {
  const len = arr === null ? 0 : arr.length
  return len ? arr[Math.floor(Math.random() * len)] : undefined
}

function find(subtitleList = [], args) {
  const key = Object.keys(args)[0]
  return subtitleList.find((item) => item[key] === args[key])
}

module.exports = {
  sample: sample,
  find: find

};