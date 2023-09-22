import { UseQueryOptions, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { baseUrl } from "./consts";
import { toast } from "react-toastify";

type Config = {
    key: string,
    value: string,
    description: string,
    default_value: string
}

export const DEVELOPMENT_BUILDS_CONFIG = "ENABLE_DEVELOPMENT_BUILDS"
export const AUTOMATIC_UPDATES_CONFIG = "ENBALE_AUTOMATIC_UPDATES"

export const useGetConfigs = <T extends object | boolean = Config[]>(IncludeAdvanced: boolean = false, options: UseQueryOptions<Config[], unknown, T, string[]> = {}) => {
    return useQuery(
        ['configs', IncludeAdvanced.toString()],
        () => axios.get(baseUrl + "/configs", { params: { advanced: IncludeAdvanced ? 1 : 0 } }).then(value => value.data as Config[]),
        options
    )
};

type updateConfigParams = { key: string, value: string };
export const useUpdateConfig = () => {
    const queryClient = useQueryClient();
    return useMutation((params: updateConfigParams) =>
        axios.post(baseUrl + "/configs", params).then(value => value.status === 200),
        {
            onSuccess: (_data, variables) => {
                queryClient.invalidateQueries(["configs"]);
                if (variables.key === DEVELOPMENT_BUILDS_CONFIG)
                    queryClient.invalidateQueries(["versions"]);

                toast.success("Config updated")
            },
            onError: () => {
                toast.error("Error updating config")
            }
        }
    )
};

export const useAutomaticUpdatesEnabled = () => {
    return useGetConfigs(true, { select: (data) => data.find(c => c.key === AUTOMATIC_UPDATES_CONFIG)?.value === "1" })
}