const tf = require('@tensorflow/tfjs-node');
//Model belum ada, tambahkan link bucket untuk menambahkan URL.
async function loadModel() {
    return tf.loadGraphModel(process.env.MODEL_URL);
}

module.exports = loadModel;