import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { TrendingUp, Hash, Calendar, Target } from "lucide-react";

interface Trend {
  topic: string;
  platform: string;
  volume: number;
}

export const TrendsList = () => {
  const [trends, setTrends] = useState<Trend[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch("/api/social/trends")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch trends");
        return res.json();
      })
      .then((data) => {
        setTrends(data);
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

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-foreground">Trending Topics</h2>
        <Button variant="outline" className="gap-2" onClick={() => window.location.reload()}>
          <TrendingUp className="h-4 w-4" />
          Refresh Trends
        </Button>
      </div>

      {loading && <div>Loading trends...</div>}
      {error && <div className="text-destructive">{error}</div>}
      <div className="grid gap-4">
        {trends.map((trend, i) => (
          <Card key={trend.topic + trend.platform + i} className="bg-gradient-card border-border hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="bg-primary/20 p-3 rounded-lg">
                    <Hash className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">{trend.topic}</h3>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <span className={platformColors[trend.platform] || ""}>
                        {trend.platform.charAt(0).toUpperCase() + trend.platform.slice(1)}
                      </span>
                      <span>•</span>
                      <span>{trend.volume.toLocaleString()} mentions</span>
                    </div>
                  </div>
                </div>
                <Button size="sm" variant="outline" className="gap-2">
                  <Target className="h-4 w-4" />
                  Create Content
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};