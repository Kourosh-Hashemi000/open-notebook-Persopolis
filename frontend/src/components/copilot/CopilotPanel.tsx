import { useEffect, useMemo, useState, useRef, type ChangeEvent, type FormEvent, type KeyboardEvent } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Loader2, Sparkles, Wand2, Check, X, Copy, RotateCcw, Plus, History, Settings, MoreHorizontal, Maximize2, Paperclip, Send, ChevronDown, MessageSquare, Trash2, Edit3, PanelLeftClose, PanelLeftOpen } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { apiClient } from '@/lib/api-client';
import type { AskResponse, ContextResponse, DefaultModelsResponse } from '@/types/api';

type CopilotMode = 'ask' | 'edit' | 'suggest';

type CopilotMessage = {
  id: string;
  role: 'user' | 'assistant';
  mode: CopilotMode;
  content: string;
  createdAt: string;
};

type CopilotSuggestion = {
  id: string;
  text: string;
  isVisible: boolean;
  isAccepted: boolean;
  isRejected: boolean;
};

type Conversation = {
  id: string;
  title: string;
  messages: CopilotMessage[];
  created: string;
  updated: string;
};

const buildContextSummary = (context?: ContextResponse) => {
  if (!context) return 'No additional notebook context provided.';
  const sources = context.sources?.slice(0, 5) ?? [];
  const notes = context.notes?.slice(0, 5) ?? [];
  const sourcesText = sources
    .map((source, index) => `(${index + 1}) ${JSON.stringify(source)}`)
    .join('\n');
  const notesText = notes
    .map((note, index) => `(${index + 1}) ${JSON.stringify(note)}`)
    .join('\n');

  return `Sources:\n${sourcesText}\n\nNotes:\n${notesText}`;
};

interface CopilotPanelProps {
  notebookId: string;
  draft: string;
  onDraftUpdate?: (markdown: string) => void;
  context?: ContextResponse;
}

const CopilotPanel = ({ notebookId, draft, onDraftUpdate, context }: CopilotPanelProps) => {
  const [mode, setMode] = useState<CopilotMode>('ask');
  const [prompt, setPrompt] = useState('');
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [currentConversationId, setCurrentConversationId] = useState<string | null>(null);
  const [suggestion, setSuggestion] = useState<CopilotSuggestion | null>(null);
  const [isGeneratingSuggestion, setIsGeneratingSuggestion] = useState(false);
  const [isEditingTitle, setIsEditingTitle] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState('');
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Get current conversation
  const currentConversation = conversations.find(c => c.id === currentConversationId);
  
  // Load messages for current conversation only
  // COMMENTED OUT FOR LOCAL-ONLY MODE
  // const messagesQuery = useQuery({
  //   queryKey: ['messages', currentConversationId],
  //   queryFn: () => apiClient.get_chat_session(currentConversationId!),
  //   enabled: !!currentConversationId,
  //   staleTime: 2 * 60 * 1000, // 2 minutes
  //   gcTime: 5 * 60 * 1000, // 5 minutes
  // });

  // const messages = (messagesQuery.data as any)?.messages || [];
  
  // Use local messages instead
  const messages = currentConversation?.messages || [];

  // Load conversations from database (without messages for performance)
  // COMMENTED OUT FOR LOCAL-ONLY MODE
  // const conversationsQuery = useQuery({
  //   queryKey: ['conversations', notebookId],
  //   queryFn: () => apiClient.get_chat_sessions(notebookId),
  //   enabled: !!notebookId,
  //   refetchOnWindowFocus: false,
  //   staleTime: 5 * 60 * 1000, // 5 minutes
  //   gcTime: 10 * 60 * 1000, // 10 minutes
  // });

  // Update local conversations when data loads
  // COMMENTED OUT FOR LOCAL-ONLY MODE
  // useEffect(() => {
  //   if (conversationsQuery.data) {
  //     const dbConversations = (conversationsQuery.data as any[]).map((conv: any) => ({
  //       id: conv.id,
  //       title: conv.title,
  //       messages: [], // Don't load messages in list view
  //       created: conv.created,
  //       updated: conv.updated,
  //     }));
  //     setConversations(dbConversations);
      
  //     // If no current conversation is selected and we have conversations, select the first one
  //     if (!currentConversationId && dbConversations.length > 0) {
  //       setCurrentConversationId(dbConversations[0].id);
  //     }
  //   }
  // }, [conversationsQuery.data, currentConversationId]);

  useEffect(() => {
    setPrompt('');
  }, [mode]);

  // Conversation management functions
  const createNewConversation = async () => {
    // COMMENTED OUT FOR LOCAL-ONLY MODE
    // try {
    //   const response = await apiClient.create_chat_session(notebookId, 'New Chat');
    //   const newConversation: Conversation = {
    //     id: response.id,
    //     title: response.title,
    //     messages: [],
    //     created: response.created,
    //     updated: response.updated,
    //   };
      
    //   // Update local state immediately
    //   setConversations(prev => [newConversation, ...prev]);
    //   setCurrentConversationId(newConversation.id);
    // } catch (error) {
    //   console.error('Failed to create conversation:', error);
    // }
    
    // LOCAL-ONLY MODE: Create conversation in local state only
    const newConversation: Conversation = {
      id: `conv-${Date.now()}`,
      title: 'New Chat',
      messages: [],
      created: new Date().toISOString(),
      updated: new Date().toISOString(),
    };
    setConversations(prev => [newConversation, ...prev]);
    setCurrentConversationId(newConversation.id);
  };

  const deleteConversation = async (conversationId: string) => {
    // COMMENTED OUT FOR LOCAL-ONLY MODE
    // try {
    //   await apiClient.delete_chat_session(conversationId);
    //   setConversations(prev => prev.filter(c => c.id !== conversationId));
    //   if (currentConversationId === conversationId) {
    //     const remaining = conversations.filter(c => c.id !== conversationId);
    //     setCurrentConversationId(remaining.length > 0 ? remaining[0].id : null);
    //   }
    // } catch (error) {
    //   console.error('Failed to delete conversation:', error);
    // }
    
    // LOCAL-ONLY MODE: Delete from local state only
    setConversations(prev => prev.filter(c => c.id !== conversationId));
    if (currentConversationId === conversationId) {
      const remaining = conversations.filter(c => c.id !== conversationId);
      setCurrentConversationId(remaining.length > 0 ? remaining[0].id : null);
    }
  };

  const updateConversationTitle = async (conversationId: string, newTitle: string) => {
    // COMMENTED OUT FOR LOCAL-ONLY MODE
    // try {
    //   await apiClient.update_chat_session(conversationId, newTitle);
    //   setConversations(prev =>
    //     prev.map(c =>
    //       c.id === conversationId
    //         ? { ...c, title: newTitle, updated: new Date().toISOString() }
    //         : c
    //     )
    //   );
    //   setIsEditingTitle(null);
    //   setEditingTitle('');
    // } catch (error) {
    //   console.error('Failed to update conversation title:', error);
    // }
    
    // LOCAL-ONLY MODE: Update title in local state only
    setConversations(prev =>
      prev.map(c =>
        c.id === conversationId
          ? { ...c, title: newTitle, updated: new Date().toISOString() }
          : c
      )
    );
    setIsEditingTitle(null);
    setEditingTitle('');
  };

  const startEditingTitle = (conversationId: string, currentTitle: string) => {
    setIsEditingTitle(conversationId);
    setEditingTitle(currentTitle);
  };

  const generateConversationTitle = (firstMessage: string) => {
    // Simple title generation - take first 30 characters
    return firstMessage.length > 30 
      ? firstMessage.substring(0, 30) + '...' 
      : firstMessage;
  };

  const defaultsQuery = useQuery<DefaultModelsResponse>({
    queryKey: ['model-defaults'],
    queryFn: () => apiClient.getDefaults(),
  });

  const defaultModels = defaultsQuery.data;
  const chatModelId = defaultModels?.default_chat_model ?? null;

  const contextSummary = useMemo(() => buildContextSummary(context), [context]);

  // VS Code Copilot-like suggestion generation
  const generateSuggestion = async (currentText: string) => {
    if (!chatModelId || isGeneratingSuggestion) return;
    
    setIsGeneratingSuggestion(true);
    try {
      const suggestionPrompt = `Based on the current notebook draft and context, suggest the next logical continuation. Return only the suggested text without any explanation or formatting.

Current draft:
${currentText}

Context:
${contextSummary}

Suggest the next few lines or paragraph:`;

      const response = await apiClient.ask({
        question: suggestionPrompt,
        strategy_model: chatModelId,
        answer_model: chatModelId,
        final_answer_model: chatModelId,
      });

      if (response.answer.trim()) {
        setSuggestion({
          id: `suggestion-${Date.now()}`,
          text: response.answer.trim(),
          isVisible: true,
          isAccepted: false,
          isRejected: false,
        });
      }
    } catch (error) {
      console.error('Failed to generate suggestion:', error);
    } finally {
      setIsGeneratingSuggestion(false);
    }
  };

  const acceptSuggestion = () => {
    if (suggestion && onDraftUpdate) {
      const newDraft = draft + suggestion.text;
      onDraftUpdate(newDraft);
      setSuggestion(null);
    }
  };

  const rejectSuggestion = () => {
    setSuggestion(null);
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Tab' && suggestion?.isVisible) {
      event.preventDefault();
      acceptSuggestion();
    } else if (event.key === 'Escape' && suggestion?.isVisible) {
      event.preventDefault();
      rejectSuggestion();
    } else if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
      event.preventDefault(); 
      generateSuggestion(prompt);
    }
  };
// theres a bug in there 
  const askMutation = useMutation<AskResponse, Error, { prompt: string; mode: CopilotMode }>({
    mutationFn: async ({ prompt: promptText, mode: activeMode }) => {
      if (!chatModelId) {
        throw new Error('Configure a default chat model in settings.');
      }

      const baseQuestion =
        activeMode === 'ask'
          ? `You are assisting with research for notebook ${notebookId}. Answer the question using the draft and context when relevant.\n\nQuestion: ${promptText}\n\nCurrent draft markdown:\n${draft}\n\nNotebook context:\n${contextSummary}`
          : `You are an expert editor rewriting the notebook draft based on the instructions below.\n\nINSTRUCTIONS:\n${promptText}\n\nRewrite the draft and return ONLY the revised markdown, without commentary.\n\n---\n${draft}`;

      return apiClient.ask({
        question: baseQuestion,
        strategy_model: chatModelId,
        answer_model: chatModelId,
        final_answer_model: chatModelId,
      });
    },
            onSuccess: async (response, variables) => {
              const assistantMessage: CopilotMessage = {
                id: `${Date.now()}-assistant`,
                role: 'assistant',
                mode: variables.mode,
                content: response.answer,
                createdAt: new Date().toISOString(),
              };

              // Save assistant message to database
              // COMMENTED OUT FOR LOCAL-ONLY MODE
              // if (currentConversationId) {
              //   try {
              //     await apiClient.add_message_to_session(
              //       currentConversationId,
              //       'assistant',
              //       variables.mode,
              //       response.answer
              //     );
              //   } catch (error) {
              //     console.error('Failed to save assistant message:', error);
              //   }

              //   // Invalidate messages query to refetch
              //   messagesQuery.refetch();

              // LOCAL-ONLY MODE: Add assistant message to local state
              if (currentConversationId) {
                setConversations(prev =>
                  prev.map(conv =>
                    conv.id === currentConversationId
                      ? {
                          ...conv,
                          messages: [...conv.messages, assistantMessage],
                          updated: new Date().toISOString(),
                          // Update title if this is the first message
                          title: conv.messages.length === 0 && conv.title === 'New Chat'
                            ? generateConversationTitle(variables.prompt)
                            : conv.title
                        }
                      : conv
                  )
                );
              }

              if (variables.mode === 'edit' && onDraftUpdate) {
                onDraftUpdate(response.answer);
              }
              setPrompt('');
            },
    onError: (error, variables) => {
      const message = error instanceof Error ? error.message : 'Copilot request failed.';
      const errorMessage: CopilotMessage = {
        id: `${Date.now()}-assistant-error`,
        role: 'assistant',
        mode: variables.mode,
        content: `⚠️ ${message}`,
        createdAt: new Date().toISOString(),
      };

      // Update current conversation with error
      if (currentConversationId) {
        setConversations(prev => 
          prev.map(conv => 
            conv.id === currentConversationId 
              ? { 
                  ...conv, 
                  messages: [...conv.messages, errorMessage],
                  updated: new Date().toISOString()
                }
              : conv
          )
        );
      }
    },
  });

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!prompt.trim()) return;

    // Create new conversation if none exists
    if (!currentConversationId) {
      await createNewConversation();
    }

    const userMessage: CopilotMessage = {
      id: `${Date.now()}-user`,
      role: 'user',
      mode,
      content: prompt.trim(),
      createdAt: new Date().toISOString(),
    };

    // Save user message to database
    // COMMENTED OUT FOR LOCAL-ONLY MODE
    // if (currentConversationId) {
    //   try {
    //     await apiClient.add_message_to_session(
    //       currentConversationId,
    //       'user',
    //       mode,
    //       prompt.trim()
    //     );
    //   } catch (error) {
    //     console.error('Failed to save user message:', error);
    //   }

    //   // Invalidate messages query to refetch
    //   messagesQuery.refetch();
    // }

    // LOCAL-ONLY MODE: Add user message to local state
    if (currentConversationId) {
      setConversations(prev =>
        prev.map(conv =>
          conv.id === currentConversationId
            ? {
                ...conv,
                messages: [...conv.messages, userMessage],
                updated: new Date().toISOString()
              }
            : conv
        )
      );
    }

    askMutation.mutate({ prompt: prompt.trim(), mode });
  };

  const handlePromptChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setPrompt(event.target.value);
  };

  return (
    <div className="relative h-full bg-background text-foreground overflow-hidden">
      {/* History Sidebar - Overlay */}
      <div className={`absolute left-0 top-0 h-full z-10 ${isSidebarCollapsed ? 'w-0' : 'w-64'} bg-card border-r border-border flex flex-col transition-all duration-300 overflow-hidden shadow-lg`}>
        {/* Sidebar Header */}
        <div className="p-3 border-b border-border">
          <div className="flex items-center justify-between gap-2">
            <Button 
              onClick={createNewConversation}
              className="flex-1"
            >
              <Plus className="h-4 w-4 mr-2" />
              New Chat
            </Button>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"
              onClick={() => setIsSidebarCollapsed(true)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Conversations List */}
        <ScrollArea className="flex-1 p-2">
          <div className="space-y-1">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={`group relative rounded-md p-2 cursor-pointer transition-colors ${
                  currentConversationId === conversation.id
                    ? 'bg-accent border border-primary'
                    : 'hover:bg-accent'
                }`}
                onClick={() => setCurrentConversationId(conversation.id)}
              >
                <div className="flex items-center gap-2 min-w-0">
                  <MessageSquare className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    {isEditingTitle === conversation.id ? (
                      <input
                        type="text"
                        value={editingTitle}
                        onChange={(e) => setEditingTitle(e.target.value)}
                        onBlur={() => updateConversationTitle(conversation.id, editingTitle)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            updateConversationTitle(conversation.id, editingTitle);
                          } else if (e.key === 'Escape') {
                            setIsEditingTitle(null);
                            setEditingTitle('');
                          }
                        }}
                        className="w-full bg-transparent text-foreground text-sm border-none outline-none"
                        autoFocus
                      />
                    ) : (
                      <div
                        className="text-sm text-foreground truncate"
                        onDoubleClick={() => startEditingTitle(conversation.id, conversation.title)}
                      >
                        {conversation.title}
                      </div>
                    )}
                    <div className="text-xs text-muted-foreground">
                      {new Date(conversation.updated).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                
                {/* Delete Button */}
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute right-1 top-1 h-6 w-6 p-0 opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-foreground hover:bg-muted"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversation(conversation.id);
                  }}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            ))}
          </div>
        </ScrollArea>
      </div>

      {/* Backdrop for sidebar overlay */}
      {!isSidebarCollapsed && (
        <div 
          className="absolute inset-0 bg-black/20 z-5"
          onClick={() => setIsSidebarCollapsed(true)}
        />
      )}

      {/* Floating toggle button when sidebar is collapsed */}
      {isSidebarCollapsed && (
        <Button
          variant="ghost"
          size="sm"
          className="absolute left-4 top-4 z-20 h-6 w-6 p-0 text-muted-foreground hover:text-foreground hover:bg-muted"
          onClick={() => setIsSidebarCollapsed(false)}
        >
          <PanelLeftOpen className="h-3 w-3" />
        </Button>
      )}

      {/* Main Chat Area */}
      <div className="w-full h-full flex flex-col">
        {/* Header Bar */}
        <div className="flex items-center justify-between border-b border-border px-4 py-3 flex-shrink-0">
          <div className="flex-1"></div>
          <div className="flex items-center gap-2 min-w-0">
            <span className="text-sm font-medium text-foreground whitespace-nowrap">
              {currentConversation?.title || 'New Chat'}
            </span>
          </div>
          <div className="flex items-center gap-1 flex-shrink-0">
            <Button variant="ghost" size="sm" className="h-6 w-6 p-0 text-muted-foreground hover:text-foreground hover:bg-muted">
              <Settings className="h-3 w-3" />
            </Button>
          </div>
        </div>

        {/* Chat Content */}
        <div className="flex-1 flex flex-col">
          {messages.length === 0 ? (
            /* Welcome Screen */
            <div className="flex-1 flex flex-col items-center justify-center px-6 text-center overflow-hidden">
              <div className="max-w-md w-full">
                <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-muted">
                  <Sparkles className="h-8 w-8 text-foreground" />
                </div>
                <h2 className="text-xl font-semibold text-foreground mb-2 leading-tight">AI Copilot</h2>
                <p className="text-sm text-muted-foreground mb-6 leading-relaxed">Ask questions or generate edits powered by your research.</p>
                <Button
                  variant="link"
                  className="p-0 h-auto text-sm leading-relaxed break-words"
                  onClick={() => setPrompt("What insights can you provide about my research?")}
                >
                  What insights can you provide about my research?
                </Button>
              </div>
            </div>
          ) : (
            /* Chat Messages */
            <ScrollArea className="flex-1 px-4 py-4 overflow-hidden">
              <div className="space-y-4 max-w-full">
                {messages.map((message: any) => (
                  <div key={message.id} className="flex gap-3 max-w-full">
                    <div className="flex-shrink-0">
                      {message.role === 'user' ? (
                        <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
                          <span className="text-xs font-medium text-primary-foreground">U</span>
                        </div>
                      ) : (
                        <div className="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
                          <Sparkles className="h-4 w-4 text-foreground" />
                        </div>
                      )}
                    </div>
                    <div className="flex-1 min-w-0 max-w-full">
                      <div className="text-sm text-muted-foreground mb-1 truncate">
                        {message.role === 'user' ? 'You' : 'Copilot'} · {message.mode}
                      </div>
                      <div className="text-foreground whitespace-pre-wrap leading-relaxed break-words max-w-full">
                        {message.content}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </ScrollArea>
          )}

          {/* Input Area */}
          <div className="border-t border-border p-4 flex-shrink-0">
            <Tabs value={mode} onValueChange={(value) => setMode(value as CopilotMode)}>
              <TabsList className="grid w-full grid-cols-2 mb-3">
                <TabsTrigger value="ask" className="gap-1 text-xs">
                  <Sparkles className="h-4 w-4" /> Ask
                </TabsTrigger>
                <TabsTrigger value="edit" className="gap-1 text-xs">
                  <Wand2 className="h-4 w-4" /> Edit
                </TabsTrigger>
              </TabsList>
              <TabsContent value="ask" className="mt-0">
                <form className="space-y-3" onSubmit={handleSubmit}>
                          <Textarea
                            ref={textareaRef}
                            placeholder="What do you want to know about your research?"
                            value={prompt}
                            onChange={handlePromptChange}
                            onKeyDown={handleKeyDown}
                            rows={3}
                            className="resize-none"
                            disabled={askMutation.isPending || !chatModelId}
                          />
                  <Button 
                    type="submit" 
                    className="w-full"
                    disabled={askMutation.isPending || !prompt.trim() || !chatModelId}
                  >
                    {askMutation.isPending ? (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Sparkles className="mr-2 h-4 w-4" />
                    )}
                    Ask Copilot
                  </Button>
                </form>
              </TabsContent>
              <TabsContent value="edit" className="mt-0">
                <form className="space-y-3" onSubmit={handleSubmit}>
                          <Textarea
                            ref={textareaRef}
                            placeholder="Describe the edits to apply to your draft..."
                            value={prompt}
                            onChange={handlePromptChange}
                            onKeyDown={handleKeyDown}
                            rows={3}
                            className="resize-none"
                            disabled={askMutation.isPending || !chatModelId}
                          />
                  <Button 
                    type="submit" 
                    className="w-full"
                    disabled={askMutation.isPending || !prompt.trim() || !chatModelId}
                  >
                    {askMutation.isPending ? (
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Wand2 className="mr-2 h-4 w-4" />
                    )}
                    Generate Edits
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CopilotPanel;
