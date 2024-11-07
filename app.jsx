import React, { useEffect, useState } from "react";
import { S3Client, HeadObjectCommand, GetObjectCommand } from "@aws-sdk/client-s3";

const REGION = process.env.REACT_APP_AWS_REGION;
const BUCKET_NAME = process.env.REACT_APP_BUCKET_NAME;
const FILE_KEY = process.env.REACT_APP_FILE_KEY;

const s3Client = new S3Client({
  region: REGION,
  credentials: {
    accessKeyId: process.env.REACT_APP_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.REACT_APP_AWS_SECRET_ACCESS_KEY,
  },
});

function App() {
  const [fileExists, setFileExists] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const checkFileExists = async () => {
      try {
        const headObjectCommand = new HeadObjectCommand({
          Bucket: BUCKET_NAME,
          Key: FILE_KEY,
        });
        await s3Client.send(headObjectCommand);
        setFileExists(true);
      } catch (err) {
        console.error("File does not exist:", err);
        setFileExists(false);
        setError("File not found or access denied.");
      }
    };

    checkFileExists();
  }, []);

  const handleDownload = async () => {
    try {
      const getObjectCommand = new GetObjectCommand({
        Bucket: BUCKET_NAME,
        Key: FILE_KEY,
      });
      const response = await s3Client.send(getObjectCommand);

      // Create a download link
      const blob = await response.Body.blob();
      const url = URL.createObjectURL(blob);
      setDownloadUrl(url);
    } catch (err) {
      console.error("Error retrieving file:", err);
      setError("Unable to download file.");
    }
  };

  return (
    <div>
      <h1>File Download Application</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {fileExists ? (
        <div>
          <p>File is available for download!</p>
          <button onClick={handleDownload}>Download File</button>
          {downloadUrl && (
            <a href={downloadUrl} download="downloaded-file">
              Click here to download
            </a>
          )}
        </div>
      ) : (
        <p>Checking if file is available...</p>
      )}
    </div>
  );
}

export default App;


REACT_APP_AWS_REGION=your-aws-region
REACT_APP_AWS_ACCESS_KEY_ID=your-access-key-id
REACT_APP_AWS_SECRET_ACCESS_KEY=your-secret-access-key
REACT_APP_BUCKET_NAME=your-bucket-name
REACT_APP_FILE_KEY=your-file-key  # S3 path to the file, e.g., "folder/file.pdf"


npm install @aws-sdk/client-s3
