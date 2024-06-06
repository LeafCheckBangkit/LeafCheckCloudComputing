const LocalStrategy = require("passport-local").Strategy;
const bcrypt = require("bcrypt");
const admin = require('firebase-admin');
const serviceAccount = require('./config/leafcheck-capstone-firebase-adminsdk-aqein-dc33dd8d42.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: 'https://leafcheck-capstone-default-rtdb.asia-southeast1.firebasedatabase.app'
});

const db = admin.database();
const usersRef = db.ref('users');

function initialize(passport) {
  // Function to authenticate users
  const authenticateUsers = async (email, password, done) => {
    try {
      // Get user by email
      const snapshot = await usersRef.orderByChild('email').equalTo(email).once('value');
      const user = snapshot.val() ? Object.values(snapshot.val())[0] : null;
      if (!user) {
        return done(null, false, { message: "No user found with that email" });
      }

      // Compare password
      const isPasswordCorrect = await bcrypt.compare(password, user.password);
      if (isPasswordCorrect) {
        return done(null, user);
      } else {
        return done(null, false, { message: "Password Incorrect" });
      }
    } catch (error) {
      console.error("Error during authentication: ", error);
      return done(error);
    }
  };

  // Configure passport to use local strategy
  passport.use(new LocalStrategy({ usernameField: 'email' }, authenticateUsers));

  // Serialize and deserialize user for session management
  passport.serializeUser((user, done) => {
    done(null, user.id);
  });

  passport.deserializeUser(async (id, done) => {
    try {
      const snapshot = await usersRef.child(id).once('value');
      const user = snapshot.val();
      done(null, user);
    } catch (error) {
      done(error, null);
    }
  });
}
module.exports = {usersRef, initialize};