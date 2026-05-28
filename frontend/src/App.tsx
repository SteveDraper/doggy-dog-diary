import { Route, Routes } from "react-router-dom";
import DogDetailPage from "./pages/DogDetailPage";
import HomePage from "./pages/HomePage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/dogs/:id" element={<DogDetailPage />} />
    </Routes>
  );
}
