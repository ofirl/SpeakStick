import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

type Config = {
    key: string,
    value: string,
    description: string,
    default_value: string
}

export const useGetConfigs = (IncludeAdvanced: boolean = false) => {
    return useQuery(['configs', IncludeAdvanced], () => axios.get(baseUrl + "/configs", { params: { advanced: IncludeAdvanced ? 1 : 0 } }).then(value => value.data as Config[]))
};

type updateConfigParams = { key: string, value: string };
export const useUpdateConfig = () => {
    const queryClient = useQueryClient();
    return useMutation((params: updateConfigParams) =>
        axios.post(baseUrl + "/configs", params).then(value => value.status === 200),
        {
            onSuccess: () => {
                queryClient.invalidateQueries(["configs"]);
                toast.success("Config updated")
            },
            onError: () => {
                toast.error("Error updating config")
            }
        }
    )
};