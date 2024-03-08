import { Box } from "@chakra-ui/react";
import ArticleCardItem from "./ArticleCardItem";
import { useEffect, useState } from "react";
import { Article } from "./ArticleCardItem";
import { API_URL } from '../config'


interface RecentArticle extends Article {
    companyname: string;
}

//pass in ticker? would work for company pages but not landing page which needs mulitple companies?
export default function ArticleCardList() {

    const [data, setData] = useState<RecentArticle[]>([]);
    const [isLoaded, setIsLoaded] = useState(false);

    useEffect(() => {
      fetchArticles();
    }, []);

    const fetchArticles = async () => {
      try {
        const response = await fetch(`${API_URL}/recent-articles`);
        if (!response.ok) {
          console.error(`HTTP error! status: ${response.status}`);
          throw new Error("Failed to fetch articles");
        }
        const articleData: RecentArticle[] = await response.json();
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
            <ArticleCardItem key={article.articleid} article={article} company={article.companyname} />
          ))
        ) : (
          <div>Loading...</div>
        )}
      </Box>
    </div>
  );
}