import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { ReviewSearchResult } from "../api/types";

export const searchKeys = {
  reviews: (q: string) => ["search", "reviews", q] as const,
};

export function useSearchReviews(query: string) {
  return useQuery({
    queryKey: searchKeys.reviews(query),
    queryFn: () =>
      api.get<ReviewSearchResult[]>(
        `/search/reviews?q=${encodeURIComponent(query)}`,
      ),
    enabled: query.length > 0,
  });
}
