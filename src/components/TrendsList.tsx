import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, Hash, Calendar, Target } from "lucide-react";

interface Trend {
  id: string;
  topic: string;
  platform: "linkedin" | "instagram" | "twitter";
  volume: number;
  sentiment: "positive" | "negative" | "neutral";
  growth: string;
  lastUpdated: string;
}

export const TrendsList = () => {
  const trends: Trend[] = [
    {
      id: "1",
      topic: "#AIInHealthcare",
      platform: "linkedin",
      volume: 12500,
      sentiment: "positive",
      growth: "+45%",
      lastUpdated: "2 minutes ago"
    },
    {
      id: "2", 
      topic: "#TechInnovation",
      platform: "twitter",
      volume: 8900,
      sentiment: "positive", 
      growth: "+32%",
      lastUpdated: "5 minutes ago"
    },
    {
      id: "3",
      topic: "#SustainableTech",
      platform: "instagram",
      volume: 6700,
      sentiment: "positive",
      growth: "+28%",
      lastUpdated: "8 minutes ago"
    },
    {
      id: "4",
      topic: "#RemoteWork",
      platform: "linkedin",
      volume: 5400,
      sentiment: "neutral",
      growth: "+15%",
      lastUpdated: "12 minutes ago"
    },
    {
      id: "5",
      topic: "#DigitalMarketing",
      platform: "instagram",
      volume: 4200,
      sentiment: "positive",
      growth: "+22%",
      lastUpdated: "15 minutes ago"
    }
  ];

  const sentimentColors = {
    positive: "bg-success/20 text-success",
    negative: "bg-destructive/20 text-destructive",
    neutral: "bg-muted text-muted-foreground"
  };

  const platformColors = {
    linkedin: "text-linkedin",
    instagram: "text-instagram", 
    twitter: "text-twitter"
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Trending Topics</h2>
        <Button variant="outline" className="gap-2">
          <TrendingUp className="h-4 w-4" />
          Refresh Trends
        </Button>
      </div>

      <div className="grid gap-4">
        {trends.map((trend) => (
          <Card key={trend.id} className="bg-gradient-card border-border hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="bg-primary/20 p-3 rounded-lg">
                    <Hash className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">{trend.topic}</h3>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span className={platformColors[trend.platform]}>
                        {trend.platform.charAt(0).toUpperCase() + trend.platform.slice(1)}
                      </span>
                      <span>•</span>
                      <span>{trend.volume.toLocaleString()} mentions</span>
                      <span>•</span>
                      <span>{trend.lastUpdated}</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Badge className={sentimentColors[trend.sentiment]}>
                    {trend.sentiment}
                  </Badge>
                  <Badge variant="secondary" className="bg-success/20 text-success">
                    {trend.growth}
                  </Badge>
                  <Button size="sm" variant="outline" className="gap-2">
                    <Target className="h-4 w-4" />
                    Create Content
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};