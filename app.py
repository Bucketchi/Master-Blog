from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)


@app.route('/')
def index():
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():

    if request.method == 'POST':
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        with open("blog_posts.json", "r") as file:
            blog_posts = json.load(file)

        new_id = 1

        for post in blog_posts:
            if new_id != post["id"]:
                break
            new_id += 1

        new_post = {"id": len(blog_posts) + 1,
                    "author": author,
                    "title": title,
                    "content": content
                    }
        blog_posts.append(new_post)

        with open("blog_posts.json", "w") as file:
            file.write(json.dumps(blog_posts))

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open("blog_posts.json", "r") as file:
        blog_posts = json.load(file)

    for i, post in enumerate(blog_posts):
        if post["id"] == post_id:
            del blog_posts[i]

    with open("blog_posts.json", "w") as file:
        file.write(json.dumps(blog_posts))

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
