import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Edit, Eye, Calendar, Linkedin, Instagram, Twitter, Sparkles, Music, Youtube, MessageSquare } from "lucide-react";

interface Draft {
  id: string;
  topic: string;
  platform: "linkedin" | "instagram" | "twitter" | "tiktok" | "youtube" | "reddit";
  content: string;
  status: "draft" | "approved" | "scheduled";
  createdAt: string;
  scheduledFor?: string;
  variant: "A" | "B";
}

export const ContentDrafts = () => {
  const [drafts, setDrafts] = useState<Draft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/drafts")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch drafts");
        return res.json();
      })
      .then((data) => {
        setDrafts(data);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const statusColors = {
    draft: "bg-warning/20 text-warning",
    approved: "bg-success/20 text-success", 
    scheduled: "bg-info/20 text-info"
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

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Content Drafts</h2>
        <Button className="gap-2 bg-gradient-primary">
          <Sparkles className="h-4 w-4" />
          Generate New Content
        </Button>
      </div>

      {loading && <div>Loading drafts...</div>}
      {error && <div className="text-destructive">{error}</div>}
      <div className="grid gap-6">
        {drafts.map((draft) => {
          const PlatformIcon = platformIcons[draft.platform];
          
          return (
            <Card key={draft.id} className="bg-gradient-card border-border">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${platformColors[draft.platform]}`}>
                      <PlatformIcon className="h-5 w-5" />
                    </div>
                    <div>
                      <CardTitle className="text-lg text-foreground">{draft.topic}</CardTitle>
                      <p className="text-sm text-muted-foreground">
                        Created {draft.createdAt} • Variant {draft.variant}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Badge className={statusColors[draft.status]}>
                      {draft.status}
                    </Badge>
                    {draft.scheduledFor && (
                      <Badge variant="outline" className="gap-1">
                        <Calendar className="h-3 w-3" />
                        {draft.scheduledFor}
                      </Badge>
                    )}
                  </div>
                </div>
              </CardHeader>
              
              <CardContent>
                <div className="bg-muted/30 rounded-lg p-4 mb-4">
                  <p className="text-foreground leading-relaxed">{draft.content}</p>
                </div>
                
                <div className="flex items-center gap-2">
                  <Button size="sm" variant="outline" className="gap-2">
                    <Edit className="h-4 w-4" />
                    Edit
                  </Button>
                  <Button size="sm" variant="outline" className="gap-2">
                    <Eye className="h-4 w-4" />
                    Preview
                  </Button>
                  {draft.status === "draft" && (
                    <Button size="sm" className="gap-2 bg-gradient-primary">
                      <Calendar className="h-4 w-4" />
                      Schedule
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};