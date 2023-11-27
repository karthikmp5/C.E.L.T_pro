import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class ImageSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def image(self):
        image = SimpleUploadedFile('img.jpg', "file_content", content_type="image/jpg")
        c = Client()
        response = c.post("/imageanalysis/", {"imgfile": image})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
