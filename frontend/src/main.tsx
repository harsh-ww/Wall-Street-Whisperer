import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { ChakraProvider, extendTheme } from "@chakra-ui/react";
import HomePage from "./routes/HomePage.tsx";
import Company from "./routes/Company.tsx";
import ErrorPage from "./ErrorPage.tsx";
import bgSVG from "../public/bgSVG.svg";

const theme = extendTheme({
  styles: {
    global: () => ({
      body: {
        bg: "purple.100",
      },
    }),
  },
});

// Routes
const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/company/:ticker",
    element: <Company />,
    errorElement: <ErrorPage />,
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <RouterProvider router={router} />
    </ChakraProvider>
  </React.StrictMode>
);
