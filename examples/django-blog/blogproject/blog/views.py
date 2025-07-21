"""
Django views for the blog application.

This module contains class-based and function-based views
demonstrating Django containerization and best practices.
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
import logging

from .models import Post, Category, Tag

logger = logging.getLogger(__name__)


class PostListView(ListView):
    """Display a list of published blog posts."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
        context['featured_posts'] = Post.objects.filter(status='published', featured=True)[:3]
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class PostDetailView(DetailView):
    """Display a single blog post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags', 'comments__author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get approved comments
        context['comments'] = post.comments.filter(is_approved=True).select_related('author')
        
        # Get related posts
        context['related_posts'] = Post.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id)[:3]
        
        return context


class CategoryDetailView(DetailView):
    """Display posts in a specific category."""
    model = Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        
        posts = Post.objects.filter(
            category=category,
            status='published'
        ).select_related('author').prefetch_related('tags')
        
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page_number)
        
        return context


class TagDetailView(DetailView):
    """Display posts with a specific tag."""
    model = Tag
    template_name = 'blog/tag_detail.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.get_object()
        
        posts = tag.posts.filter(status='published').select_related('author', 'category')
        
        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page_number)
        
        return context


def search_posts(request):
    """Search posts by title and content."""
    query = request.GET.get('q', '')
    posts = []
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).select_related('author', 'category').distinct()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'posts': posts_page,
        'query': query,
        'total_results': posts.count() if posts else 0
    }
    
    return render(request, 'blog/search_results.html', context)


@require_http_methods(["GET"])
def api_posts(request):
    """API endpoint to get posts as JSON."""
    try:
        posts = Post.objects.filter(status='published').select_related('author', 'category')[:10]
        
        posts_data = []
        for post in posts:
            posts_data.append({
                'id': post.id,
                'title': post.title,
                'slug': post.slug,
                'excerpt': post.excerpt,
                'author': post.author.username,
                'category': post.category.name,
                'created_at': post.created_at.isoformat(),
                'reading_time': post.get_reading_time(),
                'url': request.build_absolute_uri(post.get_absolute_url())
            })
        
        logger.info(f"API: Retrieved {len(posts_data)} posts")
        
        return JsonResponse({
            'status': 'success',
            'count': len(posts_data),
            'posts': posts_data
        })
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve posts'
        }, status=500)


@require_http_methods(["GET"])
def api_categories(request):
    """API endpoint to get categories as JSON."""
    try:
        categories = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'description': category.description,
                'post_count': category.post_count,
                'url': request.build_absolute_uri(category.get_absolute_url())
            })
        
        logger.info(f"API: Retrieved {len(categories_data)} categories")
        
        return JsonResponse({
            'status': 'success',
            'count': len(categories_data),
            'categories': categories_data
        })
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve categories'
        }, status=500)


def home(request):
    """Home page view with featured content."""
    try:
        # Get featured posts
        featured_posts = Post.objects.filter(
            status='published',
            featured=True
        ).select_related('author', 'category')[:3]
        
        # Get recent posts
        recent_posts = Post.objects.filter(
            status='published'
        ).select_related('author', 'category')[:6]
        
        # Get categories with post counts
        categories = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__status='published'))
        ).filter(post_count__gt=0)[:5]
        
        context = {
            'featured_posts': featured_posts,
            'recent_posts': recent_posts,
            'categories': categories,
        }
        
        logger.info("Home page loaded successfully")
        return render(request, 'blog/home.html', context)
        
    except Exception as e:
        logger.error(f"Home page error: {str(e)}")
        return render(request, 'blog/error.html', {
            'error_message': 'Sorry, there was an error loading the page.'
        })


def about(request):
    """About page view."""
    return render(request, 'blog/about.html', {
        'title': 'About Our Blog',
        'description': 'Learn more about our containerized Django blog application.'
    })
