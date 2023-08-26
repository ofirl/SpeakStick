import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useGetPositions = () => {
    return useQuery(['positions'], () => axios.get(baseUrl + "/api/positions").then(value => value.data as Record<string, string>))
};

type UpdatePositionParams = { position: string, word: string };
export const useUpdatePosition = () => {
    const queryClient = useQueryClient();
    return useMutation((params: UpdatePositionParams) =>
        axios.post(baseUrl + "/api/position", params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["positions"]);
                toast.success("Position updated")
            },
            onError: () => {
                toast.error("Error updating position")
            }
        }
    )
};

type DeletePositionParams = { position: string };
export const useDeletePosition = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DeletePositionParams) =>
        axios.delete(baseUrl + "/api/position", { params }).then(value => value.status === 200),
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