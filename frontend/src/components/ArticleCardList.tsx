import { Box } from "@chakra-ui/react";
import ArticleCardItem from "./ArticleCardItem";
import { useEffect, useState } from "react";
import { Article } from "./ArticleCardItem";
import { API_URL } from "../config";
interface Props {
  ticker: string;
  tracked: boolean;
}

export default function ArticleCardList({ ticker, tracked }: Props) {
  // State to store fetched article data and loading status
  const [data, setData] = useState<Article[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (tracked) {
      fetchArticles();
    }
  }, [ticker, tracked]);

  const fetchArticles = async () => {
    try {
      const response = await fetch(`${API_URL}/articles/${ticker}`);
      if (!response.ok) {
        console.error(`HTTP error! status: ${response.status}`);
        throw new Error("Failed to fetch articles");
      }
      const articleData = await response.json();
      articleData.sort((a,b) => {
        return (new Date(b.publisheddate)) - (new Date(a.publisheddate))
      })
      setData(articleData);
      setIsLoaded(true);
    } catch (error) {
      console.error("Error fetching news articles:", error);
    }
  };

  return (
    <div>
      <Box>
        {/* Conditionally render based on whether the company is tracked or not */}
        {tracked ? (
          isLoaded ? (
            data.map((article: Article) => (
              <ArticleCardItem key={article.articleid} article={article} />
            ))
          ) : (
            <div>Loading...</div>
          )
        ) : (
          <div>
            Follow the company to view articles. Articles will be automatically
            fetched overnight once you start following the company.
          </div>
        )}
      </Box>
    </div>
  );
}
