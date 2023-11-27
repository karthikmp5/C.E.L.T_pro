import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class DocumentSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def document(self):
        document = SimpleUploadedFile('document-sample-upload.pdf', "file_content", content_type="document/pdf")
        c = Client()
        response = c.post("/documentanalysis/", {"document": document})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
