import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

type LibraryItem = {
  libraryId: number,
  positions: number,
  word: string,
}
export const useGetLibraryItems = (libraryId?: number, options?: UseCreateQueryWrapperOptionsShort<LibraryItem[]>) => {
  return useCreateQuery({
    queryKey: ['libraryItems', libraryId],
    queryFn: () => axiosClient.get(`/library_items`, { params: { libraryId } }).then(value => value.data as LibraryItem[]),
    errorMsg: "Error getting library items",
    ...options
  })
};

type UpdateLibrartItemsParams = { libraryId: number, position: string, word: string };
export const useUpdateLibraryItems = (options?: UseCreateMutationWrapperOptions<boolean, UpdateLibrartItemsParams>) => {
  return useCreateMutation({
    mutationFn: (params: UpdateLibrartItemsParams) =>
      axiosClient.post(`/library_items`, params).then(value => value.status === 200),
    successMsg: "Library item updated",
    errorMsg: "Error updating library item",
    invalidateQueries: ["libraryItems"],
    ...options
  })
};

type DeleteLibraryItemParams = { libraryId: number, position: string };
export const useDeleteLibraryItem = (options?: UseCreateMutationWrapperOptions<boolean, DeleteLibraryItemParams>) => {
  return useCreateMutation({
    mutationFn: (params: DeleteLibraryItemParams) =>
      axiosClient.delete(`/library_items`, { params }).then(value => value.status === 200),
    successMsg: "Library item Deleted",
    errorMsg: "Error updating library items",
    invalidateQueries: ["libraryItems"],
    ...options
  })
};