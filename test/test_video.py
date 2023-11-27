import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class VideoSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def video(self):
        video = SimpleUploadedFile('sad.mp4', "file_content", content_type="video/mp4")
        c = Client()
        response = c.post("/videoanalysis/", {"video": video})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
