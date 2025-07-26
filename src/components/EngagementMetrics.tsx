import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { BarChart3, TrendingUp, Users, Heart, MessageCircle, Share, Target } from "lucide-react";

interface PostMetric {
  id: string;
  content: string;
  platform: "linkedin" | "instagram" | "twitter";
  publishedAt: string;
  metrics: {
    likes: number;
    comments: number;
    shares: number;
    reach: number;
    engagementRate: number;
  };
  trend: "up" | "down" | "stable";
}

export const EngagementMetrics = () => {
  const posts: PostMetric[] = [
    {
      id: "1",
      content: "🏥 AI is revolutionizing healthcare diagnostics! From early disease detection...",
      platform: "linkedin",
      publishedAt: "2 hours ago",
      metrics: {
        likes: 127,
        comments: 23,
        shares: 45,
        reach: 2400,
        engagementRate: 8.1
      },
      trend: "up"
    },
    {
      id: "2",
      content: "🚀 The future is here! New tech innovations are reshaping how we work...",
      platform: "twitter", 
      publishedAt: "4 hours ago",
      metrics: {
        likes: 89,
        comments: 12,
        shares: 34,
        reach: 1800,
        engagementRate: 7.5
      },
      trend: "up"
    },
    {
      id: "3",
      content: "🌱✨ Sustainable technology isn't just a trend—it's our future!...",
      platform: "instagram",
      publishedAt: "6 hours ago", 
      metrics: {
        likes: 156,
        comments: 31,
        shares: 28,
        reach: 3200,
        engagementRate: 6.7
      },
      trend: "stable"
    }
  ];

  const overallMetrics = {
    totalPosts: 35,
    avgEngagement: 7.4,
    totalReach: 45600,
    engagementLift: 32,
    baselineEngagement: 5.6
  };

  const platformColors = {
    linkedin: "text-linkedin",
    instagram: "text-instagram",
    twitter: "text-twitter"
  };

  const trendColors = {
    up: "text-success",
    down: "text-destructive", 
    stable: "text-muted-foreground"
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Engagement Analytics</h2>
        <Badge className="bg-success/20 text-success text-lg px-4 py-2">
          <Target className="h-4 w-4 mr-2" />
          +{overallMetrics.engagementLift}% Lift Achieved!
        </Badge>
      </div>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-primary/20 p-2 rounded-lg">
                <BarChart3 className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Posts</p>
                <p className="text-2xl font-bold text-foreground">{overallMetrics.totalPosts}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-success/20 p-2 rounded-lg">
                <TrendingUp className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Avg Engagement</p>
                <p className="text-2xl font-bold text-foreground">{overallMetrics.avgEngagement}%</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-info/20 p-2 rounded-lg">
                <Users className="h-5 w-5 text-info" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Reach</p>
                <p className="text-2xl font-bold text-foreground">{(overallMetrics.totalReach / 1000).toFixed(1)}K</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-success/20 p-2 rounded-lg">
                <Target className="h-5 w-5 text-success" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Baseline vs Now</p>
                <p className="text-2xl font-bold text-foreground">{overallMetrics.baselineEngagement}% → {overallMetrics.avgEngagement}%</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Engagement Progress */}
      <Card className="bg-gradient-card border-border">
        <CardHeader>
          <CardTitle className="text-foreground">KPI Progress: 30% Engagement Lift Target</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">Progress toward 30% lift goal</span>
              <span className="text-foreground font-medium">{overallMetrics.engagementLift}% / 30%</span>
            </div>
            <Progress value={(overallMetrics.engagementLift / 30) * 100} className="h-3" />
            <p className="text-success text-sm font-medium">🎯 Target exceeded! System achieved {overallMetrics.engagementLift}% lift</p>
          </div>
        </CardContent>
      </Card>

      {/* Individual Post Performance */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-foreground">Recent Post Performance</h3>
        
        {posts.map((post) => (
          <Card key={post.id} className="bg-gradient-card border-border">
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <p className="text-foreground font-medium mb-2">{post.content}</p>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span className={platformColors[post.platform]}>
                      {post.platform.charAt(0).toUpperCase() + post.platform.slice(1)}
                    </span>
                    <span>•</span>
                    <span>{post.publishedAt}</span>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-primary/20 text-primary">
                    {post.metrics.engagementRate}% engagement
                  </Badge>
                  <TrendingUp className={`h-4 w-4 ${trendColors[post.trend]}`} />
                </div>
              </div>
              
              <div className="grid grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  <Heart className="h-4 w-4 text-destructive" />
                  <span className="text-foreground font-medium">{post.metrics.likes}</span>
                  <span className="text-sm text-muted-foreground">likes</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <MessageCircle className="h-4 w-4 text-info" />
                  <span className="text-foreground font-medium">{post.metrics.comments}</span>
                  <span className="text-sm text-muted-foreground">comments</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Share className="h-4 w-4 text-success" />
                  <span className="text-foreground font-medium">{post.metrics.shares}</span>
                  <span className="text-sm text-muted-foreground">shares</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-warning" />
                  <span className="text-foreground font-medium">{(post.metrics.reach / 1000).toFixed(1)}K</span>
                  <span className="text-sm text-muted-foreground">reach</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};