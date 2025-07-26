import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Edit, Eye, Calendar, Linkedin, Instagram, Twitter, Sparkles } from "lucide-react";

interface Draft {
  id: string;
  topic: string;
  platform: "linkedin" | "instagram" | "twitter";
  content: string;
  status: "draft" | "approved" | "scheduled";
  createdAt: string;
  scheduledFor?: string;
  variant: "A" | "B";
}

export const ContentDrafts = () => {
  const drafts: Draft[] = [
    {
      id: "1",
      topic: "#AIInHealthcare",
      platform: "linkedin",
      content: "🏥 AI is revolutionizing healthcare diagnostics! From early disease detection to personalized treatment plans, artificial intelligence is helping doctors save more lives than ever before. What's your experience with AI in healthcare? #AIInHealthcare #HealthTech #Innovation",
      status: "approved",
      createdAt: "5 minutes ago",
      scheduledFor: "Today at 2:00 PM",
      variant: "A"
    },
    {
      id: "2",
      topic: "#TechInnovation", 
      platform: "twitter",
      content: "🚀 The future is here! New tech innovations are reshaping how we work, connect, and solve global challenges. Which breakthrough excites you most? #TechInnovation #Future #Innovation",
      status: "draft",
      createdAt: "8 minutes ago",
      variant: "A"
    },
    {
      id: "3",
      topic: "#SustainableTech",
      platform: "instagram",
      content: "🌱✨ Sustainable technology isn't just a trend—it's our future! From solar innovations to eco-friendly apps, tech is helping heal our planet. 🌍💚 Tag someone who cares about green tech! #SustainableTech #GreenTech #EcoFriendly #Sustainability #TechForGood",
      status: "scheduled",
      createdAt: "12 minutes ago",
      scheduledFor: "Today at 6:00 PM",
      variant: "B"
    },
    {
      id: "4",
      topic: "#RemoteWork",
      platform: "linkedin", 
      content: "🏠💼 Remote work has transformed from emergency measure to strategic advantage. Companies embracing flexible work are seeing higher productivity and happier employees. How has remote work changed your career? #RemoteWork #WorkFromHome #FutureOfWork",
      status: "draft",
      createdAt: "15 minutes ago",
      variant: "A"
    }
  ];

  const statusColors = {
    draft: "bg-warning/20 text-warning",
    approved: "bg-success/20 text-success", 
    scheduled: "bg-info/20 text-info"
  };

  const platformIcons = {
    linkedin: Linkedin,
    instagram: Instagram,
    twitter: Twitter
  };

  const platformColors = {
    linkedin: "text-linkedin bg-linkedin/20",
    instagram: "text-instagram bg-instagram/20",
    twitter: "text-twitter bg-twitter/20"
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