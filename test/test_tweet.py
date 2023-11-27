import sys
# sys.path.append("../sentimental_analysis/audio/")
import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client

# Unit Test Case for Audio Sentiment Analyzer
class TweetSentimentAnalyzerTestCase(unittest.TestCase):
    
    # Setup
    def tweet(self):
        c = Client()
        response = c.post("/tweetanalysis/", {"tweetlink": 'https://x.com/tedfrank/status/1728268149517177197?s=20'})
        self.assertEqual(response.status_code, 200)
        


# main function
if __name__ == '__main__':
     unittest.main()
