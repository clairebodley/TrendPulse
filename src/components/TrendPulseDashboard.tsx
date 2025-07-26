import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Brain, 
  TrendingUp, 
  Edit, 
  Calendar, 
  BarChart3, 
  Zap,
  Linkedin,
  Instagram,
  Twitter,
  Play,
  Pause,
  Activity
} from "lucide-react";
import { AgentCard } from "./AgentCard";
import { TrendsList } from "./TrendsList";
import { ContentDrafts } from "./ContentDrafts";
import { EngagementMetrics } from "./EngagementMetrics";
import { PostSchedule } from "./PostSchedule";

export const TrendPulseDashboard = () => {
  const [systemStatus, setSystemStatus] = useState<"active" | "paused">("active");
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const agents = [
    {
      id: "trend-watcher",
      name: "TrendWatcher",
      description: "Monitors trending topics across LinkedIn, Instagram & Twitter",
      status: "active" as const,
      color: "trend-watcher",
      icon: TrendingUp,
      lastActivity: "2 minutes ago",
      metrics: { detected: 12, analyzed: 8, priority: 3 }
    },
    {
      id: "content-crafter",
      name: "ContentCrafter", 
      description: "Generates platform-optimized posts using AI",
      status: "active" as const,
      color: "content-crafter",
      icon: Edit,
      lastActivity: "1 minute ago",
      metrics: { generated: 24, variants: 6, approved: 18 }
    },
    {
      id: "post-scheduler",
      name: "PostScheduler",
      description: "Manages posting schedule via Buffer API",
      status: "active" as const,
      color: "post-scheduler", 
      icon: Calendar,
      lastActivity: "5 minutes ago",
      metrics: { scheduled: 15, posted: 8, pending: 7 }
    },
    {
      id: "engagement-monitor",
      name: "EngagementMonitor",
      description: "Tracks post performance and engagement metrics",
      status: "active" as const,
      color: "engagement-monitor",
      icon: BarChart3,
      lastActivity: "30 seconds ago",
      metrics: { monitored: 42, alerts: 2, growth: "+32%" }
    },
    {
      id: "strategy-optimizer",
      name: "StrategyOptimizer", 
      description: "Adapts strategy based on performance data",
      status: "active" as const,
      color: "strategy-optimizer",
      icon: Zap,
      lastActivity: "3 minutes ago",
      metrics: { optimizations: 5, improvements: 3, lift: "+28%" }
    }
  ];

  const platforms = [
    { name: "LinkedIn", icon: Linkedin, color: "linkedin", posts: 8, engagement: "+45%" },
    { name: "Instagram", icon: Instagram, color: "instagram", posts: 12, engagement: "+38%" },
    { name: "Twitter", icon: Twitter, color: "twitter", posts: 15, engagement: "+22%" }
  ];

  return (
    <div className="min-h-screen bg-gradient-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="bg-gradient-primary p-3 rounded-xl">
              <Brain className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-foreground">TrendPulse AI</h1>
              <p className="text-muted-foreground">Multi-Agent Social Media Intelligence</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-muted-foreground">System Status</p>
              <div className="flex items-center gap-2">
                <Activity className={`h-4 w-4 ${systemStatus === 'active' ? 'text-success animate-pulse' : 'text-muted-foreground'}`} />
                <span className="font-medium text-foreground capitalize">{systemStatus}</span>
              </div>
            </div>
            
            <Button
              variant={systemStatus === "active" ? "destructive" : "default"}
              onClick={() => setSystemStatus(systemStatus === "active" ? "paused" : "active")}
              className="gap-2"
            >
              {systemStatus === "active" ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
              {systemStatus === "active" ? "Pause System" : "Start System"}
            </Button>
          </div>
        </div>

        {/* Platform Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {platforms.map((platform) => (
            <Card key={platform.name} className="bg-gradient-card border-border">
              <CardContent className="p-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg bg-${platform.color}/20`}>
                      <platform.icon className={`h-5 w-5 text-${platform.color}`} />
                    </div>
                    <div>
                      <p className="font-medium text-foreground">{platform.name}</p>
                      <p className="text-sm text-muted-foreground">{platform.posts} posts today</p>
                    </div>
                  </div>
                  <Badge variant="secondary" className="bg-success/20 text-success">
                    {platform.engagement}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Agents Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <AgentCard key={agent.id} agent={agent} />
          ))}
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="trends" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="trends">Trending Topics</TabsTrigger>
            <TabsTrigger value="content">Content Drafts</TabsTrigger>
            <TabsTrigger value="schedule">Post Schedule</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
          </TabsList>
          
          <TabsContent value="trends" className="space-y-4">
            <TrendsList />
          </TabsContent>
          
          <TabsContent value="content" className="space-y-4">
            <ContentDrafts />
          </TabsContent>
          
          <TabsContent value="schedule" className="space-y-4">
            <PostSchedule />
          </TabsContent>
          
          <TabsContent value="analytics" className="space-y-4">
            <EngagementMetrics />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};