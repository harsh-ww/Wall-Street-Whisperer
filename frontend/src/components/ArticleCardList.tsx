import { Box } from "@chakra-ui/react";
import ArticleCardItem from "./ArticleCardItem";
import { useEffect, useState } from "react";
import { Article } from "./ArticleCardItem";

interface Props {
  ticker: string;
}

//pass in ticker? would work for company pages but not landing page which needs mulitple companies?
export default function ArticleCardList({ ticker }: Props) {
  // for mock data
  const [data, setData] = useState<Article[]>(mockdata);
  const [isLoaded, setIsLoaded] = useState(true);

  //   USE CODE BELOW WHEN BACKEND CODE READY

  //   const [data, setData] = useState<Article[]>([]);
  //   const [isLoaded, setIsLoaded] = useState(false);

  //   useEffect(() => {
  //     fetchArticles();
  //   }, []);

  //   const fetchArticles = async () => {
  //     try {
  //       const response = await fetch(`http://localhost:5000/articles/${ticker}`);
  //       if (!response.ok) {
  //         console.error(`HTTP error! status: ${response.status}`);
  //         throw new Error("Failed to fetch articles");
  //       }
  //       const articleData = await response.json();
  //       setData(articleData);
  //       setIsLoaded(true);
  //     } catch (error) {
  //       console.error("Error fetching news articles:", error);
  //     }
  //   };

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

const mockdata = [
  {
    articleid: 1,
    articleurl:
      "https://elitenews.uk/wwf-shelved-report-exposing-river-wye-pollution-to-keep-tesco-happy-pollution/",
    authors: "William Turner",
    imageurl:
      "https://i.guim.co.uk/img/media/02a07d28ef131a6e77e5d3a86512d5b31f0d0e2d/0_275_8256_4954/master/8256.jpg?width=1200&height=630&quality=85&auto=format&fit=crop&overlay-align=bottom%2Cleft&overlay-width=100p&overlay-base64=L2ltZy9zdGF0aWMvb3ZlcmxheXMvdG8tZGVmYXVsdC5wbmc&enable=upscale&s=d08b8af9ad6f7297a939e3ba72198121",
    keywords:
      "'River Wye pollution', 'River Wye', 'Wye', 'global food production', 'food', 'river pollution', 'supply chains', 'report', 'water catchment projects', 'water pollution'",
    overallscore: -67.11759567260742,
    publisheddate: "2024-03-01T10:46:52+00:00",
    sentimentlabel: "negative",
    sentimentscore: 0.6711759567260742,
    sourceid: 1,
    sourcepopularity: 8648709,
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ac risus vitae ligula viverra semper. Proin a efficitur est. Phasellus tortor mi, dapibus rutrum neque nec, pharetra fermentum diam. Donec eu ornare justo. Maecenas leo ipsum, elementum venenatis aliquet in, fermentum et sapien. Nunc consequat est sed molestie posuere. Mauris non malesuada felis, eu pretium sapien. Donec laoreet vitae ligula eget ultricies. In et dui sed ipsum venenatis rutrum. Etiam auctor ante eros, vel maximus ipsum vestibulum sit amet",
    title:
      "WWF shelved report exposing River Wye pollution \u2018to keep Tesco happy\u2019",
  },
  {
    articleid: 2,
    articleurl:
      "https://www.gbnews.com/opinion/supermarket-loyalty-scheme-tesco-sainsburys",
    authors: "Patrick O'Donnell",
    imageurl:
      "https://www.gbnews.com/media-library/british-farmers-facing-impossible-life-due-to-cheap-supermarket-demands.jpg?id=51613348&width=1200&height=600&coordinates=0%2C0%2C0%2C100",
    keywords:
      "'Supermarket loyalty scheme prices', 'regular prices', 'full price', 'decent prices', 'discounted prices', 'other supermarkets', 'loyalty schemes', 'Supermarket shoppers', 'supermarket chains', 'supermarkets'",
    overallscore: 99.86607124852658,
    publisheddate: "2024-03-05T10:46:52+00:00",
    sentimentlabel: "negative",
    sentimentscore: 0.45467740297317505,
    sourceid: 2,
    sourcepopularity: 1485,
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ac risus vitae ligula viverra semper. Proin a efficitur est. Phasellus tortor mi, dapibus rutrum neque nec, pharetra fermentum diam. Donec eu ornare justo. Maecenas leo ipsum, elementum venenatis aliquet in, fermentum et sapien. Nunc consequat est sed molestie posuere. Mauris non malesuada felis, eu pretium sapien. Donec laoreet vitae ligula eget ultricies. In et dui sed ipsum venenatis rutrum. Etiam auctor ante eros, vel maximus ipsum vestibulum sit amet",
    title:
      "'Supermarket loyalty scheme prices are an outrage. Shoppers need a new deal to make big savings'",
  },
  {
    articleid: 1,
    articleurl:
      "https://elitenews.uk/wwf-shelved-report-exposing-river-wye-pollution-to-keep-tesco-happy-pollution/",
    authors: "William Turner",
    imageurl:
      "https://i.guim.co.uk/img/media/02a07d28ef131a6e77e5d3a86512d5b31f0d0e2d/0_275_8256_4954/master/8256.jpg?width=1200&height=630&quality=85&auto=format&fit=crop&overlay-align=bottom%2Cleft&overlay-width=100p&overlay-base64=L2ltZy9zdGF0aWMvb3ZlcmxheXMvdG8tZGVmYXVsdC5wbmc&enable=upscale&s=d08b8af9ad6f7297a939e3ba72198121",
    keywords:
      "'River Wye pollution', 'River Wye', 'Wye', 'global food production', 'food', 'river pollution', 'supply chains', 'report', 'water catchment projects', 'water pollution'",
    overallscore: 97.11759567260742,
    publisheddate: "2024-03-03T10:46:52+00:00",
    sentimentlabel: "negative",
    sentimentscore: 0.6711759567260742,
    sourceid: 1,
    sourcepopularity: 8648709,
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ac risus vitae ligula viverra semper. Proin a efficitur est. Phasellus tortor mi, dapibus rutrum neque nec, pharetra fermentum diam. Donec eu ornare justo. Maecenas leo ipsum, elementum venenatis aliquet in, fermentum et sapien. Nunc consequat est sed molestie posuere. Mauris non malesuada felis, eu pretium sapien. Donec laoreet vitae ligula eget ultricies. In et dui sed ipsum venenatis rutrum. Etiam auctor ante eros, vel maximus ipsum vestibulum sit amet",
    title:
      "WWF shelved report exposing River Wye pollution \u2018to keep Tesco happy\u2019",
  },
  {
    articleid: 2,
    articleurl:
      "https://www.gbnews.com/opinion/supermarket-loyalty-scheme-tesco-sainsburys",
    authors: "Patrick O'Donnell",
    imageurl:
      "https://www.gbnews.com/media-library/british-farmers-facing-impossible-life-due-to-cheap-supermarket-demands.jpg?id=51613348&width=1200&height=600&coordinates=0%2C0%2C0%2C100",
    keywords:
      "'Supermarket loyalty scheme prices', 'regular prices', 'full price', 'decent prices', 'discounted prices', 'other supermarkets', 'loyalty schemes', 'Supermarket shoppers', 'supermarket chains', 'supermarkets'",
    overallscore: 49.86607124852658,
    publisheddate: "2024-03-04T10:46:52+00:00",
    sentimentlabel: "negative",
    sentimentscore: 0.45467740297317505,
    sourceid: 2,
    sourcepopularity: 1485,
    summary:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ac risus vitae ligula viverra semper. Proin a efficitur est. Phasellus tortor mi, dapibus rutrum neque nec, pharetra fermentum diam. Donec eu ornare justo. Maecenas leo ipsum, elementum venenatis aliquet in, fermentum et sapien. Nunc consequat est sed molestie posuere. Mauris non malesuada felis, eu pretium sapien. Donec laoreet vitae ligula eget ultricies. In et dui sed ipsum venenatis rutrum. Etiam auctor ante eros, vel maximus ipsum vestibulum sit amet",
    title:
      "'Supermarket loyalty scheme prices are an outrage. Shoppers need a new deal to make big savings'",
  },
];
