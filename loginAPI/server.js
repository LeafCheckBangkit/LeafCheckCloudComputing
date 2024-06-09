const dotenv = require('dotenv');
const express = require('express');
const bcrypt = require('bcrypt');
const passport = require('passport');
const flash = require('express-flash');
const session = require('express-session');
const methodOverride = require('method-override');
const { initialize, usersRef } = require('./passport-config');
const app = express();
const users = [];
// console.log(usersRef); DEBUG usersRef

// Load environment variables if not in production
if (app.get('env') !== 'production') {
  dotenv.config();
}

// Middleware setup
app.use(express.urlencoded({ extended: false }));
app.use(flash());
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
}));
app.use(passport.initialize());
app.use(passport.session());
app.use(methodOverride('_method'));

// Passport configuration
initialize(
  passport,
  email => users.find(user => user.email === email),
  id => users.find(user => user.id === id)
);

// Authentication routes
app.post('/login', ensureNotAuthenticated, passport.authenticate('local', {
  successRedirect: '/',
  failureRedirect: '/login',
  failureFlash: true,
}));

// Configuring the register post functionality
app.post('/register', ensureNotAuthenticated, async (req, res) => {
  const newUserRef = usersRef.push();
  const id = newUserRef.key;

  try {
    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    await newUserRef.set({
      id: id,
      name: req.body.name,
      email: req.body.email,
      password: hashedPassword,
    });
    res.redirect('/login');
  } catch (e) {
    console.log(e);
    res.redirect('/register');
  }
});

// Logout route
app.delete("/logout", (req, res) => {
    req.logout(req.user, err => {
        if (err) return next(err)
        res.redirect("/")
    })
})

// View routes
app.get('/', ensureAuthenticated, (req, res) => {
  res.render('index.ejs', { name: req.user.name });
});

app.get('/login', ensureNotAuthenticated, (req, res) => {
  res.render('login.ejs');
});

app.get('/register', ensureNotAuthenticated, (req, res) => {
  res.render('register.ejs');
});

// Middleware for authentication checks
function ensureAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  res.redirect('/login');
}

function ensureNotAuthenticated(req, res, next) {
  if (!req.isAuthenticated()) {
    return next();
  }
  res.redirect('/');
}

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on Port: ${PORT}`);
});