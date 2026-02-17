import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { SequenceDetail } from "../api/types";

export const sequenceKeys = {
  detail: (id: number) => ["sequences", id] as const,
};

export function useSequence(id: number) {
  return useQuery({
    queryKey: sequenceKeys.detail(id),
    queryFn: () => api.get<SequenceDetail>(`/sequences/${id}`),
  });
}
