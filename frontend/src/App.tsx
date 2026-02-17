import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import ShowListPage from "./pages/ShowListPage";
import ShowDetailPage from "./pages/ShowDetailPage";
import SequenceDetailPage from "./pages/SequenceDetailPage";
import ShotDetailPage from "./pages/ShotDetailPage";
import SearchPage from "./pages/SearchPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<ShowListPage />} />
            <Route path="shows/:id" element={<ShowDetailPage />} />
            <Route path="sequences/:id" element={<SequenceDetailPage />} />
            <Route path="shots/:id" element={<ShotDetailPage />} />
            <Route path="search" element={<SearchPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
