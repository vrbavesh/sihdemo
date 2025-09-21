import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../ui/card";
import { Button } from "../ui/button";
import { Input } from "../ui/input";
import { Label } from "../ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../ui/select";
import { Checkbox } from "../ui/checkbox";
import { Badge } from "../ui/badge";
import { Linkedin, GraduationCap, X, Loader2, AlertCircle } from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";
import { RegisterRequest } from "../../services/api";

interface LoginPageProps {
  onLogin: (userType: string, userData: any) => void;
}

export function LoginPage({ onLogin }: LoginPageProps) {
  const { register, isLoading } = useAuth();
  const [isLoginMode, setIsLoginMode] = useState(true);
  const [userType, setUserType] = useState<string>("");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    password_confirm: "",
    first_name: "",
    last_name: "",
    linkedinProfile: "",
    currentPosition: "",
    company: "",
    graduationYear: "",
    department: "",
    interests: [] as string[]
  });
  const [error, setError] = useState<string>("");

  const interestOptions = [
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
  ];

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  const removeInterest = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.filter(i => i !== interest)
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (isLoginMode) {
      // Handle login
      try {
        await onLogin(userType, formData);
      } catch (error) {
        setError("Login failed. Please check your credentials.");
      }
    } else {
      // Handle registration
      if (!userType || !formData.email || !formData.password || formData.interests.length < 3) {
        setError("Please fill in all required fields and select at least 3 interests.");
        return;
      }

      if (formData.password !== formData.password_confirm) {
        setError("Passwords do not match.");
        return;
      }

      try {
        const registrationData: RegisterRequest = {
          email: formData.email,
          password: formData.password,
          password_confirm: formData.password_confirm,
          first_name: formData.first_name,
          last_name: formData.last_name,
          user_type: userType as any,
          linkedin_profile: formData.linkedinProfile,
          current_position: formData.currentPosition,
          company: formData.company,
          graduation_year: formData.graduationYear ? parseInt(formData.graduationYear) : undefined,
          department: formData.department,
          interests: formData.interests
        };

        await register(registrationData);
        onLogin(userType, formData);
      } catch (error: any) {
        setError(error.message || "Registration failed. Please try again.");
      }
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <GraduationCap className="h-12 w-12 text-primary" />
          </div>
          <CardTitle>Alumni Connect</CardTitle>
          <CardDescription>
            Connect with your institution's alumni network
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Toggle between login and register */}
          <div className="flex mb-6">
            <Button
              variant={isLoginMode ? "default" : "outline"}
              className="flex-1 mr-2"
              onClick={() => setIsLoginMode(true)}
            >
              Login
            </Button>
            <Button
              variant={!isLoginMode ? "default" : "outline"}
              className="flex-1 ml-2"
              onClick={() => setIsLoginMode(false)}
            >
              Register
            </Button>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center">
              <AlertCircle className="h-4 w-4 text-red-600 mr-2" />
              <span className="text-sm text-red-600">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLoginMode && (
              <div className="space-y-2">
                <Label htmlFor="userType">I am a</Label>
                <Select value={userType} onValueChange={setUserType}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select your role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="student">Student</SelectItem>
                    <SelectItem value="alumni">Alumni</SelectItem>
                    <SelectItem value="faculty">Faculty</SelectItem>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="recruiter">Recruiter</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="your.email@institution.edu"
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="Enter your password"
                required
              />
            </div>

            {!isLoginMode && (
              <>
                <div className="space-y-2">
                  <Label htmlFor="password_confirm">Confirm Password</Label>
                  <Input
                    id="password_confirm"
                    type="password"
                    value={formData.password_confirm}
                    onChange={(e) => setFormData({ ...formData, password_confirm: e.target.value })}
                    placeholder="Confirm your password"
                    required
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="first_name">First Name</Label>
                    <Input
                      id="first_name"
                      value={formData.first_name}
                      onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                      placeholder="John"
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="last_name">Last Name</Label>
                    <Input
                      id="last_name"
                      value={formData.last_name}
                      onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                      placeholder="Doe"
                      required
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="linkedin">LinkedIn Profile</Label>
                  <div className="relative">
                    <Linkedin className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="linkedin"
                      value={formData.linkedinProfile}
                      onChange={(e) => setFormData({ ...formData, linkedinProfile: e.target.value })}
                      placeholder="linkedin.com/in/yourprofile"
                      className="pl-10"
                    />
                  </div>
                </div>

                {(userType === "alumni" || userType === "recruiter") && (
                  <>
                    <div className="space-y-2">
                      <Label htmlFor="position">Current Position</Label>
                      <Input
                        id="position"
                        value={formData.currentPosition}
                        onChange={(e) => setFormData({ ...formData, currentPosition: e.target.value })}
                        placeholder="Software Engineer, Product Manager, etc."
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="company">Company</Label>
                      <Input
                        id="company"
                        value={formData.company}
                        onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                        placeholder="Google, Microsoft, etc."
                      />
                    </div>
                  </>
                )}

                {(userType === "student" || userType === "alumni") && (
                  <>
                    <div className="space-y-2">
                      <Label htmlFor="year">
                        {userType === "alumni" ? "Graduation Year" : "Expected Graduation Year"}
                      </Label>
                      <Input
                        id="year"
                        type="number"
                        value={formData.graduationYear}
                        onChange={(e) => setFormData({ ...formData, graduationYear: e.target.value })}
                        placeholder="2024"
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="department">Department</Label>
                      <Input
                        id="department"
                        value={formData.department}
                        onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                        placeholder="Computer Science, Business, etc."
                      />
                    </div>
                  </>
                )}

                {/* Interests Section */}
                <div className="space-y-3">
                  <Label>Your Interests (Select at least 3)</Label>
                  
                  {/* Selected Interests */}
                  {formData.interests.length > 0 && (
                    <div className="flex flex-wrap gap-2 p-3 bg-blue-50 rounded-lg border">
                      {formData.interests.map((interest) => (
                        <Badge 
                          key={interest} 
                          variant="default" 
                          className="bg-blue-600 text-white hover:bg-blue-700 cursor-pointer"
                          onClick={() => removeInterest(interest)}
                        >
                          {interest}
                          <X className="h-3 w-3 ml-1" />
                        </Badge>
                      ))}
                    </div>
                  )}
                  
                  {/* Available Interests */}
                  <div className="max-h-40 overflow-y-auto border rounded-lg p-3 bg-gray-50">
                    <div className="grid grid-cols-2 gap-2">
                      {interestOptions.map((interest) => (
                        <label
                          key={interest}
                          className={`flex items-center space-x-2 p-2 rounded cursor-pointer transition-colors ${
                            formData.interests.includes(interest)
                              ? 'bg-blue-100 text-blue-800'
                              : 'hover:bg-gray-100'
                          }`}
                        >
                          <Checkbox
                            checked={formData.interests.includes(interest)}
                            onCheckedChange={() => handleInterestToggle(interest)}
                            className="data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"
                          />
                          <span className="text-sm">{interest}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                  
                  <p className="text-xs text-muted-foreground">
                    Selected: {formData.interests.length} (minimum 3 required)
                  </p>
                </div>
              </>
            )}

            <Button 
              type="submit" 
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700" 
              disabled={isLoading || (!isLoginMode && (!userType || !formData.email || formData.interests.length < 3))}
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  {isLoginMode ? 'Signing in...' : 'Creating account...'}
                </>
              ) : (
                isLoginMode ? 'Sign In' : 'Create Account'
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
