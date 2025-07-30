import { useState, useEffect, useRef } from 'react';
import BMOExcited from './assets/BMOExcited.png';
import BMOHappy from './assets/BMOHappy.png';
import BMOCaring from './assets/BmoCaring.png';
import BMOCurious from './assets/BmoCurious.png';
import BMORight from './assets/BMORight.png';
import BMOLeft from './assets/BMOLeft.png';

export default function BMO() {
  const [currentMessage, setCurrentMessage] = useState('');
  const [bmoMood, setBmoMood] = useState('happy');
  const [chatHistory, setChatHistory] = useState(() => {
    const savedHistory = localStorage.getItem('bmoChatHistory');
    return savedHistory
      ? JSON.parse(savedHistory).map(msg => ({
          ...msg,
          timestamp: msg.timestamp ? new Date(msg.timestamp) : new Date()
        }))
      : [{ author: 'bmo', text: "Hello! I am BMO. What's on your mind?", timestamp: new Date() }];
  });

  // State to track if BMO is "thinking" (waiting for API response)
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  useEffect(() => {
    localStorage.setItem('bmoChatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!currentMessage.trim()) return;

    const userMessage = { 
      author: 'user', 
      text: currentMessage,
      timestamp: new Date()
    };
    setChatHistory(prev => [...prev, userMessage]);
    const userInput = currentMessage;
    setCurrentMessage('');
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: userInput,
          max_tokens: 150,           
          temperature: 0.8,            
          reset_conversation: false   
        })
      });

      const data = await res.json();
      const bmoReply = {
        author: 'bmo',
        text: data.response || "Hmm, I didn't catch that!",
        timestamp: new Date()
      };
      setChatHistory(prev => [...prev, bmoReply]);

      if (data.bmo_mood) {
        setBmoMood(data.bmo_mood);
      }
      
    } catch (err) {
      console.error(err);
      setChatHistory(prev => [...prev, { 
        author: 'bmo', 
        text: "Error talking to BMO!",
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetChat = async () => {
    try {
      const res = await fetch("http://localhost:8000/chat/reset", {
        method: "POST"
      });
      const data = await res.json();
      const resetMessage = { 
        author: 'bmo', 
        text: data.message,
        timestamp: new Date()
      };
      setChatHistory([resetMessage]);
      localStorage.removeItem('bmoChatHistory');
      setBmoMood('happy');
    } catch (err) {
      console.error(err);
      setChatHistory([{ 
        author: 'bmo', 
        text: "Error resetting BMO!",
        timestamp: new Date()
      }]);
    }
  };

  const getBmoFace = () => {
    switch (bmoMood) {
      case 'curious':
        return BMOCurious;
      case 'caring':
        return BMOCaring;
      case 'excited':
        return BMOExcited;
      case 'happy':
      default:
        return BMOHappy;
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="modern-chat-container">
      {/* Sidebar with BMO */}
      <div className="chat-sidebar">
        {/* Header */}
        <div className="sidebar-header">
          <div className="header-content">
            <span className="header-icon"></span>
            <h1 className="header-title">Chat with BMO</h1>
          </div>
        </div>

        {/* BMO Face Card */}
        <div className="bmo-card-container">
          <div className="bmo-card">
            <div className="bmo-face-container">
              <div className="bmo-face">
                <img 
                  src={getBmoFace()} 
                  alt={`BMO's ${bmoMood} face`}
                  className="bmo-face-img"
                />
              </div>
              <h2 className="bmo-name">BMO</h2>
              <p className="bmo-mood">
                Feeling {bmoMood}
              </p>
            </div>
          </div>
        </div>

        {/* BMO Side Buttons */}
        <div className="bmo-buttons">
          <div className="bmo-button">
            <img 
              src={BMOLeft} 
              alt="BMO Left buttons" 
              className="button-img"
            />
          </div>
          <div className="bmo-button">
            <img 
              src={BMORight} 
              alt="BMO Right buttons" 
              className="button-img"
            />
          </div>
        </div>

        {/* Controls */}
        <div className="sidebar-controls">
          <button onClick={resetChat} className="reset-button">
            <span className="reset-icon">↻</span>
            Reset Conversation
          </button>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="chat-main">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="chat-header-content">
            <div className="chat-avatar">
              <img 
                src={getBmoFace()} 
                alt="BMO" 
                className="avatar-img"
              />
            </div>
            <div className="chat-info">
              <h2 className="chat-title">BMO Assistant</h2>
              <p className="chat-status">
                {isLoading ? 'BMO is thinking...' : 'Online'}
              </p>
            </div>
          </div>
        </div>

        {/* Messages */}
        <div className="chat-content">
          <div className="messages-container">
            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`message ${msg.author === 'user' ? 'user-message' : 'bmo-message'}`}>
                <div className="message-bubble">
                  <p className="message-text">{msg.text}</p>
                  <p className="message-time">
                    {formatTime(msg.timestamp)}
                  </p>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message bmo-message">
                <div className="message-bubble">
                  <div className="thinking-indicator">
                    <div className="thinking-dots">
                      <div className="dot"></div>
                      <div className="dot"></div>
                      <div className="dot"></div>
                    </div>
                    <span className="thinking-text">beep boop... thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <div className="chat-input-container">
            <div className="chat-input-form">
              <input
                type="text"
                value={currentMessage}
                onChange={(e) => setCurrentMessage(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSubmit(e);
                  }
                }}
                placeholder="Type your message..."
                disabled={isLoading}
                className="message-input"
              />
              <button
                onClick={handleSubmit}
                disabled={isLoading || !currentMessage.trim()}
                className="send-button"
              >
                {isLoading ? (
                  <div className="loading-spinner"></div>
                ) : (
                  <span className="send-icon">→</span>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}