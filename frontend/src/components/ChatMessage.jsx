import './ChatMessage.css'

function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  
  return (
    <div className={`message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-content">
        {!isUser && <div className="avatar">🤖</div>}
        <div className="message-bubble">
          <div className="message-text">
            {message.content.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </div>
        {isUser && <div className="avatar">👤</div>}
      </div>
    </div>
  )
}

export default ChatMessage
