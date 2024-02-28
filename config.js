import dotenv from 'dotenv';
dotenv.config();
import { Storage } from '@google-cloud/storage';
import path from 'path';

// Your Google Cloud Storage should be authenticated with your service account
const storage = new Storage({
  projectId: process.env.GCLOUD_PROJECT_ID,
  credentials: {
    client_email: process.env.GCLOUD_CLIENT_EMAIL,
    private_key: process.env.GCLOUD_PRIVATE_KEY.replace(/\\n/g, '\n'),
  },
});


async function uploadImage(file) {
  try {
    const bucketName = 'manual_posts_images';
    const filename = file.path;

    // Uploads a local file to the bucket
    const [uploadedFile] = await storage.bucket(bucketName).upload(filename, {
      gzip: true,
      metadata: {
        cacheControl: 'public, max-age=31536000',
      },
    });

    // Generate a signed URL for the uploaded file
    const [url] = await uploadedFile.getSignedUrl({
      action: 'read',
      expires: Date.now() + 1000 * 60 * 60, // 1 hour
    });

    return url;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
}

export default uploadImage;