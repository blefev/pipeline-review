import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "../api/client";
import type { Shot, ShotDetail, ShotUpdate } from "../api/types";
import { sequenceKeys } from "./useSequences";

export const shotKeys = {
  detail: (id: number) => ["shots", id] as const,
};

export function useShot(id: number) {
  return useQuery({
    queryKey: shotKeys.detail(id),
    queryFn: () => api.get<ShotDetail>(`/shots/${id}`),
  });
}

export function useUpdateShot(id: number) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (update: ShotUpdate) =>
      api.patch<Shot>(`/shots/${id}`, update),

    // Optimistic update on shot detail cache
    onMutate: async (update) => {
      await queryClient.cancelQueries({ queryKey: shotKeys.detail(id) });
      const previous = queryClient.getQueryData<ShotDetail>(
        shotKeys.detail(id),
      );

      if (previous) {
        queryClient.setQueryData<ShotDetail>(shotKeys.detail(id), {
          ...previous,
          ...update,
        });
      }

      return { previous };
    },

    onError: (_err, _update, context) => {
      if (context?.previous) {
        queryClient.setQueryData(shotKeys.detail(id), context.previous);
      }
    },

    onSettled: (_data, _error, _vars, _context) => {
      // Refetch shot to get server truth
      queryClient.invalidateQueries({ queryKey: shotKeys.detail(id) });

      // Invalidate parent sequence so StatusPipeline updates
      const shot = queryClient.getQueryData<ShotDetail>(shotKeys.detail(id));
      if (shot) {
        queryClient.invalidateQueries({
          queryKey: sequenceKeys.detail(shot.sequence_id),
        });
      }
    },
  });
}
