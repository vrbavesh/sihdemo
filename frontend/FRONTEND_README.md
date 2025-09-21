# Alumni Management Platform - Frontend

A modern React-based frontend for the Alumni Management Platform, built with TypeScript, Vite, and Tailwind CSS.

## 🚀 Features

- **Modern React Architecture**: Built with React 18, TypeScript, and Vite
- **Real-time Updates**: WebSocket integration for live notifications
- **JWT Authentication**: Secure token-based authentication
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Component Library**: Radix UI components with custom styling
- **API Integration**: Comprehensive API service layer
- **State Management**: Context-based state management
- **Type Safety**: Full TypeScript support

## 🏗️ Architecture

### **Project Structure**
```
src/
├── components/           # React components
│   ├── Auth/            # Authentication components
│   ├── Dashboard/       # Dashboard components
│   ├── Features/        # Feature-specific components
│   ├── Layout/          # Layout components
│   └── ui/              # Reusable UI components
├── contexts/            # React contexts
│   └── AuthContext.tsx  # Authentication context
├── services/            # API and external services
│   ├── api.ts          # API client
│   └── websocket.ts    # WebSocket service
├── types/              # TypeScript type definitions
├── utils/              # Utility functions
├── styles/             # Global styles
└── main.tsx           # Application entry point
```

### **Key Components**

#### **Authentication System**
- `AuthContext`: Global authentication state management
- `LoginPage`: User registration and login
- JWT token management with automatic refresh
- Role-based access control

#### **API Integration**
- `apiClient`: Centralized API client with error handling
- Type-safe API calls with TypeScript interfaces
- Automatic token attachment and refresh
- Request/response interceptors

#### **Real-time Features**
- `WebSocketService`: Real-time notification system
- Automatic reconnection with exponential backoff
- Event-based message handling

#### **Dashboard Components**
- `Dashboard`: Main dashboard with user-specific content
- `PostFeed`: Social media-style post feed
- `QuickStats`: User statistics and metrics
- Real-time data updates

#### **Feature Components**
- `CrowdfundingPage`: Project funding interface
- `ClubsPage`: Community management
- `MentorshipPage`: Mentor-mentee matching
- `AdminPage`: Administrative functions

## 🛠️ Technology Stack

### **Core Technologies**
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework

### **UI Components**
- **Radix UI**: Accessible, unstyled UI primitives
- **Lucide React**: Beautiful icon library
- **Custom Components**: Tailored UI components

### **State Management**
- **React Context**: Global state management
- **Custom Hooks**: Reusable stateful logic
- **Local State**: Component-level state with useState

### **API & Data**
- **Fetch API**: Modern HTTP client
- **WebSocket**: Real-time communication
- **JWT**: Secure authentication tokens

## 🚀 Getting Started

### **Prerequisites**
- Node.js 18+ 
- npm or yarn
- Backend API running on port 8000

### **Installation**

1. **Clone the repository**
```bash
git clone <repository-url>
cd alumni-management-platform
```

2. **Install dependencies**
```bash
npm install
# or
yarn install
```

3. **Environment Setup**
```bash
cp env.example .env
# Edit .env with your configuration
```

4. **Start development server**
```bash
npm run dev
# or
yarn dev
```

5. **Open in browser**
```
http://localhost:3000
```

### **Environment Variables**

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_WS_URL=ws://localhost:8000

# App Configuration
VITE_APP_NAME=Alumni Connect
VITE_APP_VERSION=1.0.0

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_ENABLE_REAL_TIME=true

# External Services
VITE_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
VITE_GOOGLE_ANALYTICS_ID=GA_MEASUREMENT_ID
```

## 📱 Available Scripts

### **Development**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking
```

### **Production Build**
```bash
npm run build        # Create optimized production build
npm run preview      # Preview the production build locally
```

## 🔧 Configuration

### **Vite Configuration**
The project uses Vite for fast development and building. Configuration is in `vite.config.ts`:

- **Port**: 3000 (development)
- **Proxy**: API requests proxied to backend
- **Aliases**: Path mapping for clean imports
- **Build**: Optimized production builds

### **TypeScript Configuration**
TypeScript is configured in `tsconfig.json`:

- **Strict Mode**: Enabled for type safety
- **Path Mapping**: Clean import paths
- **React JSX**: Modern JSX transform
- **ES2020 Target**: Modern JavaScript features

### **Tailwind Configuration**
Tailwind CSS is configured for:

- **Custom Colors**: Brand-specific color palette
- **Responsive Design**: Mobile-first approach
- **Component Classes**: Reusable utility classes
- **Dark Mode**: Theme switching support

## 🔌 API Integration

### **API Client**
The `apiClient` provides a centralized way to interact with the backend:

```typescript
// Authentication
await apiClient.login(credentials);
await apiClient.register(userData);
await apiClient.logout();

// User Management
const users = await apiClient.getUsers();
const profile = await apiClient.getProfile();

// Posts
const posts = await apiClient.getPosts();
await apiClient.createPost(postData);

// Projects
const projects = await apiClient.getProjects();
await apiClient.createProject(projectData);
```

### **WebSocket Integration**
Real-time features are handled through WebSocket connections:

```typescript
// Subscribe to notifications
websocketService.subscribe('notification', (data) => {
  // Handle real-time notification
});

// Send messages
websocketService.send({ type: 'message', data: 'Hello' });
```

## 🎨 UI Components

### **Component Library**
The project uses a custom component library built on Radix UI:

- **Accessible**: WCAG compliant components
- **Customizable**: Tailwind CSS styling
- **Consistent**: Design system approach
- **Reusable**: Composable components

### **Key Components**
- **Cards**: Content containers with consistent styling
- **Buttons**: Interactive elements with variants
- **Forms**: Input components with validation
- **Modals**: Overlay dialogs and popups
- **Navigation**: Menu and navigation components

## 🔐 Authentication Flow

### **Login Process**
1. User enters credentials
2. API validates credentials
3. JWT tokens are returned
4. Tokens are stored in localStorage
5. User state is updated in context
6. WebSocket connection is established

### **Token Management**
- **Access Token**: Short-lived (1 hour)
- **Refresh Token**: Long-lived (7 days)
- **Automatic Refresh**: Seamless token renewal
- **Secure Storage**: localStorage with encryption

### **Role-Based Access**
- **Student**: Limited access to features
- **Alumni**: Full access to most features
- **Faculty**: Teaching and mentoring features
- **Admin**: Administrative functions
- **Recruiter**: Job posting and candidate search

## 📊 State Management

### **Context Providers**
- **AuthContext**: User authentication and profile
- **ThemeContext**: Dark/light mode switching
- **NotificationContext**: Real-time notifications

### **Custom Hooks**
- **useAuth**: Authentication state and methods
- **useApi**: API call helpers with loading states
- **useWebSocket**: Real-time connection management

## 🚀 Deployment

### **Build Process**
```bash
npm run build
```

This creates an optimized production build in the `dist` directory.

### **Environment Configuration**
Set environment variables for production:

```env
VITE_API_BASE_URL=https://api.alumni-platform.com
VITE_WS_URL=wss://api.alumni-platform.com
```

### **Static Hosting**
The build can be deployed to any static hosting service:

- **Vercel**: Zero-config deployment
- **Netlify**: Git-based deployment
- **AWS S3**: Static website hosting
- **GitHub Pages**: Free hosting option

## 🧪 Testing

### **Testing Strategy**
- **Unit Tests**: Component testing with React Testing Library
- **Integration Tests**: API integration testing
- **E2E Tests**: Full user journey testing
- **Type Checking**: TypeScript compilation

### **Running Tests**
```bash
npm run test          # Run unit tests
npm run test:e2e      # Run end-to-end tests
npm run test:coverage # Run tests with coverage
```

## 🔧 Development Guidelines

### **Code Style**
- **ESLint**: Enforced code quality
- **Prettier**: Consistent code formatting
- **TypeScript**: Type safety requirements
- **Conventional Commits**: Standardized commit messages

### **Component Guidelines**
- **Functional Components**: Use function components with hooks
- **TypeScript**: Define proper interfaces
- **Props Validation**: Use TypeScript for prop validation
- **Accessibility**: Follow WCAG guidelines

### **API Guidelines**
- **Error Handling**: Consistent error handling patterns
- **Loading States**: Show loading indicators
- **Optimistic Updates**: Update UI before API response
- **Retry Logic**: Automatic retry for failed requests

## 📈 Performance

### **Optimization Techniques**
- **Code Splitting**: Lazy loading of components
- **Bundle Analysis**: Webpack bundle analyzer
- **Image Optimization**: Responsive images
- **Caching**: API response caching

### **Performance Monitoring**
- **Core Web Vitals**: LCP, FID, CLS metrics
- **Bundle Size**: Track bundle size growth
- **API Performance**: Monitor API response times
- **User Experience**: Real user monitoring

## 🐛 Troubleshooting

### **Common Issues**

#### **API Connection Issues**
- Check if backend is running on port 8000
- Verify API_BASE_URL in environment variables
- Check CORS configuration on backend

#### **Authentication Issues**
- Clear localStorage and try again
- Check token expiration
- Verify JWT secret configuration

#### **WebSocket Issues**
- Check WebSocket URL configuration
- Verify backend WebSocket setup
- Check firewall and proxy settings

### **Debug Mode**
Enable debug mode for detailed logging:

```env
VITE_DEBUG=true
```

## 🤝 Contributing

### **Development Workflow**
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### **Code Review Process**
- All changes require code review
- Tests must pass before merging
- TypeScript compilation must succeed
- ESLint checks must pass

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Documentation**: Check this README and code comments
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub discussions for questions
- **Email**: Contact the development team

---

**Built with ❤️ for the Alumni Community**
