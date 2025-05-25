import { useState, useEffect } from "react";

const STORAGE_KEY = "read_comments";

export function useReadComments() {
  const [readComments, setReadComments] = useState<Set<string>>(() => {
    // Initialize from localStorage
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? new Set(JSON.parse(stored)) : new Set();
  });

  // Save to localStorage whenever readComments changes
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...readComments]));
  }, [readComments]);

  const markAsRead = (commentId: string) => {
    setReadComments((prev) => new Set([...prev, commentId]));
  };

  const isRead = (commentId: string) => {
    return readComments.has(commentId);
  };

  return {
    markAsRead,
    isRead,
  };
}
