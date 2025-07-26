import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, Clock, Linkedin, Instagram, Twitter, Edit, Trash2, Send, Music, Youtube, MessageSquare } from "lucide-react";

interface ScheduledPost {
  id: string;
  content: string;
  platform: "linkedin" | "instagram" | "twitter" | "tiktok" | "youtube" | "reddit";
  scheduledFor: string;
  status: "pending" | "posting" | "posted" | "failed";
  topic: string;
  variant: "A" | "B";
  bufferPostId?: string;
}

export const PostSchedule = () => {
  const [scheduledPosts, setScheduledPosts] = useState<ScheduledPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/posts")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch scheduled posts");
        return res.json();
      })
      .then((data) => {
        setScheduledPosts(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const statusColors = {
    pending: "bg-warning/20 text-warning",
    posting: "bg-info/20 text-info animate-pulse",
    posted: "bg-success/20 text-success",
    failed: "bg-destructive/20 text-destructive"
  };

  const platformIcons = {
    linkedin: Linkedin,
    instagram: Instagram, 
    twitter: Twitter,
    tiktok: Music,
    youtube: Youtube,
    reddit: MessageSquare
  };

  const platformColors = {
    linkedin: "text-linkedin bg-linkedin/20",
    instagram: "text-instagram bg-instagram/20",
    twitter: "text-twitter bg-twitter/20",
    tiktok: "text-tiktok bg-tiktok/20",
    youtube: "text-youtube bg-youtube/20",
    reddit: "text-reddit bg-reddit/20"
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "pending": return Clock;
      case "posting": return Send;
      case "posted": return Calendar;
      case "failed": return Trash2;
      default: return Clock;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Post Schedule</h2>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2">
            <Calendar className="h-4 w-4" />
            Schedule New Post
          </Button>
          <Button className="gap-2 bg-gradient-primary">
            <Send className="h-4 w-4" />
            Post Now
          </Button>
        </div>
      </div>

      {loading && <div>Loading scheduled posts...</div>}
      {error && <div className="text-destructive">{error}</div>}
      {/* Schedule Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-warning">{scheduledPosts.filter(p => p.status === 'pending').length}</p>
              <p className="text-sm text-muted-foreground">Pending</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-info">{scheduledPosts.filter(p => p.status === 'posting').length}</p>
              <p className="text-sm text-muted-foreground">Posting</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-success">{scheduledPosts.filter(p => p.status === 'posted').length}</p>
              <p className="text-sm text-muted-foreground">Posted</p>
            </div>
          </CardContent>
        </Card>
        
        <Card className="bg-gradient-card border-border">
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-destructive">{scheduledPosts.filter(p => p.status === 'failed').length}</p>
              <p className="text-sm text-muted-foreground">Failed</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scheduled Posts List */}
      <div className="space-y-4">
        {scheduledPosts.map((post) => {
          const PlatformIcon = platformIcons[post.platform];
          const StatusIcon = getStatusIcon(post.status);
          
          return (
            <Card key={post.id} className="bg-gradient-card border-border">
              <CardContent className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-start gap-4 flex-1">
                    <div className={`p-2 rounded-lg ${platformColors[post.platform]}`}>
                      <PlatformIcon className="h-5 w-5" />
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h3 className="font-semibold text-foreground">{post.topic}</h3>
                        <Badge variant="outline" className="text-xs">
                          Variant {post.variant}
                        </Badge>
                      </div>
                      
                      <p className="text-foreground mb-3 leading-relaxed">
                        {post.content.length > 150 
                          ? `${post.content.substring(0, 150)}...` 
                          : post.content
                        }
                      </p>
                      
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          <span>{post.scheduledFor}</span>
                        </div>
                        {post.bufferPostId && (
                          <div className="flex items-center gap-1">
                            <span>Buffer ID:</span>
                            <code className="bg-muted px-1 rounded text-xs">{post.bufferPostId}</code>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-2">
                      <StatusIcon className={`h-4 w-4 ${statusColors[post.status].split(' ')[1]}`} />
                      <Badge className={statusColors[post.status]}>
                        {post.status}
                      </Badge>
                    </div>
                    
                    {post.status === 'pending' && (
                      <div className="flex gap-1">
                        <Button size="sm" variant="outline" className="gap-1">
                          <Edit className="h-3 w-3" />
                        </Button>
                        <Button size="sm" variant="outline" className="gap-1">
                          <Trash2 className="h-3 w-3" />
                        </Button>
                        <Button size="sm" className="gap-1 bg-gradient-primary">
                          <Send className="h-3 w-3" />
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};