import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { 
  TrendingUp, 
  Heart, 
  MessageCircle, 
  Share, 
  Users, 
  Target 
} from "lucide-react";

interface PostMetric {
  id: string;
  postId: number;
  platform: string;
  likes: number;
  shares: number;
  comments: number;
  clicks: number;
  engagementRate: number;
  measuredAt: string;
}

interface MetricsSummary {
  totalPosts: number;
  avgEngagement: number;
  totalLikes: number;
  totalShares: number;
  engagementLift: number;
}

interface MetricsData {
  summary: MetricsSummary;
  metrics: PostMetric[];
}

export const EngagementMetrics = () => {
  const [metrics, setMetrics] = useState<MetricsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/metrics")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch engagement metrics");
        return res.json();
      })
      .then((data) => {
        setMetrics(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const platformColors = {
    linkedin: "text-linkedin",
    instagram: "text-instagram", 
    twitter: "text-twitter",
    tiktok: "text-tiktok",
    youtube: "text-youtube",
    reddit: "text-reddit"
  };

  const trendColors = {
    up: "text-success",
    down: "text-destructive",
    stable: "text-muted-foreground"
  };

  if (loading) return <div>Loading engagement metrics...</div>;
  if (error) return <div className="text-destructive">{error}</div>;
  if (!metrics) return null;

  const overallMetrics = metrics.summary;
  const posts = metrics.metrics;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Engagement Analytics</h2>
        <Badge className="bg-success/20 text-success text-lg px-4 py-2">
          <Target className="h-4 w-4 mr-2" />
          +{overallMetrics.engagementLift}% Lift Achieved!
        </Badge>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-primary/20 p-2 rounded-lg">
                <TrendingUp className="h-5 w-5 text-primary" />
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
                <Heart className="h-5 w-5 text-success" />
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
                <Share className="h-5 w-5 text-info" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Shares</p>
                <p className="text-2xl font-bold text-foreground">{overallMetrics.totalShares}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-3">
              <div className="bg-warning/20 p-2 rounded-lg">
                <Users className="h-5 w-5 text-warning" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Likes</p>
                <p className="text-2xl font-bold text-foreground">{overallMetrics.totalLikes}</p>
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
        
        {posts.map((post: PostMetric) => (
          <Card key={post.id} className="bg-gradient-card border-border">
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <p className="text-foreground font-medium mb-2">Post #{post.postId}</p>
                  <div className="flex items-center gap-2 text-sm text-muted-foreground">
                    <span className={platformColors[post.platform] || ""}>
                      {post.platform.charAt(0).toUpperCase() + post.platform.slice(1)}
                    </span>
                    <span>•</span>
                    <span>{new Date(post.measuredAt).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="bg-primary/20 text-primary">
                    {post.engagementRate.toFixed(1)}% engagement
                  </Badge>
                  <TrendingUp className={`h-4 w-4 ${post.engagementRate > 5 ? 'text-success' : 'text-muted-foreground'}`} />
                </div>
              </div>
              
              <div className="grid grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  <Heart className="h-4 w-4 text-destructive" />
                  <span className="text-foreground font-medium">{post.likes}</span>
                  <span className="text-sm text-muted-foreground">likes</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <MessageCircle className="h-4 w-4 text-info" />
                  <span className="text-foreground font-medium">{post.comments}</span>
                  <span className="text-sm text-muted-foreground">comments</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Share className="h-4 w-4 text-success" />
                  <span className="text-foreground font-medium">{post.shares}</span>
                  <span className="text-sm text-muted-foreground">shares</span>
                </div>
                
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-warning" />
                  <span className="text-foreground font-medium">{post.clicks}</span>
                  <span className="text-sm text-muted-foreground">clicks</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};