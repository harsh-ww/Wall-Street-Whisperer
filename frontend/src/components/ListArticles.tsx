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
      <Card
        width="35vw"
        h="55vh"
        bg="gray.100"
        borderWidth="2px"
        borderColor="gray.500"
        boxShadow="inner"
      >
        <CardHeader alignSelf="center">
          <Heading size="md" color="black">
            <Text>Trending Articles</Text>
          </Heading>
        </CardHeader>
        <SimpleGrid
          spacing={1}
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
