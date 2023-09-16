import { UseQueryOptions, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export type Library = {
    id: number,
    name: string,
    description: string,
    active: boolean,
    editable: boolean
}

export const useGetLibraries = (options: UseQueryOptions<Library[], unknown, Library[], string[]> = {}) => {
    return useQuery(['libraries'], () => axios.get(`${baseUrl}/libraries`).then(value => value.data as Library[]), options)
};

type DuplicateLibraryParams = { name: string, description: string, baseLibraryId: number };
export const useDuplicateLibrary = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DuplicateLibraryParams) =>
        axios.post(`${baseUrl}/library/duplicate`, params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraries"]);
                toast.success("Library duplicated")
            },
            onError: () => {
                toast.error("Error duplicating library")
            }
        }
    )
};

type CreateLibraryParams = { name: string, description: string };
export const useCreateLibrary = () => {
    const queryClient = useQueryClient();
    return useMutation((params: CreateLibraryParams) =>
        axios.post(`${baseUrl}/library`, params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraries"]);
                toast.success("Library created")
            },
            onError: () => {
                toast.error("Error creating library")
            }
        }
    )
};

type EditLibraryParams = { libraryId: number, name: string, description: string };
export const useEditLibrary = () => {
    const queryClient = useQueryClient();
    return useMutation((params: EditLibraryParams) =>
        axios.post(`${baseUrl}/library/${params.libraryId}`, { name: params.name, description: params.description }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraries"]);
                toast.success("Library updated")
            },
            onError: () => {
                toast.error("Error updating library")
            }
        }
    )
};

type DeleteLibraryParams = { libraryId: number };
export const useDeleteLibrary = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DeleteLibraryParams) =>
        axios.delete(`${baseUrl}/library`, { params }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraries"]);
                toast.success("Library deleted")
            },
            onError: () => {
                toast.error("Error deleting library")
            }
        }
    )
};

type ActivateLibraryParams = { libraryId: number };
export const useActivateLibrary = () => {
    const queryClient = useQueryClient();
    return useMutation((params: ActivateLibraryParams) =>
        axios.get(`${baseUrl}/library/activate`, { params }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraries"]);
                toast.success("Library activated")
            },
            onError: () => {
                toast.error("Error activating library")
            }
        }
    )
};