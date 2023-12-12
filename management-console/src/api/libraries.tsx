import { UseCreateMutationWrapperOptions, UseCreateQueryWrapperOptionsShort, axiosClient, useCreateMutation, useCreateQuery } from "./helpers";

export type Library = {
  id: number,
  name: string,
  description: string,
  active: boolean,
  editable: boolean
}

export const useGetLibraries = (options?: UseCreateQueryWrapperOptionsShort<Library[]>) => {
  return useCreateQuery({
    queryKey: ['libraries'],
    queryFn: () => axiosClient.get(`/libraries`).then(value => value.data as Library[]),
    errorMsg: "Error getting libraries",
    ...options
  })
};

type DuplicateLibraryParams = { name: string, description: string, baseLibraryId: number };
export const useDuplicateLibrary = (options?: UseCreateMutationWrapperOptions<boolean, DuplicateLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: DuplicateLibraryParams) =>
      axiosClient.post(`/libraries/${params.baseLibraryId}/duplicate`, { name: params.name, description: params.description }).then(value => value.status === 200),
    successMsg: "Library duplicated",
    errorMsg: "Error duplicating library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type CreateLibraryParams = { name: string, description: string };
export const useCreateLibrary = (options?: UseCreateMutationWrapperOptions<boolean, CreateLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: CreateLibraryParams) =>
      axiosClient.post(`/libraries`, params).then(value => value.status === 200),
    successMsg: "Library created",
    errorMsg: "Error creating library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type ImportLibraryParams = { name: string, description: string, libraryFile: string };
export const useImportLibrary = (options?: UseCreateMutationWrapperOptions<boolean, ImportLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: ImportLibraryParams) =>
      axiosClient.post(`/libraries/import`, params).then(value => value.status === 200),
    successMsg: "Library imported",
    errorMsg: "Error importing library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type EditLibraryParams = { libraryId: number, name: string, description: string };
export const useEditLibrary = (options?: UseCreateMutationWrapperOptions<boolean, EditLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: EditLibraryParams) =>
      axiosClient.post(`/libraries/${params.libraryId}`, { name: params.name, description: params.description }).then(value => value.status === 200),
    successMsg: "Library updated",
    errorMsg: "Error updating library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type DeleteLibraryParams = { libraryId: number };
export const useDeleteLibrary = (options?: UseCreateMutationWrapperOptions<boolean, DeleteLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: DeleteLibraryParams) =>
      axiosClient.delete(`/libraries/${params.libraryId}`).then(value => value.status === 200),
    successMsg: "Library deleted",
    errorMsg: "Error deleting library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type ActivateLibraryParams = { libraryId: number };
export const useActivateLibrary = (options?: UseCreateMutationWrapperOptions<boolean, ActivateLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: ActivateLibraryParams) =>
      axiosClient.get(`/libraries/${params.libraryId}/activate`).then(value => value.status === 200),
    successMsg: "Library activated",
    errorMsg: "Error activating library",
    invalidateQueries: ["libraries"],
    ...options
  })
};

type ExportLibraryParams = { libraryId: number };
export const useExportLibrary = (options?: UseCreateMutationWrapperOptions<boolean, ExportLibraryParams>) => {
  return useCreateMutation({
    mutationFn: (params: ExportLibraryParams) =>
      axiosClient.get(`/libraries/${params.libraryId}/export`).then(value => value.status === 200),
    successMsg: "Library exported",
    errorMsg: "Error exporting library",
    invalidateQueries: ["libraries"],
    ...options
  })
};
