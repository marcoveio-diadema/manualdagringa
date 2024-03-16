import 'dotenv/config';
import express from "express";
import expressLayout from "express-ejs-layouts";
import bodyParser from "body-parser";
import sanitizeHtml from 'sanitize-html';
import multer from 'multer';


// initiate app and ports
const app = express();
const port = 3000;

// import db
import db from './db/db.js';

// import upload image
import config from './config.js';
const { uploadImage, customSanitizeHtml, generateSlug } = config;

// middlewares
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

// middleware for templating
app.use(expressLayout);
app.set('layout', './layouts/main');
app.set('view engine', 'ejs');

// multer storage
const upload = multer({ dest: 'uploads/' });

// GET - home
app.get('/', async (req, res) => {
    try {
        // fetch all posts from database
        const result = await db.query('SELECT * FROM posts');
        const posts = result.rows;

        // render index with posts
        res.render('index.ejs', { 
            title: 'Página inicial',
            posts
        });
    } catch (error) {
        console.error('Error fetching posts', error);
        res.status(500).send('Error fetching posts');
    }
})

// GET - add post page
app.get('/create-post', (req, res) => {
    res.render('create-post.ejs', { 
        title: 'Novo post',
        errorMessage: ''
    })
});

// POST - create post
app.post('/create-post', upload.single('image'), async(req, res) => {
    // Upload the image to Google Cloud Storage
    const imageUrl = await uploadImage(req.file);
    // other data from form
    const title = req.body["title"];
    const intro = req.body["intro"];
    const body = customSanitizeHtml(req.body["body1"]);

    try {
        // Insert the post into the database
        const result = await db.query('INSERT INTO posts (title, intro, body, img_url) VALUES ($1, $2, $3, $4) RETURNING *', [title, intro, body, imageUrl ]);
        const newPost = result.rows[0];
    
        // Redirect to the post page
        res.redirect(`/post/${newPost.id}`);
    } catch (error) {
        console.error('Error creating post:', error);
        // Set the error message
        const errorMessage = 'Error creating post';
        
        // Redirect to the create-post page with the error message
        res.render('create-post.ejs', { 
            title: 'Novo post',
            errorMessage 
        });
    }

});

// GET - view post
app.get('/post/:postId', async (req, res) => {
    const postId = req.params.postId;

    try {
        // Fetch the post from the database using the post ID
        const result = await db.query('SELECT * FROM posts WHERE id = $1', [postId]);
        const post = result.rows[0];
    
        // Render the post.ejs template with the post data
        res.render('post.ejs', { 
            post,
            title: 'Post'
         });
      } catch (error) {
        console.error('Error fetching post:', error);
        res.status(500).send('Error fetching post');
      }
});

// GET - admin page
app.get('/admin', (req, res) => {
    res.render('admin.ejs', { title: 'Admin'});
});

// GET - about
app.get('/about', (req, res) => {
    res.render('about.ejs', { title: 'Sobre Nós'});
})

// GET - about
app.get('/contact', (req, res) => {
    res.render('contact.ejs', { title: 'Contato'});
})


// app listener
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
  });
  