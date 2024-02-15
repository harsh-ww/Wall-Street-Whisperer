import React from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Landing from './routes/Landing.tsx'
import HomePage from './routes/HomePage.tsx'
import Company from './routes/Company.tsx'
import ErrorPage from './ErrorPage.tsx';


// Routes
const router = createBrowserRouter([
  {
    path: "/landing",
    element: <Landing />,
    errorElement: <ErrorPage />
  },
  {
    path: "/home",
    element: <HomePage />,
    errorElement: <ErrorPage />
  },
  {
    path: "/company",
    element: <Company />,
    errorElement: <ErrorPage />
  }
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
