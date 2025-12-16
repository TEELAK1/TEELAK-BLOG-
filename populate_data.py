
import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogmota.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment

def create_users():
    print("Creating users...")
    users = []
    
    # Superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        users.append(admin)
        print("- Created superuser: admin")
    else:
        users.append(User.objects.get(username='admin'))

    # Regular users
    regular_users = [
        ('alice', 'alice@example.com', 'password123'),
        ('bob', 'bob@example.com', 'password123'),
        ('charlie', 'charlie@example.com', 'password123'),
    ]

    for username, email, password in regular_users:
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username, email, password)
            users.append(user)
            print(f"- Created user: {username}")
        else:
            users.append(User.objects.get(username=username))
            
    return users

def create_categories():
    print("Creating categories...")
    categories_data = [
        ('Technology', 'Everything about the latest tech trends.'),
        ('Travel', 'Adventures from around the globe.'),
        ('Food & Cooking', 'Delicious recipes and culinary tips.'),
        ('Lifestyle', 'Advice for a balanced and happy life.'),
        ('Programming', 'Code snippets, tutorials, and guides.'),
    ]
    
    categories = []
    for name, desc in categories_data:
        category, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': desc}
        )
        categories.append(category)
        if created:
            print(f"- Created category: {name}")
    return categories

def create_tags():
    print("Creating tags...")
    tags_data = ['Django', 'Python', 'Web Development', 'Holiday', 'Spicy', 'Tutorial', 'Tips', 'Healthy', 'AI', 'Beginner']
    
    tags = []
    for name in tags_data:
        tag, created = Tag.objects.get_or_create(name=name)
        tags.append(tag)
        if created:
            print(f"- Created tag: {name}")
    return tags

def create_posts(users, categories, tags):
    print("Creating posts...")
    
    # Pre-defined specific posts to ensure variety
    sample_posts = [
        {
            'title': 'Getting Started with Django',
            'content': '<p>Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.</p><h3>Why Django?</h3><ul><li>Fast</li><li>Secure</li><li>Scalable</li></ul>',
            'category': 'Programming',
            'tags': ['Django', 'Python', 'Web Development', 'Beginner', 'Tutorial'],
            'status': 'published',
            'date_offset': -5,
        },
        {
            'title': 'Top 10 Travel Destinations for 2025',
            'content': '<p>If you are planning your next vacation, check out these amazing places...</p><p>1. Kyoto, Japan<br>2. Paris, France...</p>',
            'category': 'Travel',
            'tags': ['Holiday', 'Tips'],
            'status': 'published',
            'date_offset': -2,
        },
        {
            'title': 'The Ultimate Spicy Chicken Curry',
            'content': '<p>This recipe will blow your mind (and maybe your taste buds)!</p><p><strong>Ingredients:</strong></p><ul><li>Chicken</li><li>Chili Powder</li><li>Garlic</li></ul>',
            'category': 'Food & Cooking',
            'tags': ['Spicy', 'Healthy'],
            'status': 'published',
            'date_offset': -10,
        },
        {
            'title': 'Understanding Artificial Intelligence',
            'content': '<p>AI is changing the world as we know it. From LLMs to computer vision...</p>',
            'category': 'Technology',
            'tags': ['AI', 'Tech'],
            'status': 'published',
            'date_offset': 0, # Today
        },
        {
            'title': 'Draft: My Secret Project',
            'content': '<p>This is a work in progress. Do not publish yet.</p>',
            'category': 'Lifestyle',
            'tags': [],
            'status': 'draft',
            'date_offset': 0,
        },
         {
            'title': '5 Tips for Better Sleep',
            'content': '<p>Sleep is essential for health. Here is how to get more of it.</p>',
            'category': 'Lifestyle',
            'tags': ['Healthy', 'Tips'],
            'status': 'published',
            'date_offset': -20,
        }
    ]

    created_posts = []
    for post_data in sample_posts:
        # Avoid duplicates based on title
        if Post.objects.filter(title=post_data['title']).exists():
            continue

        cat_obj = next((c for c in categories if c.name == post_data['category']), None)
        author = random.choice(users)
        
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            author=author,
            category=cat_obj,
            status=post_data['status'],
            publish_date=timezone.now() + timedelta(days=post_data['date_offset'])
        )
        post.save()
        
        # Add tags
        post_tags = [t for t in tags if t.name in post_data['tags']]
        post.tags.set(post_tags)
        
        created_posts.append(post)
        print(f"- Created post: {post.title} ({post.status})")

    return created_posts

def create_comments(users, posts):
    print("Creating comments...")
    comments_data = [
        "Great article! Thanks for sharing.",
        "I totally agree with this.",
        "Could you explain more about the second point?",
        "This helped me a lot.",
        "Interesting perspective.",
        "Looking forward to the next part.",
    ]

    for post in posts:
        if post.status != 'published':
            continue
            
        # Add 0-3 comments per post
        num_comments = random.randint(0, 3)
        for _ in range(num_comments):
            author = random.choice(users)
            content = random.choice(comments_data)
            Comment.objects.create(
                post=post,
                author=author,
                content=content
            )
            print(f"- Added comment by {author.username} on '{post.title}'")

if __name__ == '__main__':
    print("Starting data population...")
    try:
        users = create_users()
        categories = create_categories()
        tags = create_tags()
        posts = create_posts(users, categories, tags)
        create_comments(users, posts)
        print("Data population completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
