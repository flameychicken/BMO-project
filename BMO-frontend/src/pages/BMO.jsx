import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import BMOFace from './assets/BMO-Face.png';
import BMORight from './assets/BMORight.png';
import BMOLeft from './assets/BMOLeft.png';

export default function BMO() {
    const [currentMessage, setCurrentMessage] = useState('');
    const [chatHistory, setChatHistory] = useState(() => {
    const savedHistory = localStorage.getItem('bmoChatHistory');
    return savedHistory
        ? JSON.parse(savedHistory)
        : [{ author: 'bmo', text: "Hello! I am BMO. What's on your mind?" }];
});
    // State to track if BMO is "thinking" (waiting for API response)
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
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

        const userMessage = { author: 'user', text: currentMessage };
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
                    max_tokens: 150,             // You can make this configurable if needed
                    temperature: 0.8,            // You can make this dynamic via UI controls
                    reset_conversation: false    // Set this to true if you want to support memory resets
                })
            });

            const data = await res.json();
            const bmoReply = {
                author: 'bmo',
                text: data.response || "Hmm, I didn't catch that!"
            };
            setChatHistory(prev => [...prev, bmoReply]);
        } catch (err) {
            console.error(err);
            setChatHistory(prev => [...prev, { author: 'bmo', text: "Error talking to BMO!" }]);
        } finally {
            setIsLoading(false);
        }
    };


    return (
        <div className='background'>
            <div className='imgContainer'>
                <img src={BMOFace} alt="BMO's Face"></img>
            </div>
            <div className='chatBot'>
                <div className='column'><div className='column'><img src={BMOLeft} alt="BMO Left buttons" style={{border: '0'}}></img></div></div>
                <div className='column'>
                    <div className='chat-display'>
                        <div className='chat-messages'>
                            {isLoading && (
                            <div className="chat-message bmo">
                                <p><strong>BMO:</strong>beep boop... thinking ...</p>
                            </div>
                        )}
                        {[...chatHistory].reverse().map((msg, idx) => (
                            <div key={idx} className={`chat-message ${msg.author}`}>
                                <p><strong>{msg.author === 'bmo' ? 'BMO' : 'You'}:</strong> {msg.text}</p>
                            </div>
                        ))}
                        
                        <div ref={messagesEndRef} />
                        </div>
                        <form onSubmit={handleSubmit} className='chat-input-form'>
                            <input 
                                type="text" 
                                value={currentMessage} 
                                onChange={(e) => setCurrentMessage(e.target.value)}
                                placeholder="Type your message..." 
                                disabled={isLoading}
                            />
                            <button 
                                type="submit" 
                                className='chat-input-form-button'
                                disabled={isLoading}
                            >
                                {isLoading ? '...' : 'Send'}
                            </button>
                            <button
                                type="button"
                                onClick={async () => {
                                    try {
                                        const res = await fetch("http://localhost:8000/chat/reset", {
                                            method: "POST"
                                        });
                                        const data = await res.json();
                                        const resetMessage = { author: 'bmo', text: data.message };
                                        setChatHistory([resetMessage]);
                                        localStorage.removeItem('bmoChatHistory');
                                    } catch (err) {
                                        console.error(err);
                                        setChatHistory([{ author: 'bmo', text: "Error resetting BMO!" }]);
                                    }
                                }}
                            >
                                Reset
                            </button>
                        </form>
                    </div>
                </div>
                <div className='column'><img src={BMORight} alt="BMO Right buttons" style={{border: '0'}}></img></div>
            </div>
        </div>
    );
}