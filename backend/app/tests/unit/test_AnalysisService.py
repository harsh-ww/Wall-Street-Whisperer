import os
os.environ['SIMILARWEB_KEY'] = ''

from unittest import mock
from tests.unit.mock import MockResponse

# Mock the NewsSentiment library - we don't want to install it in CI (because it's massive) or run it in tests (slow) when we can mock the data
# aim of these tests is to test surrounding business logic
NewsSentiment = mock.MagicMock()
mock.patch.dict("sys.modules", NewsSentiment=NewsSentiment).start()

transformers = mock.MagicMock()
mock.patch.dict("sys.modules", transformers=transformers).start()


from services.AnalysisService import BatchArticleAnalysis
def mock_infer():
    return []

class TestSplitArticleTarget:
    """Tests the splitArticleTarget function"""

    def testGarbageData(self):
        """Test an article without the target name present"""
        company = "Tesco"
        article = "Councils in England will be told to cut spending on consultants and diversity schemes when Chancellor Jeremy Hunt delivers his Budget on Wednesday. Councils are facing severe financial pressures and eight have effectively declared bankruptcy since 2018. This week Nottingham City Council approved big cuts to services and Birmingham is expected to do the same. The Local Government Association said most councils spent pence on things like diversity schemes."

        analyser = BatchArticleAnalysis([])

        result = analyser.splitArticleTarget(company, article)

        assert result is None
    
    def testBoundary(self):
        """Test an article which starts with the company name"""
        company = "Tesco"
        article = "Tesco Unveils Bold Plans for Sustainable Future: A Grocery Giant's Environmental Makeover. In a groundbreaking move towards a greener future, Tesco, one of the world's largest supermarket chains, has announced an ambitious sustainability initiative that aims to revolutionize the way we shop and interact with the environment. With concerns about climate change and environmental degradation at an all-time high, Tesco is taking decisive action to reduce its carbon footprint and promote eco-friendly practices throughout its operations."

        analyser = BatchArticleAnalysis([])

        result = analyser.splitArticleTarget(company, article)
        
        assert result == ("", "Tesco", " Unveils Bold Plans for Sustainable Future: A Grocery Giant's Environmental Makeover. In a groundbreaking move towards a greener future, Tesco, one of the world's largest supermarket chains, has announced an ambitious sustainability initiative that aims to revolutionize the way we shop and interact with the environment. With concerns about climate change and environmental degradation at an all-time high, Tesco is taking decisive action to reduce its carbon footprint and promote eco-friendly practices throughout its operations.")

    def testMultipleOccurrences(self):
        """Test an article with multiple occurrences of the company name"""
        company = "Tesco"
        article = "In a groundbreaking move towards a greener future, Tesco, one of the world's largest supermarket chains, has announced an ambitious sustainability initiative that aims to revolutionize the way we shop and interact with the environment. With concerns about climate change and environmental degradation at an all-time high, Tesco is taking decisive action to reduce its carbon footprint and promote eco-friendly practices throughout its operations."

        analyser = BatchArticleAnalysis([])

        result = analyser.splitArticleTarget(company, article)
        
        assert len(result) == 3
        assert result[1] == 'Tesco'

class TestPopularityFetching:
    """Test popularity fetching and updating"""
    
    def similarwebMock(*args, **kwargs):
        if args[0]=='https://api.similarweb.com/v1/similar-rank/bbc.com/rank':
            return MockResponse({"meta": {}, "similar_rank": {"rank": 20}},200)
        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=similarwebMock)
    def testFetching(self, mocked_get):
        analyser = BatchArticleAnalysis([])
        result = analyser.fetchPopularity('bbc.com')
        assert result == 20

        result = analyser.fetchPopularity('nonexistentsite.cs261')
        assert result is None

