import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  List, 
  ListItem, 
  ListItemText, 
  Divider,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { api } from '../services/api';

function QueryHistory() {
  const [queries, setQueries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchQueries = async () => {
      try {
        setLoading(true);
        const response = await api.get('/queries/');
        setQueries(response.data.queries);
      } catch (err) {
        setError('Failed to load query history. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchQueries();
  }, []);

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
      <Typography variant="h4" gutterBottom>
        Query History
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        View your past queries and their results
      </Typography>
      <Divider sx={{ my: 2 }} />

      {queries.length === 0 ? (
        <Paper sx={{ p: 3, textAlign: 'center' }}>
          <Typography>No queries found. Try asking questions about your documents!</Typography>
        </Paper>
      ) : (
        <List>
          {queries.map((query) => (
            <Paper key={query.id} sx={{ mb: 2 }}>
              <Accordion>
                <AccordionSummary
                  expandIcon={<ExpandMoreIcon />}
                  aria-controls={`query-${query.id}-content`}
                  id={`query-${query.id}-header`}
                >
                  <Box sx={{ display: 'flex', flexDirection: 'column', width: '100%' }}>
                    <Typography variant="subtitle1">{query.query_text}</Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        {new Date(query.created_at).toLocaleString()}
                      </Typography>
                      {query.document_id && (
                        <Chip 
                          label={`Document #${query.document_id}`} 
                          size="small" 
                          color="primary" 
                          variant="outlined" 
                        />
                      )}
                    </Box>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="h6" gutterBottom>Answer</Typography>
                  <Typography paragraph>{query.response}</Typography>
                </AccordionDetails>
              </Accordion>
            </Paper>
          ))}
        </List>
      )}
    </Box>
  );
}

export default QueryHistory; 