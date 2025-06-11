import React, { useState } from 'react';
import ChatBubble from '../components/ChatBubble';
import FileUpload from '../components/FileUpload';
import LanguageSelector from '../components/LanguageSelector';
import { sendQuestion } from '../api';

const TutorChat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isThinking, setIsThinking] = useState(false);

    const handleSend = async () => {
        if (!input) return;

        const userMessage = { text: input, type: 'user' };
        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsThinking(true);

        const response = await sendQuestion(input);
        setIsThinking(false);
        setMessages((prev) => [...prev, { text: response, type: 'bot' }]);
    };

    return (
        <div className="flex flex-col items-center p-4">
            <h1 className="text-xl font-bold mb-4">AI Tutor Chat</h1>
            <FileUpload />
            <LanguageSelector />
            <div className="w-full max-w-md mb-4">
                {messages.map((msg, index) => (
                    <ChatBubble key={index} message={msg} />
                ))}
                {isThinking && <ChatBubble message={{ text: 'Thinking...', type: 'bot' }} />}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="border w-full p-2"
                placeholder="Ask your AI tutor anything..."
            />
            <button onClick={handleSend} className="bg-blue-500 text-white px-4 py-2 mt-2">Send</button>
        </div>
    );
};

export default TutorChat;
