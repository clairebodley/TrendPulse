import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LucideIcon } from "lucide-react";

interface Agent {
  id: string;
  name: string;
  description: string;
  status: "active" | "inactive" | "error";
  color: string;
  icon: LucideIcon;
  lastActivity: string;
  metrics: Record<string, string | number>;
}

interface AgentCardProps {
  agent: Agent;
}

export const AgentCard = ({ agent }: AgentCardProps) => {
  const statusColors = {
    active: "bg-success/20 text-success",
    inactive: "bg-muted text-muted-foreground", 
    error: "bg-destructive/20 text-destructive"
  };

  return (
    <Card className="bg-gradient-card border-border hover:shadow-lg transition-all duration-300 group">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg bg-${agent.color}/20 group-hover:animate-pulse`}>
              <agent.icon className={`h-5 w-5 text-${agent.color}`} />
            </div>
            <div>
              <CardTitle className="text-lg text-foreground">{agent.name}</CardTitle>
              <p className="text-sm text-muted-foreground">{agent.lastActivity}</p>
            </div>
          </div>
          <Badge className={statusColors[agent.status]}>
            {agent.status}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground mt-2">{agent.description}</p>
      </CardHeader>
      
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(agent.metrics).map(([key, value]) => (
            <div key={key} className="text-center">
              <p className="text-lg font-bold text-foreground">{value}</p>
              <p className="text-xs text-muted-foreground capitalize">{key}</p>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};