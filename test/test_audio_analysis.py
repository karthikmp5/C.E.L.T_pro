import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class AudioSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def audio(self):
        audio = SimpleUploadedFile('test_wv.wav', "file_content", content_type="audio/wav")
        c = Client()
        response = c.post("/audioanalysis/", {"document": audio})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
