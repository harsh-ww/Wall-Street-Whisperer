import {
  Card,
  CardHeader,
  SimpleGrid,
  Heading,
  Text,
  Box,
} from "@chakra-ui/react";
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
      <Card
        width="35vw"
        h="55vh"
        bg="gray.50"
        borderWidth="2px"
        borderColor="gray.500"
        boxShadow="inner"
        overflow="auto"
      >
        {" "}
        {/*{purple.500}*/}
        <CardHeader alignSelf="center">
          <Heading size="md" color="black">
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
              <Box>
                <CompanyMotif companyName={company} textSize="sm" />
              </Box>
            )
          )}
        </SimpleGrid>
      </Card>
    </>
  );
}

export default ListCompanies;
