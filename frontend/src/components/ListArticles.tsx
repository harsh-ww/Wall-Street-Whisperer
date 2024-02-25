import { Card, CardHeader, SimpleGrid, Heading, Text } from "@chakra-ui/react";
import ArticleMotif from "./ArticleMotif";

function ListArticles() {
  let articles = [
    "Headliner",
    "ArticleTitle",
    "NotAdmissible",
    "MoneyLaundering",
    "DidaGoodThing",
  ]; //dummy data

  return (
    <>
      <Card bg="purple.500" width="35vw" h="55vh">
        <CardHeader alignSelf="center">
          <Heading size="md" color="white">
            <Text>Trending Articles</Text>
          </Heading>
        </CardHeader>
        <SimpleGrid
          spacing={5}
          templateColumns="repeat(auto-fill, minmax(200px, 1fr))"
          justifyContent="space-around"
          padding="1em"
          overflow="hidden"
        >
          {articles.map((article) => (
            <ArticleMotif articleName={article} />
          ))}
        </SimpleGrid>
      </Card>
    </>
  );
}

export default ListArticles;
