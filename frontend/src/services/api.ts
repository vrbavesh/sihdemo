// API Service Layer for Django Backend Integration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// Types for API responses
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  user_type: 'student' | 'alumni' | 'faculty' | 'admin' | 'recruiter';
  linkedin_profile?: string;
  current_position?: string;
  company?: string;
  graduation_year?: number;
  department?: string;
  phone_number?: string;
  location?: string;
  bio?: string;
  interests?: string[];
}

export interface AuthResponse {
  user: User;
  tokens: {
    access: string;
    refresh: string;
  };
}

// User types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  user_type: 'student' | 'alumni' | 'faculty' | 'admin' | 'recruiter';
  status: 'active' | 'pending' | 'suspended' | 'under_review';
  linkedin_profile?: string;
  current_position?: string;
  company?: string;
  graduation_year?: number;
  department?: string;
  phone_number?: string;
  location?: string;
  bio?: string;
  profile_picture?: string;
  cover_photo?: string;
  is_verified: boolean;
  created_at: string;
  last_active: string;
  interests: UserInterest[];
  connections_count: number;
  posts_count: number;
  projects_count: number;
}

export interface UserInterest {
  id: number;
  interest: Interest;
  proficiency_level: number;
  created_at: string;
}

export interface Interest {
  id: number;
  name: string;
  category?: string;
  description?: string;
}

// Post types
export interface Post {
  id: number;
  author: User;
  content: string;
  post_type: 'general' | 'achievement' | 'project' | 'research' | 'job_opportunity' | 'event' | 'mentorship';
  visibility: 'public' | 'connections' | 'department' | 'private';
  likes_count: number;
  comments_count: number;
  shares_count: number;
  views_count: number;
  project_upvotes?: number;
  is_approved: boolean;
  is_featured: boolean;
  is_pinned: boolean;
  created_at: string;
  updated_at: string;
  images: PostImage[];
  is_liked?: boolean;
  is_bookmarked?: boolean;
}

export interface PostImage {
  id: number;
  image: string;
  caption?: string;
  order: number;
}

export interface CreatePostRequest {
  content: string;
  post_type?: string;
  visibility?: string;
  images?: File[];
}

// Project types
export interface Project {
  id: number;
  title: string;
  description: string;
  short_description?: string;
  creator: User;
  category: string;
  target_amount: number;
  current_amount: number;
  currency: string;
  start_date: string;
  end_date: string;
  duration_days: number;
  status: 'draft' | 'pending' | 'active' | 'funded' | 'expired' | 'cancelled' | 'rejected';
  is_verified: boolean;
  is_featured: boolean;
  backers_count: number;
  views_count: number;
  likes_count: number;
  shares_count: number;
  cover_image?: string;
  created_at: string;
  updated_at: string;
  funding_percentage: number;
  days_remaining: number;
  is_funded: boolean;
  is_expired: boolean;
}

export interface CreateProjectRequest {
  title: string;
  description: string;
  category: string;
  target_amount: number;
  duration_days: number;
  cover_image?: File;
}

export interface Contribution {
  id: number;
  project: number;
  contributor: User;
  amount: number;
  contribution_type: 'one_time' | 'recurring';
  payment_status: string;
  is_anonymous: boolean;
  display_name?: string;
  created_at: string;
}

// Club types
export interface Club {
  id: number;
  name: string;
  description: string;
  short_description?: string;
  category: string;
  owner: User;
  visibility: 'public' | 'private' | 'invite_only';
  status: 'active' | 'inactive' | 'suspended' | 'pending';
  is_verified: boolean;
  cover_image?: string;
  logo?: string;
  members_count: number;
  posts_count: number;
  events_count: number;
  created_at: string;
  updated_at: string;
  last_activity: string;
  is_member?: boolean;
  membership_role?: string;
}

export interface CreateClubRequest {
  name: string;
  description: string;
  category: string;
  visibility: 'public' | 'private' | 'invite_only';
  cover_image?: File;
  logo?: File;
}

// Mentorship types
export interface MentorProfile {
  id: number;
  user: User;
  bio: string;
  expertise_areas: string;
  years_of_experience: number;
  current_company?: string;
  current_position?: string;
  availability_status: 'available' | 'busy' | 'unavailable';
  max_mentees: number;
  preferred_meeting_times?: string;
  timezone: string;
  preferred_mentee_types?: string;
  mentoring_goals?: string;
  total_mentees: number;
  rating: number;
  total_sessions: number;
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface MentorshipRequest {
  id: number;
  mentee: User;
  mentor: User;
  program?: number;
  subject: string;
  message: string;
  goals: string;
  preferred_meeting_frequency?: string;
  expected_duration?: string;
  status: 'pending' | 'accepted' | 'rejected' | 'cancelled' | 'completed';
  mentor_response?: string;
  rejection_reason?: string;
  created_at: string;
  updated_at: string;
  responded_at?: string;
  started_at?: string;
  completed_at?: string;
}

// Notification types
export interface Notification {
  id: number;
  user: number;
  notification_type: string;
  title: string;
  message: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  is_read: boolean;
  is_sent: boolean;
  created_at: string;
  read_at?: string;
}

// API Client Class
class ApiClient {
  private baseURL: string;
  private accessToken: string | null = null;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
    this.accessToken = localStorage.getItem('access_token');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.accessToken) {
      headers.Authorization = `Bearer ${this.accessToken}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || data.message || 'API request failed');
      }

      return {
        data,
        status: response.status,
      };
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Auth methods
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/auth/login/', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    this.accessToken = response.data.tokens.access;
    localStorage.setItem('access_token', response.data.tokens.access);
    localStorage.setItem('refresh_token', response.data.tokens.refresh);

    return response.data;
  }

  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    this.accessToken = response.data.tokens.access;
    localStorage.setItem('access_token', response.data.tokens.access);
    localStorage.setItem('refresh_token', response.data.tokens.refresh);

    return response.data;
  }

  async logout(): Promise<void> {
    this.accessToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  async getProfile(): Promise<User> {
    const response = await this.request<User>('/auth/profile/');
    return response.data;
  }

  async updateProfile(userData: Partial<User>): Promise<User> {
    const response = await this.request<User>('/auth/profile/', {
      method: 'PUT',
      body: JSON.stringify(userData),
    });
    return response.data;
  }

  // User methods
  async getUsers(params?: {
    user_type?: string;
    department?: string;
    graduation_year?: number;
    search?: string;
    page?: number;
  }): Promise<PaginatedResponse<User>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/auth/users/?${queryString}` : '/auth/users/';
    
    const response = await this.request<PaginatedResponse<User>>(endpoint);
    return response.data;
  }

  async searchUsers(searchData: {
    query?: string;
    user_type?: string;
    department?: string;
    graduation_year?: number;
    interests?: string[];
  }): Promise<{ users: User[]; count: number }> {
    const response = await this.request<{ users: User[]; count: number }>('/auth/users/search/', {
      method: 'POST',
      body: JSON.stringify(searchData),
    });
    return response.data;
  }

  // Connection methods
  async getConnections(): Promise<UserConnection[]> {
    const response = await this.request<UserConnection[]>('/auth/connections/');
    return response.data;
  }

  async sendConnectionRequest(userId: number): Promise<void> {
    await this.request(`/auth/connections/request/${userId}/`, {
      method: 'POST',
    });
  }

  async respondToConnection(connectionId: number, action: 'accept' | 'reject'): Promise<void> {
    await this.request(`/auth/connections/${connectionId}/respond/`, {
      method: 'POST',
      body: JSON.stringify({ action }),
    });
  }

  // Post methods
  async getPosts(params?: {
    post_type?: string;
    page?: number;
    search?: string;
  }): Promise<PaginatedResponse<Post>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/posts/?${queryString}` : '/posts/';
    
    const response = await this.request<PaginatedResponse<Post>>(endpoint);
    return response.data;
  }

  async createPost(postData: CreatePostRequest): Promise<Post> {
    const formData = new FormData();
    formData.append('content', postData.content);
    if (postData.post_type) formData.append('post_type', postData.post_type);
    if (postData.visibility) formData.append('visibility', postData.visibility);
    if (postData.images) {
      postData.images.forEach((image, index) => {
        formData.append(`images`, image);
      });
    }

    const response = await this.request<Post>('/posts/create/', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
    return response.data;
  }

  async likePost(postId: number): Promise<void> {
    await this.request(`/posts/${postId}/like/`, {
      method: 'POST',
    });
  }

  async bookmarkPost(postId: number): Promise<void> {
    await this.request(`/posts/${postId}/bookmark/`, {
      method: 'POST',
    });
  }

  // Project methods
  async getProjects(params?: {
    category?: string;
    status?: string;
    page?: number;
    search?: string;
  }): Promise<PaginatedResponse<Project>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/crowdfunding/projects/?${queryString}` : '/crowdfunding/projects/';
    
    const response = await this.request<PaginatedResponse<Project>>(endpoint);
    return response.data;
  }

  async createProject(projectData: CreateProjectRequest): Promise<Project> {
    const formData = new FormData();
    formData.append('title', projectData.title);
    formData.append('description', projectData.description);
    formData.append('category', projectData.category);
    formData.append('target_amount', projectData.target_amount.toString());
    formData.append('duration_days', projectData.duration_days.toString());
    if (projectData.cover_image) {
      formData.append('cover_image', projectData.cover_image);
    }

    const response = await this.request<Project>('/crowdfunding/projects/create/', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
    return response.data;
  }

  async contributeToProject(projectId: number, amount: number, isAnonymous: boolean = false): Promise<Contribution> {
    const response = await this.request<Contribution>(`/crowdfunding/projects/${projectId}/contribute/`, {
      method: 'POST',
      body: JSON.stringify({
        amount,
        contribution_type: 'one_time',
        is_anonymous: isAnonymous,
      }),
    });
    return response.data;
  }

  // Club methods
  async getClubs(params?: {
    category?: string;
    visibility?: string;
    page?: number;
    search?: string;
  }): Promise<PaginatedResponse<Club>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/clubs/?${queryString}` : '/clubs/';
    
    const response = await this.request<PaginatedResponse<Club>>(endpoint);
    return response.data;
  }

  async createClub(clubData: CreateClubRequest): Promise<Club> {
    const formData = new FormData();
    formData.append('name', clubData.name);
    formData.append('description', clubData.description);
    formData.append('category', clubData.category);
    formData.append('visibility', clubData.visibility);
    if (clubData.cover_image) {
      formData.append('cover_image', clubData.cover_image);
    }
    if (clubData.logo) {
      formData.append('logo', clubData.logo);
    }

    const response = await this.request<Club>('/clubs/create/', {
      method: 'POST',
      body: formData,
      headers: {}, // Let browser set Content-Type for FormData
    });
    return response.data;
  }

  async joinClub(clubId: number): Promise<void> {
    await this.request(`/clubs/${clubId}/join/`, {
      method: 'POST',
    });
  }

  async leaveClub(clubId: number): Promise<void> {
    await this.request(`/clubs/${clubId}/leave/`, {
      method: 'POST',
    });
  }

  // Mentorship methods
  async getMentors(params?: {
    expertise?: string;
    availability?: string;
    page?: number;
  }): Promise<PaginatedResponse<MentorProfile>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/mentorship/mentors/?${queryString}` : '/mentorship/mentors/';
    
    const response = await this.request<PaginatedResponse<MentorProfile>>(endpoint);
    return response.data;
  }

  async createMentorshipRequest(requestData: {
    mentor: number;
    subject: string;
    message: string;
    goals: string;
  }): Promise<MentorshipRequest> {
    const response = await this.request<MentorshipRequest>('/mentorship/requests/create/', {
      method: 'POST',
      body: JSON.stringify(requestData),
    });
    return response.data;
  }

  // Notification methods
  async getNotifications(params?: {
    is_read?: boolean;
    page?: number;
  }): Promise<PaginatedResponse<Notification>> {
    const searchParams = new URLSearchParams();
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
          searchParams.append(key, value.toString());
        }
      });
    }
    const queryString = searchParams.toString();
    const endpoint = queryString ? `/notifications/?${queryString}` : '/notifications/';
    
    const response = await this.request<PaginatedResponse<Notification>>(endpoint);
    return response.data;
  }

  async markNotificationAsRead(notificationId: number): Promise<void> {
    await this.request(`/notifications/${notificationId}/mark-read/`, {
      method: 'POST',
    });
  }

  async markAllNotificationsAsRead(): Promise<void> {
    await this.request('/notifications/mark-all-read/', {
      method: 'POST',
    });
  }

  // Utility methods
  setAccessToken(token: string): void {
    this.accessToken = token;
    localStorage.setItem('access_token', token);
  }

  getAccessToken(): string | null {
    return this.accessToken;
  }
}

// Additional types
export interface UserConnection {
  id: number;
  from_user: User;
  to_user: User;
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
  updated_at: string;
}

// Export singleton instance
export const apiClient = new ApiClient(API_BASE_URL);
export default apiClient;
