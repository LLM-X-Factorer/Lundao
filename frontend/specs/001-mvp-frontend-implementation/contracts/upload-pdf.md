# API Contract: Upload PDF

## Endpoint
```
POST /api/upload_pdf
```

## Description
Uploads a PDF file for analysis. Returns a unique file ID for subsequent analysis requests.

## Request

### Content-Type
```
multipart/form-data
```

### Form Fields

| Field | Type | Required | Description | Validation |
|-------|------|----------|-------------|------------|
| `file` | File | Yes | PDF file to upload | MIME type: `application/pdf`, max size: 20MB |

### Example Request
```http
POST /api/upload_pdf HTTP/1.1
Host: api.lundao.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary...

------WebKitFormBoundary...
Content-Disposition: form-data; name="file"; filename="paper.pdf"
Content-Type: application/pdf

[binary PDF content]
------WebKitFormBoundary...--
```

## Response

### Success Response (201 Created)

**Body**:
```json
{
  "fileId": "upload-550e8400-e29b-41d4-a716-446655440000",
  "filename": "paper.pdf",
  "fileSize": 2457600,
  "uploadedAt": "2025-10-14T10:35:00Z",
  "expiresAt": "2025-10-15T10:35:00Z",
  "status": "uploaded"
}
```

**Schema**:
- `fileId`: String (UUID) - Unique file identifier (format: `"upload-{uuid}"`)
- `filename`: String - Original filename
- `fileSize`: Number - File size in bytes
- `uploadedAt`: String (ISO 8601) - Upload timestamp
- `expiresAt`: String (ISO 8601) - File expiration (24 hours)
- `status`: String (enum) - Upload status (`"uploaded"`, `"processing"`, `"ready"`)

### Error Responses

#### 400 Bad Request
Invalid file format or missing file.

```json
{
  "error": {
    "code": "INVALID_FILE_TYPE",
    "message": "Only PDF files are supported",
    "details": {
      "mimeType": "application/msword",
      "supportedTypes": ["application/pdf"]
    }
  }
}
```

#### 413 Payload Too Large
File exceeds size limit.

```json
{
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "File size exceeds 20MB limit",
    "details": {
      "fileSize": 25165824,
      "maxSize": 20971520
    }
  }
}
```

#### 422 Unprocessable Entity
PDF is corrupted or encrypted.

```json
{
  "error": {
    "code": "INVALID_PDF",
    "message": "Unable to process this PDF file. It may be corrupted or encrypted.",
    "details": {
      "reason": "encrypted"
    }
  }
}
```

#### 503 Service Unavailable
Storage service temporarily unavailable.

```json
{
  "error": {
    "code": "STORAGE_UNAVAILABLE",
    "message": "File storage service is temporarily unavailable. Please try again later.",
    "retryAfter": 60
  }
}
```

## Frontend Integration

### Axios Service (uploadService.js)
```javascript
export async function uploadPDF(file, onProgress) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/upload_pdf', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      )
      onProgress(percentCompleted)
    },
    timeout: 120000 // 2 minutes for large files
  })

  return response.data
}
```

### Composable (useFileUpload.js)
```javascript
export function useFileUpload() {
  const progress = ref(0)
  const uploading = ref(false)
  const error = ref(null)

  const uploadFile = async (file) => {
    // Client-side validation
    if (file.type !== 'application/pdf') {
      error.value = 'Only PDF files are allowed'
      throw new Error(error.value)
    }

    if (file.size > 20 * 1024 * 1024) {
      error.value = 'File size exceeds 20MB limit'
      throw new Error(error.value)
    }

    uploading.value = true
    error.value = null
    progress.value = 0

    try {
      const data = await uploadPDF(file, (percent) => {
        progress.value = percent
      })
      return data
    } catch (err) {
      error.value = err.response?.data?.error?.message || 'Upload failed'
      throw err
    } finally {
      uploading.value = false
    }
  }

  return { uploadFile, progress, uploading, error }
}
```

## Upload Flow

1. **User selects file**: Drag-and-drop or file input
2. **Client validation**: Check file type and size
3. **Upload initiated**: FormData sent with progress tracking
4. **Progress updates**: UI shows percentage via onUploadProgress
5. **Upload complete**: Backend returns fileId
6. **Auto-trigger analysis**: Frontend immediately requests analysis with fileId

## Progress Tracking

The `onUploadProgress` callback receives events with:
- `loaded`: Bytes uploaded so far
- `total`: Total bytes to upload
- Percentage: `(loaded / total) * 100`

**UI Updates**:
- 0-25%: "Preparing upload..."
- 25-75%: "Uploading... {percent}%"
- 75-100%: "Finalizing..."
- 100%: "Upload complete!"

## Edge Cases

1. **Network interruption**: Upload fails mid-transfer
   - Frontend catches error, shows "Upload failed" message
   - User can retry upload

2. **Duplicate upload**: User uploads same file twice
   - Backend allows (no deduplication in MVP)
   - Each upload gets unique fileId

3. **Upload timeout**: Large file takes >2 minutes
   - Axios throws timeout error
   - Frontend shows: "Upload timed out. Please try a smaller file."

4. **Browser close during upload**: User closes tab/window
   - Upload aborts automatically (no cleanup needed)
   - Backend cleans up incomplete uploads after 1 hour

## Performance Expectations

- **Upload speed**: Depends on network (3G: ~1MB/10s, WiFi: ~1MB/1s)
- **Max file size**: 20MB (enforced client + server)
- **Timeout**: 2 minutes (120 seconds)
- **Concurrent uploads**: 1 at a time (UI enforced)

## Notes

- Uploaded files expire after 24 hours
- No authentication required (anonymous uploads)
- Backend virus scanning not implemented in MVP
- File storage uses cloud object storage (S3-compatible)
