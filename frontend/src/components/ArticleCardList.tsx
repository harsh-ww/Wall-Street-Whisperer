import { Box } from "@chakra-ui/react";
import ArticleCardItem from "./ArticleCardItem";
import { useEffect, useState } from "react";
import { Article } from "./ArticleCardItem";
import { API_URL } from '../config'


interface Props {
  ticker: string;
}

//pass in ticker? would work for company pages but not landing page which needs mulitple companies?
export default function ArticleCardList({ ticker }: Props) {
  // for mock data
  // const [data, setData] = useState<Article[]>(mockdata);
  // const [isLoaded, setIsLoaded] = useState(true);

  //   USE CODE BELOW WHEN BACKEND CODE READY

    const [data, setData] = useState<Article[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
      fetchArticles();
    }, []);

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
        {isLoaded ? (
          data.map((article) => (
            <ArticleCardItem key={article.articleid} article={article} />
          ))
        ) : (
          <div>Loading...</div>
        )}
      </Box>
    </div>
  );
}
