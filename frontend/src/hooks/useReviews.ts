import { useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Review, ReviewCreate } from "../api/types";
import { shotKeys } from "./useShots";

export function useCreateReview(shotId: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (review: ReviewCreate) =>
      api.post<Review>(`/shots/${shotId}/reviews`, review),

    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: shotKeys.detail(shotId) });
    },
  });
}
