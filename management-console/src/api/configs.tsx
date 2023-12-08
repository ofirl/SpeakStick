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
export const LOGS_API_KEY_CONFIG = "LOGS_API_KEY"
export const DEVICE_NAME_CONFIG = "DEVICE_NAME"
export const LOGGING_LEVEL_CONFIG = "LOGGING_LEVEL"
export const LOGS_HANDLER_LOGGING_LEVEL_CONFIG = "LOGS_HANDLER_LOGGING_LEVEL"

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