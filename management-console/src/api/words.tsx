import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useGetWords = () => {
    return useQuery(['words'], () => axios.get(baseUrl + "/api/words").then(value => value.data as string[]))
};

type DeleteWordParams = { word: string };
export const useDeleteWord = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DeleteWordParams) =>
        axios.delete(baseUrl + "/api/word", { params }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["words"]);
                toast.success("Word Deleted")
            },
            onError: () => {
                toast.error("Error deleting word")
            }
        }
    )
};