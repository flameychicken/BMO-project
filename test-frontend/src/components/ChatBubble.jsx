import React from 'react'

export default function ChatBubble({ sender, text }) {
  const isUser = sender === "user"
  return (
    <div className={`bubble-row ${isUser ? "user" : "bmo"}`}>
      <div className="bubble">{text}</div>
    </div>
  )
}
