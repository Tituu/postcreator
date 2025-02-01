const express = require('express');
const fetch = require('node-fetch');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/post-to-blogger', async (req, res) => {
    const { title, link, poster, watchLink, format, releaseDate } = req.body;

    const bloggerApiKey = 'YOUR_BLOGGER_API_KEY';
    const blogId = 'YOUR_BLOG_ID';
    const bloggerApiUrl = `https://www.googleapis.com/blogger/v3/blogs/${blogId}/posts/`;

    const postData = {
        kind: "blogger#post",
        blog: { id: blogId },
        title: title,
        content: `
            <h3>${title}</h3>
            <p><strong>Link:</strong> <a href="${link}">${link}</a></p>
            <p><strong>Watch Link:</strong> <a href="${watchLink}">${watchLink}</a></p>
            <p><strong>Format:</strong> ${format}</p>
            <p><strong>Release Date 📅:</strong> ${releaseDate}</p>
            <img src="${poster}" width="200">
        `
    };

    try {
        const response = await fetch(`${bloggerApiUrl}?key=${bloggerApiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(postData)
        });

        if (response.ok) {
            res.status(200).send('Post successfully created!');
        } else {
            const errorData = await response.json();
            res.status(500).send(`Failed to create post: ${errorData.error.message}`);
        }
    } catch (error) {
        res.status(500).send(`Error posting to Blogger: ${error.message}`);
    }
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
