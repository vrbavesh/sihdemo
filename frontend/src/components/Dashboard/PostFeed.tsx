import { useState } from "react";
import { Card, CardContent, CardHeader } from "../ui/card";
import { Button } from "../ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";
import { Badge } from "../ui/badge";
import { Textarea } from "../ui/textarea";
import { 
  Heart, 
  MessageCircle, 
  Share2, 
  MoreHorizontal,
  ThumbsUp,
  TrendingUp,
  Bookmark,
  Send,
  Loader2
} from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { Post, CreatePostRequest } from "../../services/api";
import { apiClient } from "../../services/api";

interface PostFeedProps {
  userType: string;
  posts: Post[];
}

export function PostFeed({ userType, posts }: PostFeedProps) {
  const [newPost, setNewPost] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [localPosts, setLocalPosts] = useState<Post[]>(posts);

  const handleLike = async (postId: number) => {
    try {
      await apiClient.likePost(postId);
      setLocalPosts(prevPosts => 
        prevPosts.map(post => 
          post.id === postId 
            ? { 
                ...post, 
                is_liked: !post.is_liked,
                likes_count: post.is_liked ? post.likes_count - 1 : post.likes_count + 1
              }
            : post
        )
      );
    } catch (error) {
      console.error('Failed to like post:', error);
    }
  };

  const handleBookmark = async (postId: number) => {
    try {
      await apiClient.bookmarkPost(postId);
      setLocalPosts(prevPosts => 
        prevPosts.map(post => 
          post.id === postId 
            ? { ...post, is_bookmarked: !post.is_bookmarked }
            : post
        )
      );
    } catch (error) {
      console.error('Failed to bookmark post:', error);
    }
  };

  const handleUpvote = async (postId: number) => {
    try {
      // This would be a custom endpoint for project upvotes
      // For now, we'll just update the local state
      setLocalPosts(prevPosts => 
        prevPosts.map(post => 
          post.id === postId && post.project_upvotes !== undefined
            ? { ...post, project_upvotes: post.project_upvotes + 1 }
            : post
        )
      );
    } catch (error) {
      console.error('Failed to upvote project:', error);
    }
  };

  const handleSubmitPost = async () => {
    if (!newPost.trim() || isSubmitting) return;

    try {
      setIsSubmitting(true);
      const postData: CreatePostRequest = {
        content: newPost,
        post_type: userType === 'student' ? 'project' : 'general',
        visibility: 'public'
      };

      const newPostData = await apiClient.createPost(postData);
      setLocalPosts(prevPosts => [newPostData, ...prevPosts]);
      setNewPost("");
    } catch (error) {
      console.error('Failed to create post:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

    if (diffInSeconds < 60) return 'now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
    return `${Math.floor(diffInSeconds / 86400)}d ago`;
  };

  return (
    <div className="space-y-6">
      {/* Create Post */}
      <Card>
        <CardContent className="p-4">
          <div className="flex space-x-3">
            <Avatar>
              <AvatarFallback>You</AvatarFallback>
            </Avatar>
            <div className="flex-1 space-y-3">
              <Textarea
                placeholder="Share an update, achievement, or project..."
                value={newPost}
                onChange={(e) => setNewPost(e.target.value)}
                className="min-h-[80px] resize-none"
              />
              <div className="flex justify-between items-center">
                <div className="flex space-x-2">
                  <Badge variant="outline" className="text-xs">
                    {userType === 'student' ? 'Project' : 'Update'}
                  </Badge>
                  <Badge variant="outline" className="text-xs">Achievement</Badge>
                </div>
                <Button 
                  onClick={handleSubmitPost} 
                  disabled={!newPost.trim() || isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                      Posting...
                    </>
                  ) : (
                    <>
                      <Send className="h-4 w-4 mr-2" />
                      Post
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Posts */}
      {localPosts.map((post) => (
        <Card key={post.id}>
          <CardHeader className="pb-3">
            <div className="flex items-start justify-between">
              <div className="flex space-x-3">
                <Avatar>
                  <AvatarImage src={post.author.profile_picture} />
                  <AvatarFallback>
                    {post.author.first_name?.[0]}{post.author.last_name?.[0]}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <div className="flex items-center space-x-2">
                    <h4 className="font-semibold">
                      {post.author.first_name} {post.author.last_name}
                    </h4>
                    <Badge variant="secondary" className="text-xs">
                      {post.author.user_type}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {post.author.company || post.author.department || `Class of ${post.author.graduation_year}`} • {formatTimeAgo(post.created_at)}
                  </p>
                </div>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 hover:bg-accent hover:text-accent-foreground h-9 px-3">
                    <MoreHorizontal className="h-4 w-4" />
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem>Save post</DropdownMenuItem>
                  <DropdownMenuItem>Hide post</DropdownMenuItem>
                  <DropdownMenuItem>Report</DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <p className="text-sm leading-relaxed mb-4">{post.content}</p>
            
            {/* Project Upvotes for Student Posts */}
            {post.post_type === 'project' && post.project_upvotes !== undefined && (
              <div className="flex items-center space-x-2 mb-4 p-3 bg-muted/30 rounded-lg">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <span className="text-sm font-medium">{post.project_upvotes} project upvotes</span>
                {(userType === 'alumni' || userType === 'faculty') && (
                  <Button 
                    size="sm" 
                    variant="outline" 
                    onClick={() => handleUpvote(post.id)}
                    className="ml-auto"
                  >
                    <ThumbsUp className="h-3 w-3 mr-1" />
                    Upvote
                  </Button>
                )}
              </div>
            )}

            {/* Post Images */}
            {post.images && post.images.length > 0 && (
              <div className="grid grid-cols-2 gap-2 mb-4">
                {post.images.map((image, index) => (
                  <img
                    key={index}
                    src={image.image}
                    alt={image.caption || `Post image ${index + 1}`}
                    className="rounded-lg object-cover h-32 w-full"
                  />
                ))}
              </div>
            )}

            {/* Engagement Actions */}
            <div className="flex items-center justify-between pt-3 border-t">
              <div className="flex space-x-4">
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => handleLike(post.id)}
                  className={post.is_liked ? "text-red-500" : ""}
                >
                  <Heart className={`h-4 w-4 mr-1 ${post.is_liked ? "fill-current" : ""}`} />
                  {post.likes_count}
                </Button>
                <Button variant="ghost" size="sm">
                  <MessageCircle className="h-4 w-4 mr-1" />
                  {post.comments_count}
                </Button>
                <Button variant="ghost" size="sm">
                  <Share2 className="h-4 w-4 mr-1" />
                  {post.shares_count}
                </Button>
              </div>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => handleBookmark(post.id)}
                className={post.is_bookmarked ? "text-blue-500" : ""}
              >
                <Bookmark className={`h-4 w-4 ${post.is_bookmarked ? "fill-current" : ""}`} />
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}

      {localPosts.length === 0 && (
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-muted-foreground">No posts yet. Be the first to share something!</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
