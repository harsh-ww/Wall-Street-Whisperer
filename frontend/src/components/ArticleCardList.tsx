import { Box } from "@chakra-ui/react";
import ArticleCardItem from "./ArticleCardItem";
import { useEffect, useState } from "react";
import { Article } from "./ArticleCardItem";
import { API_URL } from '../config'


interface Props {
  ticker: string;
  tracked: boolean;
}

//pass in ticker? would work for company pages but not landing page which needs mulitple companies?
export default function ArticleCardList({ ticker, tracked }: Props) {
    const [data, setData] = useState<Article[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
      if (tracked){
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
        setData(articleData);
        setIsLoaded(true);
      } catch (error) {
        console.error("Error fetching news articles:", error);
      }
    };

  return (
    <div>
      <Box>
        {tracked ? (
            isLoaded ? (
              data.map((article: Article) => (
                <ArticleCardItem key={article.articleid} article={article} />
              ))
            ) : (
              <div>Loading...</div>
            )
          ) : (
            <div>Follow the company to view articles. Articles will be automatically fetched overnight once you start following the company.</div>
          )}
      </Box>
    </div>
  );
}
