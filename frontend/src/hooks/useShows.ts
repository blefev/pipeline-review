import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Show, ShowDetail } from "../api/types";

export const showKeys = {
  all: ["shows"] as const,
  detail: (id: number) => ["shows", id] as const,
};

export function useShows() {
  return useQuery({
    queryKey: showKeys.all,
    queryFn: () => api.get<Show[]>("/shows"),
  });
}

export function useShow(id: number) {
  return useQuery({
    queryKey: showKeys.detail(id),
    queryFn: () => api.get<ShowDetail>(`/shows/${id}`),
  });
}
