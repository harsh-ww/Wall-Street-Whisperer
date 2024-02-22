import { Card, CardHeader, SimpleGrid, Heading, Text } from "@chakra-ui/react";
import CompanyMotif from "./CompanyMotif";

function ListCompanies() {
  let companies = [
    "Company1",
    "NotaCompany",
    "ShellCorp",
    "LemonadeStand",
    "EvenBiggerCompany",
    "ehgeg",
  ]; //dummy data

  return (
    <>
      <Card bg="purple.500" width="35vw" h="55vh">
        <CardHeader alignSelf="center">
          <Heading size="md" color="white">
            <Text>Trending Companies</Text>
          </Heading>
        </CardHeader>
        <SimpleGrid
          spacing={5}
          templateColumns="repeat(auto-fill, minmax(200px, 1fr))"
          justifyContent="space-around"
          padding="1em"
          overflow="hidden"
        >
          {companies.map(
            (
              company //using CompanyMotif as a base, we can use backend data to populate the trending companies data
            ) => (
              <CompanyMotif companyName={company} />
            )
          )}
        </SimpleGrid>
      </Card>
    </>
  );
}

export default ListCompanies;
