-- ----------------------------
-- Insert users
-- ----------------------------
INSERT INTO users (username, hash, is_admin) VALUES 
('alice', 'hashed_password_1', 1),
('bob', 'hashed_password_2', 0),
('carol', 'hashed_password_3', 0);

-- ----------------------------
-- Insert bios
-- ----------------------------
INSERT INTO bios (user_id, bio_text, profile_pic_url) VALUES
(1, 'Hi, I am Alice! I love coding, cats, and exploring new frameworks.', '/static/profile_pics/4_default.png'),
(2, 'Bob here, coffee addict ☕ and bookworm 📚. Always learning new things.', '/static/profile_pics/4_default.png'),
(3, 'Carol: traveler 🌍, foodie 🍣, and Python enthusiast 🐍.', '/static/profile_pics/4_default.png');

-- ----------------------------
-- Insert posts with Markdown and timestamps
-- ----------------------------
-- Alice's posts
INSERT INTO posts (user_id, title, body, timestamp) VALUES
(1, 'My First Markdown Post', 
'# Hello World

This is **my first post** using Markdown!

## Why I love coding
- It''s creative
- Problem-solving is fun
- You can build amazing things

Stay tuned for more posts!',
'2026-01-01 10:15:00'),

(1, 'Cats Are Amazing', 
'## Fun Facts About Cats

1. Cats sleep for **12-16 hours** a day.
2. They have *whiskers* that detect changes in their environment.
3. Purring can be a sign of contentment or healing.

> Cats rule the world, one nap at a time.',
'2026-01-03 14:30:00');


-- Bob's posts
INSERT INTO posts (user_id, title, body, timestamp) VALUES
(2, 'Coffee Adventures', 
'### A Journey Through Coffee Shops

I visited three new cafes this week:

- **Cafe Mocha**: Amazing espresso
- **Latte Lounge**: Cozy vibes
- **Brew Heaven**: Best pastries

Coffee makes everything better!',
'2026-01-02 09:00:00'),

(2, 'Book Review: 1984', 
'# Book Review: 1984 by George Orwell

I just finished reading *1984*. Here are my thoughts:

- **Theme**: Totalitarianism and surveillance
- **Characters**: Winston is relatable yet tragic
- **Writing style**: Engaging and thought-provoking

Highly recommend it for anyone interested in dystopian literature.',
'2026-01-05 17:45:00'),

-- Carol's posts
(3, 'Travel Diary: Paris', 
'# My Paris Adventure

I recently visited Paris and it was amazing!

## Highlights
- Eiffel Tower at sunset 🌇
- Louvre Museum 🖼️
- Street food and local bakeries 🥐

Paris truly is a city of art and love!',
'2026-01-04 12:00:00'),

(3, 'Python Tips for Beginners', 
'## Python Tips

As a Python enthusiast, I want to share some tips:

1. Use **list comprehensions** for cleaner code.
2. Don''t forget about `virtualenv` or `venv`.
3. Use meaningful variable names.

> Python is powerful, simple, and fun. Keep coding!',
'2026-01-06 16:20:00');

-- ------------------------------------
-- Alice's posts get comments
-- ------------------------------------
INSERT INTO comments (post_id, user_id, comment, created_at) VALUES
(1, 2, 'Great first post, Alice! Markdown suits you 😊', '2026-01-01 11:00:00'),
(1, 3, 'Love the enthusiasm! Can’t wait for more posts 🚀', '2026-01-01 12:10:00'),
(2, 2, 'Cats truly do rule the world 😸', '2026-01-03 15:00:00'),
(2, 3, 'Fun facts! Didn’t know about the whiskers thing.', '2026-01-03 15:45:00');

-- ------------------------------------
-- Bob's posts get comments
-- ------------------------------------
INSERT INTO comments (post_id, user_id, comment, created_at) VALUES
(3, 1, 'Those cafes sound awesome ☕ I need to try Brew Heaven!', '2026-01-02 10:00:00'),
(3, 3, 'Coffee is life. Totally agree 😂', '2026-01-02 10:30:00'),
(4, 1, '1984 is one of my favourite books. Great review!', '2026-01-05 18:10:00'),
(4, 3, 'Now I want to reread it. Nice summary 👍', '2026-01-05 19:00:00');

-- ------------------------------------
-- Carol's posts get comments
-- ------------------------------------
INSERT INTO comments (post_id, user_id, comment, created_at) VALUES
(5, 1, 'Paris sounds magical! Love the highlights 🥐', '2026-01-04 13:00:00'),
(5, 2, 'Now I want to visit Paris 😄', '2026-01-04 13:40:00'),
(6, 1, 'Great Python tips! List comprehensions are the best 💻', '2026-01-06 17:00:00'),
(6, 2, 'Thanks for sharing! Really helpful as a beginner.', '2026-01-06 17:30:00');
