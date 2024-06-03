const { Firestore } = require('@google-cloud/firestore');

//Store data to firestore.
async function storeData(id, data) {
  const db = new Firestore();

  const predictCollection = db.collection('prediksi_daun');
  return predictCollection.doc(id).set(data);
}

module.exports = storeData;