import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";

import { toast } from "react-toastify";

export const useGetWords = () => {
    return useQuery(['words'], () => axios.get(baseUrl + "/words").then(value => value.data as string[]))
};

type DeleteWordParams = { word: string };
export const useDeleteWord = () => {
    const queryClient = useQueryClient();
    return useMutation((params: DeleteWordParams) =>
        axios.delete(baseUrl + "/words", { params }).then(value => value.status === 200),
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

type UploadWordParams = { file: File, fileName: string };
export const useUploadWord = () => {
    const queryClient = useQueryClient();
    return useMutation(({ file, fileName }: UploadWordParams) =>
        axios.post(baseUrl + "/words", file, {
            headers: {
                filename: fileName
            }
        }).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["words"]);
                toast.success("Word Uploaded")
            },
            onError: () => {
                toast.error("Error uploading word")
            }
        }
    )
};