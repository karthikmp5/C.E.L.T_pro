import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class EaterySentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def eatery(self):
        c = Client()
        response = c.post("/eateryanalysis/", {"blogname": 'https://maps.app.goo.gl/e2nTPZmz1DULA8JfA'})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
