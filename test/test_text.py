import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class TextSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def text(self):
        text = "Last week, my friend fell sick. It was heartbreaking to hear that she was unwell and I was worried about her health. We couldn't meet each other for several days, and it made me realize how much I value our friendship. I tried to check on her regularly, and even though she was feeling better, I still hope that she makes a full recovery soon"
        c = Client()
        response = c.post("/textanalysis/", {"Text": text})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
