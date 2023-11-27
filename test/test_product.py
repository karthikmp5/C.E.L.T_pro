import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class ProductSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def product(self):
        c = Client()
        response = c.post("/productanalysis/", {"blogname": 'https://www.nfl.com/news/2023-nfl-season-week-12-what-we-learned-from-thanksgiving-day-tripleheader-packe'})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
