import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

export const useGetWords = (options?: UseCreateQueryWrapperOptionsShort<string[]>) => {
  return useCreateQuery({
    queryKey: ['words'],
    queryFn: () => axiosClient.get("/words").then(value => (value.data as string[]).map(w => decodeURIComponent(w))),
    errorMsg: "Error getting words",
    ...options
  })
};

type DeleteWordParams = { word: string };
export const useDeleteWord = (options?: UseCreateMutationWrapperOptions<boolean, DeleteWordParams>) => {
  return useCreateMutation({
    mutationFn: ({ word }: DeleteWordParams) =>
      axiosClient.delete("/words", { params: { word: encodeURIComponent(word) } }).then(value => value.status === 200),
    successMsg: "Word Deleted",
    errorMsg: "Error deleting word",
    invalidateQueries: ["words"],
    ...options
  })
};

type UploadWordParams = { file: File, fileName: string };
export const useUploadWord = (options?: UseCreateMutationWrapperOptions<boolean, UploadWordParams>) => {
  return useCreateMutation({
    mutationFn: ({ file, fileName }: UploadWordParams) =>
      axiosClient.post("/words", file, {
        headers: {
          filename: encodeURIComponent(fileName)
        }
      }).then(value => value.status === 200),
    successMsg: "Word Uploaded",
    errorMsg: "Error uploading word",
    invalidateQueries: ["words"],
    ...options
  })
};