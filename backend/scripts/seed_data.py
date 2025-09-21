#!/usr/bin/env python
"""
Seed data script for Alumni Platform
Run with: python manage.py shell < scripts/seed_data.py
"""

from django.contrib.auth import get_user_model
from apps.accounts.models import Interest, UserInterest
from apps.posts.models import Post
from apps.crowdfunding.models import Project
from apps.clubs.models import Club
from apps.mentorship.models import MentorshipProgram, MentorProfile
from decimal import Decimal
import random

User = get_user_model()

print("🌱 Seeding database with sample data...")

# Create interests
interests_data = [
    "Technology", "Software Development", "Data Science", "Artificial Intelligence",
    "Cybersecurity", "Mobile Development", "Web Development", "Cloud Computing",
    "Business", "Entrepreneurship", "Marketing", "Finance", "Consulting",
    "Product Management", "Project Management", "Strategy", "Innovation",
    "Healthcare", "Biotechnology", "Medical Research", "Public Health",
    "Engineering", "Mechanical Engineering", "Electrical Engineering", "Civil Engineering",
    "Environment", "Sustainability", "Climate Change", "Renewable Energy",
    "Education", "Research", "Teaching", "Training", "Academia",
    "Arts & Design", "Creative Writing", "Graphic Design", "UI/UX Design",
    "Media", "Journalism", "Communications", "Public Relations",
    "Social Impact", "Non-profit", "Community Service", "Volunteering",
    "Sports", "Travel", "Photography", "Music", "Reading", "Gaming"
]

for interest_name in interests_data:
    Interest.objects.get_or_create(name=interest_name)

print("✅ Created interests")

# Create sample users
users_data = [
    {
        'email': 'sarah.chen@alumni.edu',
        'first_name': 'Sarah',
        'last_name': 'Chen',
        'user_type': 'alumni',
        'graduation_year': 2020,
        'department': 'Computer Science',
        'current_position': 'Senior Software Engineer',
        'company': 'Google',
        'location': 'San Francisco, CA',
        'linkedin_profile': 'https://linkedin.com/in/sarahchen',
        'status': 'active',
        'is_verified': True
    },
    {
        'email': 'marcus.johnson@alumni.edu',
        'first_name': 'Marcus',
        'last_name': 'Johnson',
        'user_type': 'alumni',
        'graduation_year': 2018,
        'department': 'Business Administration',
        'current_position': 'Product Manager',
        'company': 'Microsoft',
        'location': 'Seattle, WA',
        'linkedin_profile': 'https://linkedin.com/in/marcusjohnson',
        'status': 'active',
        'is_verified': True
    },
    {
        'email': 'emily.rodriguez@alumni.edu',
        'first_name': 'Emily',
        'last_name': 'Rodriguez',
        'user_type': 'faculty',
        'department': 'Electrical Engineering',
        'current_position': 'Research Scientist',
        'company': 'Tesla',
        'location': 'Austin, TX',
        'linkedin_profile': 'https://linkedin.com/in/emilyrodriguez',
        'status': 'active',
        'is_verified': True
    },
    {
        'email': 'alex.rivera@student.edu',
        'first_name': 'Alex',
        'last_name': 'Rivera',
        'user_type': 'student',
        'graduation_year': 2024,
        'department': 'Computer Science',
        'location': 'Boston, MA',
        'status': 'active',
        'is_verified': True
    },
    {
        'email': 'admin@alumni.edu',
        'first_name': 'Admin',
        'last_name': 'User',
        'user_type': 'admin',
        'status': 'active',
        'is_verified': True
    }
]

created_users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(
        email=user_data['email'],
        defaults=user_data
    )
    if created:
        user.set_password('password123')
        user.save()
    created_users.append(user)

print("✅ Created users")

# Add interests to users
all_interests = list(Interest.objects.all())
for user in created_users:
    # Add 3-8 random interests to each user
    num_interests = random.randint(3, 8)
    user_interests = random.sample(all_interests, num_interests)
    for interest in user_interests:
        UserInterest.objects.get_or_create(
            user=user,
            interest=interest,
            defaults={'proficiency_level': random.randint(1, 5)}
        )

print("✅ Added interests to users")

# Create sample posts
posts_data = [
    {
        'author': created_users[0],  # Sarah Chen
        'content': 'Just got promoted to Senior Software Engineer! Grateful for the foundation I built during my time at university. Happy to mentor current students interested in tech careers.',
        'post_type': 'achievement',
        'likes_count': 47,
        'comments_count': 12,
        'shares_count': 5
    },
    {
        'author': created_users[2],  # Emily Rodriguez
        'content': 'Exciting news! Our research paper on AI Ethics has been accepted to ICML 2024. Looking for students interested in research opportunities in this area.',
        'post_type': 'research',
        'likes_count': 23,
        'comments_count': 8,
        'shares_count': 15
    },
    {
        'author': created_users[3],  # Alex Rivera
        'content': 'Just launched my capstone project - a sustainability tracking app! Looking for feedback from alumni who work in environmental tech. Would love to connect!',
        'post_type': 'project',
        'likes_count': 31,
        'comments_count': 15,
        'shares_count': 8,
        'project_upvotes': 24
    }
]

for post_data in posts_data:
    Post.objects.get_or_create(
        author=post_data['author'],
        content=post_data['content'],
        defaults=post_data
    )

print("✅ Created posts")

# Create sample projects
projects_data = [
    {
        'creator': created_users[3],  # Alex Rivera
        'title': 'EcoTrack - Sustainable Living App',
        'description': 'A mobile app that helps users track their carbon footprint and suggests eco-friendly alternatives for daily activities.',
        'category': 'environment',
        'target_amount': Decimal('15000.00'),
        'current_amount': Decimal('8750.00'),
        'duration_days': 30,
        'status': 'active',
        'is_verified': True,
        'backers_count': 67
    },
    {
        'creator': created_users[0],  # Sarah Chen
        'title': 'AI-Powered Study Assistant',
        'description': 'An AI tool that creates personalized study plans and provides intelligent tutoring for students across various subjects.',
        'category': 'technology',
        'target_amount': Decimal('25000.00'),
        'current_amount': Decimal('18500.00'),
        'duration_days': 30,
        'status': 'active',
        'is_verified': True,
        'backers_count': 142
    }
]

for project_data in projects_data:
    Project.objects.get_or_create(
        creator=project_data['creator'],
        title=project_data['title'],
        defaults=project_data
    )

print("✅ Created projects")

# Create sample clubs
clubs_data = [
    {
        'owner': created_users[0],  # Sarah Chen
        'name': 'Tech Innovation Society',
        'description': 'A community of tech enthusiasts sharing knowledge, organizing hackathons, and building innovative projects together.',
        'category': 'technology',
        'visibility': 'public',
        'status': 'active',
        'is_verified': True,
        'members_count': 234,
        'posts_count': 45
    },
    {
        'owner': created_users[1],  # Marcus Johnson
        'name': 'Alumni Entrepreneurs',
        'description': 'Connecting alumni who are founders, providing mentorship, networking opportunities, and startup resources.',
        'category': 'business',
        'visibility': 'public',
        'status': 'active',
        'is_verified': True,
        'members_count': 156,
        'posts_count': 78
    }
]

for club_data in clubs_data:
    Club.objects.get_or_create(
        owner=club_data['owner'],
        name=club_data['name'],
        defaults=club_data
    )

print("✅ Created clubs")

# Create mentorship program
program, created = MentorshipProgram.objects.get_or_create(
    name='Tech Career Mentorship',
    defaults={
        'description': 'Connect students with alumni in tech careers for guidance and mentorship',
        'department': 'Computer Science',
        'target_audience': 'Computer Science students and recent graduates',
        'duration_weeks': 12,
        'max_mentees_per_mentor': 5,
        'status': 'active',
        'created_by': created_users[4]  # Admin
    }
)

print("✅ Created mentorship program")

# Create mentor profiles
for user in created_users[:3]:  # First 3 users as mentors
    MentorProfile.objects.get_or_create(
        user=user,
        defaults={
            'bio': f'Experienced professional in {user.current_position or "my field"}',
            'expertise_areas': 'Technology, Leadership, Career Development',
            'years_of_experience': random.randint(3, 15),
            'current_company': user.company or 'Various',
            'current_position': user.current_position or 'Professional',
            'availability_status': 'available',
            'max_mentees': 3,
            'is_verified': True,
            'is_active': True
        }
    )

print("✅ Created mentor profiles")

print("🎉 Database seeding completed!")
print(f"Created {User.objects.count()} users")
print(f"Created {Interest.objects.count()} interests")
print(f"Created {Post.objects.count()} posts")
print(f"Created {Project.objects.count()} projects")
print(f"Created {Club.objects.count()} clubs")
print(f"Created {MentorshipProgram.objects.count()} mentorship programs")
print(f"Created {MentorProfile.objects.count()} mentor profiles")
