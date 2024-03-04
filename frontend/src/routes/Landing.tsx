import "../App.css";
import BaseLayout from "../layouts/BaseLayout";
import ListCompanies from "../components/ListCompanies";
import ListArticles from "../components/ListArticles";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Button,
  SimpleGrid,
  Heading,
  Text,
  Flex,
} from "@chakra-ui/react";

function Landing() {
  return (
    <>
      <BaseLayout />
      <Flex justifyContent="space-around">
        {" "}
        {/*container to determine wrapping of two tabs*/}
        <ListCompanies />
        <ListArticles />
      </Flex>
    </>
  );
}

export default Landing;
