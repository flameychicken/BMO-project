import React, { useState, useEffect, useRef } from 'react'
import ChatBubble from './components/ChatBubble'
import Loader from './components/Loader'

const API_BASE = "http://localhost:8000"

export default function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [bmoMood, setBmoMood] = useState("happy")
  const bottomRef = useRef(null)

  useEffect(() => {
    checkStatus()
  }, [])

  const checkStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/chat/status`)
      const data = await res.json()
      if (!data.ready) {
        alert("BMO is not ready yet!")
      }
    } catch (err) {
      alert("Error connecting to BMO backend.")
    }
  }

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = input.trim()
    setMessages(prev => [...prev, { sender: "user", text: userMessage }])
    setInput("")
    setLoading(true)

    try {
      const res = await fetch(`${API_BASE}/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: userMessage })
      })

      const data = await res.json()
      setMessages(prev => [...prev, { sender: "bmo", text: data.response }])
      setBmoMood(data.bmo_mood || "happy")
    } catch (err) {
      setMessages(prev => [...prev, { sender: "bmo", text: "Oops! BMO had a glitch!" }])
    } finally {
      setLoading(false)
      scrollToBottom()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage()
  }

  const scrollToBottom = () => {
    setTimeout(() => {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, 100)
  }

  const resetConversation = async () => {
    await fetch(`${API_BASE}/chat/reset`, { method: "POST" })
    setMessages([])
    setBmoMood("happy")
  }

  return (
    <div className="chat-container">
      <h1 className="header">BMO Chat</h1>
      <div className="mood">Mood: <strong>{bmoMood}</strong></div>
      <div className="chat-box">
        {messages.map((msg, idx) => (
          <ChatBubble key={idx} sender={msg.sender} text={msg.text} />
        ))}
        {loading && <Loader />}
        <div ref={bottomRef}></div>
      </div>
      <div className="input-bar">
        <input
          type="text"
          placeholder="Say something to BMO..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={sendMessage}>Send</button>
        <button className="reset-btn" onClick={resetConversation}>Reset</button>
      </div>
    </div>
  )
}
