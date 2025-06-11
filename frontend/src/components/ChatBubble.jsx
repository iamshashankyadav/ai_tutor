const ChatBubble = ({ message }) => {
    const isUser = message.type === 'user';
    return (
        <div className={`mb-2 p-2 rounded-lg ${isUser ? 'bg-blue-200' : 'bg-gray-300'} max-w-xs`}>
            <p>{message.text}</p>
        </div>
    );
};

export default ChatBubble;
