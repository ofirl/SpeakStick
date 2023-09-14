import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useGetLibraryItems = (libraryId?: number) => {
    return useQuery(['libraryItems'], () => axios.get(`${baseUrl}/library_items`, { params: { libraryId } }).then(value => value.data as Record<string, string>))
};

type UpdateLibrartItemsParams = { libraryId: number, position: string, word: string };
export const useUpdateLibraryItems = () => {
    const queryClient = useQueryClient();
    return useMutation((params: UpdateLibrartItemsParams) =>
        axios.post(`${baseUrl}/library_item`, params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["libraryItems"]);
                toast.success("Library item updated")
            },
            onError: () => {
                toast.error("Error updating library item")
            }
        }
    )
};

type DeleteLibraryItemParams = { libraryId: number, position: string };
export const useDeleteLibraryItem = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DeleteLibraryItemParams) =>
        axios.delete(`${baseUrl}/libray_item`, { params }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["positions"]);
                toast.success("Position Deleted")
            },
            onError: () => {
                toast.error("Error updating position")
            }
        }
    )
};