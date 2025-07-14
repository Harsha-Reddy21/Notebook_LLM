import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  Box, 
  Typography, 
  Paper, 
  TextField, 
  Button, 
  Divider, 
  CircularProgress,
  Tabs,
  Tab
} from '@mui/material';
import { api } from '../services/api';

function DocumentView() {
  const { documentId } = useParams();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const [queryResult, setQueryResult] = useState(null);
  const [queryLoading, setQueryLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/documents/${documentId}`);
        setDocument(response.data);
      } catch (err) {
        setError('Failed to load document. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchDocument();
  }, [documentId]);

  const handleQuerySubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    try {
      setQueryLoading(true);
      const response = await api.post('/queries/', {
        query_text: query,
        document_id: parseInt(documentId),
        meta_data: {}
      });
      setQueryResult(response.data);
    } catch (err) {
      setError('Failed to process query. Please try again later.');
      console.error(err);
    } finally {
      setQueryLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ mt: 4 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ mt: 4 }}>
      {document && (
        <>
          <Typography variant="h4" gutterBottom>
            {document.title}
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            {document.description || 'No description provided'}
          </Typography>
          <Divider sx={{ my: 2 }} />
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
            <Tabs value={activeTab} onChange={handleTabChange}>
              <Tab label="Query Document" />
              <Tab label="Document Structure" />
            </Tabs>
          </Box>

          {activeTab === 0 && (
            <Box component="form" onSubmit={handleQuerySubmit} sx={{ mb: 4 }}>
              <TextField
                fullWidth
                label="Ask a question about this document"
                variant="outlined"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                sx={{ mb: 2 }}
              />
              <Button 
                type="submit" 
                variant="contained" 
                disabled={queryLoading}
              >
                {queryLoading ? <CircularProgress size={24} /> : 'Ask Question'}
              </Button>

              {queryResult && (
                <Paper sx={{ p: 3, mt: 3 }}>
                  <Typography variant="h6" gutterBottom>Answer</Typography>
                  <Typography paragraph>{queryResult.query.response}</Typography>
                  
                  {queryResult.citations && queryResult.citations.length > 0 && (
                    <>
                      <Typography variant="h6" gutterBottom>Sources</Typography>
                      {queryResult.citations.map((citation, index) => (
                        <Paper key={index} sx={{ p: 2, mb: 2, bgcolor: 'grey.100' }}>
                          <Typography variant="body2">{citation.content}</Typography>
                        </Paper>
                      ))}
                    </>
                  )}
                </Paper>
              )}
            </Box>
          )}

          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom>Document Information</Typography>
              <Paper sx={{ p: 3, mb: 3 }}>
                <Typography><strong>File Type:</strong> {document.file_type}</Typography>
                <Typography><strong>File Size:</strong> {Math.round(document.file_size / 1024)} KB</Typography>
                <Typography><strong>Uploaded:</strong> {new Date(document.created_at).toLocaleString()}</Typography>
              </Paper>
            </Box>
          )}
        </>
      )}
    </Box>
  );
}

export default DocumentView; 