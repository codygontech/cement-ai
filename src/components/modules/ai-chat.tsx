'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Send, Bot, User, Loader2, MessageSquare, Sparkles } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string;
}

export function AIChatModule() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hello! I'm your Cement Plant AI Assistant powered by Google Gemini. I can help you with:\n\n• Real-time plant data analysis\n• Process optimization recommendations\n• Quality control insights\n• Energy efficiency analysis\n• Predictive maintenance alerts\n\nWhat would you like to know about your cement plant operations?",
      timestamp: new Date().toISOString()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<string[]>([
    "What's the current kiln efficiency?",
    "Show me quality metrics for the last 24 hours",
    "Analyze grinding operations performance",
    "What are the top optimization opportunities?",
    "Check for any process anomalies"
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Function to format markdown-like text
  const formatMessage = (text: string) => {
    const lines = text.split('\n');
    const formatted: React.ReactElement[] = [];
    
    lines.forEach((line, index) => {
      // Bold text with **text**
      if (line.includes('**')) {
        const parts = line.split('**');
        const elements = parts.map((part, i) => 
          i % 2 === 1 ? <strong key={i} className="font-bold">{part}</strong> : part
        );
        formatted.push(<div key={index} className="mb-2">{elements}</div>);
      }
      // Bullet points
      else if (line.trim().startsWith('•') || line.trim().startsWith('-')) {
        formatted.push(<div key={index} className="ml-4 mb-1">{line}</div>);
      }
      // Empty lines for spacing
      else if (line.trim() === '') {
        formatted.push(<div key={index} className="h-2"></div>);
      }
      // Regular text
      else {
        formatted.push(<div key={index} className="mb-1">{line}</div>);
      }
    });
    
    return <div>{formatted}</div>;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          history: messages.slice(-10) // Send last 10 messages for context
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        role: 'assistant',
        content: data.message,
        timestamp: data.timestamp
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update recommendations with new context-aware suggestions
      if (data.recommendations && data.recommendations.length > 0) {
        setRecommendations(data.recommendations);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        role: 'assistant',
        content: `Sorry, I encountered an error. Please make sure the backend server is running at ${process.env.NEXT_PUBLIC_API_URL}`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleRecommendationClick = (recommendation: string) => {
    setInput(recommendation);
    // Simulate sending the message
    const userMessage: Message = {
      role: 'user',
      content: recommendation,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Send to backend
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/ai/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: recommendation,
        history: messages.slice(-10)
      }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to get response');
        }
        return response.json();
      })
      .then(data => {
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.message,
          timestamp: data.timestamp
        };
        setMessages(prev => [...prev, assistantMessage]);
        if (data.recommendations && data.recommendations.length > 0) {
          setRecommendations(data.recommendations);
        }
      })
      .catch(error => {
        console.error('Error sending message:', error);
        const errorMessage: Message = {
          role: 'assistant',
          content: `Sorry, I encountered an error. Please make sure the backend server is running at ${process.env.NEXT_PUBLIC_API_URL}`,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      })
      .finally(() => {
        setIsLoading(false);
      });
  };

  return (
    <div className="space-y-8">
      {/* Header with gradient accent */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-br from-orange-500 to-purple-600 rounded-2xl blur-lg opacity-50 animate-pulse"></div>
            <div className="relative bg-gradient-to-br from-orange-500 to-purple-600 p-3 rounded-2xl">
              <MessageSquare className="h-7 w-7 text-white" />
            </div>
          </div>
          <div>
            <h2 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-orange-500 to-purple-600 bg-clip-text text-transparent">
              AI Chat Assistant
            </h2>
            <p className="text-sm text-muted-foreground flex items-center gap-1.5 mt-1">
              <Sparkles className="h-3.5 w-3.5" />
              Powered by Google Gemini & LangGraph
            </p>
          </div>
        </div>
        <Badge variant="secondary" className="text-sm px-4 py-2 bg-emerald-500/10 text-emerald-600 border-emerald-500/20">
          <span className="relative flex h-2 w-2 mr-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          AI Agent Active
        </Badge>
      </div>

      {/* Chat Messages with modern card */}
      <Card className="h-[600px] flex flex-col shadow-xl border-0 bg-gradient-to-b from-card to-card/50 backdrop-blur">
        <CardContent className="flex-1 overflow-y-auto p-8 space-y-8">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500 ${
                message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
              }`}
            >
              <div
                className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
                  message.role === 'user'
                    ? 'bg-gradient-to-br from-orange-500 to-orange-600'
                    : 'bg-gradient-to-br from-purple-500 to-purple-600'
                }`}
              >
                {message.role === 'user' ? (
                  <User className="h-5 w-5 text-white" />
                ) : (
                  <Bot className="h-5 w-5 text-white" />
                )}
              </div>
              <div
                className={`flex-1 rounded-2xl p-5 shadow-md transition-all hover:shadow-lg max-w-[85%] ${
                  message.role === 'user'
                    ? 'bg-gradient-to-br from-orange-500 to-orange-600 text-white'
                    : 'bg-gradient-to-br from-muted to-muted/50 border border-border/50'
                }`}
              >
                <div className="text-sm leading-relaxed">
                  {message.role === 'assistant' ? formatMessage(message.content) : message.content}
                </div>
                {/* Timestamp hidden for now */}
                {/* <div className={`text-xs mt-3 flex items-center gap-1 ${
                  message.role === 'user' ? 'opacity-80' : 'opacity-60'
                }`}>
                  <span className="w-1 h-1 rounded-full bg-current"></span>
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div> */}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex gap-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-purple-600 flex items-center justify-center shadow-lg">
                <Bot className="h-5 w-5 text-white" />
              </div>
              <div className="flex-1 rounded-2xl p-5 bg-gradient-to-br from-muted to-muted/50 border border-border/50 shadow-md max-w-[85%]">
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-purple-600" />
                  <span className="text-sm">AI is analyzing your request...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </CardContent>
        <div className="border-t p-6 bg-gradient-to-r from-orange-500/5 to-purple-600/5 backdrop-blur">
          {/* Dynamic Recommendations */}
          {recommendations.length > 0 && (
            <div className="mb-4">
              <p className="text-xs font-medium text-muted-foreground mb-3 flex items-center gap-1.5">
                <Sparkles className="h-3.5 w-3.5 text-orange-500" />
                Suggested follow-ups
              </p>
              <div className="flex flex-wrap gap-2.5">
                {recommendations.map((recommendation, index) => (
                  <Button
                    key={index}
                    variant="default"
                    size="sm"
                    onClick={() => handleRecommendationClick(recommendation)}
                    className="text-xs bg-gradient-to-br from-orange-500 to-purple-600 text-white hover:from-orange-600 hover:to-purple-700 transition-all duration-300 shadow-sm hover:shadow-md border-0"
                    disabled={isLoading}
                  >
                    {recommendation}
                  </Button>
                ))}
              </div>
            </div>
          )}
          
          {/* Input Field with modern styling */}
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about plant operations, get insights, or request analysis..."
                disabled={isLoading}
                className="pr-4 py-6 shadow-md border border-border/30 bg-muted/30 focus-visible:ring-2 focus-visible:ring-orange-500 focus-visible:border-orange-500 focus-visible:bg-background transition-all"
              />
            </div>
            <Button
              onClick={handleSend}
              disabled={isLoading || !input.trim()}
              size="icon"
              className="h-auto w-12 bg-gradient-to-br from-orange-500 to-purple-600 hover:from-orange-600 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all duration-300"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </Button>
          </div>
          <p className="text-xs text-muted-foreground mt-3 flex items-center gap-1.5">
            <Sparkles className="h-3 w-3 text-purple-500" />
            Powered by Google Gemini 2.0 • Press Enter to send
          </p>
        </div>
      </Card>

      {/* AI Capabilities with enhanced cards */}
      <div className="grid gap-6 md:grid-cols-3">
        <Card className="border-0 shadow-lg bg-gradient-to-br from-orange-500/10 to-orange-600/5 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <span className="text-2xl">🔍</span>
              <span className="bg-gradient-to-r from-orange-500 to-orange-600 bg-clip-text text-transparent font-bold">
                Real-time Analysis
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="text-xs text-muted-foreground leading-relaxed">
            Access live plant data, calculate KPIs, and identify trends across all operations
          </CardContent>
        </Card>
        <Card className="border-0 shadow-lg bg-gradient-to-br from-purple-500/10 to-purple-600/5 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <span className="text-2xl">🎯</span>
              <span className="bg-gradient-to-r from-purple-500 to-purple-600 bg-clip-text text-transparent font-bold">
                Smart Recommendations
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="text-xs text-muted-foreground leading-relaxed">
            AI-powered optimization suggestions with estimated savings and implementation guidance
          </CardContent>
        </Card>
        <Card className="border-0 shadow-lg bg-gradient-to-br from-emerald-500/10 to-emerald-600/5 hover:shadow-xl transition-all duration-300 hover:scale-105">
          <CardHeader>
            <CardTitle className="text-sm flex items-center gap-2">
              <span className="text-2xl">📊</span>
              <span className="bg-gradient-to-r from-emerald-500 to-emerald-600 bg-clip-text text-transparent font-bold">
                Predictive Insights
              </span>
            </CardTitle>
          </CardHeader>
          <CardContent className="text-xs text-muted-foreground leading-relaxed">
            Forecast quality issues, predict maintenance needs, and optimize resource allocation
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
