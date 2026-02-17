import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import type { SeedResponse } from "../api/types";

export function useSeed() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => api.post<SeedResponse>("/seed", {}),

    onSuccess: () => {
      queryClient.invalidateQueries();
    },
  });
}
