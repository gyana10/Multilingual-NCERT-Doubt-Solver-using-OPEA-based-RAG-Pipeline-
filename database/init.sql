-- Database initialization for RAG NCERT System
-- Create schemas and tables for metadata, conversations, and feedback

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum types
CREATE TYPE grade_level AS ENUM ('5', '6', '7', '8', '9', '10');
CREATE TYPE subject_type AS ENUM ('mathematics', 'science', 'social_science', 'english', 'hindi', 'urdu', 'sanskrit', 'physical_education', 'ict', 'vocational_education');
CREATE TYPE language_code AS ENUM ('en', 'hi', 'ur', 'sa', 'unknown');
CREATE TYPE confidence_level AS ENUM ('high', 'medium', 'low', 'no_answer');

-- Table: chunk_metadata
-- Stores metadata for each text chunk from NCERT content
CREATE TABLE chunk_metadata (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chunk_id VARCHAR(255) UNIQUE NOT NULL,
    grade grade_level NOT NULL,
    subject subject_type NOT NULL,
    chapter VARCHAR(255),
    page_no INTEGER NOT NULL,
    source_file VARCHAR(255) NOT NULL,
    language language_code NOT NULL DEFAULT 'en',
    difficulty_level VARCHAR(50) DEFAULT 'basic',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: conversations
-- Stores user conversation sessions and context
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_grade grade_level,
    preferred_language language_code DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Table: conversation_messages
-- Stores individual messages within conversations
CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    message_type VARCHAR(20) NOT NULL CHECK (message_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    original_language language_code,
    translated_content TEXT,
    confidence_score DECIMAL(3,2),
    processing_time_ms INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: query_responses
-- Stores query-response pairs with retrieval details
CREATE TABLE query_responses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    message_id UUID REFERENCES conversation_messages(id) ON DELETE CASCADE,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    confidence_level confidence_level NOT NULL,
    processing_time_ms INTEGER,
    retrieved_chunks JSONB,  -- Array of chunk IDs and scores
    citations JSONB,         -- Citation information
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: user_feedback
-- Stores user feedback on responses
CREATE TABLE user_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    response_id UUID REFERENCES query_responses(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    feedback_type VARCHAR(50) CHECK (feedback_type IN ('helpful', 'incorrect', 'incomplete', 'irrelevant', 'excellent')),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: system_metrics
-- Stores system performance and usage metrics
CREATE TABLE system_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4),
    metric_unit VARCHAR(20),
    service_name VARCHAR(50),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table: content_processing_log
-- Logs for PDF processing and indexing operations
CREATE TABLE content_processing_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    operation_type VARCHAR(50) NOT NULL,  -- 'pdf_extraction', 'chunking', 'embedding', 'indexing'
    source_file VARCHAR(255) NOT NULL,
    grade grade_level,
    subject subject_type,
    status VARCHAR(20) NOT NULL DEFAULT 'processing',  -- 'processing', 'completed', 'failed'
    chunks_created INTEGER DEFAULT 0,
    processing_time_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance optimization
CREATE INDEX idx_chunk_metadata_grade_subject ON chunk_metadata(grade, subject);
CREATE INDEX idx_chunk_metadata_chunk_id ON chunk_metadata(chunk_id);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_conversations_last_activity ON conversations(last_activity);
CREATE INDEX idx_conversation_messages_conversation_id ON conversation_messages(conversation_id);
CREATE INDEX idx_conversation_messages_created_at ON conversation_messages(created_at);
CREATE INDEX idx_query_responses_conversation_id ON query_responses(conversation_id);
CREATE INDEX idx_query_responses_confidence_level ON query_responses(confidence_level);
CREATE INDEX idx_user_feedback_response_id ON user_feedback(response_id);
CREATE INDEX idx_user_feedback_rating ON user_feedback(rating);
CREATE INDEX idx_system_metrics_recorded_at ON system_metrics(recorded_at);
CREATE INDEX idx_system_metrics_service_name ON system_metrics(service_name);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER update_chunk_metadata_updated_at 
    BEFORE UPDATE ON chunk_metadata 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to clean up old conversation data
CREATE OR REPLACE FUNCTION cleanup_old_conversations()
RETURNS void AS $$
BEGIN
    -- Mark conversations inactive after 24 hours of inactivity
    UPDATE conversations 
    SET is_active = FALSE 
    WHERE last_activity < NOW() - INTERVAL '24 hours' 
    AND is_active = TRUE;
    
    -- Delete conversations and related data older than 30 days
    DELETE FROM conversations 
    WHERE created_at < NOW() - INTERVAL '30 days' 
    AND is_active = FALSE;
END;
$$ LANGUAGE plpgsql;

-- Insert sample data for testing
INSERT INTO chunk_metadata (chunk_id, grade, subject, chapter, page_no, source_file, language) VALUES
('class5__math__p1__c1', '5', 'mathematics', 'Numbers', 1, 'maths_class5.pdf', 'en'),
('class5__science__p15__c1', '5', 'science', 'Plants', 15, 'science_class5.pdf', 'en'),
('class6__math__p23__c1', '6', 'mathematics', 'Fractions', 23, 'maths_c6.pdf', 'en'),
('class10__science__p89__c1', '10', 'science', 'Life Processes', 89, 'science.pdf', 'en');

-- Create view for conversation statistics
CREATE VIEW conversation_stats AS
SELECT 
    DATE_TRUNC('day', created_at) as date,
    COUNT(*) as total_conversations,
    COUNT(CASE WHEN is_active THEN 1 END) as active_conversations,
    AVG(EXTRACT(EPOCH FROM (last_activity - created_at))) as avg_session_duration_seconds
FROM conversations 
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY date DESC;

-- Create view for feedback analytics
CREATE VIEW feedback_analytics AS
SELECT 
    DATE_TRUNC('day', uf.created_at) as date,
    AVG(uf.rating::DECIMAL) as avg_rating,
    COUNT(*) as total_feedback,
    COUNT(CASE WHEN uf.rating >= 4 THEN 1 END) as positive_feedback,
    COUNT(CASE WHEN uf.rating <= 2 THEN 1 END) as negative_feedback,
    qr.confidence_level,
    cm.grade
FROM user_feedback uf
JOIN query_responses qr ON uf.response_id = qr.id
JOIN conversation_messages cm_msg ON qr.message_id = cm_msg.id
JOIN conversations cm ON cm_msg.conversation_id = cm.id
GROUP BY DATE_TRUNC('day', uf.created_at), qr.confidence_level, cm.grade
ORDER BY date DESC;

COMMENT ON TABLE chunk_metadata IS 'Metadata for text chunks extracted from NCERT PDFs';
COMMENT ON TABLE conversations IS 'User conversation sessions with context and preferences';
COMMENT ON TABLE conversation_messages IS 'Individual messages within conversations';
COMMENT ON TABLE query_responses IS 'Query-response pairs with retrieval and citation details';
COMMENT ON TABLE user_feedback IS 'User feedback and ratings for system responses';
COMMENT ON TABLE system_metrics IS 'System performance and usage metrics';
COMMENT ON TABLE content_processing_log IS 'Logs for content processing operations';