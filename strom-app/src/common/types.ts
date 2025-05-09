// common/types.ts
export interface Message {
  text: string;
  sender: "user" | "bot";
  projectData?: ProjectAgentResponse;
}

export interface ProjectAgentResponse {
  points: string[];
  is_greeting: boolean;
  exists_in_data: boolean;
  exists_elsewhere: boolean;
  relevant_projects?: string[];
}