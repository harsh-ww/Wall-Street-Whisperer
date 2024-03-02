import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// Chakra Provider component
import { ChakraProvider, extendTheme } from "@chakra-ui/react";

import Landing from "./routes/Landing.tsx";
import HomePage from "./routes/HomePage.tsx";
import Company from "./routes/Company.tsx";
import ErrorPage from "./ErrorPage.tsx";

const theme = extendTheme({
  styles: {
    global: () => ({
      body: {
        // bgGradient: "linear(to-r, blue.100, purple.100, purple.300)",
        bg: "purple.100",
      },
    }),
  },
});

// Routes
const router = createBrowserRouter([
  {
    path: "/",
    element: <Landing />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/home",
    element: <HomePage />,
    errorElement: <ErrorPage />,
  },
  {
    path: "/company/:exchange/:ticker",
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
