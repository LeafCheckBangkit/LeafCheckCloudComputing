const { Firestore } = require('@google-cloud/firestore');

async function storeData(id, data) {
  //PERLU TAMBAH databaseID
  const db = new Firestore({
    databaseID: ''
  });

  const predictCollection = db.collection('prediction');
  return predictCollection.doc(id).set(data);
}

module.exports = storeData;