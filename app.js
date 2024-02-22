import express from "express";
import expressLayout from "express-ejs-layouts";
import bodyParser from "body-parser";

// initiate app and ports
const app = express();
const port = 3000;

// middlewares
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

// middleware for templating
app.use(expressLayout);
app.set('layout', './layouts/main');
app.set('view engine', 'ejs');

// GET - home
app.get('/', (req, res) => {
    res.render('index.ejs');
})
// app listener
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
  