from flask import Flask, render_template, request, redirect, url_for
import json
app = Flask(__name__)

BLOG_FILE = "blog_posts.json"


def get_blog_posts(filename):
    """
    Returns the list of blog posts from the storage file
    by taking the filename as parameter.
    """
    with open(filename, "r") as file:
        return json.load(file)


@app.route('/')
def index():
    """
    Shows the main page of the blog.
    """
    blog_posts = get_blog_posts(BLOG_FILE)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Shows the form for adding a new post if GET or
    posts the form if POST.
    """
    if request.method == 'POST':
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]

        blog_posts = get_blog_posts(BLOG_FILE)

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
    """
    Deletes the post with the ID passed to the function.
    """
    blog_posts = get_blog_posts(BLOG_FILE)

    for i, post in enumerate(blog_posts):
        if post["id"] == post_id:
            del blog_posts[i]

    with open("blog_posts.json", "w") as file:
        file.write(json.dumps(blog_posts))

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Shows the update form for the post with the ID passed
    as an argument if GET or updates the post if POST.
    """
    blog_posts = get_blog_posts(BLOG_FILE)
    for post in blog_posts:
        if post["id"] == post_id:
            selected_post = post

    if request.method == 'POST':
        selected_post["author"] = request.form["author"]
        selected_post["title"] = request.form["title"]
        selected_post["content"] = request.form["content"]

        for i, post in enumerate(blog_posts):
            if selected_post["id"] == post["id"]:
                blog_posts[i] = selected_post
        with open("blog_posts.json", "w") as file:
            file.write(json.dumps(blog_posts))
        return redirect(url_for('index'))

    return render_template('update.html', post=selected_post)


if __name__ == '__main__':
    app.run()
