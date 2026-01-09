from flask import Flask, flash,render_template, request, redirect, session, url_for
from helpers import admin_required, get_db, close_db, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import markdown2
import os
try:
    from better_profanity import profanity
    profanity_available = True
except Exception:
    profanity_available = False

app = Flask(__name__)
app.secret_key = "WHATCANISAYEXCEPTYOUSHALLNOTPASS"

# Folder inside your project, e.g., project_root/static/profile_pics
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'profile_pics')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create the folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Jinja2 filter for markdown rendering
@app.template_filter('markdown')
def markdown_filter(text):
    if text:
        return markdown2.markdown(text) 
    return ''

# Enable profanity filtering only if the package is available
profanityfilter = profanity_available
if profanityfilter:
    profanity.load_censor_words()

@app.before_request
def refresh_admin_status():
    """Refresh the user's `is_admin` value from the database on each request.

    This ensures changes to a user's admin status in the database are
    reflected immediately in `session` without requiring the user to log out
    and back in.
    """
    user_id = session.get("user_id")
    if user_id:
        db = get_db()
        row = db.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is not None:
            session["is_admin"] = bool(row["is_admin"])
        else:
            session.pop("is_admin", None)
            
# Front page
@app.route("/")
def index():
    # Retrieve all blog posts from the database
    db = get_db()
    posts = db.execute("""
        SELECT *
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.timestamp DESC
    """).fetchall()

    return render_template("index.html", posts=posts)    

@app.route("/blog/<int:post_id>", methods=["POST", "GET"])
def blog(post_id):
    """Blog post route."""
    db = get_db()
    post = db.execute("""
        SELECT *
        FROM posts
        JOIN users ON posts.user_id = users.id
        WHERE posts.id = ?
    """, (post_id,)).fetchone()

    if not post:
        flash("Post not found.", "error")
        return redirect("/")

    comments = db.execute("""
        SELECT comments.comment, comments.created_at, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE comments.post_id = ?
        ORDER BY comments.created_at ASC
    """, (post_id,)).fetchall()

    return render_template("blog.html", post=post, comments=comments)

@app.route("/blog/<int:post_id>/comment", methods=["POST"])
@login_required
def add_comment(post_id):
    """Add comment to a blog post."""

    if request.method == "POST":
        user_id = session.get("user_id")

        comment_text = request.form.get("comment", "").strip()
        if not comment_text:
            flash("Comment cannot be empty.", "error")
            return redirect(f"/blog/{post_id}")

        if profanityfilter == True:
            comment_text = profanity.censor(comment_text)
        
        db = get_db()
        db.execute("""
            INSERT INTO comments (post_id, user_id, comment) 
            VALUES (?, ?, ?)
        """, (post_id, user_id, comment_text))
        db.commit()

        flash("Comment added successfully.")
        return redirect(f"/blog/{post_id}")


@app.route("/bio/<user_name>", methods=["GET"])
def bio(user_name):
    """User bio route."""
    db = get_db()
    profile_user_name = user_name
    viewer_user_id = session.get("user_id")

    profile_user = db.execute("""
        SELECT id AS user_id 
        FROM users  
        WHERE username = ?
    """, (profile_user_name,)).fetchone()
    
    bio_info = db.execute("""
        SELECT * 
        FROM bios 
        WHERE user_id = ?
    """, (profile_user["user_id"],)).fetchone()

    posts = db.execute("""
        SELECT * 
        FROM posts 
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (profile_user["user_id"],)).fetchall()

    isuser = False
    if viewer_user_id == profile_user["user_id"]:
        isuser = True

    return render_template("bio.html", bio_info=bio_info, posts=posts, isuser=isuser, user=profile_user, user_name=user_name)

@app.route("/edit_bio", methods=["GET", "POST"])
@login_required
def edit_bio():
    user_id = session.get("user_id")
    db = get_db()
    
    if request.method == "POST":
        bio_text = request.form.get("bio_text", "")

        if profanityfilter == True:
            bio_text = profanity.censor(bio_text)

        profile_pic_url = None
        
        # Handle file upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(f"{user_id}_{file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                profile_pic_url = url_for('static', filename=f'profile_pics/{filename}')

        existing_bio = db.execute("""
            SELECT * FROM bios WHERE user_id = ?
        """, (user_id,)).fetchone()

        if existing_bio:
            if profile_pic_url:
                db.execute("""
                    UPDATE bios 
                    SET bio_text = ?, profile_pic_url = ? 
                    WHERE user_id = ?
                """, (bio_text, profile_pic_url, user_id))
            else:
                db.execute("""
                    UPDATE bios 
                    SET bio_text = ? 
                    WHERE user_id = ?
                """, (bio_text, user_id))
        else:
            db.execute("""
                INSERT INTO bios (user_id, bio_text, profile_pic_url) 
                VALUES (?, ?, ?)
            """, (user_id, bio_text, profile_pic_url))

        db.commit()
        
        user_id = session["user_id"]
        user = db.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
        return redirect("/bio/<user_name>".replace("<user_name>", user["username"]))

    bio_info = db.execute("""
        SELECT * FROM bios WHERE user_id = ?
    """, (user_id,)).fetchone()

    return render_template("edit_bio.html", bio_info=bio_info)


@app.route("/admin_dashboard", methods=["GET", "POST"])
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard route."""
    db = get_db()
    users = db.execute("""
        SELECT id, username, is_admin 
        FROM users 
        ORDER BY username
    """).fetchall()

    posts = db.execute("""  
        SELECT * from posts
    """).fetchall()

    if request.method == "POST" and "promote_user" in request.form:
        user_id = request.form["user_id"]
        if db.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()["is_admin"]:
            db.execute("""
                UPDATE users 
                SET is_admin = 0 
                WHERE id = ?
            """, (user_id,))
            db.commit()
            return redirect("/admin_dashboard")    
        if not db.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,)).fetchone()["is_admin"]:
            db.execute("""
                UPDATE users 
                SET is_admin = 1 
                WHERE id = ?
            """, (user_id,))
            db.commit()
            return redirect("/admin_dashboard")
    if request.method == "POST" and "delete_user" in request.form:
        user_id = request.form["user_id"]
        db.execute("""
            DELETE FROM users 
            WHERE id = ?
        """, (user_id,))
        db.commit()
        return redirect("/admin_dashboard")
    
    if request.method == "POST" and "delete_post" in request.form:
        post_id = request.form["post_id"]
        db.execute("""
            DELETE FROM posts 
            WHERE id = ?
        """, (post_id,))
        db.commit()
        return redirect("/admin_dashboard")

    return render_template("admin_dashboard.html", users=users, posts=posts)

@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """Dashboard route for logged-in users."""
    user_id = session.get("user_id")

    if request.method == "POST" and "write_new" in request.form:
        # Handle post creation logic here
        return redirect("/create_post")

    db = get_db()
    posts = db.execute("""
        SELECT * 
        FROM posts 
        WHERE user_id = ?
        ORDER BY timestamp DESC
    """, (user_id,)).fetchall()

    user = db.execute("""
        SELECT * 
        FROM users 
        WHERE id = ?
    """, (user_id,)).fetchone()

    return render_template("dashboard.html", posts=posts, user=user)

@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    """Route to create a new blog post."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        user_id = session.get("user_id")
        
        # Censor inappropriate content
        if profanityfilter == True:
            title = profanity.censor(title)
            body = profanity.censor(body)

        db = get_db()
        db.execute("""
            INSERT INTO posts (title, body, user_id) 
            VALUES (?, ?, ?)
        """, (title, body, user_id))
        db.commit()

        return redirect("/dashboard")

    return render_template("create_post.html")

@app.route("/delete_post/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    """Route to delete a blog post."""
    user_id = session.get("user_id")

    db = get_db()
    post = db.execute("""
        SELECT * 
        FROM posts 
        WHERE id = ? AND user_id = ?
    """, (post_id, user_id)).fetchone()

    if post:
        db.execute("""
            DELETE FROM posts 
            WHERE id = ? AND user_id = ?
        """, (post_id, user_id))
        db.commit()

    return redirect("/dashboard")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.clear()
        db = get_db()
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            flash("Missing username or password", "error")
            return redirect("/login")

        user = db.execute(
            """SELECT * 
            FROM users 
            WHERE username = ?
            """,
            (username,)).fetchone()

        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = bool(user["is_admin"])

            return redirect("/dashboard")

        flash("Invalid username or password", "error")

    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """User logout route."""
    session.clear()
    flash("You have been successfully logged out.")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirmation = request.form["confirmation"]
        hash = generate_password_hash(password)

        if not username or not password or not confirmation:
            flash("Missing username or password", "error")
            return redirect("/register")
        if password != confirmation:
            flash("Passwords do not match", "error")
            return redirect("/register")

        db = get_db()
        existing = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)).fetchone()

        if existing:
            flash("Username already exists", "error")
            return redirect("/register")

        db.execute("""
        INSERT INTO users (username, hash) 
        VALUES (?, ?)
        """, (username, hash))
        db.commit()

        flash("Registration successful.")
        
        return redirect("/login")

    return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    """Change password"""
    if request.method == "POST":
        username = request.form["username"]
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]
        confirmation = request.form["confirmation"]

        if not username or not old_password or not new_password or not confirmation:
            flash("Missing username or password", "error")
            return redirect("/change_password")
        if new_password != confirmation:
            flash("Passwords do not match", "error")
            return redirect("/change_password")
        
        db = get_db()
        user = db.execute("""
            SELECT *
            FROM users
            WHERE username = ?
            """, (username,)).fetchone() 
            
        if user and check_password_hash(user["hash"], old_password):
            new_hash = generate_password_hash(new_password)

            db.execute("""
                UPDATE users
                SET hash = ?
                WHERE username = ?
                """, (new_hash, username))
            db.commit()

            flash("Changed password successfully.")
            return redirect("/login")
        else:
            flash("Wrong username and/or old password", "error")    
            return redirect("/change_password")

    return render_template("change_password.html")


if __name__ == "__main__":
    app.run(debug=True)
