import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  LinearProgress,
  Alert,
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { documentApi } from '../services/api';

const DocumentUpload = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/html': ['.html', '.htm'],
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/vnd.ms-powerpoint': ['.ppt'],
      'application/x-ipynb+json': ['.ipynb'],
      'image/*': ['.jpg', '.jpeg', '.png', '.gif'],
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0]);
        if (!title) {
          setTitle(acceptedFiles[0].name.split('.')[0]);
        }
      }
    },
    onDropRejected: (rejectedFiles) => {
      if (rejectedFiles[0].errors[0].code === 'file-too-large') {
        setError('File is too large. Maximum size is 50MB.');
      } else {
        setError('Invalid file type. Please upload a supported document format.');
      }
    },
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    if (!title.trim()) {
      setError('Please enter a title for the document.');
      return;
    }

    setError('');
    setUploading(true);
    setProgress(0);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    if (description.trim()) {
      formData.append('description', description);
    }

    try {
      // Simulate progress for better UX
      const progressInterval = setInterval(() => {
        setProgress((prevProgress) => {
          if (prevProgress >= 95) {
            clearInterval(progressInterval);
            return prevProgress;
          }
          return prevProgress + 5;
        });
      }, 500);

      const response = await documentApi.upload(formData);
      clearInterval(progressInterval);
      setProgress(100);
      setSuccess('Document uploaded successfully!');
      
      // Navigate to the document view page after a short delay
      setTimeout(() => {
        navigate(`/documents/${response.data.id}`);
      }, 1500);
    } catch (error) {
      console.error('Upload error:', error);
      setError(error.response?.data?.detail || 'Failed to upload document. Please try again.');
      setProgress(0);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" component="h1" gutterBottom>
        Upload Document
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box component="form" onSubmit={handleSubmit} noValidate>
          <Box
            {...getRootProps()}
            className="dropzone"
            sx={{
              border: '2px dashed',
              borderColor: isDragActive ? 'primary.main' : 'grey.400',
              borderRadius: 1,
              p: 3,
              mb: 3,
              textAlign: 'center',
              cursor: 'pointer',
              bgcolor: isDragActive ? 'rgba(25, 118, 210, 0.04)' : 'transparent',
            }}
          >
            <input {...getInputProps()} />
            <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 1 }} />
            {file ? (
              <Typography variant="body1">{file.name}</Typography>
            ) : isDragActive ? (
              <Typography variant="body1">Drop the file here...</Typography>
            ) : (
              <Typography variant="body1">
                Drag and drop a file here, or click to select a file
              </Typography>
            )}
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Supported formats: PDF, DOCX, HTML, CSV, Excel, PowerPoint, Jupyter notebooks, Images
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Maximum file size: 50MB
            </Typography>
          </Box>

          <TextField
            margin="normal"
            required
            fullWidth
            id="title"
            label="Document Title"
            name="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={uploading}
          />

          <TextField
            margin="normal"
            fullWidth
            id="description"
            label="Description (Optional)"
            name="description"
            multiline
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={uploading}
          />

          {uploading && (
            <Box sx={{ width: '100%', mt: 2 }}>
              <LinearProgress variant="determinate" value={progress} />
              <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
                {progress}% - Processing document...
              </Typography>
            </Box>
          )}

          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
            <Button
              type="button"
              variant="outlined"
              onClick={() => navigate('/')}
              disabled={uploading}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={!file || uploading}
            >
              {uploading ? 'Uploading...' : 'Upload Document'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default DocumentUpload; 